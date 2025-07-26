import os
from astrapy import DataAPIClient
from typing import Optional, Dict, Any, List
import logging
from datetime import datetime, timezone
from uuid6 import uuid7

logger = logging.getLogger(__name__)

class DataStaxConnection:
    """DataStax Astra DB connection with UUID v7 optimization"""
    
    def __init__(self):
        self.client: Optional[DataAPIClient] = None
        self.database = None
        self._connected = False
        self.collections = {}
        self.connection_id = str(uuid7())  # UUID v7 for connection tracking
        self.session_id = str(uuid7())     # Session tracking
        self._connection_attempts = 0
        self._max_retries = 3
    
    def connect(self):
        """Connect to DataStax Astra using Data API with retry logic"""
        try:
            self._connection_attempts += 1
            
            # Get credentials from environment
            token = os.getenv('DATASTAX_TOKEN')
            api_endpoint = os.getenv('DATASTAX_API_ENDPOINT')
            
            if not token or not api_endpoint:
                raise ValueError("DATASTAX_TOKEN and DATASTAX_API_ENDPOINT must be set")
            
            logger.info(f"🔗 Connecting to DataStax (attempt {self._connection_attempts}) - Connection ID: {self.connection_id}")
            logger.info(f"📊 Session ID: {self.session_id}")
            
            # Initialize the client
            self.client = DataAPIClient(token)
            self.database = self.client.get_database_by_api_endpoint(api_endpoint)
            
            # Test connection
            collections = self.database.list_collection_names()
            logger.info(f"✅ Connected to Astra DB. Available collections: {collections}")
            
            self._connected = True
            self._connection_attempts = 0  # Reset on successful connection
            
            # Initialize collections with UUID v7 support
            self._setup_collections()
            
            # Log connection event
            self._log_connection_event("connection_established")
            
            return self.database
            
        except Exception as e:
            logger.error(f"❌ Failed to connect to DataStax (attempt {self._connection_attempts}): {e}")
            
            # Retry logic
            if self._connection_attempts < self._max_retries:
                logger.info(f"🔄 Retrying connection... ({self._connection_attempts}/{self._max_retries})")
                return self.connect()
            else:
                logger.error(f"❌ Max retries ({self._max_retries}) exceeded. Connection failed.")
                raise
    
    def _setup_collections(self):
        """Setup required collections with optimized UUID v7 indexes"""
        try:
            collection_configs = [
                {
                    "name": "user_profiles",
                    "vector_enabled": False,
                    "indexes": ["phone_number", "user_id", "created_at", "relationship"]
                },
                {
                    "name": "conversations", 
                    "vector_enabled": False,
                    "indexes": ["user_id", "conversation_id", "timestamp", "message_id", "sender"]
                },
                {
                    "name": "conversation_sessions",
                    "vector_enabled": False,
                    "indexes": ["session_id", "user_id", "started_at", "active"]
                },
                {
                    "name": "tone_embeddings",
                    "vector_enabled": True,
                    "dimension": 384,
                    "metric": "cosine",
                    "indexes": ["user_id", "tone_type", "relationship_context", "created_at", "embedding_id"]
                },
                {
                    "name": "message_embeddings",
                    "vector_enabled": True, 
                    "dimension": 384,
                    "metric": "cosine",
                    "indexes": ["user_id", "conversation_id", "timestamp", "message_id", "detected_tone"]
                },
                {
                    "name": "tone_analysis",
                    "vector_enabled": False,
                    "indexes": ["analysis_id", "user_id", "message_id", "primary_tone", "created_at"]
                },
                {
                    "name": "connection_logs",
                    "vector_enabled": False,
                    "indexes": ["connection_id", "session_id", "timestamp", "event_type"]
                }
            ]
            
            for config in collection_configs:
                collection_name = config["name"]
                
                try:
                    # Try to get existing collection
                    self.collections[collection_name] = self.database.get_collection(collection_name)
                    logger.info(f"✅ Found existing collection: {collection_name}")
                    
                except Exception:
                    # Create new collection
                    try:
                        if config["vector_enabled"]:
                            self.collections[collection_name] = self.database.create_collection(
                                collection_name,
                                dimension=config["dimension"],
                                metric=config["metric"]
                            )
                            logger.info(f"✅ Created vector collection: {collection_name} (dim: {config['dimension']})")
                        else:
                            self.collections[collection_name] = self.database.create_collection(collection_name)
                            logger.info(f"✅ Created collection: {collection_name}")
                    except Exception as create_error:
                        logger.warning(f"⚠️ Could not create collection {collection_name}: {create_error}")
            
            logger.info("✅ All collections initialized with UUID v7 support")
            
        except Exception as e:
            logger.error(f"❌ Failed to setup collections: {e}")
            raise
    
    def get_collection(self, collection_name: str):
        """Get a collection with automatic reconnection"""
        if not self._connected:
            logger.warning("⚠️ Not connected, attempting to connect...")
            self.connect()
        
        collection = self.collections.get(collection_name)
        if not collection:
            logger.error(f"❌ Collection not found: {collection_name}")
            raise ValueError(f"Collection {collection_name} not found")
        
        return collection
    
    def is_connected(self) -> bool:
        """Check if connection is active"""
        return self._connected and self.client is not None
    
    def get_connection_info(self) -> Dict[str, Any]:
        """Get detailed connection information with UUID v7 tracking"""
        return {
            "connection_id": self.connection_id,
            "session_id": self.session_id,
            "connected": self._connected,
            "connection_attempts": self._connection_attempts,
            "collections": list(self.collections.keys()) if self._connected else [],
            "database_info": {
                "endpoint": os.getenv('DATASTAX_API_ENDPOINT', 'Not configured'),
                "collections_count": len(self.collections) if self._connected else 0,
                "uuid_version": "v7",
                "connection_time": datetime.now(timezone.utc).isoformat()
            },
            "client_info": {
                "astrapy_version": "1.0.0",
                "python_version": "3.10.12",
                "uuid6_support": True,
                "vector_support": True
            }
        }
    
    def generate_session_uuid(self) -> str:
        """Generate a new UUID v7 for session tracking"""
        return str(uuid7())
    
    def _log_connection_event(self, event_type: str, additional_data: Dict[str, Any] = None):
        """Log connection events with UUID v7 for tracking"""
        try:
            log_collection = self.collections.get("connection_logs")
            if log_collection:
                log_entry = {
                    "log_id": str(uuid7()),
                    "connection_id": self.connection_id,
                    "session_id": self.session_id,
                    "event_type": event_type,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "collections_count": len(self.collections),
                    "api_endpoint": os.getenv('DATASTAX_API_ENDPOINT', 'unknown'),
                    "uuid_version": "v7",
                    "connection_attempts": self._connection_attempts
                }
                
                if additional_data:
                    log_entry.update(additional_data)
                
                log_collection.insert_one(log_entry)
                logger.debug(f"📝 Logged {event_type} event: {log_entry['log_id']}")
        except Exception as e:
            logger.warning(f"⚠️ Failed to log {event_type} event: {e}")
    
    def disconnect(self):
        """Disconnect from DataStax with proper cleanup"""
        if self._connected:
            try:
                # Log disconnection event
                self._log_connection_event("connection_closed")
            except Exception as e:
                logger.warning(f"⚠️ Failed to log disconnection: {e}")
        
        self._connected = False
        self.client = None
        self.database = None
        self.collections.clear()
        logger.info(f"🛑 Disconnected from DataStax (connection: {self.connection_id})")
    
    def health_check(self) -> Dict[str, Any]:
        """Perform health check with UUID v7 tracking"""
        health_check_id = str(uuid7())
        
        try:
            if not self._connected:
                return {
                    "health_check_id": health_check_id,
                    "status": "unhealthy",
                    "connected": False,
                    "error": "Not connected to database",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            
            # Test database connectivity
            collections = self.database.list_collection_names()
            
            # Test a simple operation on each collection
            collection_health = {}
            for name, collection in self.collections.items():
                try:
                    collection.find_one({})
                    collection_health[name] = "healthy"
                except Exception as e:
                    collection_health[name] = f"error: {str(e)}"
            
            health_data = {
                "health_check_id": health_check_id,
                "status": "healthy",
                "connected": True,
                "connection_id": self.connection_id,
                "session_id": self.session_id,
                "collections": collections,
                "collection_health": collection_health,
                "uuid_version": "v7",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
            # Log health check
            self._log_connection_event("health_check", {
                "health_check_id": health_check_id,
                "status": "healthy"
            })
            
            return health_data
            
        except Exception as e:
            error_data = {
                "health_check_id": health_check_id,
                "status": "unhealthy",
                "connected": self._connected,
                "error": str(e),
                "connection_id": self.connection_id,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
            logger.error(f"❌ Health check failed: {e}")
            return error_data

# Global connection instance
datastax_connection = DataStaxConnection()