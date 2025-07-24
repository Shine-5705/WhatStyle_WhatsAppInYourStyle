from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ToneCategory(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TONE_CATEGORY_UNSPECIFIED: _ClassVar[ToneCategory]
    TONE_CATEGORY_CASUAL: _ClassVar[ToneCategory]
    TONE_CATEGORY_FORMAL: _ClassVar[ToneCategory]
    TONE_CATEGORY_PLAYFUL: _ClassVar[ToneCategory]
    TONE_CATEGORY_CARING: _ClassVar[ToneCategory]
    TONE_CATEGORY_BUSINESS: _ClassVar[ToneCategory]
    TONE_CATEGORY_ROMANTIC: _ClassVar[ToneCategory]
    TONE_CATEGORY_FRIENDLY: _ClassVar[ToneCategory]
    TONE_CATEGORY_PROFESSIONAL: _ClassVar[ToneCategory]
    TONE_CATEGORY_EXCITED: _ClassVar[ToneCategory]
    TONE_CATEGORY_CONCERNED: _ClassVar[ToneCategory]
    TONE_CATEGORY_ANGRY: _ClassVar[ToneCategory]
    TONE_CATEGORY_HAPPY: _ClassVar[ToneCategory]
    TONE_CATEGORY_SAD: _ClassVar[ToneCategory]
    TONE_CATEGORY_NEUTRAL: _ClassVar[ToneCategory]
TONE_CATEGORY_UNSPECIFIED: ToneCategory
TONE_CATEGORY_CASUAL: ToneCategory
TONE_CATEGORY_FORMAL: ToneCategory
TONE_CATEGORY_PLAYFUL: ToneCategory
TONE_CATEGORY_CARING: ToneCategory
TONE_CATEGORY_BUSINESS: ToneCategory
TONE_CATEGORY_ROMANTIC: ToneCategory
TONE_CATEGORY_FRIENDLY: ToneCategory
TONE_CATEGORY_PROFESSIONAL: ToneCategory
TONE_CATEGORY_EXCITED: ToneCategory
TONE_CATEGORY_CONCERNED: ToneCategory
TONE_CATEGORY_ANGRY: ToneCategory
TONE_CATEGORY_HAPPY: ToneCategory
TONE_CATEGORY_SAD: ToneCategory
TONE_CATEGORY_NEUTRAL: ToneCategory

class ToneAnalysisRequest(_message.Message):
    __slots__ = ("message_id", "text", "user_id", "context", "previous_messages")
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    message_id: str
    text: str
    user_id: str
    context: str
    previous_messages: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, message_id: _Optional[str] = ..., text: _Optional[str] = ..., user_id: _Optional[str] = ..., context: _Optional[str] = ..., previous_messages: _Optional[_Iterable[str]] = ...) -> None: ...

class ToneAnalysisResponse(_message.Message):
    __slots__ = ("message_id", "primary_tone", "alternative_tones", "confidence_score", "emotional_profile", "tone_features", "analyzed_at")
    class ToneFeaturesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: float
        def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    PRIMARY_TONE_FIELD_NUMBER: _ClassVar[int]
    ALTERNATIVE_TONES_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_SCORE_FIELD_NUMBER: _ClassVar[int]
    EMOTIONAL_PROFILE_FIELD_NUMBER: _ClassVar[int]
    TONE_FEATURES_FIELD_NUMBER: _ClassVar[int]
    ANALYZED_AT_FIELD_NUMBER: _ClassVar[int]
    message_id: str
    primary_tone: ToneClassification
    alternative_tones: _containers.RepeatedCompositeFieldContainer[ToneClassification]
    confidence_score: float
    emotional_profile: EmotionalProfile
    tone_features: _containers.ScalarMap[str, float]
    analyzed_at: _timestamp_pb2.Timestamp
    def __init__(self, message_id: _Optional[str] = ..., primary_tone: _Optional[_Union[ToneClassification, _Mapping]] = ..., alternative_tones: _Optional[_Iterable[_Union[ToneClassification, _Mapping]]] = ..., confidence_score: _Optional[float] = ..., emotional_profile: _Optional[_Union[EmotionalProfile, _Mapping]] = ..., tone_features: _Optional[_Mapping[str, float]] = ..., analyzed_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ToneClassification(_message.Message):
    __slots__ = ("category", "confidence", "description", "key_indicators")
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    KEY_INDICATORS_FIELD_NUMBER: _ClassVar[int]
    category: ToneCategory
    confidence: float
    description: str
    key_indicators: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, category: _Optional[_Union[ToneCategory, str]] = ..., confidence: _Optional[float] = ..., description: _Optional[str] = ..., key_indicators: _Optional[_Iterable[str]] = ...) -> None: ...

