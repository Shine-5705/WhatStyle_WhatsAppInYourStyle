import asyncio
import grpc
from grpc import aio
import sys
import os
from datetime import datetime, timezone
from uuid6 import uuid7
import time
from typing import Dict, Any, List
import logging

# Add generated directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'generated'))

try:
    import tone_service_pb2
    import tone_service_pb2_grpc
    logger = logging.getLogger(__name__)
    logger.info("✅ Successfully imported Tone service modules")
except ImportError as e:
    logger.error(f"❌ Failed to import Tone modules: {e}")
    sys.exit(1)

# Import repositories and services
from app.db.cassandra.repositories.user_repo import UserRepository, ToneRepository
from app.db.vector.vector_operations import vector_ops
from app.models.tone import ToneAnalysis, ToneEmbedding

class ToneServicer(tone_service_pb2_grpc.ToneServiceServicer):
    """Tone Analysis Service with UUID v7 optimization and vector operations"""
    
    def __init__(self):
        self.user_repo = UserRepository()
        self.tone_repo = ToneRepository()
        self.service_id = str(uuid7())  # UUID v7 for service instance tracking
        self.analysis_count = 0
        self.start_time = datetime.now(timezone.utc)
        
        logger.info(f"🎯 Tone Service initialized with ID: {self.service_id}")
    
    async def AnalyzeTone(self, request, context):
        """Analyze tone of message with comprehensive UUID v7 tracking"""
        analysis_start = time.time()
        analysis_id = str(uuid7())
        self.analysis_count += 1
        
        try:
            logger.info(f"🔍 Analyzing tone (ID: {analysis_id[:8]}) #{self.analysis_count}")
            logger.debug(f"📝 Message: {request.message_text[:100]}...")
            
            # Get user context if provided
            user = None
            if request.user_id:
                user = await self.user_repo.get_user_by_id(request.user_id)
                if not user:
                    logger.warning(f"⚠️ User not found: {request.user_id}")
            
            # Perform comprehensive tone analysis
            tone_analysis = await self._perform_comprehensive_analysis(
                request.message_text,
                user,
                request.context_hint,
                analysis_id
            )
            
            # Store analysis results
            if user:
                await self.tone_repo.save_tone_analysis(
                    user_id=user.user_id,
                    message_id=request.message_id or str(uuid7()),
                    primary_tone=tone_analysis["primary_tone"],
                    confidence_score=tone_analysis["confidence"],
                    tone_features=tone_analysis["tone_features"],
                    emotional_profile=tone_analysis["emotional_profile"],
                    message_text=request.message_text,
                    relationship_context=user.relationship,
                    processing_time_ms=tone_analysis["processing_time_ms"]
                )
            
            # Calculate processing time
            processing_time_ms = (time.time() - analysis_start) * 1000
            
            # Create comprehensive response
            response = tone_service_pb2.ToneAnalysisResponse(
                analysis_id=analysis_id,
                primary_tone=self._map_tone_to_enum(tone_analysis["primary_tone"]),
                confidence_score=tone_analysis["confidence"],
                tone_scores=tone_analysis["tone_scores"],
                emotional_metrics=tone_service_pb2.EmotionalMetrics(
                    valence=tone_analysis["emotional_profile"].get("positivity", 0.5),
                    arousal=tone_analysis["emotional_profile"].get("intensity", 0.5),
                    dominance=tone_analysis["emotional_profile"].get("formality", 0.5)
                ),
                style_features=tone_service_pb2.StyleFeatures(
                    formality_level=tone_analysis["tone_features"].get("formality_level", 0.5),
                    emotional_intensity=tone_analysis["tone_features"].get("emotional_intensity", 0.5),
                    message_length=int(tone_analysis["tone_features"].get("message_length", 0)),
                    emoji_count=int(tone_analysis["tone_features"].get("emoji_count", 0))
                ),
                processing_time_ms=int(processing_time_ms),
                analyzed_at=datetime.now(timezone.utc).isoformat()
            )
            
            logger.info(f"✅ Tone analysis completed (ID: {analysis_id[:8]}) in {processing_time_ms:.2f}ms: {tone_analysis['primary_tone']}")
            return response
            
        except Exception as e:
            logger.error(f"❌ Error in tone analysis (ID: {analysis_id[:8]}): {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Tone analysis failed: {str(e)}")
            raise
    
    async def _perform_comprehensive_analysis(self, message_text: str, user, context_hint: str, analysis_id: str) -> Dict[str, Any]:
        """Perform comprehensive tone analysis using vector similarity and rule-based methods"""
        analysis_start = time.time()
        
        try:
            # Vector-based analysis if user exists
            vector_tone = "casual"
            vector_confidence = 0.5
            
            if user:
                # Try user-specific tone matching
                vector_tone, vector_confidence = await vector_ops.get_best_tone_for_user(
                    user.user_id, message_text, user.relationship
                )
                
                # If confidence is low, try broader relationship matching
                if vector_confidence < 0.7:
                    similar_tones = await vector_ops.find_similar_tones(
                        query_text=message_text,
                        relationship=user.relationship,
                        limit=3,
                        min_similarity=0.6
                    )
                    
                    if similar_tones and similar_tones[0]["similarity"] > 0.6:
                        vector_tone = similar_tones[0]["tone_type"]
                        vector_confidence = similar_tones[0]["similarity"]
            
            # Rule-based analysis for fallback and validation
            rule_based_analysis = self._rule_based_tone_analysis(message_text, context_hint)
            
            # Combine vector and rule-based results
            primary_tone, combined_confidence = self._combine_analysis_results(
                vector_tone, vector_confidence,
                rule_based_analysis["primary_tone"], rule_based_analysis["confidence"]
            )
            
            # Generate comprehensive tone scores
            tone_scores = self._generate_comprehensive_tone_scores(
                message_text, primary_tone, combined_confidence
            )
            
            # Extract detailed features
            tone_features = self._extract_comprehensive_tone_features(message_text)
            emotional_profile = self._analyze_emotional_profile(message_text)
            
            processing_time_ms = (time.time() - analysis_start) * 1000
            
            return {
                "analysis_id": analysis_id,
                "primary_tone": primary_tone,
                "confidence": combined_confidence,
                "tone_scores": tone_scores,
                "tone_features": tone_features,
                "emotional_profile": emotional_profile,
                "processing_time_ms": processing_time_ms,
                "vector_used": user is not None,
                "vector_confidence": vector_confidence,
                "rule_confidence": rule_based_analysis["confidence"]
            }
            
        except Exception as e:
            logger.error(f"❌ Comprehensive analysis failed (ID: {analysis_id[:8]}): {e}")
            # Fallback to basic rule-based analysis
            return self._rule_based_tone_analysis(message_text, context_hint)
    
    def _rule_based_tone_analysis(self, message_text: str, context_hint: str = "") -> Dict[str, Any]:
        """Enhanced rule-based tone analysis"""
        text_lower = message_text.lower()
        context_lower = context_hint.lower() if context_hint else ""
        
        # Define tone patterns with weights
        tone_patterns = {
            "formal": {
                "patterns": ["dear", "sir", "madam", "please", "thank you", "regards", "sincerely", "kindly"],
                "weight": 1.0
            },
            "casual": {
                "patterns": ["hey", "hi", "hello", "what's up", "how's it going", "yeah", "yep"],
                "weight": 1.0
            },
            "playful": {
                "patterns": ["haha", "lol", "😂", "🤣", "funny", "crazy", "awesome", "cool"],
                "weight": 1.2
            },
            "caring": {
                "patterns": ["love", "care", "miss", "❤️", "💕", "worried", "hope", "safe"],
                "weight": 1.1
            },
            "business": {
                "patterns": ["meeting", "project", "deadline", "report", "schedule", "appointment"],
                "weight": 1.0
            },
            "romantic": {
                "patterns": ["baby", "babe", "honey", "sweetheart", "my love", "💕", "😘", "kiss"],
                "weight": 1.3
            }
        }
        
        # Calculate scores for each tone
        tone_scores = {}
        for tone, config in tone_patterns.items():
            score = 0
            for pattern in config["patterns"]:
                if pattern in text_lower or pattern in context_lower:
                    score += config["weight"]
            
            # Normalize score
            tone_scores[tone] = min(1.0, score / len(config["patterns"]))
        
        # Additional contextual analysis
        self._apply_contextual_adjustments(tone_scores, message_text, context_hint)
        
        # Determine primary tone
        primary_tone = max(tone_scores, key=tone_scores.get) if tone_scores else "casual"
        confidence = tone_scores.get(primary_tone, 0.5)
        
        # Ensure minimum confidence
        if confidence < 0.3:
            primary_tone = "casual"
            confidence = 0.5
        
        return {
            "primary_tone": primary_tone,
            "confidence": confidence,
            "tone_scores": tone_scores
        }
    
    def _apply_contextual_adjustments(self, tone_scores: Dict[str, float], message_text: str, context_hint: str):
        """Apply contextual adjustments to tone scores"""
        text_lower = message_text.lower()
        
        # Punctuation and capitalization adjustments
        exclamation_count = message_text.count('!')
        if exclamation_count > 0:
            tone_scores["playful"] = min(1.0, tone_scores.get("playful", 0) + (exclamation_count * 0.1))
        
        caps_ratio = sum(1 for c in message_text if c.isupper()) / len(message_text) if message_text else 0
        if caps_ratio > 0.3:
            tone_scores["business"] = min(1.0, tone_scores.get("business", 0) + 0.2)
        
        # Question patterns
        if "?" in message_text:
            if any(word in text_lower for word in ["how", "what", "when", "where", "why"]):
                tone_scores["formal"] = min(1.0, tone_scores.get("formal", 0) + 0.1)
        
        # Length-based adjustments
        word_count = len(message_text.split())
        if word_count > 20:
            tone_scores["formal"] = min(1.0, tone_scores.get("formal", 0) + 0.1)
        elif word_count < 5:
            tone_scores["casual"] = min(1.0, tone_scores.get("casual", 0) + 0.1)
    
    def _combine_analysis_results(self, vector_tone: str, vector_confidence: float,
                                rule_tone: str, rule_confidence: float) -> tuple:
        """Combine vector and rule-based analysis results"""
        # Weight vector results higher if confidence is good
        if vector_confidence > 0.7:
            primary_tone = vector_tone
            combined_confidence = (vector_confidence * 0.7) + (rule_confidence * 0.3)
        elif rule_confidence > 0.6:
            primary_tone = rule_tone
            combined_confidence = (rule_confidence * 0.7) + (vector_confidence * 0.3)
        else:
            # If both have low confidence, prefer the higher one
            if vector_confidence >= rule_confidence:
                primary_tone = vector_tone
                combined_confidence = vector_confidence
            else:
                primary_tone = rule_tone
                combined_confidence = rule_confidence
        
        return primary_tone, min(1.0, combined_confidence)
    
    def _generate_comprehensive_tone_scores(self, message_text: str, primary_tone: str, confidence: float) -> Dict[str, float]:
        """Generate comprehensive tone scores for all tone types"""
        base_scores = {
            "casual": 0.1,
            "formal": 0.1,
            "playful": 0.1,
            "caring": 0.1,
            "business": 0.1,
            "romantic": 0.1
        }
        
        # Set primary tone confidence
        if primary_tone in base_scores:
            base_scores[primary_tone] = confidence
        
        # Distribute remaining confidence
        remaining = 1.0 - confidence
        other_tones = [t for t in base_scores.keys() if t != primary_tone]
        
        if other_tones:
            per_tone = remaining / len(other_tones)
            for tone in other_tones:
                base_scores[tone] = per_tone
        
        return base_scores
    
    def _extract_comprehensive_tone_features(self, message_text: str) -> Dict[str, float]:
        """Extract comprehensive tone features"""
        features = {
            "message_length": len(message_text),
            "word_count": len(message_text.split()),
            "exclamation_count": message_text.count('!'),
            "question_count": message_text.count('?'),
            "emoji_count": len([c for c in message_text if ord(c) > 127]),
            "caps_ratio": sum(1 for c in message_text if c.isupper()) / len(message_text) if message_text else 0,
            "punctuation_density": len([c for c in message_text if c in '.,!?;:']) / len(message_text) if message_text else 0,
            "avg_word_length": sum(len(word) for word in message_text.split()) / len(message_text.split()) if message_text.split() else 0,
            "formality_level": self._calculate_formality_level(message_text),
            "emotional_intensity": self._calculate_emotional_intensity(message_text)
        }
        return features
    
    def _analyze_emotional_profile(self, message_text: str) -> Dict[str, float]:
        """Analyze emotional profile with detailed metrics"""
        # Emotion word dictionaries
        positive_words = ['great', 'awesome', 'good', 'happy', 'love', 'amazing', 'wonderful', 'excellent', 'fantastic', 'perfect']
        negative_words = ['bad', 'terrible', 'hate', 'sad', 'angry', 'frustrated', 'disappointed', 'awful', 'horrible', 'upset']
        excitement_words = ['wow', 'amazing', 'incredible', 'fantastic', 'awesome', '!', '!!!']
        calm_words = ['peaceful', 'calm', 'relaxed', 'gentle', 'quiet', 'serene']
        
        text_lower = message_text.lower()
        
        # Count emotional indicators
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        excitement_count = sum(1 for word in excitement_words if word in text_lower)
        calm_count = sum(1 for word in calm_words if word in text_lower)
        
        # Calculate metrics
        total_emotional_words = positive_count + negative_count + excitement_count + calm_count
        
        profile = {
            "positivity": min(1.0, positive_count * 0.3) if positive_count > 0 else 0.0,
            "negativity": min(1.0, negative_count * 0.3) if negative_count > 0 else 0.0,
            "excitement": min(1.0, excitement_count * 0.2) if excitement_count > 0 else 0.0,
            "calmness": min(1.0, calm_count * 0.3) if calm_count > 0 else 0.0,
            "neutrality": max(0.0, 1.0 - min(1.0, total_emotional_words * 0.2)),
            "intensity": self._calculate_emotional_intensity(message_text),
            "formality": self._calculate_formality_level(message_text)
        }
        
        return profile
    
    def _calculate_emotional_intensity(self, message_text: str) -> float:
        """Calculate emotional intensity (0.0 to 1.0)"""
        intensity_indicators = ['!', '!!!', '😍', '😭', '😂', '❤️', '💕', '🔥', 'AMAZING', 'TERRIBLE', 'LOVE', 'HATE']
        
        count = sum(1 for indicator in intensity_indicators if indicator in message_text)
        exclamation_count = message_text.count('!')
        caps_ratio = sum(1 for c in message_text if c.isupper()) / len(message_text) if message_text else 0
        
        intensity = min(1.0, (count * 0.2) + (exclamation_count * 0.1) + (caps_ratio * 0.5))
        return max(0.1, intensity)
    
    def _calculate_formality_level(self, message_text: str) -> float:
        """Calculate formality level (0.0 = informal, 1.0 = formal)"""
        formal_indicators = ['please', 'thank you', 'sir', 'madam', 'kindly', 'regards', 'sincerely', 'hereby', 'furthermore']
        informal_indicators = ['yeah', 'yep', 'nah', 'gonna', 'wanna', 'lol', 'haha', '😂', '👍', 'sup', 'dude']
        
        text_lower = message_text.lower()
        formal_count = sum(1 for word in formal_indicators if word in text_lower)
        informal_count = sum(1 for word in informal_indicators if word in text_lower)
        
        if formal_count > informal_count:
            return min(1.0, 0.5 + (formal_count * 0.1))
        elif informal_count > formal_count:
            return max(0.0, 0.5 - (informal_count * 0.1))
        else:
            return 0.5
    
    def _map_tone_to_enum(self, tone_str: str):
        """Map string tone to protobuf enum"""
        tone_map = {
            "casual": tone_service_pb2.TONE_CASUAL,
            "formal": tone_service_pb2.TONE_FORMAL,
            "playful": tone_service_pb2.TONE_PLAYFUL,
            "caring": tone_service_pb2.TONE_CARING,
            "business": tone_service_pb2.TONE_BUSINESS,
            "romantic": tone_service_pb2.TONE_CASUAL  # Map to casual if romantic not available
        }
        return tone_map.get(tone_str, tone_service_pb2.TONE_CASUAL)
    
    async def GetUserToneProfile(self, request, context):
        """Get comprehensive user tone profile with UUID v7 tracking"""
        try:
            profile_request_id = str(uuid7())
            logger.info(f"👤 Getting tone profile (ID: {profile_request_id[:8]}) for user: {request.user_id}")
            
            user = await self.user_repo.get_user_by_id(request.user_id)
            if not user:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("User not found")
                return tone_service_pb2.UserToneProfileResponse()
            
            # Get tone statistics
            tone_stats = await self.tone_repo.get_tone_stats(
                request.user_id, 
                days_back=request.days_back or 30
            )
            
            # Get tone pattern analysis
            tone_patterns = await vector_ops.analyze_user_tone_patterns(
                request.user_id,
                days_back=request.days_back or 30
            )
            
            # Create comprehensive profile response
            tone_distribution = {}
            for tone, count in tone_stats.get("tone_distribution", {}).items():
                if tone in ["casual", "formal", "playful", "caring", "business"]:
                    tone_distribution[tone] = float(count)
            
            response = tone_service_pb2.UserToneProfileResponse(
                profile_id=profile_request_id,
                user_id=str(user.user_id),
                dominant_tone=self._map_tone_to_enum(tone_stats.get("dominant_tone", "casual")),
                tone_distribution=tone_distribution,
                average_confidence=tone_stats.get("average_confidence", 0.5),
                total_analyses=tone_stats.get("total_analyses", 0),
                relationship_context=user.relationship,
                analysis_period_days=request.days_back or 30,
                profile_generated_at=datetime.now(timezone.utc).isoformat()
            )
            
            logger.info(f"✅ Tone profile generated (ID: {profile_request_id[:8]})")
            return response
            
        except Exception as e:
            logger.error(f"❌ Error getting tone profile: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Profile retrieval failed: {str(e)}")
            raise
    
    async def GetSimilarTones(self, request, context):
        """Find similar tone patterns using vector search"""
        try:
            search_id = str(uuid7())
            logger.info(f"🔍 Finding similar tones (ID: {search_id[:8]}) for: {request.query_text[:50]}...")
            
            similar_tones = await vector_ops.find_similar_tones(
                query_text=request.query_text,
                relationship=request.relationship_filter if request.relationship_filter else None,
                user_id=request.user_id if request.user_id else None,
                limit=request.limit or 5,
                min_similarity=request.min_similarity or 0.6
            )
            
            # Convert to protobuf response
            tone_matches = []
            for tone_data in similar_tones:
                match = tone_service_pb2.ToneMatch(
                    embedding_id=tone_data["embedding_id"],
                    tone_type=self._map_tone_to_enum(tone_data["tone_type"]),
                    message_sample=tone_data["message_sample"],
                    similarity_score=tone_data["similarity"],
                    confidence_score=tone_data["confidence"],
                    relationship_context=tone_data["relationship"],
                    created_at=tone_data["created_at"]
                )
                tone_matches.append(match)
            
            response = tone_service_pb2.SimilarTonesResponse(
                search_id=search_id,
                matches=tone_matches,
                total_found=len(tone_matches),
                search_performed_at=datetime.now(timezone.utc).isoformat()
            )
            
            logger.info(f"✅ Found {len(tone_matches)} similar tones (ID: {search_id[:8]})")
            return response
            
        except Exception as e:
            logger.error(f"❌ Error finding similar tones: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Similar tones search failed: {str(e)}")
            raise
    
    async def HealthCheck(self, request, context):
        """Health check for tone service"""
        try:
            health_check_id = str(uuid7())
            
            # Check vector operations
            vector_info = vector_ops.get_operation_info()
            vector_healthy = vector_info.get("model_loaded", False)
            
            # Check database connectivity
            try:
                # Simple database check
                await self.user_repo.get_collection()
                db_healthy = True
            except Exception:
                db_healthy = False
            
            # Determine status
            if vector_healthy and db_healthy:
                status = tone_service_pb2.HEALTH_STATUS_HEALTHY
                message = "Tone service is fully operational"
            elif db_healthy:
                status = tone_service_pb2.HEALTH_STATUS_DEGRADED
                message = "Tone service operational but vector operations limited"
            else:
                status = tone_service_pb2.HEALTH_STATUS_UNHEALTHY
                message = "Tone service has connectivity issues"
            
            # Service metrics
            uptime_seconds = (datetime.now(timezone.utc) - self.start_time).total_seconds()
            
            details = {
                "service_id": self.service_id,
                "health_check_id": health_check_id,
                "vector_operations": "healthy" if vector_healthy else "unhealthy",
                "database": "connected" if db_healthy else "disconnected",
                "total_analyses": self.analysis_count,
                "uptime_seconds": uptime_seconds,
                "analyses_per_minute": (self.analysis_count / max(1, uptime_seconds)) * 60,
                "vector_dimension": vector_info.get("vector_dimension", 0),
                "uuid_version": "v7"
            }
            
            return tone_service_pb2.ToneHealthResponse(
                status=status,
                message=f"{message} (ID: {self.service_id[:8]})",
                details=details,
                timestamp=datetime.now(timezone.utc).isoformat()
            )
            
        except Exception as e:
            return tone_service_pb2.ToneHealthResponse(
                status=tone_service_pb2.HEALTH_STATUS_UNHEALTHY,
                message=f"Health check failed: {str(e)}",
                timestamp=datetime.now(timezone.utc).isoformat()
            )

