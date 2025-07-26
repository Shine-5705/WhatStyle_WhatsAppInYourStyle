import asyncio
from typing import Any, Dict, List, Tuple
import grpc
from grpc import aio
from grpc_reflection.v1alpha import reflection
import sys
import os
from datetime import datetime, timezone
from uuid6 import uuid7
import json
import time
import logging

# Add generated directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'generated'))

try:
    import mcp_service_pb2
    import mcp_service_pb2_grpc
    logger = logging.getLogger(__name__)
    logger.info("✅ Successfully imported MCP service modules")
except ImportError as e:
    logger.error(f"❌ Failed to import MCP modules: {e}")
    sys.exit(1)

# Import repositories
from app.db.cassandra.repositories.user_repo import UserRepository, ConversationRepository, ToneRepository
from app.db.cassandra.connection import datastax_connection
from app.db.vector.vector_operations import vector_ops

class MCPServicer(mcp_service_pb2_grpc.MCPServiceServicer):
    """MCP Service with UUID v7 optimization and enhanced vector operations"""
    
    def __init__(self):
        self.user_repo = UserRepository()
        self.conversation_repo = ConversationRepository()
        self.tone_repo = ToneRepository()
        self.service_id = str(uuid7())  # UUID v7 for service instance tracking
        self.request_count = 0
        self.start_time = datetime.now(timezone.utc)
        
        logger.info(f"🤖 MCP Service initialized with ID: {self.service_id}")
    
    async def ProcessMessage(self, request, context):
        """Process incoming WhatsApp message with comprehensive UUID v7 tracking"""
        processing_start = time.time()
        processing_id = str(uuid7())
        self.request_count += 1
        
        try:
            logger.info(f"🔍 Processing message (ID: {processing_id[:8]}) #{self.request_count} from: {request.sender_phone}")
            
            # Get or create user profile
            user = await self.user_repo.get_user_by_phone(request.sender_phone)
            if not user:
                logger.info(f"👤 Creating new user for: {request.sender_phone}")
                user = await self.user_repo.create_user(
                    phone_number=request.sender_phone,
                    name=request.sender_name or "Unknown User",
                    relationship=self._detect_relationship_from_context(request)
                )
            
            # Record interaction with enhanced tracking
            await self.user_repo.record_interaction(user.user_id, "whatsapp_message")
            
            # Advanced tone detection using vector similarity
            detected_tone, tone_confidence = await self._detect_advanced_tone(
                request.message_text, user, processing_id
            )
            
            # Generate conversation ID with UUID v7
            conversation_id = str(uuid7())
            
            # Save message to conversation history with enhanced metadata
            message = await self.conversation_repo.save_message(
                user_id=user.user_id,
                conversation_id=conversation_id,
                message_text=request.message_text,
                sender="user",
                detected_tone=detected_tone,
                tone_confidence=tone_confidence,
                message_type="text",
                context_data={
                    "processing_id": processing_id,
                    "request_number": self.request_count,
                    "sender_phone": request.sender_phone,
                    "received_at": datetime.now(timezone.utc).isoformat()
                }
            )
            
            # Store comprehensive tone embedding for future similarity matching
            await vector_ops.store_tone_embedding(
                user_id=user.user_id,
                message_text=request.message_text,
                tone_type=detected_tone,
                relationship=user.relationship,
                confidence=tone_confidence,
                message_id=message.message_id,
                emotional_intensity=self._calculate_emotional_intensity(request.message_text),
                formality_level=self._calculate_formality_level(request.message_text)
            )
            
            # Generate intelligent response based on user profile and similar patterns
            response_text = await self._generate_smart_response(
                request.message_text, user, detected_tone, processing_id
            )
            
            # Save bot response with tracking
            bot_message = await self.conversation_repo.save_message(
                user_id=user.user_id,
                conversation_id=conversation_id,
                message_text=response_text,
                sender="bot",
                detected_tone=user.primary_tone,
                context_data={
                    "processing_id": processing_id,
                    "response_generated_at": datetime.now(timezone.utc).isoformat(),
                    "original_message_id": message.message_id
                }
            )
            
            # Store response embedding for learning
            await vector_ops.store_message_embedding(
                message_id=bot_message.message_id,
                user_id=user.user_id,
                conversation_id=conversation_id,
                message_text=response_text,
                detected_tone=user.primary_tone,
                sentiment_score=0.8,
                emotional_score=0.7,
                formality_score=self._calculate_formality_level(response_text)
            )
            
            # Calculate processing time
            processing_time_ms = (time.time() - processing_start) * 1000
            
            # Save detailed tone analysis
            await self.tone_repo.save_tone_analysis(
                user_id=user.user_id,
                message_id=message.message_id,
                primary_tone=detected_tone,
                confidence_score=tone_confidence,
                tone_features=self._extract_tone_features(request.message_text),
                emotional_profile=self._analyze_emotional_profile(request.message_text),
                message_text=request.message_text[:100],  # Truncated for storage
                relationship_context=user.relationship,
                processing_time_ms=processing_time_ms
            )
            
            # Create comprehensive response with UUID v7 tracking
            processing_metadata = mcp_service_pb2.ProcessingMetadata(
                processing_time_ms=int(processing_time_ms),
                model_used="advanced_vector_tone_detector_v2",
                tone_profile_id=str(user.user_id),
                tone_scores=self._get_tone_scores_dict(detected_tone, tone_confidence)
            )
            
            response = mcp_service_pb2.MessageResponse(
                response_id=str(uuid7()),  # UUID v7 for response tracking
                response_text=response_text,
                applied_tone=self._map_tone_to_enum(user.primary_tone),
                confidence_score=tone_confidence,
                generated_at=datetime.now(timezone.utc).isoformat(),
                processing_info=processing_metadata
            )
            
            logger.info(f"✅ Generated response (ID: {processing_id[:8]}) in {processing_time_ms:.2f}ms: {response_text}")
            return response
            
        except Exception as e:
            logger.error(f"❌ Error processing message (ID: {processing_id[:8]}): {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Processing failed: {str(e)}")
            raise
    
    async def _detect_advanced_tone(self, message_text: str, user, processing_id: str) -> Tuple[str, float]:
        """Advanced tone detection using vector similarity with confidence scoring"""
        try:
            # First try user-specific tone matching
            best_tone, confidence = await vector_ops.get_best_tone_for_user(
                user.user_id, message_text, user.relationship
            )
            
            # If confidence is low, try relationship-based matching
            if confidence < 0.7:
                similar_tones = await vector_ops.find_similar_tones(
                    query_text=message_text,
                    relationship=user.relationship,
                    limit=3,
                    min_similarity=0.6
                )
                
                if similar_tones and similar_tones[0]["similarity"] > 0.6:
                    best_tone = similar_tones[0]["tone_type"]
                    confidence = similar_tones[0]["similarity"]
                    logger.info(f"🎯 Relationship-based tone match: {best_tone} (conf: {confidence:.3f})")
                else:
                    # Fallback to enhanced rule-based detection
                    best_tone = self._detect_enhanced_tone(message_text, user)
                    confidence = 0.6  # Moderate confidence for rule-based
                    logger.info(f"🎯 Rule-based tone detection: {best_tone}")
            else:
                logger.info(f"🎯 User-specific tone match: {best_tone} (conf: {confidence:.3f})")
            
            return best_tone, confidence
            
        except Exception as e:
            logger.error(f"❌ Advanced tone detection failed (ID: {processing_id[:8]}): {e}")
            return self._detect_enhanced_tone(message_text, user), 0.5
    
    def _detect_enhanced_tone(self, message_text: str, user) -> str:
        """Enhanced rule-based tone detection with user context"""
        text_lower = message_text.lower()
        
        # Relationship-specific patterns
        if user.relationship == "girlfriend" or user.relationship == "boyfriend":
            if any(word in text_lower for word in ['love', 'miss', 'baby', 'babe', '❤️', '💕', '😘']):
                return "romantic"
            elif any(word in text_lower for word in ['cute', 'adorable', 'sweet', '😊', '🥰']):
                return "caring"
        
        elif user.relationship == "father" or user.relationship == "mother":
            if any(word in text_lower for word in ['thank you', 'thanks', 'grateful', 'appreciate']):
                return "formal"
            elif any(word in text_lower for word in ['dad', 'mom', 'papa', 'mama']):
                return "caring"
        
        elif user.relationship == "friend" or user.relationship == "brother" or user.relationship == "sister":
            if any(word in text_lower for word in ['haha', 'lol', '😂', '🤣', 'funny', 'crazy']):
                return "playful"
            elif any(word in text_lower for word in ['bro', 'dude', 'man', 'hey']):
                return "casual"
        
        # General patterns
        if any(word in text_lower for word in ['meeting', 'project', 'work', 'business', 'appointment']):
            return "business"
        elif any(word in text_lower for word in ['hello', 'hi', 'hey', 'what\'s up']):
            return "casual"
        elif any(word in text_lower for word in ['good morning', 'good afternoon', 'sir', 'madam']):
            return "formal"
        else:
            return user.primary_tone or "casual"
    
    def _detect_relationship_from_context(self, request) -> str:
        """Detect relationship from message context"""
        # This could be enhanced with ML models in the future
        message_lower = request.message_text.lower()
        
        if any(word in message_lower for word in ['love', 'baby', 'babe', 'honey']):
            return "romantic"
        elif any(word in message_lower for word in ['dad', 'father', 'papa']):
            return "father"
        elif any(word in message_lower for word in ['mom', 'mother', 'mama']):
            return "mother"
        elif any(word in message_lower for word in ['bro', 'brother']):
            return "brother"
        elif any(word in message_lower for word in ['sis', 'sister']):
            return "sister"
        elif any(word in message_lower for word in ['work', 'office', 'meeting']):
            return "business"
        else:
            return "friend"  # Default assumption
    
    def _calculate_emotional_intensity(self, message_text: str) -> float:
        """Calculate emotional intensity of message (0.0 to 1.0)"""
        # Simple heuristic - could be enhanced with sentiment analysis models
        intensity_indicators = ['!', '!!!', '😍', '😭', '😂', '❤️', '💕', '🔥', 'amazing', 'terrible', 'love', 'hate']
        
        count = sum(1 for indicator in intensity_indicators if indicator in message_text.lower())
        exclamation_count = message_text.count('!')
        caps_ratio = sum(1 for c in message_text if c.isupper()) / len(message_text) if message_text else 0
        
        intensity = min(1.0, (count * 0.2) + (exclamation_count * 0.1) + (caps_ratio * 0.5))
        return max(0.1, intensity)  # Minimum intensity
    
    def _calculate_formality_level(self, message_text: str) -> float:
        """Calculate formality level of message (0.0 = informal, 1.0 = formal)"""
        formal_indicators = ['please', 'thank you', 'sir', 'madam', 'kindly', 'regards', 'sincerely']
        informal_indicators = ['yeah', 'yep', 'nah', 'gonna', 'wanna', 'lol', 'haha', '😂', '👍']
        
        formal_count = sum(1 for word in formal_indicators if word in message_text.lower())
        informal_count = sum(1 for word in informal_indicators if word in message_text.lower())
        
        if formal_count > informal_count:
            return min(1.0, 0.5 + (formal_count * 0.1))
        elif informal_count > formal_count:
            return max(0.0, 0.5 - (informal_count * 0.1))
        else:
            return 0.5  # Neutral
    
    def _extract_tone_features(self, message_text: str) -> Dict[str, float]:
        """Extract comprehensive tone features from message"""
        return {
            "message_length": len(message_text),
            "exclamation_count": message_text.count('!'),
            "question_count": message_text.count('?'),
            "emoji_count": len([c for c in message_text if ord(c) > 127]),
            "caps_ratio": sum(1 for c in message_text if c.isupper()) / len(message_text) if message_text else 0,
            "word_count": len(message_text.split()),
            "avg_word_length": sum(len(word) for word in message_text.split()) / len(message_text.split()) if message_text.split() else 0,
            "punctuation_density": len([c for c in message_text if c in '.,!?;:']) / len(message_text) if message_text else 0
        }
    
    def _analyze_emotional_profile(self, message_text: str) -> Dict[str, float]:
        """Analyze emotional profile of message"""
        positive_words = ['great', 'awesome', 'good', 'happy', 'love', 'amazing', 'wonderful', 'excellent']
        negative_words = ['bad', 'terrible', 'hate', 'sad', 'angry', 'frustrated', 'disappointed', 'awful']
        
        text_lower = message_text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        return {
            "positivity": min(1.0, positive_count * 0.3),
            "negativity": min(1.0, negative_count * 0.3),
            "neutrality": 1.0 - min(1.0, (positive_count + negative_count) * 0.2),
            "intensity": self._calculate_emotional_intensity(message_text),
            "formality": self._calculate_formality_level(message_text)
        }
    
    async def _generate_smart_response(self, message_text: str, user, detected_tone: str, processing_id: str) -> str:
        """Generate intelligent response using similarity patterns and user history"""
        try:
            # Find similar messages from this user or relationship
            similar_patterns = await vector_ops.find_similar_tones(
                query_text=message_text,
                user_id=user.user_id,
                limit=3,
                min_similarity=0.7
            )
            
            # Get recent conversation context
            recent_messages = await self.conversation_repo.get_conversation_history(
                user_id=user.user_id,
                limit=5
            )
            
            # Base response generation with context awareness
            response_text = self._generate_contextual_response(
                message_text, user, detected_tone, recent_messages
            )
            
            # Enhance response based on similar successful patterns
            if similar_patterns and similar_patterns[0]["similarity"] > 0.8:
                pattern = similar_patterns[0]
                logger.info(f"🔗 Using similar pattern (ID: {processing_id[:8]}): {pattern['message_sample'][:50]}...")
                # Could enhance response based on successful past patterns
                response_text = self._enhance_response_with_pattern(response_text, pattern)
            
            return response_text
            
        except Exception as e:
            logger.error(f"❌ Smart response generation failed (ID: {processing_id[:8]}): {e}")
            return self._generate_contextual_response(message_text, user, detected_tone, [])
    
    def _generate_contextual_response(self, message_text: str, user, detected_tone: str, 
                                    recent_messages: List) -> str:
        """Generate response with conversation context"""
        # Check if this is a continuation of previous conversation
        is_continuation = len(recent_messages) > 0 and \
                         recent_messages[0].timestamp and \
                         (datetime.now(timezone.utc) - datetime.fromisoformat(recent_messages[0].timestamp.replace('Z', '+00:00'))).seconds < 3600
        
        # Enhanced responses by relationship and tone
        responses_by_relationship = {
            "romantic": {
                "casual": ["Hey love! 😘", "What's up babe?", "Miss you! 💕"],
                "caring": ["I love you too ❤️", "You mean everything to me 💕", "I'm here for you always 😘"],
                "playful": ["You're so silly! 😄", "Haha you're the best! 🤣", "You always make me smile 😊"],
                "romantic": ["My heart is yours ❤️", "You're my everything 💕", "I can't wait to see you 😘"]
            },
            "father": {
                "formal": ["Thank you, Dad.", "I appreciate your guidance.", "How are you doing, Dad?"],
                "caring": ["I love you too, Dad.", "Thank you for everything.", "You're the best father."],
                "casual": ["Hey Dad!", "What's up?", "How's everything?"]
            },
            "mother": {
                "formal": ["Thank you, Mom.", "I appreciate you.", "How are you, Mom?"],
                "caring": ["I love you too, Mom.", "Thank you for caring.", "You're amazing, Mom."],
                "casual": ["Hey Mom!", "What's up?", "How's your day?"]
            },
            "brother": {
                "casual": ["What's up bro!", "Hey dude!", "Yo! How's it going?"],
                "playful": ["Haha nice one!", "You're crazy man! 😂", "That's hilarious! 🤣"],
                "business": ["Sure thing.", "Let me know.", "Sounds good."]
            },
            "sister": {
                "casual": ["Hey sis!", "What's up girl!", "How are you?"],
                "playful": ["Haha love it! 😄", "You're the best! 🤣", "So funny! 😂"],
                "caring": ["Love you sis ❤️", "I'm here for you", "You got this! 💪"]
            },
            "friend": {
                "casual": ["Hey there!", "What's up?", "How's it going?"],
                "playful": ["Haha awesome! 😄", "That's great! 🤣", "You're hilarious! 😂"],
                "business": ["Sounds good.", "Let me know.", "Sure thing."]
            },
            "business": {
                "formal": ["Thank you for your message.", "I appreciate your inquiry.", "How may I assist you?"],
                "business": ["I'll look into that.", "Let me get back to you.", "That sounds feasible."],
                "casual": ["Thanks for reaching out.", "Got it.", "Sounds good."]
            }
        }
        
        # Get appropriate responses
        relationship_key = user.relationship if user.relationship in responses_by_relationship else "friend"
        relationship_responses = responses_by_relationship[relationship_key]
        tone_responses = relationship_responses.get(detected_tone, relationship_responses.get("casual", ["Hello!"]))
        
        # Add continuation context if applicable
        if is_continuation and recent_messages:
            last_message = recent_messages[0]
            if last_message.sender == "user":
                # Add contextual awareness
                if "?" in message_text:
                    tone_responses = [r + " What would you like to know?" for r in tone_responses[:1]]
                elif "thanks" in message_text.lower():
                    tone_responses = ["You're welcome! 😊", "Anytime!", "Happy to help!"]
        
        # Select response based on message hash for consistency
        response_index = hash(message_text + user.user_id) % len(tone_responses)
        return tone_responses[response_index]
    
    def _enhance_response_with_pattern(self, base_response: str, pattern: Dict[str, Any]) -> str:
        """Enhance response based on successful pattern"""
        # Simple enhancement - could be more sophisticated
        if pattern["confidence"] > 0.9:
            # High confidence pattern - add enthusiasm
            if not any(emoji in base_response for emoji in ['😊', '😄', '🤣', '❤️', '💕']):
                if pattern["tone_type"] == "playful":
                    base_response += " 😄"
                elif pattern["tone_type"] == "caring":
                    base_response += " ❤️"
                elif pattern["tone_type"] == "casual":
                    base_response += " 😊"
        
        return base_response
    
    def _get_tone_scores_dict(self, detected_tone: str, confidence: float) -> Dict[str, float]:
        """Get tone scores dictionary for protobuf"""
        scores = {
            "casual": 0.1,
            "formal": 0.1,
            "playful": 0.1,
            "caring": 0.1,
            "business": 0.1,
            "romantic": 0.1
        }
        
        # Set the detected tone confidence
        if detected_tone in scores:
            scores[detected_tone] = confidence
            
        # Distribute remaining confidence among other tones
        remaining = 1.0 - confidence
        other_tones = [t for t in scores.keys() if t != detected_tone]
        if other_tones:
            per_tone = remaining / len(other_tones)
            for tone in other_tones:
                scores[tone] = per_tone
        
        return scores
    
    def _map_tone_to_enum(self, tone_str: str):
        """Map string tone to protobuf enum"""
        tone_map = {
            "casual": mcp_service_pb2.TONE_TYPE_CASUAL,
            "formal": mcp_service_pb2.TONE_TYPE_FORMAL,
            "playful": mcp_service_pb2.TONE_TYPE_PLAYFUL,
            "caring": mcp_service_pb2.TONE_TYPE_CARING,
            "business": mcp_service_pb2.TONE_TYPE_BUSINESS,
            "romantic": mcp_service_pb2.TONE_TYPE_CASUAL  # Map romantic to casual if not available
        }
        return tone_map.get(tone_str, mcp_service_pb2.TONE_TYPE_CASUAL)
    
    async def GetContext(self, request, context):
        """Get conversation context with comprehensive UUID v7 support"""
        try:
            context_id = str(uuid7())
            logger.info(f"📋 Getting context (ID: {context_id[:8]}) for conversation: {request.conversation_id}")
            
            user = await self.user_repo.get_user_by_id(request.user_id)
            if not user:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("User not found")
                return mcp_service_pb2.ContextResponse()
            
            # Get conversation history with enhanced metadata
            conversations = await self.conversation_repo.get_conversation_history(
                user_id=request.user_id,
                limit=request.message_limit or 10,
                conversation_id=request.conversation_id if request.conversation_id else None
            )
            
            # Get user's tone statistics
            tone_stats = await self.tone_repo.get_tone_stats(request.user_id, days_back=7)
            
            context_messages = []
            for conv in conversations:
                msg = mcp_service_pb2.ContextMessage(
                    message_id=str(conv.message_id),
                    sender_id=conv.sender,
                    content=conv.message_text,
                    type=mcp_service_pb2.MESSAGE_TYPE_TEXT,
                    detected_tone=self._map_tone_to_enum(conv.detected_tone or "casual"),
                    timestamp=conv.timestamp
                )
                context_messages.append(msg)
            
            # Enhanced user profile with tone information
            user_profile = mcp_service_pb2.UserProfile(
                user_id=str(user.user_id),
                phone_number=user.phone_number,
                name=user.name,
                relationship=user.relationship
            )
            
            response = mcp_service_pb2.ContextResponse(
                conversation_id=request.conversation_id or str(uuid7()),
                messages=context_messages,
                user_profile=user_profile,
                state=mcp_service_pb2.CONVERSATION_STATE_ACTIVE
            )
            
            logger.info(f"✅ Context retrieved (ID: {context_id[:8]}): {len(context_messages)} messages")
            return response
            
        except Exception as e:
            logger.error(f"❌ Error getting context: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Context retrieval failed: {str(e)}")
            raise
    
    async def HealthCheck(self, request, context):
        """Comprehensive health check with service UUID v7 tracking"""
        try:
            health_check_id = str(uuid7())
            
            # Check database connectivity
            db_healthy = datastax_connection.is_connected()
            db_health = datastax_connection.health_check() if db_healthy else {"status": "unhealthy"}
            
            # Check vector operations
            vector_healthy = vector_ops.get_operation_info()
            
            # Determine overall status
            if db_healthy and vector_healthy.get("model_loaded", False):
                status = mcp_service_pb2.HEALTH_STATUS_HEALTHY
                message = "MCP Service is fully operational"
            elif db_healthy:
                status = mcp_service_pb2.HEALTH_STATUS_DEGRADED
                message = "MCP Service is operational but vector operations may be limited"
            else:
                status = mcp_service_pb2.HEALTH_STATUS_UNHEALTHY
                message = "MCP Service has connectivity issues"
            
            # Comprehensive health details
            uptime_seconds = (datetime.now(timezone.utc) - self.start_time).total_seconds()
            
            details = {
                "database": "connected" if db_healthy else "disconnected",
                "vector_operations": "operational" if vector_healthy.get("model_loaded") else "limited",
                "service": "mcp_service",
                "service_id": self.service_id,
                "health_check_id": health_check_id,
                "version": "2.0.0",
                "uuid_version": "v7",
                "uptime_seconds": uptime_seconds,
                "total_requests": self.request_count,
                "requests_per_minute": (self.request_count / max(1, uptime_seconds)) * 60,
                "database_collections": len(datastax_connection.collections) if db_healthy else 0,
                "vector_dimension": vector_healthy.get("vector_dimension", 0)
            }
            
            return mcp_service_pb2.HealthResponse(
                status=status,
                message=f"{message} (ID: {self.service_id[:8]})",
                details=details,
                timestamp=datetime.now(timezone.utc).isoformat()
            )
            
        except Exception as e:
            return mcp_service_pb2.HealthResponse(
                status=mcp_service_pb2.HEALTH_STATUS_UNHEALTHY,
                message=f"Health check failed: {str(e)}",
                timestamp=datetime.now(timezone.utc).isoformat()
            )

