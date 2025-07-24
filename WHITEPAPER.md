# WhatStyle 

## Sequence Diagram

**Scenario 1** -> Girlfriend sends casual message

```mermaid
sequenceDiagram
    participant GF as 👩 Girlfriend
    participant WA as 📱 WhatsApp API
    participant Gateway as 🌐 API Gateway
    participant MCP as 🤖 MCP Service
    participant ToneService as 🎯 Tone Service
    participant ProfileService as 👤 Profile Service
    participant AIService as 🧠 AI Service
    participant MistralAPI as 🔮 Mistral AI
    participant CacheService as ⚡ Cache Service
    participant DBService as 🗄️ Database Service

    Note over GF, DBService: Casual conversation with girlfriend
    
    GF->>WA: "hey babe 😘 what's up?"
    WA->>Gateway: POST /webhook message
    Gateway->>MCP: ProcessMessage text and sender
    
    MCP->>ProfileService: GetUserProfile phone number
    ProfileService->>CacheService: Check profile cache
    
    alt Profile in cache
        CacheService-->>ProfileService: Profile with casual tone
    else Profile not cached
        ProfileService->>DBService: Query user profile
        DBService-->>ProfileService: Profile data
        ProfileService->>CacheService: Cache profile
    end
    
    ProfileService-->>MCP: UserProfile casual tone
    
    MCP->>ToneService: AnalyzeTone with user profile
    ToneService->>ToneService: Extract emojis and casual words
    ToneService-->>MCP: ToneAnalysis casual with high confidence
    
    MCP->>AIService: GenerateResponse with casual tone
    AIService->>AIService: Build dynamic prompt for girlfriend
    AIService->>MistralAPI: Chat completion with casual prompt
    MistralAPI-->>AIService: Response with emojis
    AIService-->>MCP: Formatted response
    
    MCP->>DBService: Store conversation context
    MCP->>CacheService: Update recent conversations
    
    MCP-->>Gateway: MessageResponse with casual text
    Gateway->>WA: Send message to girlfriend
    WA->>GF: "Hey love! Just working on my project 😊 Missing you! What are you up to? 💕"
```

**Scenario 2** -> Father sends formal message 
```mermaid
sequenceDiagram
    participant Dad as 👨 Father
    participant WA as 📱 WhatsApp API
    participant Gateway as 🌐 API Gateway
    participant MCP as 🤖 MCP Service
    participant ToneService as 🎯 Tone Service
    participant ProfileService as 👤 Profile Service
    participant AIService as 🧠 AI Service
    participant MistralAPI as 🔮 Mistral AI

    Note over Dad, MistralAPI: Formal conversation with father
    
    Dad->>WA: "Good morning. How are your studies going?"
    WA->>Gateway: POST /webhook with message
    Gateway->>MCP: ProcessMessage formal text
    
    MCP->>ProfileService: GetUserProfile father phone
    ProfileService-->>MCP: UserProfile formal tone no emojis
    
    MCP->>ToneService: AnalyzeTone formal message
    ToneService->>ToneService: Detect formal greeting and proper grammar
    ToneService-->>MCP: ToneAnalysis formal caring high confidence
    
    MCP->>AIService: GenerateResponse formal tone father relationship
    AIService->>AIService: Build respectful informative prompt
    AIService->>MistralAPI: Chat completion with formal prompt
    MistralAPI-->>AIService: Professional respectful response
    AIService-->>MCP: Formatted formal response
    
    MCP-->>Gateway: MessageResponse formal text
    Gateway->>WA: Send formal response
    WA->>Dad: "Good morning Dad. My studies are going well, thank you for asking. I'm currently working on my final project and making good progress. How are you doing?"
```

**Scenario 3** -> Brother sends sad message
```mermaid
sequenceDiagram
    participant Bro as 👦 Brother
    participant WA as 📱 WhatsApp API
    participant Gateway as 🌐 API Gateway
    participant MCP as 🤖 MCP Service
    participant ToneService as 🎯 Tone Service
    participant EmotionService as 😢 Emotion Service
    participant StickerService as 🎭 Sticker Service
    participant AIService as 🧠 AI Service
    participant MediaService as 🖼️ Media Service

    Note over Bro, MediaService: Brother is sad, respond with supportive sticker
    
    Bro->>WA: "failed my exam again 😭 feeling terrible"
    WA->>Gateway: POST /webhook sad message
    Gateway->>MCP: ProcessMessage with crying emoji
    
    MCP->>ToneService: AnalyzeTone sad text
    ToneService->>EmotionService: DetectEmotion text and crying emoji
    EmotionService-->>ToneService: Emotion sadness high intensity needs support
    ToneService-->>MCP: ToneAnalysis sad distressed requires empathy
    
    alt Emotional support needed
        MCP->>StickerService: GetSupportiveSticker emotion sad relationship brother
        StickerService->>StickerService: Select appropriate supportive sticker
        StickerService-->>MCP: Sticker hug sticker supportive virtual hug
        
        MCP->>AIService: GenerateEmpatheticResponse emotion sad context exam failure
        AIService-->>MCP: "Aw man, that sucks 😞 Don't worry bro, you'll get it next time! Want to talk about it?"
        
        MCP->>MediaService: PrepareMultiMediaResponse text and sticker
        MediaService-->>MCP: MultiMediaMessage with sticker and text
    end
    
    MCP-->>Gateway: MultiMediaResponse sticker and supportive text
    Gateway->>WA: Send sticker plus supportive message
    WA->>Bro: [🤗 Supportive Hug Sticker] + "Aw man, that sucks 😞 Don't worry bro, you'll get it next time! Want to talk about it?"
```

