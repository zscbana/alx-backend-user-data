#!/usr/bin/env python3
"""Session authentication with expiration and storage support module for the API.
"""
from flask import request
from datetime import datetime, timedelta

from models.user_session import UserSession
from .session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """Handles session-based authentication with expiration and database storage support.
    """

    def create_session(self, user_id=None) -> str:
        """Creates and stores a session ID for a user.
        
        Args:
            user_id (str): The ID of the user for whom to create a session.
        
        Returns:
            str: The created session ID, or None if creation fails.
        """
        session_id = super().create_session(user_id)
        if isinstance(session_id, str):
            session_data = {
                'user_id': user_id,
                'session_id': session_id,
            }
            user_session = UserSession(**session_data)
            user_session.save()
            return session_id

    def get_user_id_from_session(self, session_id=None) -> str:
        """Retrieves the user ID associated with a given session ID.
        
        Args:
            session_id (str): The ID of the session to look up.
        
        Returns:
            str: The user ID associated with the session ID, or None if not found or expired.
        """
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        
        if not sessions:
            return None
        
        current_time = datetime.now()
        expiration_time = sessions[0].created_at + timedelta(seconds=self.session_duration)
        
        if expiration_time < current_time:
            return None
        
        return sessions[0].user_id

    def terminate_session(self, request=None) -> bool:
        """Ends an authenticated session.
        
        Args:
            request: The Flask request object.

        Returns:
            bool: True if the session was successfully terminated, False otherwise.
        """
        session_id = self.session_cookie(request)
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False
        
        if not sessions:
            return False
        
        sessions[0].remove()
        return True
