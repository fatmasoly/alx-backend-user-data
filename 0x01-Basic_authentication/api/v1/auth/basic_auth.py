#!/usr/bin/env python3
""" Basic authentication"""

from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ Basic authentication class"""
    def __init__(self) -> None:
        """ Constructor"""
        super().__init__()
