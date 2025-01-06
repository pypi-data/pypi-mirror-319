from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any
from datetime import datetime
import json
import uuid
from dataclasses_json import DataClassJsonMixin


@dataclass
class BaseEvent(DataClassJsonMixin):
    """Base event class with common attributes for all events"""

    event_id: str
    event_type: str
    timestamp: str
    entity: str
    location: str
    site: str
    survey_date: str
    correlation_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    def __init__(self, event_type: str, entity: str, site: str, **kwargs):
        self.event_id = str(uuid.uuid4())
        self.event_type = event_type
        self.timestamp = datetime.now(datetime.UTC)
        self.entity = entity
        self.site = site
        self.correlation_id = kwargs.get("correlation_id")
        self.metadata = kwargs.get("metadata", {})
        self.location = kwargs.get("location")
        self.survey_date = kwargs.get("survey_date")
