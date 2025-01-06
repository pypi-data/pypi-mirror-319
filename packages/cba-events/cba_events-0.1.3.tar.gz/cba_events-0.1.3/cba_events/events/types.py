from dataclasses import dataclass
from typing import Optional, Dict, Any
from .base_event import BaseEvent


@dataclass
class VolumetricEvent(BaseEvent):
    """Stockpile-related event class"""

    user_id: str
    action: str
    payload: Optional[Dict[str, Any]] = None

    def __init__(
        self,
        user_id: str,
        action: str,
        site: str,
        location: str,
        entity: str,
        survey_date: str,
        **kwargs,
    ):
        super().__init__(
            event_type="stockpile",
            entity=entity,
            location=location,
            survey_date=survey_date,
            site=site,
            **kwargs,
        )
        self.user_id = user_id
        self.action = action
        self.payload = kwargs.get("payload", {})