**Scenario 4** -> Real-time Tone learning and adaptation
```mermaid
sequenceDiagram
    participant User as 👤 User
    participant MCP as 🤖 MCP Service
    participant ToneService as 🎯 Tone Service
    participant MLService as 🤖 ML Service
    participant SparkService as ⚡ Spark Service
    participant VectorDB as 🔍 Vector DB
    participant AIService as 🧠 AI Service

    Note over User, AIService: System learns from conversation patterns
    
    User->>MCP: Series of messages over time
    MCP->>ToneService: AnalyzeTone conversation history
    
    ToneService->>MLService: UpdateUserToneProfile user id and new patterns
    MLService->>SparkService: ProcessToneEvolution user data
    
    par Real-time Learning
        SparkService->>SparkService: Analyze communication patterns
        SparkService->>VectorDB: Update tone embeddings
    and Batch Processing
        SparkService->>SparkService: Train personalized model
        SparkService->>MLService: UpdatedPersonalizedModel
    end
    
    MLService-->>ToneService: EnhancedToneProfile updated preferences new patterns
    ToneService-->>MCP: ImprovedToneUnderstanding
    
    Note over MCP: Next messages use improved understanding
    
    User->>MCP: New message
    MCP->>AIService: GenerateResponse enhanced profile
    AIService-->>User: More accurate personalized response
```

**Scenario 5** -> Group chat with multiple tone
```mermaid
sequenceDiagram
    participant User as 👤 User
    participant MCP as 🤖 MCP Service
    participant ToneService as 🎯 Tone Service
    participant MLService as 🤖 ML Service
    participant SparkService as ⚡ Spark Service
    participant VectorDB as 🔍 Vector DB
    participant AIService as 🧠 AI Service

    Note over User, AIService: System learns from conversation patterns
    
    User->>MCP: Series of messages over time
    MCP->>ToneService: AnalyzeTone conversation history
    
    ToneService->>MLService: UpdateUserToneProfile user id and new patterns
    MLService->>SparkService: ProcessToneEvolution user data
    
    par Real-time Learning
        SparkService->>SparkService: Analyze communication patterns
        SparkService->>VectorDB: Update tone embeddings
    and Batch Processing
        SparkService->>SparkService: Train personalized model
        SparkService->>MLService: UpdatedPersonalizedModel
    end
    
    MLService-->>ToneService: EnhancedToneProfile updated preferences new patterns
    ToneService-->>MCP: ImprovedToneUnderstanding
    
    Note over MCP: Next messages use improved understanding
    
    User->>MCP: New message
    MCP->>AIService: GenerateResponse enhanced profile
    AIService-->>User: More accurate personalized response
```

**Error Handling and Fallback Sequence**
```mermaid
sequenceDiagram
    participant User as 👤 User
    participant WA as 📱 WhatsApp API
    participant Gateway as 🌐 API Gateway
    participant MCP as 🤖 MCP Service
    participant ToneService as 🎯 Tone Service
    participant AIService as 🧠 AI Service
    participant MistralAPI as 🔮 Mistral AI
    participant FallbackService as 🔄 Fallback Service
    participant LocalAI as 🏠 Local AI

    Note over User, LocalAI: Handle API failures gracefully
    
    User->>WA: "How's your day going?"
    WA->>Gateway: POST webhook
    Gateway->>MCP: ProcessMessage
    
    MCP->>ToneService: AnalyzeTone
    ToneService-->>MCP: ToneAnalysis casual type
    
    MCP->>AIService: GenerateResponse
    AIService->>MistralAPI: API call
    
    Note over MistralAPI: API Failure Rate Limit
    MistralAPI-->>AIService: Error 429 Rate limit exceeded
    
    AIService->>FallbackService: HandleAPIFailure error rate limit
    FallbackService->>LocalAI: GenerateLocalResponse tone casual
    LocalAI-->>FallbackService: Basic but appropriate response
    FallbackService-->>AIService: FallbackResponse
    
    AIService-->>MCP: Response with fallback indicator
    MCP-->>Gateway: Response text and fallback source
    Gateway->>WA: Send response
    WA->>User: "Pretty good! Thanks for asking 😊"
    
    Note over FallbackService: Log for later retry
    FallbackService->>FallbackService: Queue for retry when API available
```

