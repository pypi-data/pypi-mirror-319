from .config import ConfigBase
from .data import SafeDataLoader, batch_to
from .slack import notify_info, notify_warn, notify_priority
from .imports import *
from dataclasses import dataclass, field
import torch.optim as optim
from torch.amp import GradScaler, autocast
from torch.utils.data import default_collate
from typing import Union
from .loggers import train_logger as logger

class TrainerArgs(ConfigBase):
    # Optimization settings
    optimizer: str = "AdamW"
    lr: float = 1e-5
    optimizer_kwargs: dict = field(default_factory=dict)
    scheduler: str = None
    scheduler_kwargs: dict = field(default_factory=dict)
    grad_accumulation_steps: int = 1
    grad_clip_norm: Union[float, bool] = 1.0  # False for no clipping
    mixed_precision: bool = True

    # Training settings
    batch_size: int = 32
    train_steps_per_epoch: int = None
    val_steps_per_epoch: int = None
    max_epochs: int = 10000
    num_workers: int = 0
    safe_dataloader: bool = True
    val_data_shuffle: bool = False
    dataloader_kwargs: dict = field(default_factory=dict)
    device: str = None  # Auto infer


    # Checkpoint settings
    results_dir: str = "results"
    n_best_checkpoints: int = 3  # Negative value for saving all checkpoints
    n_latest_checkpoints: int = 2  # Negative value for saving all checkpoints
    checkpoint_metric: str = "loss"
    checkpoint_metric_type: str = "val"
    checkpoint_metric_minimize: bool = True
    resume_from_checkpoint: Union[str, bool] = None  # None for no resuming, True for latest checkpoint, or path to checkpoint

    # Logging settings
    log_every_n_steps: int = 32
    save_every_n_steps: int = 1000
    log_grad_norm: bool = True

    # Debugging and monitoring
    debug_mode: bool = False
    disable_wandb: bool = False
    wandb_project: str = None  # wandb login
    wandb_run_name: str = None
    wandb_run_id: str = None
    wandb_resume: bool = False
    wandb_kwargs: dict = field(default_factory=dict)
    slack_notify: bool = False
    



