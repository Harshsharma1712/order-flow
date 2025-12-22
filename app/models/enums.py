from enum import Enum as PyEnum

class UserType(str, PyEnum):
    NORMAL = "normal"
    SHOP_OWNER = "shop_owner"

class ItemStatus(str, PyEnum):
    PENDING = "pending"
    READY = "ready"
    PICKED = "picked"
    CANCELLED = "cancelled"