## Class Diagram

Core MCP Service Classes 
```mermaid
classDiagram
    class MCPService {
        +processMessage(MessageRequest) MessageResponse
        +streamConversation(ConversationStreamRequest) Stream~ConversationUpdate~
        +getContext(ContextRequest) ContextResponse
        +updateContext(UpdateContextRequest) ContextResponse
        +getTools(ToolsRequest) ToolsResponse
        +executeTool(ToolExecutionRequest) ToolExecutionResponse
        -validateMessage(MessageRequest) bool
        -enrichContext(Context) EnrichedContext
    }

    class MessageHandler {
        +handleIncoming(WhatsAppMessage) ProcessedMessage
        +parseContent(string) ParsedContent
        +extractMetadata(WhatsAppMessage) MessageMetadata
        +validateSender(string) UserProfile
        -sanitizeInput(string) string
        -detectLanguage(string) string
    }

    class ContextManager {
        +loadContext(conversationId) ConversationContext
        +updateContext(Context, NewMessage) UpdatedContext
        +getRecentMessages(userId, limit) List~Message~
        +saveContext(Context) bool
        -cleanOldContext() void
        -compressContext(Context) CompressedContext
    }

    class ToolRegistry {
        +registerTool(Tool) bool
        +getTool(toolName) Tool
        +getAvailableTools(context) List~Tool~
        +executeTool(toolName, params) ToolResult
        -validateToolParams(Tool, params) bool
        -checkPermissions(Tool, user) bool
    }

    MCPService --> MessageHandler : uses
    MCPService --> ContextManager : manages
    MCPService --> ToolRegistry : coordinates
    MessageHandler --> ContextManager : updates
    ToolRegistry --> ContextManager : accesses
```

Tone Analysis Service Classes 
```mermaid
classDiagram
    class ToneAnalysisService {
        +analyzeTone(ToneAnalysisRequest) ToneAnalysisResponse
        +batchAnalyzeTone(BatchRequest) BatchResponse
        +getToneProfile(userId) ToneProfile
        +updateToneProfile(userId, profile) bool
        +streamToneAnalysis() Stream~ToneAnalysis~
        +trainUserModel(TrainingData) ModelResult
    }

    class ToneClassifier {
        +classifyTone(text, context) ToneClassification
        +extractFeatures(text) ToneFeatures
        +calculateConfidence(classification) float
        +detectEmotions(text) EmotionalProfile
        -preprocessText(text) ProcessedText
        -loadModel(userId) PersonalizedModel
    }

    class EmotionDetector {
        +detectEmotion(text, emojis) EmotionResult
        +analyzeSentiment(text) SentimentScore
        +detectUrgency(text) UrgencyLevel
        +extractEmotionalCues(text) List~EmotionalCue~
        -analyzeEmojis(emojis) EmojiSentiment
        -detectSarcasm(text) SarcasmScore
    }

    class ToneProfileManager {
        +createProfile(userId) ToneProfile
        +updateProfile(userId, newData) ToneProfile
        +getProfile(userId) ToneProfile
        +evolveProfile(userId, interactions) ToneProfile
        -calculateToneWeights(interactions) Map~ToneType, float~
        -identifyPatterns(history) List~Pattern~
    }

    class PersonalizedModel {
        +predict(features) ToneResult
        +train(examples) TrainingResult
        +update(newData) void
        +getAccuracy() float
        -featureEngineering(data) Features
        -crossValidate() ValidationResult
    }

    ToneAnalysisService --> ToneClassifier : uses
    ToneAnalysisService --> ToneProfileManager : manages
    ToneClassifier --> EmotionDetector : integrates
    ToneClassifier --> PersonalizedModel : uses
    ToneProfileManager --> PersonalizedModel : maintains
```

