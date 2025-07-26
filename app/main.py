from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from datetime import datetime, timezone
import asyncio
import threading
import grpc
from grpc import aio
import sys
import os
from pathlib import Path
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from uuid6 import uuid7
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from dotenv import load_dotenv
load_dotenv()  # Explicitly load .env file

# Add project root to Python path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Add generated directory to path
generated_path = os.path.join(os.path.dirname(__file__), 'grpc_services', 'generated')
sys.path.append(generated_path)

# Import your UUID v7 enhanced components
from app.db.cassandra.connection import datastax_connection
from app.db.cassandra.repositories.user_repo import UserRepository, ConversationRepository, ToneRepository
from app.db.vector.vector_operations import vector_ops
from app.models.user import UserProfile
from app.models.conversation import Conversation
from app.models.tone import ToneAnalysis

# Pydantic models for API requests/responses
class MessageRequest(BaseModel):
    sender_phone: str = Field(..., description="Phone number of the sender")
    sender_name: Optional[str] = Field(None, description="Name of the sender")
    message_text: str = Field(..., description="The message text to process")
    relationship: Optional[str] = Field("friend", description="Relationship context")

class MessageResponse(BaseModel):
    response_id: str
    response_text: str
    detected_tone: str
    confidence_score: float
    processing_time_ms: float
    user_id: str
    conversation_id: str
    timestamp: str

class UserCreateRequest(BaseModel):
    phone_number: str = Field(..., description="Phone number")
    name: str = Field(..., description="User name")
    relationship: str = Field("friend", description="Relationship type")
    primary_tone: str = Field("casual", description="Primary tone preference")

class ToneAnalysisRequest(BaseModel):
    message_text: str = Field(..., description="Message to analyze")
    user_id: Optional[str] = Field(None, description="User ID for context")
    context_hint: Optional[str] = Field(None, description="Additional context")

# Global variables
grpc_server_status = {"running": False, "port": 50051, "error": None}
grpc_server_task = None
app_startup_id = str(uuid7())

# Initialize repositories
user_repo = UserRepository()
conversation_repo = ConversationRepository() 
tone_repo = ToneRepository()

