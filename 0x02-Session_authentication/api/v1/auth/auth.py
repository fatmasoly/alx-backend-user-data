#!/usr/bin/env python3
""" Auth module"""

from flask import request, jsonify
from typing import List, TypeVar
import os


class Auth:
    """ Auth class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require_auth method"""
        if path is None or excluded_paths is None or excluded_paths == []:
            return True

        if not path.endswith('/'):
            path = path + '/'

        for excluded_path in excluded_paths:
            if (excluded_path.endswith('*')
                    and path.startswith(excluded_path[:-1])):
                return False

            if path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ authorization_header method"""
        if request is None:
            return None

        header = request.headers.get('Authorization')
        if not header:
            return None

        return header

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user"""
        return None

    def session_cookie(self, request=None):
        """Session cookie"""
        if request:
            cookie_name = os.getenv('SESSION_NAME')
            return request.cookies.get(cookie_name)