AI Response Generation Classes
```mermaid
classDiagram
    class AIService {
        +generateResponse(context, toneProfile) Response
        +generateEmpatheticResponse(emotion, context) Response
        +adaptResponseTone(response, targetTone) AdaptedResponse
        +selectModel(complexity, user) AIModel
        -buildPrompt(context, tone) Prompt
        -postProcessResponse(response) ProcessedResponse
    }

    class ModelRouter {
        +selectOptimalModel(request) AIModel
        +routeRequest(request) ModelEndpoint
        +handleFailover(failedModel) AlternativeModel
        +monitorPerformance() PerformanceMetrics
        -calculateCost(model, request) float
        -checkAvailability(model) bool
    }

    class PromptBuilder {
        +buildDynamicPrompt(context, tone, relationship) Prompt
        +addPersonalityContext(prompt, profile) EnhancedPrompt
        +injectToneInstructions(prompt, tone) TonedPrompt
        +addConversationHistory(prompt, history) ContextualPrompt
        -templatePrompt(base, variables) Prompt
        -validatePrompt(prompt) bool
    }

    class ResponseProcessor {
        +formatResponse(rawResponse, tone) FormattedResponse
        +addEmojis(response, profile) EmojiResponse
        +adjustLength(response, preference) AdjustedResponse
        +applySafetyFilter(response) SafeResponse
        -detectInappropriate(response) bool
        -enhanceReadability(response) EnhancedResponse
    }

    class MistralClient {
        +chatCompletion(prompt) Response
        +streamCompletion(prompt) Stream~Response~
        +embedText(text) Embeddings
        +handleError(error) ErrorResponse
        -retryWithBackoff(request) Response
        -manageRateLimit() void
    }

    AIService --> ModelRouter : uses
    AIService --> PromptBuilder : creates
    AIService --> ResponseProcessor : processes
    ModelRouter --> MistralClient : routes to
    PromptBuilder --> ResponseProcessor : feeds into
```

Data Layer Classes
```mermaid
classDiagram
    class UserRepository {
        +createUser(userProfile) User
        +getUser(userId) User
        +updateUser(userId, updates) User
        +deleteUser(userId) bool
        +findByPhone(phone) User
        -validateUserData(data) bool
        -encryptSensitiveData(data) EncryptedData
    }

    class ConversationRepository {
        +createConversation(conversation) Conversation
        +getConversation(conversationId) Conversation
        +updateConversation(conversationId, updates) Conversation
        +getConversationHistory(userId, limit) List~Message~
        +archiveConversation(conversationId) bool
        -partitionByDate(conversations) PartitionedData
        -compressOldMessages(messages) CompressedMessages
    }

    class ToneDataRepository {
        +saveToneAnalysis(analysis) bool
        +getToneHistory(userId) List~ToneAnalysis~
        +updateToneProfile(userId, profile) ToneProfile
        +getToneStatistics(userId) ToneStats
        +batchInsertAnalyses(analyses) bool
        -indexToneData(data) IndexedData
        -aggregateToneMetrics(data) AggregatedMetrics
    }

    class CacheService {
        +get(key) CachedData
        +set(key, data, ttl) bool
        +delete(key) bool
        +exists(key) bool
        +invalidatePattern(pattern) bool
        -serializeData(data) SerializedData
        -compressData(data) CompressedData
    }

    class VectorDatabase {
        +storeEmbedding(id, vector) bool
        +searchSimilar(vector, limit) List~SimilarityResult~
        +updateEmbedding(id, vector) bool
        +deleteEmbedding(id) bool
        +batchSearch(vectors) List~SearchResult~
        -calculateSimilarity(v1, v2) float
        -indexVector(vector) IndexedVector
    }

    UserRepository --> CacheService : caches
    ConversationRepository --> VectorDatabase : stores embeddings
    ToneDataRepository --> CacheService : caches profiles
    VectorDatabase --> CacheService : caches results
```

WhatsApp Integration Classes
```mermaid
classDiagram
    class WhatsAppClient {
        +sendMessage(recipient, message) SendResult
        +sendSticker(recipient, sticker) SendResult
        +sendMedia(recipient, media) SendResult
        +getMessageStatus(messageId) MessageStatus
        +handleWebhook(webhookData) ProcessedWebhook
        -validateRecipient(phone) bool
        -formatMessage(content) FormattedMessage
    }

    class WebhookHandler {
        +processIncoming(webhook) ProcessedMessage
        +validateSignature(signature, body) bool
        +parseMessage(webhookData) ParsedMessage
        +extractSender(webhookData) SenderInfo
        +handleDeliveryStatus(status) void
        -verifyWebhookSource(webhook) bool
        -extractMessageContent(data) MessageContent
    }

    class MessageParser {
        +parseText(textMessage) ParsedText
        +parseMedia(mediaMessage) ParsedMedia
        +parseLocation(locationMessage) ParsedLocation
        +parseContact(contactMessage) ParsedContact
        +extractMetadata(message) MessageMetadata
        -detectMessageType(message) MessageType
        -sanitizeContent(content) SanitizedContent
    }

    class MessageSender {
        +sendTextMessage(recipient, text) bool
        +sendMediaMessage(recipient, media) bool
        +sendTemplateMessage(recipient, template) bool
        +queueMessage(message) bool
        +retryFailedMessage(messageId) bool
        -rateLimitCheck() bool
        -formatForWhatsApp(message) WhatsAppMessage
    }

    class StickerService {
        +getSupportiveSticker(emotion) Sticker
        +getRandomSticker(category) Sticker
        +createCustomSticker(image) Sticker
        +getAllStickers() List~Sticker~
        +getStickerByEmotion(emotion) List~Sticker~
        -categorizeSticker(sticker) Category
        -validateStickerFormat(sticker) bool
    }

    WhatsAppClient --> WebhookHandler : processes
    WhatsAppClient --> MessageSender : sends through
    WebhookHandler --> MessageParser : parses with
    MessageSender --> StickerService : gets stickers from
```