async def serve_tone_service():
    """Start the Tone Analysis gRPC server"""
    server_id = str(uuid7())
    logger.info(f"🎯 Starting Tone Analysis gRPC Server with ID: {server_id}")
    
    server = aio.server()
    
    # Add Tone service
    tone_servicer = ToneServicer()
    tone_service_pb2_grpc.add_ToneServiceServicer_to_server(tone_servicer, server)
    
    # Configure server address
    listen_addr = '[::]:50053'
    server.add_insecure_port(listen_addr)
    
    logger.info(f"🚀 Starting Tone Analysis Server on {listen_addr}")
    await server.start()
    
    logger.info("✅ Tone Analysis server started successfully!")
    logger.info("📋 Available services:")
    logger.info("   - tone.ToneService/AnalyzeTone")
    logger.info("   - tone.ToneService/GetUserToneProfile")
    logger.info("   - tone.ToneService/GetSimilarTones")
    logger.info("   - tone.ToneService/HealthCheck")
    logger.info(f"🆔 Server ID: {server_id}")
    
    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info(f"\n🛑 Shutting down Tone Analysis server (ID: {server_id[:8]})...")
        await server.stop(5)
        logger.info("✅ Tone Analysis server shutdown complete")

if __name__ == '__main__':
    asyncio.run(serve_tone_service())