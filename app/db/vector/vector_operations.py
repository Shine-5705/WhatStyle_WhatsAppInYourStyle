from typing import List, Tuple, Optional, Dict, Any
import numpy as np
from sentence_transformers import SentenceTransformer
from app.models.tone import ToneEmbedding, MessageEmbedding, ToneAnalysis
from app.models.user import UserProfile
from app.db.cassandra.connection import datastax_connection
from uuid6 import uuid7
from datetime import datetime, timezone
import logging
import time

logger = logging.getLogger(__name__)

class VectorOperations:
    """Vector operations for tone and message embeddings with UUID v7 optimization"""
    
    def __init__(self):
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.vector_dim = 384
        self.tone_collection = None
        self.message_collection = None
        self.analysis_collection = None
        self.operation_id = str(uuid7())
        self._model_loaded = True
        
    def _ensure_model_loaded(self):
        """Ensure embedding model is loaded"""
        if not self._model_loaded:
            logger.info(f"🤖 Loading embedding model: all-MiniLM-L6-v2")
            # Model is already loaded in __init__, just marking as loaded
            self._model_loaded = True
    
    def get_tone_collection(self):
        """Get tone embeddings collection"""
        if not self.tone_collection:
            self.tone_collection = datastax_connection.get_collection('tone_embeddings')
        return self.tone_collection
    
    def get_message_collection(self):
        """Get message embeddings collection"""
        if not self.message_collection:
            self.message_collection = datastax_connection.get_collection('message_embeddings')
        return self.message_collection
    
    def get_analysis_collection(self):
        """Get tone analysis collection"""
        if not self.analysis_collection:
            self.analysis_collection = datastax_connection.get_collection('tone_analysis')
        return self.analysis_collection
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate text embedding with performance tracking"""
        try:
            self._ensure_model_loaded()
            start_time = time.time()
            
            embedding = self.embedding_model.encode(text)
            
            processing_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            logger.debug(f"🔤 Generated embedding in {processing_time:.2f}ms (op: {self.operation_id[:8]})")
            
            return embedding.tolist()
        except Exception as e:
            logger.error(f"❌ Failed to generate embedding: {e}")
            return [0.0] * self.vector_dim
    
    def generate_multiple_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate multiple embeddings efficiently"""
        try:
            self._ensure_model_loaded()
            start_time = time.time()
            
            embeddings = self.embedding_model.encode(texts)
            
            processing_time = (time.time() - start_time) * 1000
            logger.debug(f"🔤 Generated {len(texts)} embeddings in {processing_time:.2f}ms")
            
            return [emb.tolist() for emb in embeddings]
        except Exception as e:
            logger.error(f"❌ Failed to generate multiple embeddings: {e}")
            return [[0.0] * self.vector_dim] * len(texts)
    
    async def store_tone_embedding(self, user_id: str, message_text: str, 
                                 tone_type: str, relationship: str,
                                 confidence: float, message_id: str = None,
                                 emotional_intensity: float = 0.5,
                                 formality_level: float = 0.5) -> ToneEmbedding:
        """Store comprehensive tone embedding with UUID v7"""
        try:
            # Generate UUID v7 for this embedding
            embedding_id = str(uuid7())
            
            # Generate different types of embeddings
            tone_context = f"{tone_type} {relationship}: {message_text}"
            style_context = f"style {relationship}: {message_text}"
            
            # Generate embeddings efficiently
            texts = [tone_context, message_text, style_context]
            embeddings = self.generate_multiple_embeddings(texts)
            
            tone_vector = embeddings[0]
            message_vector = embeddings[1]
            style_vector = embeddings[2]
            
            # Create embedding object with UUID v7
            tone_embedding = ToneEmbedding(
                embedding_id=embedding_id,
                user_id=str(user_id),
                tone_vector=tone_vector,
                message_vector=message_vector,
                style_vector=style_vector,
                tone_type=tone_type,
                message_sample=message_text[:200],
                confidence_score=confidence,
                relationship_context=relationship,
                emotional_intensity=emotional_intensity,
                formality_level=formality_level,
                created_at=datetime.now(timezone.utc).isoformat(),
                metadata={
                    "message_id": str(message_id) if message_id else str(uuid7()),
                    "operation_id": self.operation_id,
                    "vector_dim": self.vector_dim,
                    "model_version": "all-MiniLM-L6-v2",
                    "processing_timestamp": datetime.now(timezone.utc).isoformat()
                }
            )
            
            # Store in vector collection
            collection = self.get_tone_collection()
            result = collection.insert_one(tone_embedding.to_dict())
            
            logger.info(f"✅ Stored tone embedding with UUID v7: {embedding_id}")
            return tone_embedding
            
        except Exception as e:
            logger.error(f"❌ Failed to store tone embedding: {e}")
            raise
    
    async def store_message_embedding(self, message_id: str, user_id: str, 
                                    conversation_id: str, message_text: str,
                                    detected_tone: str, sentiment_score: float = 0.0,
                                    emotional_score: float = 0.0,
                                    formality_score: float = 0.5) -> MessageEmbedding:
        """Store comprehensive message embedding with UUID v7"""
        try:
            # Generate UUID v7 for this message embedding
            message_embedding_id = str(uuid7())
            
            # Generate different types of vectors for comprehensive analysis
            contexts = [
                message_text,  # Content vector
                f"style: {message_text}",  # Style vector
                f"{detected_tone}: {message_text}",  # Tone vector
                f"semantic meaning: {message_text}"  # Semantic vector
            ]
            
            embeddings = self.generate_multiple_embeddings(contexts)
            
            message_embedding = MessageEmbedding(
                message_embedding_id=message_embedding_id,
                message_id=str(message_id),
                user_id=str(user_id),
                conversation_id=str(conversation_id),
                content_vector=embeddings[0],
                style_vector=embeddings[1],
                tone_vector=embeddings[2],
                semantic_vector=embeddings[3],
                message_text=message_text,
                detected_tone=detected_tone,
                sentiment_score=sentiment_score,
                emotional_score=emotional_score,
                formality_score=formality_score,
                timestamp=datetime.now(timezone.utc).isoformat(),
                metadata={
                    "operation_id": self.operation_id,
                    "vector_model": "all-MiniLM-L6-v2",
                    "processing_timestamp": datetime.now(timezone.utc).isoformat()
                }
            )
            
            collection = self.get_message_collection()
            result = collection.insert_one(message_embedding.to_dict())
            
            logger.info(f"💬 Stored message embedding with UUID v7: {message_embedding_id}")
            return message_embedding
            
        except Exception as e:
            logger.error(f"❌ Failed to store message embedding: {e}")
            raise
    
    async def find_similar_tones(self, query_text: str, relationship: str = None,
                               user_id: str = None, limit: int = 5,
                               min_similarity: float = 0.6) -> List[Dict[str, Any]]:
        """Find similar tone patterns using vector search with UUID v7 support"""
        try:
            search_id = str(uuid7())
            logger.debug(f"🔍 Starting similarity search (ID: {search_id[:8]})")
            
            # Generate query vector
            query_vector = self.generate_embedding(query_text)
            
            # Build search filter
            filter_criteria = {}
            if relationship:
                filter_criteria["relationship_context"] = relationship
            if user_id:
                filter_criteria["user_id"] = str(user_id)
            
            # Perform vector search
            collection = self.get_tone_collection()
            results = collection.find(
                filter=filter_criteria,
                sort={"$vector": query_vector},
                limit=limit,
                include_similarity=True
            )
            
            similar_tones = []
            for result in results:
                similarity = result.get("$similarity", 0.0)
                
                # Filter by minimum similarity threshold
                if similarity >= min_similarity:
                    similar_tones.append({
                        "embedding_id": result.get("embedding_id"),
                        "tone_type": result["tone_type"],
                        "message_sample": result["message_sample"],
                        "confidence": result["confidence_score"],
                        "similarity": similarity,
                        "relationship": result["relationship_context"],
                        "user_id": result.get("user_id"),
                        "created_at": result.get("created_at"),
                        "emotional_intensity": result.get("emotional_intensity", 0.5),
                        "formality_level": result.get("formality_level", 0.5)
                    })
            
            logger.info(f"🔍 Found {len(similar_tones)} similar tones (search: {search_id[:8]})")
            return similar_tones
            
        except Exception as e:
            logger.error(f"❌ Vector search failed: {e}")
            return []
    
    async def get_best_tone_for_user(self, user_id: str, message_text: str,
                                   relationship: str = None) -> Tuple[str, float]:
        """Get best tone based on user's historical patterns with confidence score"""
        try:
            # Generate message vector
            query_vector = self.generate_embedding(message_text)
            
            # Search user's tone history
            collection = self.get_tone_collection()
            filter_criteria = {"user_id": str(user_id)}
            if relationship:
                filter_criteria["relationship_context"] = relationship
            
            results = collection.find(
                filter=filter_criteria,
                sort={"$vector": query_vector},
                limit=5,
                include_similarity=True
            )
            
            # Find best matching tone with weighted scoring
            best_tone = "casual"  # Default
            best_score = 0.0
            best_embedding_id = None
            
            tone_scores = {}
            
            for result in results:
                similarity = result.get("$similarity", 0.0)
                confidence = result.get("confidence_score", 0.0)
                tone_type = result.get("tone_type", "casual")
                
                # Weighted score combining similarity and historical confidence
                weighted_score = (similarity * 0.7) + (confidence * 0.3)
                
                if tone_type not in tone_scores:
                    tone_scores[tone_type] = []
                tone_scores[tone_type].append(weighted_score)
            
            # Calculate average scores for each tone
            for tone_type, scores in tone_scores.items():
                avg_score = sum(scores) / len(scores)
                if avg_score > best_score and avg_score > 0.6:  # Minimum threshold
                    best_score = avg_score
                    best_tone = tone_type
            
            logger.info(f"🎯 Best tone: {best_tone} (score: {best_score:.3f}) for user: {user_id}")
            return best_tone, best_score
            
        except Exception as e:
            logger.error(f"❌ Best tone detection failed: {e}")
            return "casual", 0.5
    
    async def analyze_user_tone_patterns(self, user_id: str, days_back: int = 30) -> Dict[str, Any]:
        """Analyze user's tone patterns over time"""
        try:
            analysis_id = str(uuid7())
            
            # Get user's recent tone history
            collection = self.get_tone_collection()
            
            # Calculate date threshold
            from datetime import timedelta
            threshold_date = datetime.now(timezone.utc) - timedelta(days=days_back)
            
            results = collection.find(
                filter={
                    "user_id": str(user_id),
                    "created_at": {"$gte": threshold_date.isoformat()}
                },
                sort={"created_at": -1},
                limit=200
            )
            
            # Analyze patterns
            tone_counts = {}
            relationship_tones = {}
            confidence_scores = []
            emotional_intensities = []
            formality_levels = []
            
            for result in results:
                tone_type = result.get("tone_type", "casual")
                relationship = result.get("relationship_context", "unknown")
                confidence = result.get("confidence_score", 0.0)
                emotional_intensity = result.get("emotional_intensity", 0.5)
                formality_level = result.get("formality_level", 0.5)
                
                # Count tones
                tone_counts[tone_type] = tone_counts.get(tone_type, 0) + 1
                
                # Track relationship-specific tones
                if relationship not in relationship_tones:
                    relationship_tones[relationship] = {}
                relationship_tones[relationship][tone_type] = relationship_tones[relationship].get(tone_type, 0) + 1
                
                # Collect metrics
                confidence_scores.append(confidence)
                emotional_intensities.append(emotional_intensity)
                formality_levels.append(formality_level)
            
            # Calculate statistics
            total_messages = sum(tone_counts.values())
            dominant_tone = max(tone_counts, key=tone_counts.get) if tone_counts else "casual"
            
            tone_distribution = {tone: count/total_messages for tone, count in tone_counts.items()} if total_messages > 0 else {}
            
            avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.0
            avg_emotional_intensity = sum(emotional_intensities) / len(emotional_intensities) if emotional_intensities else 0.5
            avg_formality = sum(formality_levels) / len(formality_levels) if formality_levels else 0.5
            
            analysis = {
                "analysis_id": analysis_id,
                "user_id": str(user_id),
                "analysis_period_days": days_back,
                "total_messages_analyzed": total_messages,
                "dominant_tone": dominant_tone,
                "tone_distribution": tone_distribution,
                "relationship_patterns": relationship_tones,
                "average_confidence": avg_confidence,
                "average_emotional_intensity": avg_emotional_intensity,
                "average_formality_level": avg_formality,
                "analysis_timestamp": datetime.now(timezone.utc).isoformat(),
                "uuid_version": "v7"
            }
            
            # Store analysis
            analysis_collection = self.get_analysis_collection()
            tone_analysis = ToneAnalysis(
                analysis_id=analysis_id,
                user_id=str(user_id),
                primary_tone=dominant_tone,
                confidence_scores=tone_counts,
                emotional_profile={
                    "average_intensity": avg_emotional_intensity,
                    "average_formality": avg_formality
                },
                style_features={
                    "tone_distribution": tone_distribution,
                    "relationship_patterns": relationship_tones
                },
                created_at=datetime.now(timezone.utc).isoformat()
            )
            
            analysis_collection.insert_one(tone_analysis.to_dict())
            
            logger.info(f"📊 Completed tone pattern analysis: {analysis_id}")
            return analysis
            
        except Exception as e:
            logger.error(f"❌ Tone pattern analysis failed: {e}")
            return {"error": str(e)}
    
    async def update_user_style_vector(self, user_id: str, recent_messages: List[str]) -> bool:
        """Update user's style vector based on recent messages"""
        try:
            if not recent_messages:
                return False
            
            # Combine recent messages to create updated style profile
            combined_text = " ".join(recent_messages[-10:])  # Last 10 messages
            style_vector = self.generate_embedding(combined_text)
            
            # Update user profile
            from app.db.cassandra.repositories.user_repo import UserRepository
            user_repo = UserRepository()
            
            result = await user_repo.update_user_profile(
                user_id=str(user_id),
                updates={
                    "style_vector": style_vector,
                    "updated_at": datetime.now(timezone.utc).isoformat(),
                    "metadata.style_updated_at": datetime.now(timezone.utc).isoformat(),
                    "metadata.style_update_id": str(uuid7())
                }
            )
            
            if result:
                logger.info(f"🎨 Updated style vector for user: {user_id}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"❌ Failed to update style vector: {e}")
            return False
    
    def get_operation_info(self) -> Dict[str, Any]:
        """Get vector operations information"""
        return {
            "operation_id": self.operation_id,
            "vector_dimension": self.vector_dim,
            "embedding_model": "all-MiniLM-L6-v2",
            "model_loaded": self._model_loaded,
            "uuid_version": "v7",
            "collections": {
                "tone_embeddings": bool(self.tone_collection),
                "message_embeddings": bool(self.message_collection),
                "tone_analysis": bool(self.analysis_collection)
            }
        }

# Global vector operations instance
vector_ops = VectorOperations()