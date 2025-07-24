from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import any_pb2 as _any_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AnalyticsMetric(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ANALYTICS_METRIC_UNSPECIFIED: _ClassVar[AnalyticsMetric]
    ANALYTICS_METRIC_MESSAGE_COUNT: _ClassVar[AnalyticsMetric]
    ANALYTICS_METRIC_RESPONSE_TIME: _ClassVar[AnalyticsMetric]
    ANALYTICS_METRIC_TONE_DISTRIBUTION: _ClassVar[AnalyticsMetric]
    ANALYTICS_METRIC_SENTIMENT_ANALYSIS: _ClassVar[AnalyticsMetric]
    ANALYTICS_METRIC_USER_SATISFACTION: _ClassVar[AnalyticsMetric]
    ANALYTICS_METRIC_ENGAGEMENT_RATE: _ClassVar[AnalyticsMetric]
    ANALYTICS_METRIC_CONVERSATION_FLOW: _ClassVar[AnalyticsMetric]

class AnalyticsType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ANALYTICS_TYPE_UNSPECIFIED: _ClassVar[AnalyticsType]
    ANALYTICS_TYPE_CONVERSATION: _ClassVar[AnalyticsType]
    ANALYTICS_TYPE_USER_BEHAVIOR: _ClassVar[AnalyticsType]
    ANALYTICS_TYPE_SYSTEM_PERFORMANCE: _ClassVar[AnalyticsType]
    ANALYTICS_TYPE_TONE_ANALYSIS: _ClassVar[AnalyticsType]
    ANALYTICS_TYPE_REAL_TIME: _ClassVar[AnalyticsType]

class ReportType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    REPORT_TYPE_UNSPECIFIED: _ClassVar[ReportType]
    REPORT_TYPE_CONVERSATION_SUMMARY: _ClassVar[ReportType]
    REPORT_TYPE_USER_BEHAVIOR: _ClassVar[ReportType]
    REPORT_TYPE_TONE_ANALYSIS: _ClassVar[ReportType]
    REPORT_TYPE_SYSTEM_PERFORMANCE: _ClassVar[ReportType]
    REPORT_TYPE_EXECUTIVE_SUMMARY: _ClassVar[ReportType]
    REPORT_TYPE_CUSTOM: _ClassVar[ReportType]

class ReportFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    REPORT_FORMAT_UNSPECIFIED: _ClassVar[ReportFormat]
    REPORT_FORMAT_PDF: _ClassVar[ReportFormat]
    REPORT_FORMAT_JSON: _ClassVar[ReportFormat]
    REPORT_FORMAT_CSV: _ClassVar[ReportFormat]
    REPORT_FORMAT_EXCEL: _ClassVar[ReportFormat]
    REPORT_FORMAT_HTML: _ClassVar[ReportFormat]
ANALYTICS_METRIC_UNSPECIFIED: AnalyticsMetric
ANALYTICS_METRIC_MESSAGE_COUNT: AnalyticsMetric
ANALYTICS_METRIC_RESPONSE_TIME: AnalyticsMetric
ANALYTICS_METRIC_TONE_DISTRIBUTION: AnalyticsMetric
ANALYTICS_METRIC_SENTIMENT_ANALYSIS: AnalyticsMetric
ANALYTICS_METRIC_USER_SATISFACTION: AnalyticsMetric
ANALYTICS_METRIC_ENGAGEMENT_RATE: AnalyticsMetric
ANALYTICS_METRIC_CONVERSATION_FLOW: AnalyticsMetric
ANALYTICS_TYPE_UNSPECIFIED: AnalyticsType
ANALYTICS_TYPE_CONVERSATION: AnalyticsType
ANALYTICS_TYPE_USER_BEHAVIOR: AnalyticsType
ANALYTICS_TYPE_SYSTEM_PERFORMANCE: AnalyticsType
ANALYTICS_TYPE_TONE_ANALYSIS: AnalyticsType
ANALYTICS_TYPE_REAL_TIME: AnalyticsType
REPORT_TYPE_UNSPECIFIED: ReportType
REPORT_TYPE_CONVERSATION_SUMMARY: ReportType
REPORT_TYPE_USER_BEHAVIOR: ReportType
REPORT_TYPE_TONE_ANALYSIS: ReportType
REPORT_TYPE_SYSTEM_PERFORMANCE: ReportType
REPORT_TYPE_EXECUTIVE_SUMMARY: ReportType
REPORT_TYPE_CUSTOM: ReportType
REPORT_FORMAT_UNSPECIFIED: ReportFormat
REPORT_FORMAT_PDF: ReportFormat
REPORT_FORMAT_JSON: ReportFormat
REPORT_FORMAT_CSV: ReportFormat
REPORT_FORMAT_EXCEL: ReportFormat
REPORT_FORMAT_HTML: ReportFormat

class ConversationAnalyticsRequest(_message.Message):
    __slots__ = ("conversation_ids", "start_time", "end_time", "metrics")
    CONVERSATION_IDS_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    conversation_ids: _containers.RepeatedScalarFieldContainer[str]
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    metrics: _containers.RepeatedScalarFieldContainer[AnalyticsMetric]
    def __init__(self, conversation_ids: _Optional[_Iterable[str]] = ..., start_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., metrics: _Optional[_Iterable[_Union[AnalyticsMetric, str]]] = ...) -> None: ...

class ConversationAnalyticsResponse(_message.Message):
    __slots__ = ("metrics", "summary", "generated_at")
    METRICS_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    GENERATED_AT_FIELD_NUMBER: _ClassVar[int]
    metrics: _containers.RepeatedCompositeFieldContainer[ConversationMetrics]
    summary: AnalyticsSummary
    generated_at: _timestamp_pb2.Timestamp
    def __init__(self, metrics: _Optional[_Iterable[_Union[ConversationMetrics, _Mapping]]] = ..., summary: _Optional[_Union[AnalyticsSummary, _Mapping]] = ..., generated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ConversationMetrics(_message.Message):
    __slots__ = ("conversation_id", "total_messages", "avg_response_time", "tone_distribution", "sentiment_trend", "user_satisfaction_score", "flow_analysis")
    class ToneDistributionEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    TOTAL_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    AVG_RESPONSE_TIME_FIELD_NUMBER: _ClassVar[int]
    TONE_DISTRIBUTION_FIELD_NUMBER: _ClassVar[int]
    SENTIMENT_TREND_FIELD_NUMBER: _ClassVar[int]
    USER_SATISFACTION_SCORE_FIELD_NUMBER: _ClassVar[int]
    FLOW_ANALYSIS_FIELD_NUMBER: _ClassVar[int]
    conversation_id: str
    total_messages: int
    avg_response_time: _duration_pb2.Duration
    tone_distribution: _containers.ScalarMap[str, int]
    sentiment_trend: float
    user_satisfaction_score: int
    flow_analysis: ConversationFlow
    def __init__(self, conversation_id: _Optional[str] = ..., total_messages: _Optional[int] = ..., avg_response_time: _Optional[_Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]] = ..., tone_distribution: _Optional[_Mapping[str, int]] = ..., sentiment_trend: _Optional[float] = ..., user_satisfaction_score: _Optional[int] = ..., flow_analysis: _Optional[_Union[ConversationFlow, _Mapping]] = ...) -> None: ...

class ConversationFlow(_message.Message):
    __slots__ = ("stages", "transitions", "engagement_score")
    STAGES_FIELD_NUMBER: _ClassVar[int]
    TRANSITIONS_FIELD_NUMBER: _ClassVar[int]
    ENGAGEMENT_SCORE_FIELD_NUMBER: _ClassVar[int]
    stages: _containers.RepeatedCompositeFieldContainer[FlowStage]
    transitions: _containers.RepeatedCompositeFieldContainer[FlowTransition]
    engagement_score: float
    def __init__(self, stages: _Optional[_Iterable[_Union[FlowStage, _Mapping]]] = ..., transitions: _Optional[_Iterable[_Union[FlowTransition, _Mapping]]] = ..., engagement_score: _Optional[float] = ...) -> None: ...

class FlowStage(_message.Message):
    __slots__ = ("stage_name", "duration", "message_count", "dominant_tone")
    STAGE_NAME_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_COUNT_FIELD_NUMBER: _ClassVar[int]
    DOMINANT_TONE_FIELD_NUMBER: _ClassVar[int]
    stage_name: str
    duration: _duration_pb2.Duration
    message_count: int
    dominant_tone: str
    def __init__(self, stage_name: _Optional[str] = ..., duration: _Optional[_Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]] = ..., message_count: _Optional[int] = ..., dominant_tone: _Optional[str] = ...) -> None: ...

