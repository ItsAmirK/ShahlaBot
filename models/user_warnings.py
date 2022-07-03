from .model_base import ModelBase, dataclass


@dataclass
class UserWarning(ModelBase):
    user_chat_id: int
    warns_count: int = 0
