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

class ToneType(Enum):
    CASUAL = "casual"
    FORMAL = "formal"
    PLAYFUL = "playful"
    CARING = "caring"
    BUSINESS = "business"
    ROMANTIC = "romantic"
    FRIENDLY = "friendly"
    SERIOUS = "serious"

class RelationshipContext(Enum):
    FAMILY = "family"
    FRIEND = "friend"
    ROMANTIC = "romantic"
    BUSINESS = "business"
    ACQUAINTANCE = "acquaintance"
    UNKNOWN = "unknown"

@dataclass
class ToneEmbedding:
    """Tone embedding for vector search with UUID v7"""
    embedding_id: str = field(default_factory=generate_uuid7)
    user_id: str = ""
    tone_vector: List[float] = field(default_factory=list)
    message_vector: List[float] = field(default_factory=list)
    style_vector: List[float] = field(default_factory=list)
    tone_type: str = ToneType.CASUAL.value
    message_sample: str = ""
    confidence_score: float = 0.0
    relationship_context: str = RelationshipContext.UNKNOWN.value
    emotional_intensity: float = 0.5
    formality_level: float = 0.5
    created_at: str = field(default_factory=current_iso_timestamp)
    metadata: Dict[str, Any] = field(default_factory=dict)
    vector_model: str = "all-MiniLM-L6-v2"
    vector_dimension: int = 384
    
    def __post_init__(self):
        """Ensure UUID v7 format and metadata"""
        if not self.embedding_id or len(self.embedding_id) < 30:
            self.embedding_id = generate_uuid7()
        if not self.created_at:
            self.created_at = current_iso_timestamp()
        
        # Add metadata
        if "uuid_version" not in self.metadata:
            self.metadata["uuid_version"] = "v7"
        if "embedding_created_at" not in self.metadata:
            self.metadata["embedding_created_at"] = self.created_at
    
    def to_dict(self):
        """Convert to dictionary for DataStax storage with vector field"""
        data = asdict(self)
        # Ensure UUIDs are stored as strings
        data['embedding_id'] = str(self.embedding_id)
        data['user_id'] = str(self.user_id)
        
        # Add vector field for Astra vector search (primary vector)
        if self.tone_vector:
            data['$vector'] = self.tone_vector
        
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create ToneEmbedding from dictionary"""
        # Remove vector field before creating object
        if '$vector' in data:
            if not data.get('tone_vector'):
                data['tone_vector'] = data['$vector']
            data.pop('$vector')
        
        defaults = {
            'metadata': {},
            'tone_vector': [],
            'message_vector': [],
            'style_vector': [],
            'vector_model': 'all-MiniLM-L6-v2',
            'vector_dimension': 384,
            'emotional_intensity': 0.5,
            'formality_level': 0.5
        }
        
        for key, default_value in defaults.items():
            if key not in data:
                data[key] = default_value
            
        return cls(**data)
    
    def get_vector_info(self) -> Dict[str, Any]:
        """Get vector information for debugging"""
        return {
            "embedding_id": self.embedding_id,
            "tone_vector_dim": len(self.tone_vector),
            "message_vector_dim": len(self.message_vector),
            "style_vector_dim": len(self.style_vector),
            "vector_model": self.vector_model,
            "confidence_score": self.confidence_score,
            "uuid_version": "v7"
        }

@dataclass
class MessageEmbedding:
    """Message embedding for advanced vector operations with UUID v7"""
    message_embedding_id: str = field(default_factory=generate_uuid7)
    message_id: str = ""
    user_id: str = ""
    conversation_id: str = ""
    content_vector: List[float] = field(default_factory=list)
    style_vector: List[float] = field(default_factory=list)
    tone_vector: List[float] = field(default_factory=list)
    semantic_vector: List[float] = field(default_factory=list)
    message_text: str = ""
    detected_tone: str = ToneType.CASUAL.value
    sentiment_score: float = 0.0
    emotional_score: float = 0.0
    formality_score: float = 0.5
    timestamp: str = field(default_factory=current_iso_timestamp)
    metadata: Dict[str, Any] = field(default_factory=dict)
    vector_model: str = "all-MiniLM-L6-v2"
    
    def __post_init__(self):
        """Ensure UUID v7 format"""
        if not self.message_embedding_id:
            self.message_embedding_id = generate_uuid7()
        if not self.message_id:
            self.message_id = generate_uuid7()
        if not self.conversation_id:
            self.conversation_id = generate_uuid7()
        
        # Add metadata
        if "uuid_version" not in self.metadata:
            self.metadata["uuid_version"] = "v7"
        if "message_length" not in self.metadata:
            self.metadata["message_length"] = len(self.message_text)
    
    def to_dict(self):
        """Convert to dictionary with primary vector for search"""
        data = asdict(self)
        # Ensure UUIDs are strings
        data['message_embedding_id'] = str(self.message_embedding_id)
        data['message_id'] = str(self.message_id)
        data['user_id'] = str(self.user_id)
        data['conversation_id'] = str(self.conversation_id)
        
        # Use content_vector as primary vector for search
        if self.content_vector:
            data['$vector'] = self.content_vector
        
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create from dictionary"""
        if '$vector' in data:
            if not data.get('content_vector'):
                data['content_vector'] = data['$vector']
            data.pop('$vector')
        
        defaults = {
            'metadata': {},
            'content_vector': [],
            'style_vector': [],
            'tone_vector': [],
            'semantic_vector': [],
            'sentiment_score': 0.0,
            'emotional_score': 0.0,
            'formality_score': 0.5,
            'vector_model': 'all-MiniLM-L6-v2'
        }
        
        for key, default_value in defaults.items():
            if key not in data:
                data[key] = default_value
        
        return cls(**data)

@dataclass
class ToneAnalysis:
    """Comprehensive tone analysis results with UUID v7"""
    analysis_id: str = field(default_factory=generate_uuid7)
    message_id: str = ""
    user_id: str = ""
    primary_tone: str = ToneType.CASUAL.value
    secondary_tones: List[str] = field(default_factory=list)
    confidence_scores: Dict[str, float] = field(default_factory=dict)
    emotional_profile: Dict[str, float] = field(default_factory=dict)
    style_features: Dict[str, Any] = field(default_factory=dict)
    relationship_context: str = RelationshipContext.UNKNOWN.value
    formality_level: float = 0.5
    emotional_intensity: float = 0.5
    sentiment_polarity: float = 0.0
    created_at: str = field(default_factory=current_iso_timestamp)
    processing_time_ms: float = 0.0
    model_version: str = "1.0"
    
    def __post_init__(self):
        """Initialize with UUID v7"""
        if not self.analysis_id:
            self.analysis_id = generate_uuid7()
    
    def to_dict(self):
        """Convert to dictionary"""
        data = asdict(self)
        data['analysis_id'] = str(self.analysis_id)
        data['message_id'] = str(self.message_id)
        data['user_id'] = str(self.user_id)
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create from dictionary"""
        defaults = {
            'secondary_tones': [],
            'confidence_scores': {},
            'emotional_profile': {},
            'style_features': {},
            'formality_level': 0.5,
            'emotional_intensity': 0.5,
            'sentiment_polarity': 0.0,
            'processing_time_ms': 0.0,
            'model_version': '1.0'
        }
        
        for key, default_value in defaults.items():
            if key not in data:
                data[key] = default_value
        
        return cls(**data)
    
    def get_dominant_tone(self) -> str:
        """Get the tone with highest confidence"""
        if not self.confidence_scores:
            return self.primary_tone
        
        max_confidence_tone = max(self.confidence_scores.items(), key=lambda x: x[1])
        return max_confidence_tone[0]