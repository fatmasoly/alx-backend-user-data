#!/usr/bin/env python3
""" SessionAuth module"""

from models.user import User
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """SessionAuth class"""
    user_id_by_session_id = {}

    def __init__(self) -> None:
        """ Constructor"""
        super().__init__()

    def create_session(self, user_id: str = None) -> str:
        """ Create a session"""
        if not user_id or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ User ID for session ID"""
        if not session_id or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)
