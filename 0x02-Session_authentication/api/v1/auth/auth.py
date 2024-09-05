#!/usr/bin/env python3
"""Authentication module for the API.
"""
import os
import re
from typing import List, TypeVar
from flask import request

UserType = TypeVar('UserType')  # Define a type variable for User type


class Auth:
    """Base class for authentication methods.
    """
    
    def requires_authentication(self, path: str, excluded_paths: List[str]) -> bool:
        """Determines if a given path requires authentication.

        Args:
            path (str): The request path to check.
            excluded_paths (List[str]): List of paths that do not require authentication.

        Returns:
            bool: True if authentication is required, False otherwise.
        """
        if path and excluded_paths:
            for exclusion_path in map(lambda p: p.strip(), excluded_paths):
                pattern = ''
                if exclusion_path.endswith('*'):
                    pattern = '{}.*'.format(exclusion_path[:-1])
                elif exclusion_path.endswith('/'):
                    pattern = '{}/*'.format(exclusion_path[:-1])
                else:
                    pattern = '{}/*'.format(exclusion_path)
                if re.match(pattern, path):
                    return False
        return True

    def get_authorization_header(self, request=None) -> str:
        """Retrieves the Authorization header from the request.

        Args:
            request: The Flask request object.

        Returns:
            str: The Authorization header value, or None if not present.
        """
        if request:
            return request.headers.get('Authorization', None)
        return None

    def get_current_user(self, request=None) -> UserType:
        """Retrieves the user associated with the current request.

        Args:
            request: The Flask request object.

        Returns:
            UserType: The current user, or None if not authenticated.
        """
        return None

    def get_session_cookie(self, request=None) -> str:
        """Retrieves the value of the session cookie named SESSION_NAME.

        Args:
            request: The Flask request object.

        Returns:
            str: The session cookie value, or None if not present.
        """
        if request:
            cookie_name = os.getenv('SESSION_NAME')
            return request.cookies.get(cookie_name)
        return None
