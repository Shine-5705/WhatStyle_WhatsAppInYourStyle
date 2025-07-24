from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MessageType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MESSAGE_TYPE_UNSPECIFIED: _ClassVar[MessageType]
    MESSAGE_TYPE_TEXT: _ClassVar[MessageType]
    MESSAGE_TYPE_IMAGE: _ClassVar[MessageType]
    MESSAGE_TYPE_AUDIO: _ClassVar[MessageType]
    MESSAGE_VIDEO: _ClassVar[MessageType]
    MESSAGE_TYPE_DOCUMENT: _ClassVar[MessageType]
    MESSAGE_TYPE_STICKER: _ClassVar[MessageType]
    MESSAGE_TYPE_LOCATION: _ClassVar[MessageType]
    MESSAGE_TYPE_CONTACT: _ClassVar[MessageType]

class ToneType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TONE_TYPE_UNSPECIFIED: _ClassVar[ToneType]
    TONE_TYPE_CASUAL: _ClassVar[ToneType]
    TONE_TYPE_FORMAL: _ClassVar[ToneType]
    TONE_TYPE_PLAYFUL: _ClassVar[ToneType]
    TONE_TYPE_CARING: _ClassVar[ToneType]
    TONE_TYPE_BUSINESS: _ClassVar[ToneType]
    TONE_TYPE_ROMANTIC: _ClassVar[ToneType]
    TONE_TYPE_FRIENDLY: _ClassVar[ToneType]
    TONE_TYPE_PROFESSIONAL: _ClassVar[ToneType]

