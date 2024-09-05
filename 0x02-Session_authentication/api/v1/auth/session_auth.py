#!/usr/bin/env python3
"""Session authentication module for the API.
"""
from uuid import uuid4
from flask import request

from .auth import Auth
from models.user import User


class SessionAuth(Auth):
    """Handles session-based authentication.
    """
    sessions = {}

    def create_session(self, user_id: str = None) -> str:
        """Generates a new session ID for the given user ID.
        
        Args:
            user_id (str): The ID of the user for whom to create a session.

        Returns:
            str: The newly created session ID, or None if user_id is invalid.
        """
        if isinstance(user_id, str):
            session_id = str(uuid4())
            self.sessions[session_id] = user_id
            return session_id

    def get_user_id_from_session(self, session_id: str = None) -> str:
        """Fetches the user ID associated with a given session ID.
        
        Args:
            session_id (str): The ID of the session to look up.

        Returns:
            str: The user ID associated with the session ID, or None if not found.
        """
        if isinstance(session_id, str):
            return self.sessions.get(session_id)

    def get_current_user(self, request=None) -> User:
        """Retrieves the user associated with the current request.
        
        Args:
            request: The Flask request object.

        Returns:
            User: The user associated with the request, or None if not found.
        """
        session_id = self.session_cookie(request)
        user_id = self.get_user_id_from_session(session_id)
        return User.get(user_id)

    def terminate_session(self, request=None) -> bool:
        """Ends the session associated with the current request.
        
        Args:
            request: The Flask request object.

        Returns:
            bool: True if the session was successfully destroyed, False otherwise.
        """
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.get_user_id_from_session(session_id)
        if user_id is None:
            return False
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False