class FlowTransition(_message.Message):
    __slots__ = ("from_stage", "to_stage", "trigger", "probability")
    FROM_STAGE_FIELD_NUMBER: _ClassVar[int]
    TO_STAGE_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_FIELD_NUMBER: _ClassVar[int]
    PROBABILITY_FIELD_NUMBER: _ClassVar[int]
    from_stage: str
    to_stage: str
    trigger: str
    probability: float
    def __init__(self, from_stage: _Optional[str] = ..., to_stage: _Optional[str] = ..., trigger: _Optional[str] = ..., probability: _Optional[float] = ...) -> None: ...

class UserAnalyticsRequest(_message.Message):
    __slots__ = ("user_ids", "start_time", "end_time", "include_behavioral_patterns")
    USER_IDS_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_BEHAVIORAL_PATTERNS_FIELD_NUMBER: _ClassVar[int]
    user_ids: _containers.RepeatedScalarFieldContainer[str]
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    include_behavioral_patterns: bool
    def __init__(self, user_ids: _Optional[_Iterable[str]] = ..., start_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., include_behavioral_patterns: bool = ...) -> None: ...

class UserAnalyticsResponse(_message.Message):
    __slots__ = ("user_metrics", "behavior_analysis")
    USER_METRICS_FIELD_NUMBER: _ClassVar[int]
    BEHAVIOR_ANALYSIS_FIELD_NUMBER: _ClassVar[int]
    user_metrics: _containers.RepeatedCompositeFieldContainer[UserMetrics]
    behavior_analysis: UserBehaviorAnalysis
    def __init__(self, user_metrics: _Optional[_Iterable[_Union[UserMetrics, _Mapping]]] = ..., behavior_analysis: _Optional[_Union[UserBehaviorAnalysis, _Mapping]] = ...) -> None: ...

