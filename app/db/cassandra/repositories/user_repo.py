from typing import Optional, List, Dict, Any
from app.models.user import UserProfile
from app.models.conversation import Conversation, ConversationSession
from app.models.tone import ToneEmbedding, ToneAnalysis
from app.db.cassandra.connection import datastax_connection
from uuid6 import uuid7
from datetime import datetime, timezone, timedelta
import logging

logger = logging.getLogger(__name__)

class UserRepository:
    """User repository with UUID v7 optimization"""
    
    def __init__(self):
        self.collection = None
        self.repo_id = str(uuid7())  # Repository instance tracking
    
    def get_collection(self):
        """Get user profiles collection"""
        if not self.collection:
            self.collection = datastax_connection.get_collection('user_profiles')
        return self.collection
    
    async def create_user(self, phone_number: str, name: str, relationship: str,
                         primary_tone: str = "casual") -> UserProfile:
        """Create a new user profile with UUID v7"""
        try:
            user = UserProfile(
                user_id=str(uuid7()),  # Explicit UUID v7 generation
                phone_number=phone_number,
                name=name,
                relationship=relationship,
                primary_tone=primary_tone,
                created_at=datetime.now(timezone.utc).isoformat(),
                updated_at=datetime.now(timezone.utc).isoformat(),
                metadata={
                    "created_by_repo": self.repo_id,
                    "uuid_version": "v7",
                    "creation_timestamp": datetime.now(timezone.utc).isoformat()
                }
            )
            
            collection = self.get_collection()
            result = collection.insert_one(user.to_dict())
            
            logger.info(f"✅ Created user with UUID v7: {user.user_id} (phone: {phone_number})")
            return user
            
        except Exception as e:
            logger.error(f"❌ Failed to create user: {e}")
            raise
    
    async def get_user_by_phone(self, phone_number: str) -> Optional[UserProfile]:
        """Get user by phone number with caching optimization"""
        try:
            collection = self.get_collection()
            result = collection.find_one({"phone_number": phone_number})
            
            if result:
                user = UserProfile.from_dict(result)
                logger.info(f"📱 Found user by phone: {user.user_id} ({phone_number})")
                return user
            
            logger.debug(f"📱 No user found for phone: {phone_number}")
            return None
            
        except Exception as e:
            logger.error(f"❌ Failed to get user by phone: {e}")
            return None
    
    async def get_user_by_id(self, user_id: str) -> Optional[UserProfile]:
        """Get user by UUID v7 ID"""
        try:
            collection = self.get_collection()
            result = collection.find_one({"user_id": str(user_id)})
            
            if result:
                user = UserProfile.from_dict(result)
                logger.info(f"🔍 Found user by ID: {user.user_id}")
                return user
            
            logger.debug(f"🔍 No user found for ID: {user_id}")
            return None
            
        except Exception as e:
            logger.error(f"❌ Failed to get user by ID: {e}")
            return None
    
    async def get_users_by_ids(self, user_ids: List[str]) -> List[UserProfile]:
        """Get multiple users by IDs efficiently"""
        try:
            collection = self.get_collection()
            str_ids = [str(uid) for uid in user_ids]
            
            results = collection.find({"user_id": {"$in": str_ids}})
            
            users = []
            for result in results:
                users.append(UserProfile.from_dict(result))
            
            logger.info(f"👥 Retrieved {len(users)} users from {len(user_ids)} requested IDs")
            return users
            
        except Exception as e:
            logger.error(f"❌ Failed to get users by IDs: {e}")
            return []
    
    async def update_user_profile(self, user_id: str, updates: Dict[str, Any]) -> Optional[UserProfile]:
        """Update user profile with timestamp and tracking"""
        try:
            # Add update metadata
            updates['updated_at'] = datetime.now(timezone.utc).isoformat()
            updates['metadata.last_update_id'] = str(uuid7())
            updates['metadata.updated_by_repo'] = self.repo_id
            
            collection = self.get_collection()
            result = collection.find_one_and_update(
                {"user_id": str(user_id)},
                {"$set": updates},
                return_document="after"
            )
            
            if result:
                user = UserProfile.from_dict(result)
                logger.info(f"🔄 Updated user: {user.user_id}")
                return user
            
            logger.warning(f"⚠️ No user found to update: {user_id}")
            return None
            
        except Exception as e:
            logger.error(f"❌ Failed to update user: {e}")
            return None
    
    async def record_interaction(self, user_id: str, interaction_type: str = "message") -> bool:
        """Record user interaction with detailed tracking"""
        try:
            interaction_id = str(uuid7())
            
            collection = self.get_collection()
            result = collection.find_one_and_update(
                {"user_id": str(user_id)},
                {
                    "$set": {
                        "last_interaction": datetime.now(timezone.utc).isoformat(),
                        "updated_at": datetime.now(timezone.utc).isoformat(),
                        f"metadata.last_{interaction_type}_interaction": datetime.now(timezone.utc).isoformat(),
                        "metadata.last_interaction_id": interaction_id
                    },
                    "$inc": {"interaction_count": 1}
                }
            )
            
            if result:
                logger.info(f"📊 Recorded {interaction_type} interaction for user: {user_id} (ID: {interaction_id[:8]})")
                return True
            return False
                
        except Exception as e:
            logger.error(f"❌ Failed to record interaction: {e}")
            return False
    
    async def get_users_by_relationship(self, relationship: str, limit: int = 50) -> List[UserProfile]:
        """Get users by relationship type with pagination"""
        try:
            collection = self.get_collection()
            results = collection.find(
                {"relationship": relationship},
                limit=limit,
                sort={"updated_at": -1}
            )
            
            users = []
            for result in results:
                users.append(UserProfile.from_dict(result))
            
            logger.info(f"👥 Found {len(users)} users with relationship: {relationship}")
            return users
            
        except Exception as e:
            logger.error(f"❌ Failed to get users by relationship: {e}")
            return []
    
    async def get_active_users(self, days_back: int = 7, limit: int = 100) -> List[UserProfile]:
        """Get users active within specified days"""
        try:
            threshold_date = datetime.now(timezone.utc) - timedelta(days=days_back)
            
            collection = self.get_collection()
            results = collection.find(
                {"last_interaction": {"$gte": threshold_date.isoformat()}},
                limit=limit,
                sort={"last_interaction": -1}
            )
            
            users = []
            for result in results:
                users.append(UserProfile.from_dict(result))
            
            logger.info(f"📈 Found {len(users)} active users in last {days_back} days")
            return users
            
        except Exception as e:
            logger.error(f"❌ Failed to get active users: {e}")
            return []
    
    async def delete_user(self, user_id: str) -> bool:
        """Delete user and related data"""
        try:
            collection = self.get_collection()
            result = collection.delete_one({"user_id": str(user_id)})
            
            if result.deleted_count > 0:
                logger.info(f"🗑️ Deleted user: {user_id}")
                
                # Also clean up related data (conversations, embeddings)
                await self._cleanup_user_data(str(user_id))
                return True
            return False
            
        except Exception as e:
            logger.error(f"❌ Failed to delete user: {e}")
            return False
    
    async def _cleanup_user_data(self, user_id: str):
        """Clean up user-related data from other collections"""
        try:
            cleanup_id = str(uuid7())
            logger.info(f"🧹 Starting cleanup for user {user_id} (cleanup: {cleanup_id[:8]})")
            
            # Cleanup conversations
            conv_collection = datastax_connection.get_collection('conversations')
            conv_result = conv_collection.delete_many({"user_id": str(user_id)})
            logger.info(f"🗑️ Deleted {conv_result.deleted_count} conversations")
            
            # Cleanup tone embeddings
            tone_collection = datastax_connection.get_collection('tone_embeddings')
            tone_result = tone_collection.delete_many({"user_id": str(user_id)})
            logger.info(f"🗑️ Deleted {tone_result.deleted_count} tone embeddings")
            
            # Cleanup message embeddings
            msg_collection = datastax_connection.get_collection('message_embeddings')
            msg_result = msg_collection.delete_many({"user_id": str(user_id)})
            logger.info(f"🗑️ Deleted {msg_result.deleted_count} message embeddings")
            
            # Cleanup tone analysis
            analysis_collection = datastax_connection.get_collection('tone_analysis')
            analysis_result = analysis_collection.delete_many({"user_id": str(user_id)})
            logger.info(f"🗑️ Deleted {analysis_result.deleted_count} tone analyses")
            
            logger.info(f"✅ Cleanup completed for user {user_id}")
            
        except Exception as e:
            logger.error(f"❌ Failed to cleanup user data: {e}")

