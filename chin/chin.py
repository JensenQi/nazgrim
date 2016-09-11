from core import engine
from core.models import BaseModel

BaseModel.metadata.create_all(engine)