class UserMetrics(_message.Message):
    __slots__ = ("user_id", "total_conversations", "total_messages", "avg_session_length", "tone_preferences", "patterns", "engagement")
    class TonePreferencesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: float
        def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    TOTAL_CONVERSATIONS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    AVG_SESSION_LENGTH_FIELD_NUMBER: _ClassVar[int]
    TONE_PREFERENCES_FIELD_NUMBER: _ClassVar[int]
    PATTERNS_FIELD_NUMBER: _ClassVar[int]
    ENGAGEMENT_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    total_conversations: int
    total_messages: int
    avg_session_length: _duration_pb2.Duration
    tone_preferences: _containers.ScalarMap[str, float]
    patterns: CommunicationPatterns
    engagement: EngagementMetrics
    def __init__(self, user_id: _Optional[str] = ..., total_conversations: _Optional[int] = ..., total_messages: _Optional[int] = ..., avg_session_length: _Optional[_Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]] = ..., tone_preferences: _Optional[_Mapping[str, float]] = ..., patterns: _Optional[_Union[CommunicationPatterns, _Mapping]] = ..., engagement: _Optional[_Union[EngagementMetrics, _Mapping]] = ...) -> None: ...

class CommunicationPatterns(_message.Message):
    __slots__ = ("active_hours", "preferred_topics", "avg_message_length", "emoji_usage_rate", "vocabulary_analysis")
    class VocabularyAnalysisEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    ACTIVE_HOURS_FIELD_NUMBER: _ClassVar[int]
    PREFERRED_TOPICS_FIELD_NUMBER: _ClassVar[int]
    AVG_MESSAGE_LENGTH_FIELD_NUMBER: _ClassVar[int]
    EMOJI_USAGE_RATE_FIELD_NUMBER: _ClassVar[int]
    VOCABULARY_ANALYSIS_FIELD_NUMBER: _ClassVar[int]
    active_hours: _containers.RepeatedScalarFieldContainer[int]
    preferred_topics: _containers.RepeatedScalarFieldContainer[str]
    avg_message_length: float
    emoji_usage_rate: float
    vocabulary_analysis: _containers.ScalarMap[str, int]
    def __init__(self, active_hours: _Optional[_Iterable[int]] = ..., preferred_topics: _Optional[_Iterable[str]] = ..., avg_message_length: _Optional[float] = ..., emoji_usage_rate: _Optional[float] = ..., vocabulary_analysis: _Optional[_Mapping[str, int]] = ...) -> None: ...