class ConversationRepository:
    """Conversation repository with UUID v7 optimization"""
    
    def __init__(self):
        self.collection = None
        self.session_collection = None
        self.repo_id = str(uuid7())
    
    def get_collection(self):
        """Get conversations collection"""
        if not self.collection:
            self.collection = datastax_connection.get_collection('conversations')
        return self.collection
    
    def get_session_collection(self):
        """Get conversation sessions collection"""
        if not self.session_collection:
            self.session_collection = datastax_connection.get_collection('conversation_sessions')
        return self.session_collection
    
    async def save_message(self, user_id: str, conversation_id: str, 
                          message_text: str, sender: str, detected_tone: str = None,
                          tone_confidence: float = None, message_type: str = "text",
                          context_data: Dict[str, Any] = None) -> Conversation:
        """Save a conversation message with UUID v7"""
        try:
            conversation = Conversation(
                message_id=str(uuid7()),  # Generate UUID v7 for message
                user_id=str(user_id),
                conversation_id=str(conversation_id),
                message_text=message_text,
                sender=sender,
                message_type=message_type,
                detected_tone=detected_tone,
                tone_confidence=tone_confidence,
                timestamp=datetime.now(timezone.utc).isoformat(),
                context_data=context_data or {},
                metadata={
                    "saved_by_repo": self.repo_id,
                    "uuid_version": "v7"
                }
            )
            
            collection = self.get_collection()
            result = collection.insert_one(conversation.to_dict())
            
            # Update conversation session
            await self._update_conversation_session(str(user_id), str(conversation_id))
            
            logger.info(f"💬 Saved message with UUID v7: {conversation.message_id}")
            return conversation
            
        except Exception as e:
            logger.error(f"❌ Failed to save message: {e}")
            raise
    
    async def _update_conversation_session(self, user_id: str, conversation_id: str):
        """Update or create conversation session"""
        try:
            session_collection = self.get_session_collection()
            
            # Try to update existing session
            result = session_collection.find_one_and_update(
                {"user_id": user_id, "session_id": conversation_id, "active": True},
                {
                    "$inc": {"message_count": 1},
                    "$set": {"updated_at": datetime.now(timezone.utc).isoformat()}
                },
                return_document="after"
            )
            
            # If no active session found, create new one
            if not result:
                session = ConversationSession(
                    session_id=conversation_id,
                    user_id=user_id,
                    started_at=datetime.now(timezone.utc).isoformat(),
                    message_count=1,
                    active=True
                )
                session_collection.insert_one(session.to_dict())
                logger.debug(f"📝 Created new conversation session: {conversation_id}")
            
        except Exception as e:
            logger.warning(f"⚠️ Failed to update conversation session: {e}")
    
    async def get_conversation_history(self, user_id: str, limit: int = 50,
                                     conversation_id: str = None) -> List[Conversation]:
        """Get recent conversation history sorted by timestamp"""
        try:
            collection = self.get_collection()
            
            filter_criteria = {"user_id": str(user_id)}
            if conversation_id:
                filter_criteria["conversation_id"] = str(conversation_id)
            
            results = collection.find(
                filter_criteria,
                sort={"timestamp": -1},
                limit=limit
            )
            
            conversations = []
            for result in results:
                conversations.append(Conversation.from_dict(result))
            
            logger.info(f"📚 Retrieved {len(conversations)} messages for user: {user_id}")
            return conversations
            
        except Exception as e:
            logger.error(f"❌ Failed to get conversation history: {e}")
            return []
    
    async def get_conversation_by_id(self, conversation_id: str) -> List[Conversation]:
        """Get all messages in a specific conversation"""
        try:
            collection = self.get_collection()
            results = collection.find(
                {"conversation_id": str(conversation_id)},
                sort={"timestamp": 1}  # Ascending order for conversation flow
            )
            
            conversations = []
            for result in results:
                conversations.append(Conversation.from_dict(result))
            
            logger.info(f"🗨️ Retrieved conversation: {conversation_id} with {len(conversations)} messages")
            return conversations
            
        except Exception as e:
            logger.error(f"❌ Failed to get conversation by ID: {e}")
            return []
    
    async def get_recent_messages_by_sender(self, user_id: str, sender: str,
                                          limit: int = 20) -> List[Conversation]:
        """Get recent messages from specific sender (user or bot)"""
        try:
            collection = self.get_collection()
            results = collection.find(
                {"user_id": str(user_id), "sender": sender},
                sort={"timestamp": -1},
                limit=limit
            )
            
            messages = []
            for result in results:
                messages.append(Conversation.from_dict(result))
            
            logger.info(f"📱 Retrieved {len(messages)} recent {sender} messages for user: {user_id}")
            return messages
            
        except Exception as e:
            logger.error(f"❌ Failed to get recent messages by sender: {e}")
            return []
    
    async def get_conversation_stats(self, user_id: str, days_back: int = 30) -> Dict[str, Any]:
        """Get conversation statistics for user"""
        try:
            stats_id = str(uuid7())
            threshold_date = datetime.now(timezone.utc) - timedelta(days=days_back)
            
            collection = self.get_collection()
            results = collection.find({
                "user_id": str(user_id),
                "timestamp": {"$gte": threshold_date.isoformat()}
            })
            
            total_messages = 0
            user_messages = 0
            bot_messages = 0
            tone_counts = {}
            avg_message_length = 0
            total_length = 0
            
            for result in results:
                total_messages += 1
                message_length = len(result.get("message_text", ""))
                total_length += message_length
                
                if result.get("sender") == "user":
                    user_messages += 1
                elif result.get("sender") == "bot":
                    bot_messages += 1
                
                tone = result.get("detected_tone", "unknown")
                tone_counts[tone] = tone_counts.get(tone, 0) + 1
            
            avg_message_length = total_length / total_messages if total_messages > 0 else 0
            
            stats = {
                "stats_id": stats_id,
                "user_id": str(user_id),
                "period_days": days_back,
                "total_messages": total_messages,
                "user_messages": user_messages,
                "bot_messages": bot_messages,
                "avg_message_length": avg_message_length,
                "tone_distribution": tone_counts,
                "most_common_tone": max(tone_counts, key=tone_counts.get) if tone_counts else "unknown",
                "analysis_timestamp": datetime.now(timezone.utc).isoformat()
            }
            
            logger.info(f"📊 Generated conversation stats: {stats_id}")
            return stats
            
        except Exception as e:
            logger.error(f"❌ Failed to get conversation stats: {e}")
            return {"error": str(e)}