class ConversationEvent(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONVERSATION_EVENT_UNSPECIFIED: _ClassVar[ConversationEvent]
    CONVERSATION_EVENT_MESSAGE_RECEIVED: _ClassVar[ConversationEvent]
    CONVERSATION_EVENT_MESSAGE_SENT: _ClassVar[ConversationEvent]
    CONVERSATION_EVENT_TONE_UPDATED: _ClassVar[ConversationEvent]
    CONVERSATION_EVENT_CONTEXT_CHANGED: _ClassVar[ConversationEvent]
    CONVERSATION_EVENT_USER_TYPING: _ClassVar[ConversationEvent]

class ConversationState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONVERSATION_STATE_UNSPECIFIED: _ClassVar[ConversationState]
    CONVERSATION_STATE_ACTIVE: _ClassVar[ConversationState]
    CONVERSATION_STATE_WAITING: _ClassVar[ConversationState]
    CONVERSATION_STATE_PAUSED: _ClassVar[ConversationState]
    CONVERSATION_STATE_ENDED: _ClassVar[ConversationState]

class HealthStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    HEALTH_STATUS_UNSPECIFIED: _ClassVar[HealthStatus]
    HEALTH_STATUS_HEALTHY: _ClassVar[HealthStatus]
    HEALTH_STATUS_DEGRADED: _ClassVar[HealthStatus]
    HEALTH_STATUS_UNHEALTHY: _ClassVar[HealthStatus]
    HEALTH_STATUS_UNKNOWN: _ClassVar[HealthStatus]
MESSAGE_TYPE_UNSPECIFIED: MessageType
MESSAGE_TYPE_TEXT: MessageType
MESSAGE_TYPE_IMAGE: MessageType
MESSAGE_TYPE_AUDIO: MessageType
MESSAGE_VIDEO: MessageType
MESSAGE_TYPE_DOCUMENT: MessageType
MESSAGE_TYPE_STICKER: MessageType
MESSAGE_TYPE_LOCATION: MessageType
MESSAGE_TYPE_CONTACT: MessageType
TONE_TYPE_UNSPECIFIED: ToneType
TONE_TYPE_CASUAL: ToneType
TONE_TYPE_FORMAL: ToneType
TONE_TYPE_PLAYFUL: ToneType
TONE_TYPE_CARING: ToneType
TONE_TYPE_BUSINESS: ToneType
TONE_TYPE_ROMANTIC: ToneType
TONE_TYPE_FRIENDLY: ToneType
TONE_TYPE_PROFESSIONAL: ToneType
CONVERSATION_EVENT_UNSPECIFIED: ConversationEvent
CONVERSATION_EVENT_MESSAGE_RECEIVED: ConversationEvent
CONVERSATION_EVENT_MESSAGE_SENT: ConversationEvent
CONVERSATION_EVENT_TONE_UPDATED: ConversationEvent
CONVERSATION_EVENT_CONTEXT_CHANGED: ConversationEvent
CONVERSATION_EVENT_USER_TYPING: ConversationEvent
CONVERSATION_STATE_UNSPECIFIED: ConversationState
CONVERSATION_STATE_ACTIVE: ConversationState
CONVERSATION_STATE_WAITING: ConversationState
CONVERSATION_STATE_PAUSED: ConversationState
CONVERSATION_STATE_ENDED: ConversationState
HEALTH_STATUS_UNSPECIFIED: HealthStatus
HEALTH_STATUS_HEALTHY: HealthStatus
HEALTH_STATUS_DEGRADED: HealthStatus
HEALTH_STATUS_UNHEALTHY: HealthStatus
HEALTH_STATUS_UNKNOWN: HealthStatus

class MessageRequest(_message.Message):
    __slots__ = ("message_id", "sender_phone", "message_text", "message_type", "timestamp", "metadata", "conversation_id")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    SENDER_PHONE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_TEXT_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    message_id: str
    sender_phone: str
    message_text: str
    message_type: MessageType
    timestamp: _timestamp_pb2.Timestamp
    metadata: _containers.ScalarMap[str, str]
    conversation_id: str
    def __init__(self, message_id: _Optional[str] = ..., sender_phone: _Optional[str] = ..., message_text: _Optional[str] = ..., message_type: _Optional[_Union[MessageType, str]] = ..., timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., metadata: _Optional[_Mapping[str, str]] = ..., conversation_id: _Optional[str] = ...) -> None: ...

class MessageResponse(_message.Message):
    __slots__ = ("response_id", "response_text", "applied_tone", "confidence_score", "generated_at", "suggested_responses", "processing_info")
    RESPONSE_ID_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_TEXT_FIELD_NUMBER: _ClassVar[int]
    APPLIED_TONE_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_SCORE_FIELD_NUMBER: _ClassVar[int]
    GENERATED_AT_FIELD_NUMBER: _ClassVar[int]
    SUGGESTED_RESPONSES_FIELD_NUMBER: _ClassVar[int]
    PROCESSING_INFO_FIELD_NUMBER: _ClassVar[int]
    response_id: str
    response_text: str
    applied_tone: ToneType
    confidence_score: float
    generated_at: _timestamp_pb2.Timestamp
    suggested_responses: _containers.RepeatedScalarFieldContainer[str]
    processing_info: ProcessingMetadata
    def __init__(self, response_id: _Optional[str] = ..., response_text: _Optional[str] = ..., applied_tone: _Optional[_Union[ToneType, str]] = ..., confidence_score: _Optional[float] = ..., generated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., suggested_responses: _Optional[_Iterable[str]] = ..., processing_info: _Optional[_Union[ProcessingMetadata, _Mapping]] = ...) -> None: ...

class ProcessingMetadata(_message.Message):
    __slots__ = ("processing_time_ms", "model_used", "tone_profile_id", "tone_scores")
    class ToneScoresEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: float
        def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
    PROCESSING_TIME_MS_FIELD_NUMBER: _ClassVar[int]
    MODEL_USED_FIELD_NUMBER: _ClassVar[int]
    TONE_PROFILE_ID_FIELD_NUMBER: _ClassVar[int]
    TONE_SCORES_FIELD_NUMBER: _ClassVar[int]
    processing_time_ms: int
    model_used: str
    tone_profile_id: str
    tone_scores: _containers.ScalarMap[str, float]
    def __init__(self, processing_time_ms: _Optional[int] = ..., model_used: _Optional[str] = ..., tone_profile_id: _Optional[str] = ..., tone_scores: _Optional[_Mapping[str, float]] = ...) -> None: ...

class ConversationStreamRequest(_message.Message):
    __slots__ = ("user_id", "conversation_ids", "include_tone_analysis")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    CONVERSATION_IDS_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_TONE_ANALYSIS_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    conversation_ids: _containers.RepeatedScalarFieldContainer[str]
    include_tone_analysis: bool
    def __init__(self, user_id: _Optional[str] = ..., conversation_ids: _Optional[_Iterable[str]] = ..., include_tone_analysis: bool = ...) -> None: ...

class ConversationUpdate(_message.Message):
    __slots__ = ("conversation_id", "user_id", "message_limit")
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_LIMIT_FIELD_NUMBER: _ClassVar[int]
    conversation_id: str
    user_id: str
    message_limit: int
    def __init__(self, conversation_id: _Optional[str] = ..., user_id: _Optional[str] = ..., message_limit: _Optional[int] = ...) -> None: ...

class ContextRequest(_message.Message):
    __slots__ = ("conversation_id", "user_id", "message_limit")
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_LIMIT_FIELD_NUMBER: _ClassVar[int]
    conversation_id: str
    user_id: str
    message_limit: int
    def __init__(self, conversation_id: _Optional[str] = ..., user_id: _Optional[str] = ..., message_limit: _Optional[int] = ...) -> None: ...

class ContextResponse(_message.Message):
    __slots__ = ("conversation_id", "messages", "user_profile", "state")
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    USER_PROFILE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    conversation_id: str
    messages: _containers.RepeatedCompositeFieldContainer[ContextMessage]
    user_profile: UserProfile
    state: ConversationState
    def __init__(self, conversation_id: _Optional[str] = ..., messages: _Optional[_Iterable[_Union[ContextMessage, _Mapping]]] = ..., user_profile: _Optional[_Union[UserProfile, _Mapping]] = ..., state: _Optional[_Union[ConversationState, str]] = ...) -> None: ...

class UpdateContextRequest(_message.Message):
    __slots__ = ("conversation_id", "new_message", "update_tone_profile")
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    NEW_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TONE_PROFILE_FIELD_NUMBER: _ClassVar[int]
    conversation_id: str
    new_message: ContextMessage
    update_tone_profile: bool
    def __init__(self, conversation_id: _Optional[str] = ..., new_message: _Optional[_Union[ContextMessage, _Mapping]] = ..., update_tone_profile: bool = ...) -> None: ...

class ContextMessage(_message.Message):
    __slots__ = ("message_id", "sender_id", "content", "type", "detected_tone", "timestamp", "metadata")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...) -> None: ...
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    SENDER_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    DETECTED_TONE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    message_id: str
    sender_id: str
    content: str
    type: MessageType
    detected_tone: ToneType
    timestamp: _timestamp_pb2.Timestamp
    metadata: _containers.MessageMap[str, _struct_pb2.Value]
    def __init__(self, message_id: _Optional[str] = ..., sender_id: _Optional[str] = ..., content: _Optional[str] = ..., type: _Optional[_Union[MessageType, str]] = ..., detected_tone: _Optional[_Union[ToneType, str]] = ..., timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., metadata: _Optional[_Mapping[str, _struct_pb2.Value]] = ...) -> None: ...

