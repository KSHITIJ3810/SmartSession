
from pydantic import BaseModel
from datetime import datetime
from typing import List


class UserState(BaseModel):
    student_id: str
    look: str
    mood: str
    confused_val: float
    time: datetime


class SessionData(BaseModel):
    s_id: str
    u_id: str
    logs: List[UserState]
    look: str
    mood: str
    confused_val: float
    time: datetime




class TeacherInfo(BaseModel):
    t_id: str
    students: List[str]
    updated_at: datetime


class SocketMsg(BaseModel):
    msg_type: str
    data: dict

class SimpleError(BaseModel):
    err: str
    status: int = 404