Analytics and Monitoring Classes
```mermaid
classDiagram
    class AnalyticsService {
        +getConversationAnalytics(request) ConversationAnalytics
        +getUserAnalytics(request) UserAnalytics
        +getSystemMetrics(request) SystemMetrics
        +streamAnalytics(subscription) Stream~AnalyticsUpdate~
        +generateReport(reportRequest) Report
        -aggregateMetrics(data) AggregatedMetrics
        -calculateTrends(timeSeries) TrendAnalysis
    }

    class MetricsCollector {
        +collectSystemMetrics() SystemMetrics
        +collectUserMetrics(userId) UserMetrics
        +collectConversationMetrics(convId) ConversationMetrics
        +collectPerformanceMetrics() PerformanceMetrics
        +recordEvent(event) bool
        -calculateAverages(metrics) AverageMetrics
        -detectAnomalies(metrics) List~Anomaly~
    }

    class ReportGenerator {
        +generateUserReport(userId, period) UserReport
        +generateSystemReport(period) SystemReport
        +generateToneReport(userId, period) ToneReport
        +exportToPDF(report) PDFReport
        +exportToCSV(data) CSVExport
        -formatReport(data, template) FormattedReport
        -addVisualizations(report) VisualReport
    }

    class PerformanceMonitor {
        +monitorResponseTime() ResponseTimeMetrics
        +monitorThroughput() ThroughputMetrics
        +monitorErrorRate() ErrorMetrics
        +alertOnThreshold(metric, threshold) Alert
        +trackResourceUsage() ResourceMetrics
        -calculatePercentiles(data) PercentileMetrics
        -detectPerformanceIssues(metrics) List~Issue~
    }

    AnalyticsService --> MetricsCollector : collects from
    AnalyticsService --> ReportGenerator : generates with
    MetricsCollector --> PerformanceMonitor : monitors through
    ReportGenerator --> PerformanceMonitor : includes metrics from
```

Spark Integration Classes
```mermaid
classDiagram
    class SparkJobManager {
        +submitToneAnalysisJob(data) JobResult
        +submitModelTrainingJob(config) TrainingResult
        +submitAnalyticsJob(query) AnalyticsResult
        +monitorJob(jobId) JobStatus
        +cancelJob(jobId) bool
        -createSparkSession() SparkSession
        -optimizeQuery(query) OptimizedQuery
    }

    class ToneAnalyticsBatch {
        +analyzeBatchTones(messages) BatchToneResult
        +identifyTonePatterns(userData) TonePatterns
        +calculateToneEvolution(userHistory) ToneEvolution
        +generateToneInsights(analysis) ToneInsights
        -preprocessMessages(messages) ProcessedMessages
        -featureExtraction(messages) Features
    }

    class ConversationAnalytics {
        +analyzeConversationFlow(conversations) FlowAnalysis
        +identifyEngagementPatterns(data) EngagementPatterns
        +calculateSatisfactionScores(feedback) SatisfactionMetrics
        +detectConversationAnomalies(data) List~Anomaly~
        -aggregateConversationData(data) AggregatedData
        -timeSeriesAnalysis(data) TimeSeriesResults
    }

    class ModelTrainer {
        +trainPersonalizedModel(userData) TrainedModel
        +crossValidateModel(model, data) ValidationResults
        +hyperparameterTuning(model) OptimizedModel
        +evaluateModel(model, testData) EvaluationMetrics
        -prepareTrainingData(rawData) TrainingDataset
        -featureEngineering(data) EngineeredFeatures
    }

    class StreamProcessor {
        +processMessageStream() Stream~ProcessedMessage~
        +processAnalyticsStream() Stream~Analytics~
        +processToneUpdates() Stream~ToneUpdate~
        +handleBackpressure() void
        -createKafkaStream() KafkaStream
        -applyWindowingFunction(stream) WindowedStream
    }

    SparkJobManager --> ToneAnalyticsBatch : manages
    SparkJobManager --> ConversationAnalytics : manages
    SparkJobManager --> ModelTrainer : manages
    SparkJobManager --> StreamProcessor : manages
    ModelTrainer --> ToneAnalyticsBatch : uses data from
```

## System Architecture