class UserProfile(_message.Message):
    __slots__ = ("user_id", "phone_number", "name", "relationship", "tone_preferences", "communication_style", "last_updated")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    PHONE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    RELATIONSHIP_FIELD_NUMBER: _ClassVar[int]
    TONE_PREFERENCES_FIELD_NUMBER: _ClassVar[int]
    COMMUNICATION_STYLE_FIELD_NUMBER: _ClassVar[int]
    LAST_UPDATED_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    phone_number: str
    name: str
    relationship: str
    tone_preferences: TonePreferences
    communication_style: CommunicationStyle
    last_updated: _timestamp_pb2.Timestamp
    def __init__(self, user_id: _Optional[str] = ..., phone_number: _Optional[str] = ..., name: _Optional[str] = ..., relationship: _Optional[str] = ..., tone_preferences: _Optional[_Union[TonePreferences, _Mapping]] = ..., communication_style: _Optional[_Union[CommunicationStyle, _Mapping]] = ..., last_updated: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class TonePreferences(_message.Message):
    __slots__ = ("primary_tone", "acceptable_tones", "tone_weights", "formality_level", "emoji_frequency")
    class ToneWeightsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: float
        def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
    PRIMARY_TONE_FIELD_NUMBER: _ClassVar[int]
    ACCEPTABLE_TONES_FIELD_NUMBER: _ClassVar[int]
    TONE_WEIGHTS_FIELD_NUMBER: _ClassVar[int]
    FORMALITY_LEVEL_FIELD_NUMBER: _ClassVar[int]
    EMOJI_FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    primary_tone: ToneType
    acceptable_tones: _containers.RepeatedScalarFieldContainer[ToneType]
    tone_weights: _containers.ScalarMap[str, float]
    formality_level: float
    emoji_frequency: float
    def __init__(self, primary_tone: _Optional[_Union[ToneType, str]] = ..., acceptable_tones: _Optional[_Iterable[_Union[ToneType, str]]] = ..., tone_weights: _Optional[_Mapping[str, float]] = ..., formality_level: _Optional[float] = ..., emoji_frequency: _Optional[float] = ...) -> None: ...

class CommunicationStyle(_message.Message):
    __slots__ = ("avg_message_length", "common_phrases", "vocabulary", "response_time_preference", "emoji_usage", "uses_abbreviations", "language_pattern")
    class EmojiUsageEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    AVG_MESSAGE_LENGTH_FIELD_NUMBER: _ClassVar[int]
    COMMON_PHRASES_FIELD_NUMBER: _ClassVar[int]
    VOCABULARY_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_TIME_PREFERENCE_FIELD_NUMBER: _ClassVar[int]
    EMOJI_USAGE_FIELD_NUMBER: _ClassVar[int]
    USES_ABBREVIATIONS_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_PATTERN_FIELD_NUMBER: _ClassVar[int]
    avg_message_length: float
    common_phrases: _containers.RepeatedScalarFieldContainer[str]
    vocabulary: _containers.RepeatedScalarFieldContainer[str]
    response_time_preference: float
    emoji_usage: _containers.ScalarMap[str, int]
    uses_abbreviations: bool
    language_pattern: LanguagePattern
    def __init__(self, avg_message_length: _Optional[float] = ..., common_phrases: _Optional[_Iterable[str]] = ..., vocabulary: _Optional[_Iterable[str]] = ..., response_time_preference: _Optional[float] = ..., emoji_usage: _Optional[_Mapping[str, int]] = ..., uses_abbreviations: bool = ..., language_pattern: _Optional[_Union[LanguagePattern, _Mapping]] = ...) -> None: ...

class LanguagePattern(_message.Message):
    __slots__ = ("primary_language", "formality_score", "enthusiasm_level", "characteristic_words", "topic_preferences")
    class TopicPreferencesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: float
        def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
    PRIMARY_LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    FORMALITY_SCORE_FIELD_NUMBER: _ClassVar[int]
    ENTHUSIASM_LEVEL_FIELD_NUMBER: _ClassVar[int]
    CHARACTERISTIC_WORDS_FIELD_NUMBER: _ClassVar[int]
    TOPIC_PREFERENCES_FIELD_NUMBER: _ClassVar[int]
    primary_language: str
    formality_score: float
    enthusiasm_level: float
    characteristic_words: _containers.RepeatedScalarFieldContainer[str]
    topic_preferences: _containers.ScalarMap[str, float]
    def __init__(self, primary_language: _Optional[str] = ..., formality_score: _Optional[float] = ..., enthusiasm_level: _Optional[float] = ..., characteristic_words: _Optional[_Iterable[str]] = ..., topic_preferences: _Optional[_Mapping[str, float]] = ...) -> None: ...

class ToolsRequest(_message.Message):
    __slots__ = ("context", "requested_tools")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    REQUESTED_TOOLS_FIELD_NUMBER: _ClassVar[int]
    context: str
    requested_tools: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, context: _Optional[str] = ..., requested_tools: _Optional[_Iterable[str]] = ...) -> None: ...