class EngagementMetrics(_message.Message):
    __slots__ = ("response_rate", "avg_response_time", "conversation_initiation_count", "satisfaction_score")
    RESPONSE_RATE_FIELD_NUMBER: _ClassVar[int]
    AVG_RESPONSE_TIME_FIELD_NUMBER: _ClassVar[int]
    CONVERSATION_INITIATION_COUNT_FIELD_NUMBER: _ClassVar[int]
    SATISFACTION_SCORE_FIELD_NUMBER: _ClassVar[int]
    response_rate: float
    avg_response_time: _duration_pb2.Duration
    conversation_initiation_count: int
    satisfaction_score: float
    def __init__(self, response_rate: _Optional[float] = ..., avg_response_time: _Optional[_Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]] = ..., conversation_initiation_count: _Optional[int] = ..., satisfaction_score: _Optional[float] = ...) -> None: ...

class UserBehaviorAnalysis(_message.Message):
    __slots__ = ("patterns", "anomalies", "personality")
    PATTERNS_FIELD_NUMBER: _ClassVar[int]
    ANOMALIES_FIELD_NUMBER: _ClassVar[int]
    PERSONALITY_FIELD_NUMBER: _ClassVar[int]
    patterns: _containers.RepeatedCompositeFieldContainer[BehaviorPattern]
    anomalies: _containers.RepeatedCompositeFieldContainer[BehaviorAnomaly]
    personality: PersonalityInsights
    def __init__(self, patterns: _Optional[_Iterable[_Union[BehaviorPattern, _Mapping]]] = ..., anomalies: _Optional[_Iterable[_Union[BehaviorAnomaly, _Mapping]]] = ..., personality: _Optional[_Union[PersonalityInsights, _Mapping]] = ...) -> None: ...

class BehaviorPattern(_message.Message):
    __slots__ = ("pattern_name", "description", "confidence", "supporting_evidence")
    PATTERN_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    SUPPORTING_EVIDENCE_FIELD_NUMBER: _ClassVar[int]
    pattern_name: str
    description: str
    confidence: float
    supporting_evidence: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, pattern_name: _Optional[str] = ..., description: _Optional[str] = ..., confidence: _Optional[float] = ..., supporting_evidence: _Optional[_Iterable[str]] = ...) -> None: ...

class BehaviorAnomaly(_message.Message):
    __slots__ = ("anomaly_type", "detected_at", "severity", "description")
    ANOMALY_TYPE_FIELD_NUMBER: _ClassVar[int]
    DETECTED_AT_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    anomaly_type: str
    detected_at: _timestamp_pb2.Timestamp
    severity: float
    description: str
    def __init__(self, anomaly_type: _Optional[str] = ..., detected_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., severity: _Optional[float] = ..., description: _Optional[str] = ...) -> None: ...

class PersonalityInsights(_message.Message):
    __slots__ = ("traits", "communication_preferences", "extroversion_score", "emotional_stability")
    class TraitsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: float
        def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
    TRAITS_FIELD_NUMBER: _ClassVar[int]
    COMMUNICATION_PREFERENCES_FIELD_NUMBER: _ClassVar[int]
    EXTROVERSION_SCORE_FIELD_NUMBER: _ClassVar[int]
    EMOTIONAL_STABILITY_FIELD_NUMBER: _ClassVar[int]
    traits: _containers.ScalarMap[str, float]
    communication_preferences: _containers.RepeatedScalarFieldContainer[str]
    extroversion_score: float
    emotional_stability: float
    def __init__(self, traits: _Optional[_Mapping[str, float]] = ..., communication_preferences: _Optional[_Iterable[str]] = ..., extroversion_score: _Optional[float] = ..., emotional_stability: _Optional[float] = ...) -> None: ...