class Trainer:
    def __init__(self,args):
        self.args = args
        self.logs = []
        self._current_state = {'steps':0,
                              'epoch': 0,
                              'run_id':self.args.wandb_run_id ,
                            'best_checkpoint':None,
                            'best_score':math.inf if self.args.checkpoint_metric_minimize else -math.inf,
                            "train_steps_per_epoch":None,
                            "val_steps_per_epoch":None,
                            "device":None,
                            "track_metric_name" : self.args.checkpoint_metric_type+"/"+self.args.checkpoint_metric +"_epoch",
                            'device' : self.infer_device(),
                            'starttime':None,
                            'timeout':None}
        
        self.logger = wandb.init(project=self.args.wandb_project,
                                name=self.args.wandb_run_name,
                                id=self.args.wandb_run_id ,
                                resume=self.args.wandb_resume,
                                mode="disabled" if self.args.debug_mode or self.args.disable_wandb else "online",
                                **self.args.wandb_kwargs)
        os.makedirs(self.args.results_dir, exist_ok=True)

        for key in self.current_state:
            self._create_property(key)
    
    def _create_property(self, key):
        # Getter function
        def getter(self):
            return self._current_state.get(key)
        
        # Setter function
        def setter(self, value):
            self._current_state[key] = value
        
        # Create a property and set it on the class
        setattr(self.__class__, key, property(getter, setter))

    @property
    def current_state(self):
        return self._current_state
        
    def train(self, model, train_dataset, val_dataset=None, collate_fn=None,timeout=None):
        train_dataloader, optimizer, scheduler, grad_scaler, pbar = self._initialize_train(model,train_dataset,val_dataset,collate_fn,timeout)
        for epoch in tqdm(range(int(self.epoch), self.nepochs),total=self.nepochs,desc="Training epochs...",leave=False):
            self.epoch = epoch
            model.train()
            self.notify(f"Epoch {epoch+1}/{self.nepochs} started!")
            step_losses = defaultdict(float)
            running_losses = defaultdict(float)

            for batch_idx, batch in enumerate(train_dataloader):
                if self.steps > self.total_steps:
                    break
                if self.timedout():
                    self.notify(f"Training timed out after {timeout}!")
                    self.save_checkpoint(model, f"latest_{self.steps}")
                    return
                
                losses = self._training_step(model,batch,batch_idx,grad_scaler) 

                if (batch_idx+1)%self.args.grad_accumulation_steps==0:
                    self._optimizer_step(model,grad_scaler,optimizer,losses)

                self._update_losses(losses,step_losses,running_losses,batch_idx)
                
                if (batch_idx+1)%self.args.save_every_n_steps==0:
                    self.save_checkpoint(model, f"latest_{self.steps+1}")
                  
                self._pbar_step(pbar,step_losses)
                
                if (batch_idx+1)%self.args.log_every_n_steps==0:
                    self.log_it(step_losses,log_type="train", level="step")
                    self.log_it(running_losses,log_type="train", level="step_running_means")
                    step_losses = defaultdict(float) # reset it here!

                if (batch_idx+1)==self.train_steps_per_epoch:
                    break

            self.log_it(running_losses,log_type="train", level="epoch")
            if val_dataset is not None:
                self.evaluate(model, val_dataset, collate_fn)
            self.notify(f"Epoch {epoch+1}/{self.nepochs} completed!\n\n{self.format_state(self.current_state)}")

            self.save_if_best(model)
            self.save_checkpoint(model, os.path.join(self.args.results_dir,f"latest_{self.steps}"))
        self.notify(f"Training completed! Best checkpoint found at {self.best_checkpoint} with {self.track_metric_name}: {self.best_score}")

    def _initialize_train(self,model,train_dataset,val_dataset,collate_fn,timeout):
        train_dataloader, optimizer, scheduler, grad_scaler = self.train_setup(model, train_dataset, collate_fn)
        self.make_dummy_call(model, train_dataloader)
        self.load_latest_checkpoint(model)
        self.infer_train_val_steps(train_dataset, val_dataset)
        self.steps = round(self.steps/self.train_steps_per_epoch) * self.train_steps_per_epoch
        self.epoch = self.steps//self.train_steps_per_epoch
        self.nepochs = self.args.max_epochs if not self.args.debug_mode else 1
        self.total_steps = self.train_steps_per_epoch * self.nepochs
        self.starttime = datetime.now()
        self.timeout = timeout
        model.trainer_state = self.current_state # Pass reference to model

        self.notify(f"Training started! - Run ID: {self.run_id}")
        self.print_model_summary(model)

        pbar = tqdm(total=self.total_steps,
                initial=self.steps,
                desc=f"Training")
        return train_dataloader, optimizer, scheduler, grad_scaler, pbar
        
    
    def _optimizer_step(self,model,grad_scaler,optimizer,losses):
        grad_scaler.unscale_(optimizer)
        if self.args.log_grad_norm:
            grad_norm = self.get_grad_norm(model)
            losses['grad_norm'] = grad_norm
        self.clip_grad_norm(model)
        grad_scaler.step(optimizer)
        grad_scaler.update()
        optimizer.zero_grad()

    def _training_step(self,model,batch,batch_idx,grad_scaler):
        batch = batch_to(batch, self.device)
        with autocast(enabled=self.args.mixed_precision,device_type=self.device):
            losses = model.training_step(batch, batch_idx)
        loss = losses['loss']
        loss = loss / self.args.grad_accumulation_steps
        grad_scaler.scale(loss).backward()
        return losses
    
    def _pbar_step(self,pbar,step_losses,increment_step=True):
        postfix_str = f"Loss: {step_losses['loss']:.4f} | Epoch: {self.steps/self.train_steps_per_epoch:.4f}"
        if self.track_metric_name in self.current_state:
            postfix_str += f" | {self.track_metric_name}: {self.current_state[self.track_metric_name]:.4f}"
        pbar.set_postfix_str(postfix_str)
        pbar.update(1)
        if increment_step:
            self.steps += 1
    
    def _update_losses(self,losses,step_losses,running_losses,batch_idx):
        losses = {k: v.item() if isinstance(v, torch.Tensor) else v for k, v in losses.items()}
        step_losses.update(losses)
        for k,v in losses.items():
            running_losses[k] = (running_losses[k]*batch_idx+ v)/(batch_idx+1)
        
    
    def save_if_best(self,model):
        score = self.current_state[self.track_metric_name]
        is_best = (score < self.best_score if self.args.checkpoint_metric_minimize
                        else score > self.best_score
                    )
        if is_best:
            self.best_score = score
            best_path = os.path.join(self.args.results_dir,f"best_{self.steps}")
            self.save_checkpoint(model, os.path.join(self.args.results_dir,f"best_{self.steps}"))
            self.best_checkpoint = best_path
            self.notify(f"New best checkpoint found at {best_path}")
            self.remove_checkpoints()

    def timedout(self):
        elapsed = datetime.now() - self.starttime
        return self.timeout and elapsed > self.timeout

    def evaluate(self, model, dataset, collate_fn=None):
        if self.timedout():
            self.notify(f"Evaluation timed out after {self.timeout}! Update timeouts by setting trainer.timeout=[None|new-value]")
            return
        dataloader = self.get_dataloader(dataset,collate_fn)
        self.infer_train_val_steps(None, dataset)
        self.infer_device()

        pbar = tqdm(total=self.val_steps_per_epoch,leave=False,desc= f"Evaluating")
        model.eval()
        model.to(self.device)
        step_losses = defaultdict(float)
        running_losses = defaultdict(float)
        for batch_idx, batch in enumerate(dataloader):
            elapsed = datetime.now() - self.starttime
            if self.timeout and elapsed > self.timeout:
                self.notify(f"Evaluation timed out after {self.timeout}!")
                self.save_checkpoint(model, f"latest_{self.steps}")
                return
            batch = batch_to(batch, self.device)
            with torch.no_grad():
                losses = model.validation_step(batch, batch_idx)
            self._update_losses(losses, step_losses, running_losses, batch_idx)
            self._pbar_step(pbar, step_losses, increment_step=False)

            if (batch_idx+1)%self.args.log_every_n_steps==0:
                self.log_it(step_losses, log_type="val", level="step")
                self.log_it(running_losses, log_type="val", level="step_running")
                step_losses = defaultdict(float) # reset it here!

            if (batch_idx+1)==self.val_steps_per_epoch:
                break
            
        self.log_it(running_losses, log_type="val", level="epoch")
        pbar.close()

    def train_setup(self, model, train_dataset, collate_fn=None):
        model.to(self.device)
        train_dataloader = self.get_dataloader(train_dataset,collate_fn)
        optimizer = model.get_optimizer(self)
        scheduler = model.get_scheduler(optimizer,self)
        grad_scaler = self.get_grad_scaler(model)

        return train_dataloader, optimizer, scheduler, grad_scaler
    
    def make_dummy_call(self,model, loader):
        batch = next(iter(loader))
        batch = batch_to(batch, self.device)
        with torch.no_grad():
            model.training_step(batch, -1)
    
    def load_latest_checkpoint(self,model):
        if self.args.resume_from_checkpoint:
            if isinstance(self.args.resume_from_checkpoint, str):
                self.load_checkpoint(model, self.args.resume_from_checkpoint)
                self.notify(f"Resuming from checkpoint: {self.args.resume_from_checkpoint}")
            else:
                path = self.get_latest_checkpoint()
                if path:
                    self.load_checkpoint(model, path)
                    self.notify(f"Resuming from latest checkpoint: {path}")
        
    def get_dataloader(self,dataset,collate_fn=None):
        return (SafeDataLoader if self.args.safe_dataloader else DataLoader)(dataset,
                     batch_size=self.args.batch_size, 
                     num_workers=self.args.num_workers, collate_fn=collate_fn,shuffle=True,**self.args.dataloader_kwargs)


    def print_model_summary(self,model):
        from .modeling import ModelUtils
        data = []
        
        for name, instance in model.named_children():
            data.append({"Module":instance.__class__.__name__,
                    "parameter_count(m)":ModelUtils.get_parameter_count(instance) / 1e6,
                    "trainable_parameter_count(m)":ModelUtils.get_trainable_parameter_count(instance)/1e6,
                    "trainable": not ModelUtils.is_module_frozen(instance)})
            dtype = ModelUtils.get_dtype(instance)
            itemsize = dtype.itemsize if dtype is not None else 0
            data[-1]["Estimated Size (MB)"] = data[-1]["parameter_count(m)"] *1e6 * itemsize/1024/1024

        data.append({
            "Module": model.__class__.__name__ + " (Total)",
            "parameter_count(m)": model.parameter_count/1e6,
            "trainable_parameter_count(m)": model.trainable_parameter_count/1e6,
            "trainable": not model.isfrozen()
        })
        dtype = model.get_dtype()
        itemsize = dtype.itemsize if dtype is not None else 0
        data[-1]["Estimated Size (MB)"] = data[-1]["parameter_count(m)"] *1e6 * itemsize/1024/1024

        table = pd.DataFrame(data).round(2).to_markdown(index=False)
        s = f"\n{'-'*10} Model Summary {'-'*10}\n{table}\n{'-'*35}"
        logger.info(s)
    
    def infer_train_val_steps(self, train_dataset=None, val_dataset=None):
        if train_dataset is not None:
            self.train_steps_per_epoch = len(train_dataset) // self.args.batch_size
        if val_dataset is not None:
            self.val_steps_per_epoch = len(val_dataset) // self.args.batch_size
        if self.args.debug_mode:
            self.train_steps_per_epoch = self.args.grad_accumulation_steps + 5
            self.val_steps_per_epoch = 10
        if self.args.train_steps_per_epoch:
            self.train_steps_per_epoch = min(self.train_steps_per_epoch,self.args.train_steps_per_epoch)
        if self.args.val_steps_per_epoch:
            self.val_steps_per_epoch = min(self.val_steps_per_epoch,self.args.val_steps_per_epoch)
    
    def infer_device(self):
        if self.args.device:
            self.device = self.args.device
            return self.args.device
        if torch.cuda.is_available():
            self.device = "cuda"
            return "cuda"
        self.device= "cpu"
        return "cpu"
        
 
    def get_grad_scaler(self, model):
        return GradScaler(enabled=self.args.mixed_precision)
    
    def clip_grad_norm(self, model):
        if not self.args.grad_clip_norm:
            return
        torch.nn.utils.clip_grad_norm_(model.get_trainable_parameters(), self.args.grad_clip_norm)
    
    def get_current_lr(self, optimizer):
        for param_group in optimizer.param_groups:
            return param_group['lr']

    def get_grad_norm(self, model):
        grad_norm = torch.sqrt(
                    sum(param.grad.norm(2).pow(2) for param in model.parameters() if param.grad is not None)
                ).item()
        return grad_norm

    
    def log_it(self, log, prefix='',pbar=None,wandb=True, log_type="", level=""):
        log = log.copy()
        if level:
            level = f"_{level}"
        if log_type:
            log_type = f"{log_type}/"
        log = {f'{log_type}{prefix}{k}{level}': v for k, v in log.items()}
        self.current_state.update(log)
        log['step'] = self.current_state['steps']
        log['epoch'] = self.current_state['steps']/self.current_state['train_steps_per_epoch']
        self.logger.log(log)
        log['datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.logs.append(log)
        
    
    def save_checkpoint(self,model, path):
        if self.args.results_dir not in path:
            path = os.path.join(self.args.results_dir,path)
        os.makedirs(path, exist_ok=True)
        model.save(path)
        trainer_state = self.current_state.copy()
        trainer_state['logs'] = self.logs
        del trainer_state['timeout']
        del trainer_state['starttime']
        with open(os.path.join(path,'trainer_state.json'),'w') as f:
            json.dump(trainer_state,f,indent=4)
        self.args.to_json(os.path.join(path,'train_config.json'))
        self.remove_checkpoints()
    
    def load_checkpoint(self,model, path):
        if self.args.results_dir not in path:
            path = os.path.join(self.args.results_dir,path)
        checkpoint_path = os.path.join(path,'weights.safetensors')
        model.load_from_safetensors(checkpoint_path)
        with open(os.path.join(path,'trainer_state.json'),'r') as f:
            trainer_state = json.load(f)
        self.logs = trainer_state.pop('logs')
        self._current_state = trainer_state

    def get_checkpoints(self):
        checkpoints = os.listdir(self.args.results_dir)
        best_checkpoints = [os.path.join(self.args.results_dir,f) for f in checkpoints if f.startswith("best_")]
        latest_checkpoints = [os.path.join(self.args.results_dir,f) for f in checkpoints if f.startswith("latest_")]

        latest_checkpoints = sorted(latest_checkpoints, key=lambda x: float(x.split('latest_')[-1]), reverse=True)
        def best_key(x):
            with open(os.path.join(x,'trainer_state.json'),'r') as f:
                trainer_state = json.load(f)
                return trainer_state[self.current_state['track_metric_name']]
        best_checkpoints = sorted(best_checkpoints, key=best_key, reverse=False if self.args.checkpoint_metric_minimize else True)
        return best_checkpoints, latest_checkpoints
    
    def get_latest_checkpoint(self):
        return self.get_checkpoints()[1][0] if len(self.get_checkpoints()[1]) else None
    
    def get_best_checkpoint(self):
        return self.get_checkpoints()[0][0] if len(self.get_checkpoints()[0]) else None
    
    def remove_checkpoints(self):
        best_checkpoints, latest_checkpoints = self.get_checkpoints()
        to_remove = []
        if self.args.n_latest_checkpoints>0 and len(latest_checkpoints) > self.args.n_latest_checkpoints:
            to_remove.extend(latest_checkpoints[self.args.n_latest_checkpoints:])
        
     
        if self.args.n_best_checkpoints>0 and len(best_checkpoints) > self.args.n_best_checkpoints:
            to_remove.extend(best_checkpoints[self.args.n_best_checkpoints:])
        
        for path in to_remove:
            logger.info(f"Removing checkpoint: {path}")
            shutil.rmtree(path)

    def notify(self, message, level="info"):
        message += f"\n\n by {self.logger.project_name()} / {self.logger.name}"
        webhook = os.environ.get("SLACK_WEBHOOK_URL")
        if not webhook and self.args.slack_notify:
            logger.warning(f"Slack webhook not found. Skipping slack notification.")

        if level == "info":
            logger.info(message)
            if self.args.slack_notify and not self.args.debug_mode:
                notify_info(webhook, message)
        elif level == "warn":
            logger.warning(message)
            if self.args.slack_notify and not self.args.debug_mode:
                notify_warn(webhook, message)
        elif level == "priority":
            logger.error(message)
            if self.args.slack_notify and not self.args.debug_mode:
                notify_priority(webhook, message)
        else:
            logger.error(f"Invalid level: {level}. Skipping notification.")
            return
    def format_state(self,state):
        formatted = "\n".join(f"{key}: {value}" for key, value in state.items())
        return formatted

