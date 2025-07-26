from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from datetime import datetime
from typing import Dict, Any, Optional
from uuid6 import uuid7

class UserProfile(Model):
    """ User profile model for DataStax """
    __table_name__ = 'user_profiles'

    # Primary key
    user_id = columns.UUID(primary_key=True, default=uuid7)
    phone_number = columns.Text(index=True)

    # Basic information
    name = columns.Text()
    relationship = columns.Text()

    # Tone preferences
    primary_tone = columns.Text()
    tone_weights = columns.Map(columns.Text, columns.Float)

    # Communication style
    avg_messsage_length = columns.Float(default=0.0)
    emoji_frequency = columns.Float(default=0.0)
    formality_level = columns.Float(default=0.5)
    common_phrases = columns.List(columns.Text)
    vocabulary = columns.List(columns.Text)

    # Metadata
    created_at = columns.DateTime(default=datetime.now)
    updated_at = columns.DateTime(default=datetime.now)
    last_interation = columns.DateTime()
    interaction_count = columns.Integer(default=0)

    # Additional data
    metadata = columns.Map(columns.Text, columns.Text)

class Conversation(Model):
    """ Converstation model for DataStax """
    __table_name__ = 'conversations'

    # Composite primary key for time-series data
    user_id = columns.UUID(partition_key=True)
    conversation_id = columns.UUID(primary_key=True, default=uuid7)
    message_id = columns.UUID(primary_key=True, default=uuid7)
    timestamp = columns.DateTime(primary_key=True, default=datetime.now)

    # Message content
    message_text = columns.Text()
    message_type = columns.Text(default='text')
    sender = columns.Text()

    # Tone analysis
    detacted_tone = columns.Text()
    tone_confidence = columns.Float()
    emotional_score = columns.Float()

    # Context
    context_data = columns.Map(columns.Text, columns.Text)

class ToneAnalysis(Model):
    """ Tone analysis results for DataStax """
    __table_name__ = 'tone_analysis'

    # Primary key
    analysis_id = columns.UUID(primary_key=True, default=uuid7)
    user_id = columns.UUID(index=True)
    message_id = columns.UUID(index=True)

    # Analysis results
    primary_tone = columns.Text()
    confidence_scores = columns.Float()
    tone_features = columns.Map(columns.Text, columns.Float)
    emotional_profile = columns.Map(columns.Text, columns.Float)

    # Metadata
    analyzed_at = columns.DateTime(default=datetime.now)
    model_version = columns.Text()

    