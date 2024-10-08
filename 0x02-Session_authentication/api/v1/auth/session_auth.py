#!/usr/bin/env python3
""" SessionAuth module"""

from models.user import User
from api.v1.auth.auth import Auth
from api.v1.views import app_views
import uuid
from flask import request, jsonify, abort
from os import getenv


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

    def current_user(self, request=None):
        """ Current user"""
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)

        return User.get(user_id)

    def destroy_session(self, request=None):
        """Destroy the user session"""
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False

        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
        return True
