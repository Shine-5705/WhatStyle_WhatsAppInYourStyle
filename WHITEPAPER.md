# WhatStyle 

### Sequence Diagram

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