class SystemMetricsRequest(_message.Message):
    __slots__ = ("start_time", "end_time", "metric_types")
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    METRIC_TYPES_FIELD_NUMBER: _ClassVar[int]
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    metric_types: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, start_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., metric_types: _Optional[_Iterable[str]] = ...) -> None: ...

class SystemMetricsResponse(_message.Message):
    __slots__ = ("performance", "resources", "errors", "throughput")
    PERFORMANCE_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    THROUGHPUT_FIELD_NUMBER: _ClassVar[int]
    performance: PerformanceMetrics
    resources: ResourceUtilization
    errors: ErrorAnalysis
    throughput: ThroughputMetrics
    def __init__(self, performance: _Optional[_Union[PerformanceMetrics, _Mapping]] = ..., resources: _Optional[_Union[ResourceUtilization, _Mapping]] = ..., errors: _Optional[_Union[ErrorAnalysis, _Mapping]] = ..., throughput: _Optional[_Union[ThroughputMetrics, _Mapping]] = ...) -> None: ...

class PerformanceMetrics(_message.Message):
    __slots__ = ("avg_response_time", "p95_response_time", "p99_response_time", "success_rate", "total_requests")
    AVG_RESPONSE_TIME_FIELD_NUMBER: _ClassVar[int]
    P95_RESPONSE_TIME_FIELD_NUMBER: _ClassVar[int]
    P99_RESPONSE_TIME_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_RATE_FIELD_NUMBER: _ClassVar[int]
    TOTAL_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    avg_response_time: _duration_pb2.Duration
    p95_response_time: _duration_pb2.Duration
    p99_response_time: _duration_pb2.Duration
    success_rate: float
    total_requests: int
    def __init__(self, avg_response_time: _Optional[_Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]] = ..., p95_response_time: _Optional[_Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]] = ..., p99_response_time: _Optional[_Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]] = ..., success_rate: _Optional[float] = ..., total_requests: _Optional[int] = ...) -> None: ...

class ResourceUtilization(_message.Message):
    __slots__ = ("cpu_usage_percent", "memory_usage_percent", "disk_usage_percent", "active_connections", "custom_metrics")
    class CustomMetricsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: float
        def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
    CPU_USAGE_PERCENT_FIELD_NUMBER: _ClassVar[int]
    MEMORY_USAGE_PERCENT_FIELD_NUMBER: _ClassVar[int]
    DISK_USAGE_PERCENT_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_CONNECTIONS_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_METRICS_FIELD_NUMBER: _ClassVar[int]
    cpu_usage_percent: float
    memory_usage_percent: float
    disk_usage_percent: float
    active_connections: int
    custom_metrics: _containers.ScalarMap[str, float]
    def __init__(self, cpu_usage_percent: _Optional[float] = ..., memory_usage_percent: _Optional[float] = ..., disk_usage_percent: _Optional[float] = ..., active_connections: _Optional[int] = ..., custom_metrics: _Optional[_Mapping[str, float]] = ...) -> None: ...

class ErrorAnalysis(_message.Message):
    __slots__ = ("total_errors", "error_types", "trends")
    class ErrorTypesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    TOTAL_ERRORS_FIELD_NUMBER: _ClassVar[int]
    ERROR_TYPES_FIELD_NUMBER: _ClassVar[int]
    TRENDS_FIELD_NUMBER: _ClassVar[int]
    total_errors: int
    error_types: _containers.ScalarMap[str, int]
    trends: _containers.RepeatedCompositeFieldContainer[ErrorTrend]
    def __init__(self, total_errors: _Optional[int] = ..., error_types: _Optional[_Mapping[str, int]] = ..., trends: _Optional[_Iterable[_Union[ErrorTrend, _Mapping]]] = ...) -> None: ...

