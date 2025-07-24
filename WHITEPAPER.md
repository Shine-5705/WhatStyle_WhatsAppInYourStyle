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