Mircoservice Architecture Overview with DataStax 
```mermaid
graph TB
    subgraph "External Layer"
        WhatsApp[📱 WhatsApp Business API]
        WebInterface[🌐 Web Dashboard]
        MobileApp[📱 Mobile App]
    end
    
    subgraph "API Gateway Layer"
        Gateway[🌐 API Gateway<br/>Rate Limiting, Auth, Routing]
        LoadBalancer[⚖️ Load Balancer<br/>Traffic Distribution]
    end
    
    subgraph "Core Services"
        MCPService[🤖 MCP Service<br/>Protocol Handler]
        ToneService[🎯 Tone Analysis Service<br/>ML-Powered Classification]
        AIService[🧠 AI Service<br/>Response Generation]
        UserService[👤 User Profile Service<br/>Profile Management]
        ConversationService[💬 Conversation Service<br/>Context Management]
    end
    
    subgraph "Specialized Services"
        StickerService[🎭 Sticker Service<br/>Media Selection]
        AnalyticsService[📊 Analytics Service<br/>Insights & Reports]
        NotificationService[🔔 Notification Service<br/>Alerts & Updates]
        FallbackService[🔄 Fallback Service<br/>Error Recovery]
    end
    
    subgraph "Data Layer"
        DataStaxAstra[(🗄️ DataStax Astra DB<br/>Cloud-Native Database)]
        DataStaxVector[(🔍 DataStax Vector Search<br/>Embeddings & Similarity)]
        RedisCluster[(⚡ Redis Cluster<br/>Cache & Sessions)]
    end
    
    subgraph "Processing Layer"
        SparkCluster[⚡ Spark Cluster<br/>Batch & Stream Processing]
        KafkaCluster[📊 Kafka Cluster<br/>Event Streaming]
        MLPipeline[🤖 ML Pipeline<br/>Model Training]
    end
    
    subgraph "External AI"
        MistralAPI[🔮 Mistral AI API]
        OpenAIAPI[🤖 OpenAI API]
        LocalLLM[🏠 Local LLM<br/>Ollama/Local Models]
    end
    
    subgraph "Monitoring"
        Prometheus[📈 Prometheus<br/>Metrics Collection]
        Grafana[📊 Grafana<br/>Dashboards]
        AlertManager[🚨 Alert Manager<br/>Incident Response]
    end
    
    %% External connections
    WhatsApp --> Gateway
    WebInterface --> Gateway
    MobileApp --> Gateway
    
    %% Gateway layer
    Gateway --> LoadBalancer
    LoadBalancer --> MCPService
    LoadBalancer --> UserService
    LoadBalancer --> AnalyticsService
    
    %% Core service interactions
    MCPService --> ToneService
    MCPService --> AIService
    MCPService --> ConversationService
    MCPService --> UserService
    
    ToneService --> AIService
    AIService --> StickerService
    ConversationService --> AnalyticsService
    UserService --> NotificationService
    
    %% AI service connections
    AIService --> MistralAPI
    AIService --> OpenAIAPI
    AIService --> LocalLLM
    FallbackService --> LocalLLM
    
    %% Data layer connections
    MCPService --> RedisCluster
    ToneService --> DataStaxAstra
    ToneService --> DataStaxVector
    UserService --> DataStaxAstra
    ConversationService --> DataStaxAstra
    AnalyticsService --> DataStaxAstra
    
    %% Processing layer
    ToneService --> KafkaCluster
    AnalyticsService --> SparkCluster
    KafkaCluster --> SparkCluster
    SparkCluster --> MLPipeline
    MLPipeline --> ToneService
    
    %% Monitoring connections
    MCPService -.-> Prometheus
    ToneService -.-> Prometheus
    AIService -.-> Prometheus
    Prometheus --> Grafana
    Prometheus --> AlertManager
```

Service Communication Patterns 
```mermaid
graph LR
    subgraph "Synchronous gRPC"
        MCPSync[MCP Service] --> ToneSync[Tone Service]
        MCPSync --> UserSync[User Service]
        ToneSync --> AISync[AI Service]
    end
    
    subgraph "Asynchronous Messaging"
        ToneAsync[Tone Service] -->|Kafka| AnalyticsAsync[Analytics Service]
        ConvAsync[Conversation Service] -->|Kafka| MLAsync[ML Pipeline]
        UserAsync[User Service] -->|Kafka| NotifAsync[Notification Service]
    end
    
    subgraph "Event Streaming"
        KafkaTopics[📊 Kafka Topics<br/>• message-events<br/>• tone-updates<br/>• user-actions<br/>• system-metrics]
        
        SparkStream[⚡ Spark Streaming<br/>Real-time Processing]
        
        KafkaTopics --> SparkStream
        SparkStream --> KafkaTopics
    end
    
    subgraph "Caching Strategy"
        L1Cache[🔥 L1 Cache<br/>Application Memory]
        L2Cache[⚡ L2 Cache<br/>Redis Cluster]
        Database[(🗄️ Database<br/>DataStax Astra)]
        
        L1Cache -->|Miss| L2Cache
        L2Cache -->|Miss| Database
    end

```