class EmotionalProfile(_message.Message):
    __slots__ = ("sentiment_score", "energy_level", "formality_level", "urgency_level", "dimensions")
    SENTIMENT_SCORE_FIELD_NUMBER: _ClassVar[int]
    ENERGY_LEVEL_FIELD_NUMBER: _ClassVar[int]
    FORMALITY_LEVEL_FIELD_NUMBER: _ClassVar[int]
    URGENCY_LEVEL_FIELD_NUMBER: _ClassVar[int]
    DIMENSIONS_FIELD_NUMBER: _ClassVar[int]
    sentiment_score: float
    energy_level: float
    formality_level: float
    urgency_level: float
    dimensions: _containers.RepeatedCompositeFieldContainer[EmotionalDimension]
    def __init__(self, sentiment_score: _Optional[float] = ..., energy_level: _Optional[float] = ..., formality_level: _Optional[float] = ..., urgency_level: _Optional[float] = ..., dimensions: _Optional[_Iterable[_Union[EmotionalDimension, _Mapping]]] = ...) -> None: ...

class EmotionalDimension(_message.Message):
    __slots__ = ("name", "value", "confidence")
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    name: str
    value: float
    confidence: float
    def __init__(self, name: _Optional[str] = ..., value: _Optional[float] = ..., confidence: _Optional[float] = ...) -> None: ...

class BatchToneAnalysisRequest(_message.Message):
    __slots__ = ("requests", "parallel_processing")
    REQUESTS_FIELD_NUMBER: _ClassVar[int]
    PARALLEL_PROCESSING_FIELD_NUMBER: _ClassVar[int]
    requests: _containers.RepeatedCompositeFieldContainer[ToneAnalysisRequest]
    parallel_processing: bool
    def __init__(self, requests: _Optional[_Iterable[_Union[ToneAnalysisRequest, _Mapping]]] = ..., parallel_processing: bool = ...) -> None: ...

class BatchToneAnalysisResponse(_message.Message):
    __slots__ = ("responses", "processed_count", "failed_count", "total_processing_time_ms")
    RESPONSES_FIELD_NUMBER: _ClassVar[int]
    PROCESSED_COUNT_FIELD_NUMBER: _ClassVar[int]
    FAILED_COUNT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_PROCESSING_TIME_MS_FIELD_NUMBER: _ClassVar[int]
    responses: _containers.RepeatedCompositeFieldContainer[ToneAnalysisResponse]
    processed_count: int
    failed_count: int
    total_processing_time_ms: int
    def __init__(self, responses: _Optional[_Iterable[_Union[ToneAnalysisResponse, _Mapping]]] = ..., processed_count: _Optional[int] = ..., failed_count: _Optional[int] = ..., total_processing_time_ms: _Optional[int] = ...) -> None: ...

class ToneProfileRequest(_message.Message):
    __slots__ = ("user_id", "include_history")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_HISTORY_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    include_history: bool
    def __init__(self, user_id: _Optional[str] = ..., include_history: bool = ...) -> None: ...

