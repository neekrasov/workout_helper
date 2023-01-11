import uuid
from typing import NewType

UserId = NewType("UserId", uuid.UUID)
GroundId = NewType("GroundId", int)
