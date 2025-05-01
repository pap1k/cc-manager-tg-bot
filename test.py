from config import settings
from database import Base
from models import *


for table in Base.metadata.tables:
    print(table)