async def start_grpc_server():
    """Start comprehensive gRPC health server using the enhanced health service"""
    global grpc_server_status
    try:
        # Import the enhanced health service
        from app.grpc_services.services.health_service import serve_health_service
        
        logger.info("🏥 Starting enhanced health service with UUID v7 support...")
        grpc_server_status["running"] = True
        grpc_server_status["error"] = None
        
        # Start the comprehensive health service
        await serve_health_service()
        
    except Exception as e:
        error_msg = f"gRPC health service error: {str(e)}"
        logger.error(f"❌ {error_msg}")
        grpc_server_status["running"] = False
        grpc_server_status["error"] = error_msg

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown"""
    # Startup
    logger.info(f"🚀 Starting services with startup ID: {app_startup_id}")
    global grpc_server_task
    
    try:
        # Initialize DataStax connection
        logger.info("📊 Connecting to DataStax Astra...")
        datastax_connection.connect()
        logger.info("✅ DataStax connection established")
        
        # Initialize vector operations
        logger.info("🤖 Initializing vector operations...")
        vector_info = vector_ops.get_operation_info()
        logger.info(f"✅ Vector operations ready: {vector_info}")
        
    except Exception as e:
        logger.warning(f"⚠️ Database initialization failed: {e}")
        logger.info("📝 Continuing in limited mode")
    
    # Start gRPC health server
    try:
        import health_pb2
        import health_pb2_grpc
        logger.info("✅ gRPC modules found")
        
        # Start gRPC server as background task
        grpc_server_task = asyncio.create_task(start_grpc_server())
        
        # Give it a moment to start
        await asyncio.sleep(1)
        
        logger.info("🎉 All services started!")
        
    except ImportError as e:
        error_msg = f"gRPC modules not found: {e}. Generate them first with protoc."
        logger.warning(f"⚠️ {error_msg}")
        grpc_server_status["running"] = False
        grpc_server_status["error"] = error_msg
    except Exception as e:
        error_msg = f"Startup error: {e}"
        logger.error(f"❌ {error_msg}")
        grpc_server_status["running"] = False
        grpc_server_status["error"] = error_msg
    
    # Yield control to FastAPI
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down services...")
    grpc_server_status["running"] = False
    
    # Disconnect from database
    try:
        datastax_connection.disconnect()
        logger.info("✅ Database disconnected")
    except Exception as e:
        logger.warning(f"⚠️ Database disconnect error: {e}")
    
    # Cancel gRPC server task
    if grpc_server_task and not grpc_server_task.done():
        grpc_server_task.cancel()
        try:
            await grpc_server_task
        except asyncio.CancelledError:
            logger.info("✅ gRPC server shutdown complete")

# Create FastAPI app with lifespan
app = FastAPI(
    title="WhatsApp MCP Server with UUID v7",
    description="Tone-Adaptive WhatsApp Bot with Vector Database and UUID v7 Support",
    version="2.0.0",
    lifespan=lifespan
)

@app.get("/")
async def root():
    """Root endpoint with comprehensive service status"""
    connection_info = datastax_connection.get_connection_info()
    vector_info = vector_ops.get_operation_info()
    
    return {
        "message": "WhatsApp MCP Server with UUID v7 is running!",
        "startup_id": app_startup_id,
        "services": {
            "fastapi": "running",
            "grpc_health": grpc_server_status["running"],
            "database": connection_info["connected"],
            "vector_operations": vector_info.get("model_loaded", False)
        },
        "database_info": {
            "collections": connection_info["collections"],
            "connection_id": connection_info["connection_id"],
            "uuid_version": "v7"
        },
        "vector_info": {
            "dimension": vector_info.get("vector_dimension", 0),
            "model": "all-MiniLM-L6-v2",
            "operation_id": vector_info.get("operation_id")
        },
        "version": "2.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/health")
async def health_check():
    """Comprehensive health check endpoint"""
    health_check_id = str(uuid7())
    
    # Check database health
    db_health = datastax_connection.health_check()
    
    # Check vector operations
    vector_info = vector_ops.get_operation_info()
    
    return {
        "health_check_id": health_check_id,
        "status": "healthy" if db_health.get("status") == "healthy" else "degraded",
        "service": "whatsapp-mcp-server",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "components": {
            "fastapi": "healthy",
            "grpc_health": "healthy" if grpc_server_status["running"] else "not_running",
            "database": db_health.get("status", "unhealthy"),
            "vector_operations": "healthy" if vector_info.get("model_loaded") else "not_loaded"
        },
        "database_details": db_health,
        "vector_details": vector_info,
        "uuid_version": "v7",
        "test_endpoints": {
            "process_message": "/api/v1/process-message",
            "create_user": "/api/v1/users",
            "analyze_tone": "/api/v1/analyze-tone",
            "grpc_test": "/test-grpc"
        }
    }

# API v1 Routes
@app.post("/api/v1/users", response_model=Dict[str, Any])
async def create_user(request: UserCreateRequest):
    """Create a new user with UUID v7"""
    try:
        user = await user_repo.create_user(
            phone_number=request.phone_number,
            name=request.name,
            relationship=request.relationship,
            primary_tone=request.primary_tone
        )
        
        return {
            "success": True,
            "user": user.to_dict(),
            "message": f"User created with UUID v7: {user.user_id}",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Error creating user: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create user: {str(e)}")

@app.get("/api/v1/users/{user_id}")
async def get_user(user_id: str):
    """Get user by UUID v7 ID"""
    try:
        user = await user_repo.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {
            "success": True,
            "user": user.to_dict(),
            "uuid_info": user.get_uuid_info(),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error getting user: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get user: {str(e)}")

@app.post("/api/v1/process-message", response_model=MessageResponse)
async def process_message(request: MessageRequest, background_tasks: BackgroundTasks):
    """Process WhatsApp message with comprehensive tone analysis and UUID v7 tracking"""
    processing_start = datetime.now(timezone.utc)
    processing_id = str(uuid7())
    
    try:
        logger.info(f"🔍 Processing message (ID: {processing_id[:8]}) from: {request.sender_phone}")
        
        # Get or create user
        user = await user_repo.get_user_by_phone(request.sender_phone)
        if not user:
            user = await user_repo.create_user(
                phone_number=request.sender_phone,
                name=request.sender_name or "Unknown User",
                relationship=request.relationship
            )
        
        # Record interaction
        await user_repo.record_interaction(user.user_id, "api_message")
        
        # Detect tone using vector similarity
        detected_tone, confidence = await vector_ops.get_best_tone_for_user(
            user.user_id, request.message_text, user.relationship
        )
        
        # Generate conversation ID
        conversation_id = str(uuid7())
        
        # Save message
        message = await conversation_repo.save_message(
            user_id=user.user_id,
            conversation_id=conversation_id,
            message_text=request.message_text,
            sender="user",
            detected_tone=detected_tone,
            tone_confidence=confidence,
            context_data={
                "processing_id": processing_id,
                "api_endpoint": "/api/v1/process-message",
                "sender_phone": request.sender_phone
            }
        )
        
        # Store tone embedding for learning
        background_tasks.add_task(
            store_tone_embedding_task,
            user.user_id,
            request.message_text,
            detected_tone,
            user.relationship,
            confidence,
            message.message_id
        )
        
        # Generate response
        response_text = generate_response_by_tone(
            request.message_text, user, detected_tone
        )
        
        # Save bot response
        bot_message = await conversation_repo.save_message(
            user_id=user.user_id,
            conversation_id=conversation_id,
            message_text=response_text,
            sender="bot",
            detected_tone=user.primary_tone,
            context_data={
                "processing_id": processing_id,
                "original_message_id": message.message_id
            }
        )
        
        processing_time_ms = (datetime.now(timezone.utc) - processing_start).total_seconds() * 1000
        
        return MessageResponse(
            response_id=str(uuid7()),
            response_text=response_text,
            detected_tone=detected_tone,
            confidence_score=confidence,
            processing_time_ms=processing_time_ms,
            user_id=user.user_id,
            conversation_id=conversation_id,
            timestamp=datetime.now(timezone.utc).isoformat()
        )
        
    except Exception as e:
        logger.error(f"❌ Error processing message (ID: {processing_id[:8]}): {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process message: {str(e)}")

@app.post("/api/v1/analyze-tone")
async def analyze_tone(request: ToneAnalysisRequest):
    """Analyze tone of a message using vector operations"""
    analysis_id = str(uuid7())
    
    try:
        logger.info(f"🎯 Analyzing tone (ID: {analysis_id[:8]})")
        
        user = None
        if request.user_id:
            user = await user_repo.get_user_by_id(request.user_id)
        
        # Get tone using vector similarity if user exists
        if user:
            detected_tone, confidence = await vector_ops.get_best_tone_for_user(
                user.user_id, request.message_text, user.relationship
            )
        else:
            # Use rule-based detection for unknown users
            detected_tone = detect_basic_tone(request.message_text)
            confidence = 0.6
        
        # Find similar tones
        similar_tones = await vector_ops.find_similar_tones(
            query_text=request.message_text,
            relationship=user.relationship if user else None,
            limit=3
        )
        
        return {
            "analysis_id": analysis_id,
            "message_text": request.message_text,
            "detected_tone": detected_tone,
            "confidence_score": confidence,
            "user_context": user.to_dict() if user else None,
            "similar_patterns": similar_tones[:3],
            "analysis_timestamp": datetime.now(timezone.utc).isoformat(),
            "uuid_version": "v7"
        }
        
    except Exception as e:
        logger.error(f"❌ Error analyzing tone (ID: {analysis_id[:8]}): {e}")
        raise HTTPException(status_code=500, detail=f"Failed to analyze tone: {str(e)}")

@app.get("/api/v1/users/{user_id}/tone-stats")
async def get_user_tone_stats(user_id: str, days_back: int = 30):
    """Get user's tone statistics"""
    try:
        user = await user_repo.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get tone statistics
        tone_stats = await tone_repo.get_tone_stats(user_id, days_back)
        
        # Get conversation stats
        conv_stats = await conversation_repo.get_conversation_stats(user_id, days_back)
        
        # Get tone pattern analysis
        pattern_analysis = await vector_ops.analyze_user_tone_patterns(user_id, days_back)
        
        return {
            "user_id": user_id,
            "user_name": user.name,
            "analysis_period_days": days_back,
            "tone_statistics": tone_stats,
            "conversation_statistics": conv_stats,
            "pattern_analysis": pattern_analysis,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "uuid_version": "v7"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error getting tone stats: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get tone stats: {str(e)}")

@app.get("/test-grpc")
async def test_grpc_connection():
    """Test gRPC connection from FastAPI"""
    if not grpc_server_status["running"]:
        return {
            "status": "error",
            "message": "gRPC server is not running",
            "error": grpc_server_status["error"]
        }
    
    try:
        # Test gRPC connection
        channel = grpc.aio.insecure_channel('localhost:50051')
        
        try:
            import health_pb2
            import health_pb2_grpc
        except ImportError:
            return {
                "status": "error", 
                "message": "gRPC modules not found. Generate them first."
            }
        
        stub = health_pb2_grpc.HealthServiceStub(channel)
        request = health_pb2.HealthCheckRequest(service="mcp")
        
        response = await stub.Check(request, timeout=5.0)
        await channel.close()
        
        return {
            "status": "success",
            "message": "gRPC connection successful",
            "grpc_response": {
                "status": response.status,
                "message": response.message
            },
            "test_id": str(uuid7()),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"gRPC connection failed: {str(e)}",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

# Helper functions
async def store_tone_embedding_task(user_id: str, message_text: str, tone_type: str, 
                                   relationship: str, confidence: float, message_id: str):
    """Background task to store tone embedding"""
    try:
        await vector_ops.store_tone_embedding(
            user_id=user_id,
            message_text=message_text,
            tone_type=tone_type,
            relationship=relationship,
            confidence=confidence,
            message_id=message_id
        )
        logger.info(f"✅ Stored tone embedding for message: {message_id}")
    except Exception as e:
        logger.error(f"❌ Failed to store tone embedding: {e}")

def generate_response_by_tone(message_text: str, user: UserProfile, detected_tone: str) -> str:
    """Generate response based on detected tone and user relationship"""
    responses_by_relationship = {
        "romantic": {
            "casual": ["Hey love! 😘", "What's up babe?", "Miss you! 💕"],
            "caring": ["I love you too ❤️", "You mean everything to me 💕", "I'm here for you always 😘"],
            "playful": ["You're so silly! 😄", "Haha you're the best! 🤣", "You always make me smile 😊"]
        },
        "friend": {
            "casual": ["Hey there!", "What's up?", "How's it going?"],
            "playful": ["Haha awesome! 😄", "That's great! 🤣", "You're hilarious! 😂"],
            "caring": ["I'm here for you", "That sounds tough", "Hope you're okay"]
        },
        "family": {
            "formal": ["Thank you for your message.", "I appreciate you.", "How are you?"],
            "caring": ["Love you too!", "Thank you for caring.", "You're amazing."],
            "casual": ["Hey!", "What's up?", "How's everything?"]
        }
    }
    
    # Get appropriate responses
    relationship_key = user.relationship if user.relationship in responses_by_relationship else "friend"
    relationship_responses = responses_by_relationship[relationship_key]
    tone_responses = relationship_responses.get(detected_tone, relationship_responses.get("casual", ["Hello!"]))
    
    # Select response based on message hash for consistency
    response_index = hash(message_text + user.user_id) % len(tone_responses)
    return tone_responses[response_index]

def detect_basic_tone(message_text: str) -> str:
    """Basic tone detection for messages without user context"""
    text_lower = message_text.lower()
    
    if any(word in text_lower for word in ['hello', 'hi', 'hey', '😊', '😄']):
        return "casual"
    elif any(word in text_lower for word in ['thank you', 'please', 'sir', 'madam']):
        return "formal"
    elif any(word in text_lower for word in ['haha', 'lol', '😂', '🤣', 'funny']):
        return "playful"
    elif any(word in text_lower for word in ['love', 'miss', '❤️', '💕', 'care']):
        return "caring"
    else:
        return "casual"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=False,  # Disable reload to prevent gRPC threading issues
        log_level="info",
    )