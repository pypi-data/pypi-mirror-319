from dataclasses import dataclass
from typing import Optional, Dict, Any
from .base_event import BaseEvent


# @dataclass
class VolumetricEvent(BaseEvent):
    """Stockpile-related event class"""

    user_id: str
    action: str
    payload: Optional[Dict[str, Any]] = None

    def __init__(
        self,
        site: str,
        location: str,
        entity: str,
        survey_date: str,
        user_id: str,
        action: str,
        **kwargs,
    ):
        super().__init__(entity, location, site, survey_date, "stockpile")
        self.user_id = user_id
        self.action = action
        self.payload = kwargs.get("payload", {})