class ToneRepository:
    """Tone analysis repository with UUID v7 optimization"""
    
    def __init__(self):
        self.collection = None
        self.analysis_collection = None
        self.repo_id = str(uuid7())
    
    def get_collection(self):
        """Get tone embeddings collection"""
        if not self.collection:
            self.collection = datastax_connection.get_collection('tone_embeddings')
        return self.collection
    
    def get_analysis_collection(self):
        """Get tone analysis collection"""
        if not self.analysis_collection:
            self.analysis_collection = datastax_connection.get_collection('tone_analysis')
        return self.analysis_collection
    
    async def save_tone_analysis(self, user_id: str, message_id: str,
                                primary_tone: str, confidence_score: float,
                                tone_features: Dict[str, float],
                                emotional_profile: Dict[str, float],
                                message_text: str = "",
                                relationship_context: str = "",
                                processing_time_ms: float = 0.0) -> ToneAnalysis:
        """Save comprehensive tone analysis results with UUID v7"""
        try:
            analysis = ToneAnalysis(
                analysis_id=str(uuid7()),
                message_id=str(message_id),
                user_id=str(user_id),
                primary_tone=primary_tone,
                confidence_scores={primary_tone: confidence_score},
                emotional_profile=emotional_profile,
                style_features=tone_features,
                relationship_context=relationship_context,
                processing_time_ms=processing_time_ms,
                created_at=datetime.now(timezone.utc).isoformat()
            )
            
            collection = self.get_analysis_collection()
            result = collection.insert_one(analysis.to_dict())
            
            logger.info(f"🎯 Saved tone analysis with UUID v7: {analysis.analysis_id}")
            return analysis
            
        except Exception as e:
            logger.error(f"❌ Failed to save tone analysis: {e}")
            raise
    
    async def get_user_tone_history(self, user_id: str, limit: int = 100) -> List[ToneAnalysis]:
        """Get user's tone analysis history"""
        try:
            collection = self.get_analysis_collection()
            results = collection.find(
                {"user_id": str(user_id)},
                sort={"created_at": -1},
                limit=limit
            )
            
            analyses = []
            for result in results:
                analyses.append(ToneAnalysis.from_dict(result))
            
            logger.info(f"📊 Retrieved {len(analyses)} tone analyses for user: {user_id}")
            return analyses
            
        except Exception as e:
            logger.error(f"❌ Failed to get tone history: {e}")
            return []
    
    async def get_tone_stats(self, user_id: str, days_back: int = 30) -> Dict[str, Any]:
        """Get comprehensive tone statistics for a user"""
        try:
            stats_id = str(uuid7())
            threshold_date = datetime.now(timezone.utc) - timedelta(days=days_back)
            
            collection = self.get_analysis_collection()
            results = collection.find({
                "user_id": str(user_id),
                "created_at": {"$gte": threshold_date.isoformat()}
            })
            
            tone_counts = {}
            total_confidence = 0.0
            total_analyses = 0
            processing_times = []
            emotional_intensities = []
            formality_levels = []
            
            for result in results:
                primary_tone = result.get("primary_tone", "unknown")
                confidence_scores = result.get("confidence_scores", {})
                emotional_profile = result.get("emotional_profile", {})
                processing_time = result.get("processing_time_ms", 0.0)
                
                tone_counts[primary_tone] = tone_counts.get(primary_tone, 0) + 1
                
                if confidence_scores and primary_tone in confidence_scores:
                    total_confidence += confidence_scores[primary_tone]
                
                total_analyses += 1
                processing_times.append(processing_time)
                
                if "average_intensity" in emotional_profile:
                    emotional_intensities.append(emotional_profile["average_intensity"])
                if "average_formality" in emotional_profile:
                    formality_levels.append(emotional_profile["average_formality"])
            
            avg_confidence = total_confidence / total_analyses if total_analyses > 0 else 0.0
            avg_processing_time = sum(processing_times) / len(processing_times) if processing_times else 0.0
            avg_emotional_intensity = sum(emotional_intensities) / len(emotional_intensities) if emotional_intensities else 0.5
            avg_formality = sum(formality_levels) / len(formality_levels) if formality_levels else 0.5
            
            stats = {
                "stats_id": stats_id,
                "user_id": str(user_id),
                "period_days": days_back,
                "total_analyses": total_analyses,
                "average_confidence": avg_confidence,
                "average_processing_time_ms": avg_processing_time,
                "average_emotional_intensity": avg_emotional_intensity,
                "average_formality_level": avg_formality,
                "tone_distribution": tone_counts,
                "dominant_tone": max(tone_counts, key=tone_counts.get) if tone_counts else "unknown",
                "analysis_timestamp": datetime.now(timezone.utc).isoformat(),
                "uuid_version": "v7"
            }
            
            logger.info(f"📈 Generated tone stats: {stats_id}")
            return stats
            
        except Exception as e:
            logger.error(f"❌ Failed to get tone stats: {e}")
            return {"error": str(e)}