class ToolsResponse(_message.Message):
    __slots__ = ("available_tools",)
    AVAILABLE_TOOLS_FIELD_NUMBER: _ClassVar[int]
    available_tools: _containers.RepeatedCompositeFieldContainer[MCPTool]
    def __init__(self, available_tools: _Optional[_Iterable[_Union[MCPTool, _Mapping]]] = ...) -> None: ...

class MCPTool(_message.Message):
    __slots__ = ("name", "description", "parameters_schema", "required_permissions", "is_available")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    IS_AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    parameters_schema: _struct_pb2.Struct
    required_permissions: _containers.RepeatedScalarFieldContainer[str]
    is_available: bool
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., parameters_schema: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., required_permissions: _Optional[_Iterable[str]] = ..., is_available: bool = ...) -> None: ...

class ToolExecutionRequest(_message.Message):
    __slots__ = ("tool_name", "parameters", "context_id", "user_id")
    TOOL_NAME_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    tool_name: str
    parameters: _struct_pb2.Struct
    context_id: str
    user_id: str
    def __init__(self, tool_name: _Optional[str] = ..., parameters: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., context_id: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...

class ToolExecutionResponse(_message.Message):
    __slots__ = ("success", "result", "error_message", "execution_time_ms")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    EXECUTION_TIME_MS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    result: _any_pb2.Any
    error_message: str
    execution_time_ms: int
    def __init__(self, success: bool = ..., result: _Optional[_Union[_any_pb2.Any, _Mapping]] = ..., error_message: _Optional[str] = ..., execution_time_ms: _Optional[int] = ...) -> None: ...

class HealthRequest(_message.Message):
    __slots__ = ("service_name",)
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    def __init__(self, service_name: _Optional[str] = ...) -> None: ...

class HealthResponse(_message.Message):
    __slots__ = ("status", "message", "details", "timestamp")
    class DetailsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    status: HealthStatus
    message: str
    details: _containers.ScalarMap[str, str]
    timestamp: _timestamp_pb2.Timestamp
    def __init__(self, status: _Optional[_Union[HealthStatus, str]] = ..., message: _Optional[str] = ..., details: _Optional[_Mapping[str, str]] = ..., timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
