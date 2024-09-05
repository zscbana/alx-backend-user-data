#!/usr/bin/env python3
"""User session management module.
"""
from models.base import Base


class UserSession(Base):
    """Represents a user session for tracking and management.
    """
    
    def __init__(self, *args, **kwargs):
        """Initializes a UserSession instance with user and session details.
        
        Args:
            *args: Additional positional arguments (if any) passed to the base class.
            **kwargs: Keyword arguments including 'user_id' and 'session_id'.
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
