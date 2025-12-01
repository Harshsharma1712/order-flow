from enum import Enum

class UserTypeEnum(str, Enum):
    NORMAL = "normal"
    SHOP_OWNER = "shop_owner"


class ItemStatusEnum(str, Enum):
    PENDING = "pending"
    READY = "ready"
    PICKED = "picked"