class ErrorTrend(_message.Message):
    __slots__ = ("error_type", "points")
    ERROR_TYPE_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    error_type: str
    points: _containers.RepeatedCompositeFieldContainer[TimeSeriesPoint]
    def __init__(self, error_type: _Optional[str] = ..., points: _Optional[_Iterable[_Union[TimeSeriesPoint, _Mapping]]] = ...) -> None: ...

class TimeSeriesPoint(_message.Message):
    __slots__ = ("timestamp", "value")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    value: float
    def __init__(self, timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., value: _Optional[float] = ...) -> None: ...

class ThroughputMetrics(_message.Message):
    __slots__ = ("messages_per_second", "conversations_per_minute", "ai_requests_per_minute", "service_throughput")
    class ServiceThroughputEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: float
        def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
    MESSAGES_PER_SECOND_FIELD_NUMBER: _ClassVar[int]
    CONVERSATIONS_PER_MINUTE_FIELD_NUMBER: _ClassVar[int]
    AI_REQUESTS_PER_MINUTE_FIELD_NUMBER: _ClassVar[int]
    SERVICE_THROUGHPUT_FIELD_NUMBER: _ClassVar[int]
    messages_per_second: float
    conversations_per_minute: float
    ai_requests_per_minute: float
    service_throughput: _containers.ScalarMap[str, float]
    def __init__(self, messages_per_second: _Optional[float] = ..., conversations_per_minute: _Optional[float] = ..., ai_requests_per_minute: _Optional[float] = ..., service_throughput: _Optional[_Mapping[str, float]] = ...) -> None: ...

class AnalyticsStreamRequest(_message.Message):
    __slots__ = ("subscriptions", "update_interval")
    SUBSCRIPTIONS_FIELD_NUMBER: _ClassVar[int]
    UPDATE_INTERVAL_FIELD_NUMBER: _ClassVar[int]
    subscriptions: _containers.RepeatedCompositeFieldContainer[AnalyticsSubscription]
    update_interval: _duration_pb2.Duration
    def __init__(self, subscriptions: _Optional[_Iterable[_Union[AnalyticsSubscription, _Mapping]]] = ..., update_interval: _Optional[_Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]] = ...) -> None: ...

class AnalyticsSubscription(_message.Message):
    __slots__ = ("type", "filters", "subscription_id")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTION_ID_FIELD_NUMBER: _ClassVar[int]
    type: AnalyticsType
    filters: _containers.RepeatedScalarFieldContainer[str]
    subscription_id: str
    def __init__(self, type: _Optional[_Union[AnalyticsType, str]] = ..., filters: _Optional[_Iterable[str]] = ..., subscription_id: _Optional[str] = ...) -> None: ...

class AnalyticsUpdate(_message.Message):
    __slots__ = ("subscription_id", "type", "data", "timestamp")
    SUBSCRIPTION_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    subscription_id: str
    type: AnalyticsType
    data: _any_pb2.Any
    timestamp: _timestamp_pb2.Timestamp
    def __init__(self, subscription_id: _Optional[str] = ..., type: _Optional[_Union[AnalyticsType, str]] = ..., data: _Optional[_Union[_any_pb2.Any, _Mapping]] = ..., timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ReportRequest(_message.Message):
    __slots__ = ("report_type", "start_time", "end_time", "entity_ids", "config")
    REPORT_TYPE_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    ENTITY_IDS_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    report_type: ReportType
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    entity_ids: _containers.RepeatedScalarFieldContainer[str]
    config: ReportConfig
    def __init__(self, report_type: _Optional[_Union[ReportType, str]] = ..., start_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., entity_ids: _Optional[_Iterable[str]] = ..., config: _Optional[_Union[ReportConfig, _Mapping]] = ...) -> None: ...

class ReportConfig(_message.Message):
    __slots__ = ("format", "metrics", "include_visualizations", "parameters")
    class ParametersEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_VISUALIZATIONS_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    format: ReportFormat
    metrics: _containers.RepeatedScalarFieldContainer[str]
    include_visualizations: bool
    parameters: _containers.ScalarMap[str, str]
    def __init__(self, format: _Optional[_Union[ReportFormat, str]] = ..., metrics: _Optional[_Iterable[str]] = ..., include_visualizations: bool = ..., parameters: _Optional[_Mapping[str, str]] = ...) -> None: ...

class ReportResponse(_message.Message):
    __slots__ = ("report_id", "report_data", "metadata", "download_urls")
    REPORT_ID_FIELD_NUMBER: _ClassVar[int]
    REPORT_DATA_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    DOWNLOAD_URLS_FIELD_NUMBER: _ClassVar[int]
    report_id: str
    report_data: bytes
    metadata: ReportMetadata
    download_urls: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, report_id: _Optional[str] = ..., report_data: _Optional[bytes] = ..., metadata: _Optional[_Union[ReportMetadata, _Mapping]] = ..., download_urls: _Optional[_Iterable[str]] = ...) -> None: ...