Data Flow Architecture
```mermaid
flowchart TD
    subgraph "Ingestion Layer"
        WAMessage[📱 WhatsApp Message] --> MessageQueue[📬 Message Queue]
        WebInput[🌐 Web Input] --> MessageQueue
        APIInput[🔌 API Input] --> MessageQueue
    end
    
    subgraph "Processing Pipeline"
        MessageQueue --> Validator[✅ Message Validator]
        Validator --> ToneAnalyzer[🎯 Tone Analyzer]
        ToneAnalyzer --> ContextBuilder[📋 Context Builder]
        ContextBuilder --> ResponseGen[🧠 Response Generator]
        ResponseGen --> OutputFormatter[📝 Output Formatter]
    end
    
    subgraph "Real-time Stream"
        ToneAnalyzer --> ToneStream[🌊 Tone Stream]
        ContextBuilder --> ConversationStream[💬 Conversation Stream]
        ResponseGen --> AnalyticsStream[📊 Analytics Stream]
        
        ToneStream --> SparkProcessor[⚡ Spark Processor]
        ConversationStream --> SparkProcessor
        AnalyticsStream --> SparkProcessor
        
        SparkProcessor --> MLUpdater[🤖 ML Model Updater]
        SparkProcessor --> DashboardUpdater[📈 Dashboard Updater]
    end
    
    subgraph "Storage Layer"
        OutputFormatter --> MessageStore[(💬 Message Store<br/>DataStax Astra)]
        ToneAnalyzer --> ToneStore[(🎯 Tone Store<br/>DataStax Astra)]
        ContextBuilder --> ContextStore[(📋 Context Store<br/>DataStax Astra)]
        MLUpdater --> ModelStore[(🤖 Model Store<br/>DataStax Vector)]
    end
    
    subgraph "Output Layer"
        OutputFormatter --> WhatsAppAPI[📱 WhatsApp API]
        OutputFormatter --> WebSocket[🔌 WebSocket]
        OutputFormatter --> PushNotification[🔔 Push Notification]
    end
```

State Management and Event Flow
```mermaid
stateDiagram-v2
    [*] --> MessageReceived
    
    MessageReceived --> ValidatingMessage
    ValidatingMessage --> MessageValid: validation_success
    ValidatingMessage --> MessageRejected: validation_failed
    
    MessageValid --> LoadingUserProfile
    LoadingUserProfile --> ProfileLoaded: profile_found
    LoadingUserProfile --> CreatingProfile: profile_not_found
    
    CreatingProfile --> ProfileLoaded: profile_created
    
    ProfileLoaded --> AnalyzingTone
    AnalyzingTone --> ToneAnalyzed: analysis_complete
    AnalyzingTone --> ToneFallback: analysis_failed
    
    ToneAnalyzed --> GeneratingResponse
    ToneFallback --> GeneratingResponse
    
    GeneratingResponse --> ResponseGenerated: generation_success
    GeneratingResponse --> UsingFallback: generation_failed
    
    UsingFallback --> ResponseGenerated: fallback_success
    UsingFallback --> ErrorResponse: fallback_failed
    
    ResponseGenerated --> SendingResponse
    SendingResponse --> MessageSent: send_success
    SendingResponse --> RetryingSend: send_failed
    
    RetryingSend --> MessageSent: retry_success
    RetryingSend --> SendFailed: max_retries_exceeded
    
    MessageSent --> UpdatingContext
    UpdatingContext --> ContextUpdated
    
    ContextUpdated --> LearningFromInteraction
    LearningFromInteraction --> [*]
    
    MessageRejected --> [*]
    ErrorResponse --> [*]
    SendFailed --> [*]
```

Event Driven Architecture
```mermaid
graph TB
    subgraph "Event Sources"
        UserAction[👤 User Actions]
        SystemEvent[⚙️ System Events]
        ExternalAPI[🔌 External API Events]
        ScheduledJob[⏰ Scheduled Jobs]
    end
    
    subgraph "Event Bus"
        EventBus[📊 Kafka Event Bus<br/>Central Message Broker]
    end
    
    subgraph "Event Topics"
        MessageTopic[📬 message-events<br/>• message_received<br/>• message_sent<br/>• message_failed]
        
        ToneTopic[🎯 tone-events<br/>• tone_analyzed<br/>• profile_updated<br/>• model_trained]
        
        UserTopic[👤 user-events<br/>• user_created<br/>• profile_updated<br/>• preference_changed]
        
        SystemTopic[⚙️ system-events<br/>• service_started<br/>• error_occurred<br/>• health_check]
    end
    
    subgraph "Event Consumers"
        AnalyticsConsumer[📊 Analytics Consumer<br/>Real-time metrics]
        
        MLConsumer[🤖 ML Consumer<br/>Model training data]
        
        NotificationConsumer[🔔 Notification Consumer<br/>User alerts]
        
        AuditConsumer[📋 Audit Consumer<br/>Compliance logging]
        
        DashboardConsumer[📈 Dashboard Consumer<br/>Live updates]
    end
    
    subgraph "Event Processing"
        StreamProcessor[⚡ Stream Processor<br/>Real-time aggregation]
        
        BatchProcessor[📦 Batch Processor<br/>Scheduled analysis]
        
        CEPEngine[🔍 Complex Event Processing<br/>Pattern detection]
    end
    
    %% Event flow
    UserAction --> EventBus
    SystemEvent --> EventBus
    ExternalAPI --> EventBus
    ScheduledJob --> EventBus
    
    EventBus --> MessageTopic
    EventBus --> ToneTopic
    EventBus --> UserTopic
    EventBus --> SystemTopic
    
    MessageTopic --> AnalyticsConsumer
    MessageTopic --> AuditConsumer
    
    ToneTopic --> MLConsumer
    ToneTopic --> DashboardConsumer
    
    UserTopic --> NotificationConsumer
    UserTopic --> AnalyticsConsumer
    
    SystemTopic --> DashboardConsumer
    SystemTopic --> AuditConsumer
    
    AnalyticsConsumer --> StreamProcessor
    MLConsumer --> BatchProcessor
    DashboardConsumer --> CEPEngine
```

