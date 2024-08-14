#!/usr/bin/env python3
""" Auth module"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """ Returns a salted hash of the input password"""
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hash_password
