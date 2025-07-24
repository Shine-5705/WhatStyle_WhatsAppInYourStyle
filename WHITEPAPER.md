# WhatStyle 

### Sequence Diagram

Scenario 1 -> Girlfriend sends casual message

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
```

```
