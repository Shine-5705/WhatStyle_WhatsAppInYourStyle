from typing import Dict, Any, Optional, List
from datetime import datetime, timezone
from dataclasses import dataclass, asdict, field
from uuid6 import uuid7
from enum import Enum

def generate_uuid7() -> str:
    """Generate UUID v7 string"""
    return str(uuid7())

def current_iso_timestamp() -> str:
    """Generate current ISO timestamp with timezone"""
    return datetime.now(timezone.utc).isoformat()

class MessageType(Enum):
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    DOCUMENT = "document"
    LOCATION = "location"
    CONTACT = "contact"

class SenderType(Enum):
    USER = "user"
    BOT = "bot"
    SYSTEM = "system"

@dataclass 
class Conversation:
    """Conversation message for DataStax Astra with UUID v7"""
    message_id: str = field(default_factory=generate_uuid7)
    user_id: str = ""
    conversation_id: str = ""
    message_text: str = ""
    sender: str = SenderType.USER.value  # 'user' or 'bot'
    message_type: str = MessageType.TEXT.value
    detected_tone: Optional[str] = None
    tone_confidence: Optional[float] = None
    emotional_score: Optional[float] = None
    sentiment_score: Optional[float] = None
    timestamp: str = field(default_factory=current_iso_timestamp)
    context_data: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    processed: bool = False
    response_generated: bool = False
    
    def __post_init__(self):
        """Ensure UUID v7 format"""
        if not self.message_id or len(self.message_id) < 30:
            self.message_id = generate_uuid7()
        if not self.conversation_id:
            self.conversation_id = generate_uuid7()
        if not self.timestamp:
            self.timestamp = current_iso_timestamp()
        
        # Add metadata
        if "uuid_version" not in self.metadata:
            self.metadata["uuid_version"] = "v7"
        if "message_length" not in self.metadata:
            self.metadata["message_length"] = len(self.message_text)
    
    def to_dict(self):
        """Convert to dictionary for DataStax storage"""
        data = asdict(self)
        # Ensure UUIDs are stored as strings
        data['message_id'] = str(self.message_id)
        data['user_id'] = str(self.user_id)
        data['conversation_id'] = str(self.conversation_id)
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create Conversation from dictionary"""
        defaults = {
            'context_data': {},
            'metadata': {},
            'processed': False,
            'response_generated': False,
            'sentiment_score': None,
            'message_type': MessageType.TEXT.value,
            'sender': SenderType.USER.value
        }
        
        for key, default_value in defaults.items():
            if key not in data:
                data[key] = default_value
        
        return cls(**data)
    
    def mark_processed(self):
        """Mark message as processed"""
        self.processed = True
        self.metadata["processed_at"] = current_iso_timestamp()
    
    def mark_response_generated(self):
        """Mark that response has been generated"""
        self.response_generated = True
        self.metadata["response_generated_at"] = current_iso_timestamp()
    
    def get_message_info(self) -> Dict[str, Any]:
        """Get message information for debugging"""
        return {
            "message_id": self.message_id,
            "conversation_id": self.conversation_id,
            "sender": self.sender,
            "message_type": self.message_type,
            "timestamp": self.timestamp,
            "processed": self.processed,
            "uuid_version": "v7",
            "character_count": len(self.message_text)
        }

@dataclass
class ConversationSession:
    """Conversation session tracking with UUID v7"""
    session_id: str = field(default_factory=generate_uuid7)
    user_id: str = ""
    started_at: str = field(default_factory=current_iso_timestamp)
    ended_at: Optional[str] = None
    message_count: int = 0
    active: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Initialize session with UUID v7"""
        if not self.session_id:
            self.session_id = generate_uuid7()
        if "uuid_version" not in self.metadata:
            self.metadata["uuid_version"] = "v7"
    
    def add_message(self):
        """Increment message count"""
        self.message_count += 1
    
    def end_session(self):
        """End the conversation session"""
        self.active = False
        self.ended_at = current_iso_timestamp()
    
    def to_dict(self):
        """Convert to dictionary for storage"""
        data = asdict(self)
        data['session_id'] = str(self.session_id)
        data['user_id'] = str(self.user_id)
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create from dictionary"""
        defaults = {
            'metadata': {},
            'message_count': 0,
            'active': True
        }
        
        for key, default_value in defaults.items():
            if key not in data:
                data[key] = default_value
        
        return cls(**data)