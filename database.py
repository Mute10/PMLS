from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from tools import Base

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index = True)
    description = Column(String)
    start_date = Column(DateTime, default = datetime.utcnow)
    end_date = Column(DateTime, nullable = True)
    is_complete = Column(Boolean, default = False)
   
