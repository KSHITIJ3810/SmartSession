
import logging
from datetime import datetime
from typing import Dict, List
from models import UserState


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger("engagement")


def handle_error(err: Exception) -> Dict:
    logger.error(f"Error: {err}")
    return {"error": str(err), "timestamp": datetime.now().isoformat()}


class TimelineStore:
    def __init__(self):
        self.sessions: Dict[str, List[UserState]] = {}

    def add_event(self, session_id: str, state: UserState):
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        self.sessions[session_id].append(state)
        logger.info(f"Event added for session {session_id}: {state.dict()}")

    def get_timeline(self, session_id: str) -> List[UserState]:
        return self.sessions.get(session_id, [])

    def clear_session(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]
            logger.info(f"Timeline cleared for session {session_id}")


timeline_store = TimelineStore()