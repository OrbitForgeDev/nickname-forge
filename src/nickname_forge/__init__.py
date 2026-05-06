"""
Nickname Forge — CLI tool for generating memorable nicknames.
"""

from .engine import NicknameForge, Nickname, StyleNotFoundError

__all__ = ["NicknameForge", "Nickname", "StyleNotFoundError"]
__version__ = "0.1.0"