async def serve():
    """Start the MCP gRPC server with comprehensive UUID v7 support"""
    server_id = str(uuid7())
    logger.info(f"🚀 Starting MCP gRPC Server with ID: {server_id}")
    
    # Initialize database connection with retry logic
    try:
        datastax_connection.connect()
        logger.info("✅ DataStax connection established")
        
        # Initialize vector operations
        vector_info = vector_ops.get_operation_info()
        logger.info(f"🤖 Vector operations initialized: {vector_info}")
        
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        logger.warning("⚠️ Continuing without database (some features will be limited)")
    
    server = aio.server()
    
    # Add MCP service
    mcp_servicer = MCPServicer()
    mcp_service_pb2_grpc.add_MCPServiceServicer_to_server(mcp_servicer, server)
    
    # Add reflection support for debugging
    SERVICE_NAMES = (
        mcp_service_pb2.DESCRIPTOR.services_by_name['MCPService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    
    # Configure server address
    listen_addr = '[::]:50052'
    server.add_insecure_port(listen_addr)
    
    logger.info(f"🚀 Starting MCP gRPC Server on {listen_addr}")
    await server.start()
    
    logger.info("✅ MCP server started successfully!")
    logger.info("📋 Available services:")
    logger.info("   - mcp.MCPService/ProcessMessage (Enhanced with UUID v7)")
    logger.info("   - mcp.MCPService/GetContext (With comprehensive tracking)")
    logger.info("   - mcp.MCPService/HealthCheck (Full system monitoring)")
    logger.info(f"🆔 Server ID: {server_id}")
    logger.info(f"🔤 Vector Operations ID: {vector_ops.operation_id}")
    
    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info(f"\n🛑 Shutting down MCP server (ID: {server_id[:8]})...")
        datastax_connection.disconnect()
        await server.stop(5)
        logger.info("✅ MCP server shutdown complete")

if __name__ == '__main__':
    asyncio.run(serve())