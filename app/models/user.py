from typing import Dict, Any, Optional, List
from datetime import datetime, timezone
from dataclasses import dataclass, asdict, field
from uuid6 import uuid7
import json

def generate_uuid7() -> str:
    """Generate UUID v7 string"""
    return str(uuid7())

def current_iso_timestamp() -> str:
    """Generate current ISO timestamp with timezone"""
    return datetime.now(timezone.utc).isoformat()

@dataclass
class UserProfile:
    """User profile for DataStax Astra with UUID v7 optimization"""
    user_id: str = field(default_factory=generate_uuid7)
    phone_number: str = ""
    name: str = ""
    relationship: str = ""
    primary_tone: str = "casual"
    tone_weights: Dict[str, float] = field(default_factory=lambda: {
        "casual": 0.7, "formal": 0.2, "playful": 0.1
    })
    avg_message_length: float = 0.0
    emoji_frequency: float = 0.0
    formality_level: float = 0.5
    common_phrases: List[str] = field(default_factory=list)
    vocabulary: List[str] = field(default_factory=list)
    style_vector: Optional[List[float]] = None
    created_at: str = field(default_factory=current_iso_timestamp)
    updated_at: str = field(default_factory=current_iso_timestamp)
    last_interaction: Optional[str] = None
    interaction_count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    version: str = "1.0"  # For schema versioning
    
    def __post_init__(self):
        """Ensure UUID v7 format and proper timestamps"""
        if not self.user_id or len(self.user_id) < 30:  # Basic UUID validation
            self.user_id = generate_uuid7()
        
        # Ensure timestamps are properly formatted
        if not self.created_at:
            self.created_at = current_iso_timestamp()
        if not self.updated_at:
            self.updated_at = current_iso_timestamp()
        
        # Add UUID version info to metadata
        if "uuid_version" not in self.metadata:
            self.metadata["uuid_version"] = "v7"
    
    def update_timestamp(self):
        """Update the updated_at timestamp"""
        self.updated_at = current_iso_timestamp()
    
    def to_dict(self):
        """Convert to dictionary for DataStax storage"""
        data = asdict(self)
        # Ensure UUID v7 is stored as string
        data['user_id'] = str(self.user_id)
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create UserProfile from dictionary"""
        data_copy = data.copy()
        data_copy.pop('_id', None)  # Remove _id field from DataStax
        data_copy.pop('$vector', None)  # Remove vector field if present

        defaults = {
            'tone_weights': {"casual": 0.7, "formal": 0.2, "playful": 0.1},
            'common_phrases': [],
            'vocabulary': [],
            'metadata': {},
            'interaction_count': 0,
            'avg_message_length': 0.0,
            'emoji_frequency': 0.0,
            'formality_level': 0.5,
            'version': '1.0'
        }
        
        # Apply defaults to data_copy
        for key, default_value in defaults.items():
            if key not in data_copy:
                data_copy[key] = default_value
        
        return cls(**data_copy)  # Use data_copy instead of data

    def get_uuid_info(self) -> Dict[str, Any]:
        """Get UUID information for debugging"""
        return {
            "user_id": self.user_id,
            "uuid_version": "v7",
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "uuid_timestamp": uuid7().time if hasattr(uuid7(), 'time') else None
        }