class ToneProfileResponse(_message.Message):
    __slots__ = ("user_id", "profile", "history")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    PROFILE_FIELD_NUMBER: _ClassVar[int]
    HISTORY_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    profile: UserToneProfile
    history: _containers.RepeatedCompositeFieldContainer[ToneHistoryEntry]
    def __init__(self, user_id: _Optional[str] = ..., profile: _Optional[_Union[UserToneProfile, _Mapping]] = ..., history: _Optional[_Iterable[_Union[ToneHistoryEntry, _Mapping]]] = ...) -> None: ...

class UpdateToneProfileRequest(_message.Message):
    __slots__ = ("user_id", "profile", "merge_with_existing")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    PROFILE_FIELD_NUMBER: _ClassVar[int]
    MERGE_WITH_EXISTING_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    profile: UserToneProfile
    merge_with_existing: bool
    def __init__(self, user_id: _Optional[str] = ..., profile: _Optional[_Union[UserToneProfile, _Mapping]] = ..., merge_with_existing: bool = ...) -> None: ...

class UserToneProfile(_message.Message):
    __slots__ = ("user_id", "tone_preferences", "tone_patterns", "characteristics", "last_analyzed", "message_count")
    class TonePreferencesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: float
        def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
    class TonePatternsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: float
        def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    TONE_PREFERENCES_FIELD_NUMBER: _ClassVar[int]
    TONE_PATTERNS_FIELD_NUMBER: _ClassVar[int]
    CHARACTERISTICS_FIELD_NUMBER: _ClassVar[int]
    LAST_ANALYZED_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_COUNT_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    tone_preferences: _containers.ScalarMap[str, float]
    tone_patterns: _containers.ScalarMap[str, float]
    characteristics: CommunicationCharacteristics
    last_analyzed: _timestamp_pb2.Timestamp
    message_count: int
    def __init__(self, user_id: _Optional[str] = ..., tone_preferences: _Optional[_Mapping[str, float]] = ..., tone_patterns: _Optional[_Mapping[str, float]] = ..., characteristics: _Optional[_Union[CommunicationCharacteristics, _Mapping]] = ..., last_analyzed: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., message_count: _Optional[int] = ...) -> None: ...

class CommunicationCharacteristics(_message.Message):
    __slots__ = ("avg_message_length", "emoji_frequency", "capitalization_frequency", "punctuation_intensity", "common_phrases", "word_frequency", "time_preferences")
    class WordFrequencyEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    AVG_MESSAGE_LENGTH_FIELD_NUMBER: _ClassVar[int]
    EMOJI_FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    CAPITALIZATION_FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    PUNCTUATION_INTENSITY_FIELD_NUMBER: _ClassVar[int]
    COMMON_PHRASES_FIELD_NUMBER: _ClassVar[int]
    WORD_FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    TIME_PREFERENCES_FIELD_NUMBER: _ClassVar[int]
    avg_message_length: float
    emoji_frequency: float
    capitalization_frequency: float
    punctuation_intensity: float
    common_phrases: _containers.RepeatedScalarFieldContainer[str]
    word_frequency: _containers.ScalarMap[str, int]
    time_preferences: TimePreferences
    def __init__(self, avg_message_length: _Optional[float] = ..., emoji_frequency: _Optional[float] = ..., capitalization_frequency: _Optional[float] = ..., punctuation_intensity: _Optional[float] = ..., common_phrases: _Optional[_Iterable[str]] = ..., word_frequency: _Optional[_Mapping[str, int]] = ..., time_preferences: _Optional[_Union[TimePreferences, _Mapping]] = ...) -> None: ...

class TimePreferences(_message.Message):
    __slots__ = ("active_hours", "avg_response_time_minutes", "prefers_quick_responses")
    ACTIVE_HOURS_FIELD_NUMBER: _ClassVar[int]
    AVG_RESPONSE_TIME_MINUTES_FIELD_NUMBER: _ClassVar[int]
    PREFERS_QUICK_RESPONSES_FIELD_NUMBER: _ClassVar[int]
    active_hours: _containers.RepeatedScalarFieldContainer[int]
    avg_response_time_minutes: float
    prefers_quick_responses: bool
    def __init__(self, active_hours: _Optional[_Iterable[int]] = ..., avg_response_time_minutes: _Optional[float] = ..., prefers_quick_responses: bool = ...) -> None: ...