class ReportMetadata(_message.Message):
    __slots__ = ("type", "format", "size_bytes", "generated_at", "expires_at", "checksum")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    GENERATED_AT_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    CHECKSUM_FIELD_NUMBER: _ClassVar[int]
    type: ReportType
    format: ReportFormat
    size_bytes: int
    generated_at: _timestamp_pb2.Timestamp
    expires_at: _timestamp_pb2.Timestamp
    checksum: str
    def __init__(self, type: _Optional[_Union[ReportType, str]] = ..., format: _Optional[_Union[ReportFormat, str]] = ..., size_bytes: _Optional[int] = ..., generated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., expires_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., checksum: _Optional[str] = ...) -> None: ...

class AnalyticsSummary(_message.Message):
    __slots__ = ("total_conversations", "total_messages", "active_users", "avg_satisfaction", "top_topics", "trends")
    class TopTopicsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    TOTAL_CONVERSATIONS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_USERS_FIELD_NUMBER: _ClassVar[int]
    AVG_SATISFACTION_FIELD_NUMBER: _ClassVar[int]
    TOP_TOPICS_FIELD_NUMBER: _ClassVar[int]
    TRENDS_FIELD_NUMBER: _ClassVar[int]
    total_conversations: int
    total_messages: int
    active_users: int
    avg_satisfaction: float
    top_topics: _containers.ScalarMap[str, int]
    trends: TrendAnalysis
    def __init__(self, total_conversations: _Optional[int] = ..., total_messages: _Optional[int] = ..., active_users: _Optional[int] = ..., avg_satisfaction: _Optional[float] = ..., top_topics: _Optional[_Mapping[str, int]] = ..., trends: _Optional[_Union[TrendAnalysis, _Mapping]] = ...) -> None: ...

class TrendAnalysis(_message.Message):
    __slots__ = ("conversation_growth_rate", "user_engagement_trend", "tone_satisfaction_trend", "data_points")
    CONVERSATION_GROWTH_RATE_FIELD_NUMBER: _ClassVar[int]
    USER_ENGAGEMENT_TREND_FIELD_NUMBER: _ClassVar[int]
    TONE_SATISFACTION_TREND_FIELD_NUMBER: _ClassVar[int]
    DATA_POINTS_FIELD_NUMBER: _ClassVar[int]
    conversation_growth_rate: float
    user_engagement_trend: float
    tone_satisfaction_trend: float
    data_points: _containers.RepeatedCompositeFieldContainer[TrendPoint]
    def __init__(self, conversation_growth_rate: _Optional[float] = ..., user_engagement_trend: _Optional[float] = ..., tone_satisfaction_trend: _Optional[float] = ..., data_points: _Optional[_Iterable[_Union[TrendPoint, _Mapping]]] = ...) -> None: ...

class TrendPoint(_message.Message):
    __slots__ = ("timestamp", "values")
    class ValuesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: float
        def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    values: _containers.ScalarMap[str, float]
    def __init__(self, timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., values: _Optional[_Mapping[str, float]] = ...) -> None: ...