Deployment Architecture with DataStax
```mermaid
graph TB
    subgraph "Load Balancers"
        ELB[🌐 External Load Balancer<br/>AWS ALB / nginx]
        ILB[⚖️ Internal Load Balancer<br/>Service mesh / Istio]
    end
    
    subgraph "Kubernetes Cluster"
        subgraph "API Services Namespace"
            APIPod1[🤖 MCP Service Pod 1]
            APIPod2[🤖 MCP Service Pod 2]
            APIPod3[🤖 MCP Service Pod 3]
        end
        
        subgraph "AI Services Namespace"
            AIPod1[🧠 AI Service Pod 1]
            AIPod2[🧠 AI Service Pod 2]
            TonePod1[🎯 Tone Service Pod 1]
            TonePod2[🎯 Tone Service Pod 2]
        end
        
        subgraph "Data Services Namespace"
            UserPod[👤 User Service Pod]
            ConvPod[💬 Conversation Service Pod]
            AnalyticsPod[📊 Analytics Service Pod]
        end
        
        subgraph "Processing Namespace"
            SparkDriver[⚡ Spark Driver]
            SparkWorker1[⚡ Spark Worker 1]
            SparkWorker2[⚡ Spark Worker 2]
            SparkWorker3[⚡ Spark Worker 3]
        end
    end
    
    subgraph "Cloud Database Layer"
        DataStaxAstra1[(🗄️ DataStax Astra<br/>Multi-Region Node 1)]
        DataStaxAstra2[(🗄️ DataStax Astra<br/>Multi-Region Node 2)]
        DataStaxAstra3[(🗄️ DataStax Astra<br/>Multi-Region Node 3)]
        DataStaxVector[(🔍 DataStax Vector<br/>Embeddings Database)]
        
        RedisNode1[(⚡ Redis Node 1)]
        RedisNode2[(⚡ Redis Node 2)]
        RedisNode3[(⚡ Redis Node 3)]
    end
    
    subgraph "Message Queue"
        Kafka1[📊 Kafka Broker 1]
        Kafka2[📊 Kafka Broker 2]
        Kafka3[📊 Kafka Broker 3]
        Zookeeper[🔧 Zookeeper Ensemble]
    end
    
    subgraph "Monitoring Stack"
        PrometheusServer[📈 Prometheus Server]
        GrafanaServer[📊 Grafana Server]
        AlertManagerServer[🚨 AlertManager]
        ElasticStack[🔍 ELK Stack]
    end
    
    %% External traffic flow
    ELB --> ILB
    ILB --> APIPod1
    ILB --> APIPod2
    ILB --> APIPod3
    
    %% Internal service communication
    APIPod1 --> AIPod1
    APIPod2 --> AIPod2
    APIPod3 --> TonePod1
    
    AIPod1 --> UserPod
    AIPod2 --> ConvPod
    TonePod1 --> AnalyticsPod
    
    %% DataStax connections
    UserPod --> DataStaxAstra1
    ConvPod --> DataStaxAstra2
    AnalyticsPod --> DataStaxAstra3
    TonePod1 --> DataStaxVector
    TonePod2 --> DataStaxVector
    
    %% Redis connections
    APIPod1 --> RedisNode1
    APIPod2 --> RedisNode2
    APIPod3 --> RedisNode3
    
    %% Messaging
    TonePod1 --> Kafka1
    TonePod2 --> Kafka2
    AnalyticsPod --> Kafka3
    
    Kafka1 --> SparkDriver
    Kafka2 --> SparkWorker1
    Kafka3 --> SparkWorker2
    
    %% Monitoring
    APIPod1 -.-> PrometheusServer
    AIPod1 -.-> PrometheusServer
    TonePod1 -.-> PrometheusServer
    PrometheusServer --> GrafanaServer
    PrometheusServer --> AlertManagerServer
```