class ToneHistoryEntry(_message.Message):
    __slots__ = ("timestamp", "detected_tone", "confidence", "message_sample")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    DETECTED_TONE_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_SAMPLE_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    detected_tone: ToneCategory
    confidence: float
    message_sample: str
    def __init__(self, timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., detected_tone: _Optional[_Union[ToneCategory, str]] = ..., confidence: _Optional[float] = ..., message_sample: _Optional[str] = ...) -> None: ...

class TrainModelRequest(_message.Message):
    __slots__ = ("user_id", "examples", "config")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    EXAMPLES_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    examples: _containers.RepeatedCompositeFieldContainer[TrainingExample]
    config: TrainingConfig
    def __init__(self, user_id: _Optional[str] = ..., examples: _Optional[_Iterable[_Union[TrainingExample, _Mapping]]] = ..., config: _Optional[_Union[TrainingConfig, _Mapping]] = ...) -> None: ...

class TrainingExample(_message.Message):
    __slots__ = ("text", "expected_tone", "weight", "metadata")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    TEXT_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_TONE_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    text: str
    expected_tone: ToneCategory
    weight: float
    metadata: _containers.ScalarMap[str, str]
    def __init__(self, text: _Optional[str] = ..., expected_tone: _Optional[_Union[ToneCategory, str]] = ..., weight: _Optional[float] = ..., metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class TrainingConfig(_message.Message):
    __slots__ = ("epochs", "learning_rate", "batch_size", "use_pretrained", "features_to_use")
    EPOCHS_FIELD_NUMBER: _ClassVar[int]
    LEARNING_RATE_FIELD_NUMBER: _ClassVar[int]
    BATCH_SIZE_FIELD_NUMBER: _ClassVar[int]
    USE_PRETRAINED_FIELD_NUMBER: _ClassVar[int]
    FEATURES_TO_USE_FIELD_NUMBER: _ClassVar[int]
    epochs: int
    learning_rate: float
    batch_size: int
    use_pretrained: bool
    features_to_use: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, epochs: _Optional[int] = ..., learning_rate: _Optional[float] = ..., batch_size: _Optional[int] = ..., use_pretrained: bool = ..., features_to_use: _Optional[_Iterable[str]] = ...) -> None: ...

class TrainModelResponse(_message.Message):
    __slots__ = ("success", "model_id", "results", "error_message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    model_id: str
    results: TrainingResults
    error_message: str
    def __init__(self, success: bool = ..., model_id: _Optional[str] = ..., results: _Optional[_Union[TrainingResults, _Mapping]] = ..., error_message: _Optional[str] = ...) -> None: ...

class TrainingResults(_message.Message):
    __slots__ = ("accuracy", "precision", "recall", "f1_score", "training_samples", "training_time_ms", "class_metrics")
    class ClassMetricsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: float
        def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
    ACCURACY_FIELD_NUMBER: _ClassVar[int]
    PRECISION_FIELD_NUMBER: _ClassVar[int]
    RECALL_FIELD_NUMBER: _ClassVar[int]
    F1_SCORE_FIELD_NUMBER: _ClassVar[int]
    TRAINING_SAMPLES_FIELD_NUMBER: _ClassVar[int]
    TRAINING_TIME_MS_FIELD_NUMBER: _ClassVar[int]
    CLASS_METRICS_FIELD_NUMBER: _ClassVar[int]
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    training_samples: int
    training_time_ms: int
    class_metrics: _containers.ScalarMap[str, float]
    def __init__(self, accuracy: _Optional[float] = ..., precision: _Optional[float] = ..., recall: _Optional[float] = ..., f1_score: _Optional[float] = ..., training_samples: _Optional[int] = ..., training_time_ms: _Optional[int] = ..., class_metrics: _Optional[_Mapping[str, float]] = ...) -> None: ...
