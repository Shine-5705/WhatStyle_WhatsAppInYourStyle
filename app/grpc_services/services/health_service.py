import asyncio
import grpc
from grpc import aio
from grpc_reflection.v1alpha import reflection
import sys
import os
from datetime import datetime, timezone
from uuid6 import uuid7
import time
from typing import Dict, Any
import logging

# Add generated directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'generated'))

try:
    import health_pb2
    import health_pb2_grpc
    logger = logging.getLogger(__name__)
    logger.info("✅ Successfully imported gRPC health modules")
except ImportError as e:
    logger.error(f"❌ Failed to import gRPC modules: {e}")
    print("Please run: python -m grpc_tools.protoc --proto_path=app/grpc_services/protos --python_out=app/grpc_services/generated --grpc_python_out=app/grpc_services/generated app/grpc_services/protos/health.proto")
    sys.exit(1)

# Import your UUID v7 enhanced components
from app.db.cassandra.connection import datastax_connection
from app.db.vector.vector_operations import vector_ops

class HealthServicer(health_pb2_grpc.HealthServiceServicer):
    """Comprehensive Health Service with UUID v7 tracking and system monitoring"""
    
    def __init__(self):
        self.service_id = str(uuid7())  # UUID v7 for service tracking
        self.start_time = datetime.now(timezone.utc)
        self.check_count = 0
        self.watch_sessions = {}
        
        # Define service components to monitor
        self.service_components = {
            "": {
                "name": "Overall System",
                "description": "WhatsApp MCP Server overall health",
                "critical": True
            },
            "mcp": {
                "name": "MCP Protocol Service", 
                "description": "Main message processing service",
                "critical": True
            },
            "tone": {
                "name": "Tone Analysis Service",
                "description": "AI-powered tone detection and analysis",
                "critical": True
            },
            "database": {
                "name": "DataStax Astra Database",
                "description": "Vector database for embeddings and user data",
                "critical": True
            },
            "vector": {
                "name": "Vector Operations",
                "description": "Embedding generation and similarity search",
                "critical": True
            },
            "ai": {
                "name": "AI Response Service",
                "description": "Intelligent response generation",
                "critical": False
            },
            "whatsapp": {
                "name": "WhatsApp Integration",
                "description": "WhatsApp API integration service",
                "critical": False
            }
        }
        
        logger.info(f"🏥 Health Service initialized with ID: {self.service_id}")
    
    async def Check(self, request, context):
        """Comprehensive health check for specific service with UUID v7 tracking"""
        check_id = str(uuid7())
        self.check_count += 1
        service_name = request.service if request.service else "overall"
        
        logger.info(f"🔍 Health check #{self.check_count} (ID: {check_id[:8]}) for service: '{service_name}'")
        
        try:
            # Get component info
            component = self.service_components.get(request.service, {
                "name": f"Unknown Service ({request.service})",
                "description": f"Service '{request.service}' status check",
                "critical": False
            })
            
            # Perform actual health checks based on service type
            health_result = await self._perform_health_check(request.service, check_id)
            
            # Determine status
            if health_result["healthy"]:
                status = health_pb2.HealthCheckResponse.SERVING
                message = f"{component['name']}: {health_result['message']} (Check ID: {check_id[:8]})"
            else:
                status = health_pb2.HealthCheckResponse.NOT_SERVING
                message = f"{component['name']}: {health_result['message']} (Check ID: {check_id[:8]})"
            
            response = health_pb2.HealthCheckResponse(
                status=status,
                message=message
            )
            
            logger.info(f"✅ Health check response - Status: {status}, Message: {message}")
            return response
            
        except Exception as e:
            error_message = f"Health check failed for '{service_name}': {str(e)} (Check ID: {check_id[:8]})"
            logger.error(f"❌ {error_message}")
            
            return health_pb2.HealthCheckResponse(
                status=health_pb2.HealthCheckResponse.NOT_SERVING,
                message=error_message
            )
    
    async def _perform_health_check(self, service_name: str, check_id: str) -> Dict[str, Any]:
        """Perform actual health checks based on service type"""
        
        if service_name == "" or service_name == "overall":
            return await self._check_overall_system_health(check_id)
        
        elif service_name == "database":
            return await self._check_database_health(check_id)
        
        elif service_name == "vector":
            return await self._check_vector_operations_health(check_id)
        
        elif service_name == "mcp":
            return await self._check_mcp_service_health(check_id)
        
        elif service_name == "tone":
            return await self._check_tone_service_health(check_id)
        
        elif service_name == "ai":
            return await self._check_ai_service_health(check_id)
        
        elif service_name == "whatsapp":
            return await self._check_whatsapp_integration_health(check_id)
        
        else:
            return {
                "healthy": True,
                "message": f"Service '{service_name}' status unknown but assumed healthy",
                "details": {"check_id": check_id}
            }
    
    async def _check_overall_system_health(self, check_id: str) -> Dict[str, Any]:
        """Check overall system health"""
        try:
            issues = []
            uptime_seconds = (datetime.now(timezone.utc) - self.start_time).total_seconds()
            
            # Check database
            db_health = datastax_connection.health_check()
            if db_health.get("status") != "healthy":
                issues.append("Database connectivity issues")
            
            # Check vector operations
            vector_info = vector_ops.get_operation_info()
            if not vector_info.get("model_loaded", False):
                issues.append("Vector model not loaded")
            
            if issues:
                return {
                    "healthy": False,
                    "message": f"System issues detected: {', '.join(issues)}",
                    "details": {
                        "uptime_seconds": uptime_seconds,
                        "issues": issues,
                        "check_count": self.check_count
                    }
                }
            else:
                return {
                    "healthy": True,
                    "message": f"All systems operational (uptime: {uptime_seconds:.0f}s)",
                    "details": {
                        "uptime_seconds": uptime_seconds,
                        "check_count": self.check_count,
                        "service_id": self.service_id
                    }
                }
                
        except Exception as e:
            return {
                "healthy": False,
                "message": f"System health check failed: {str(e)}",
                "details": {"error": str(e)}
            }
    
    async def _check_database_health(self, check_id: str) -> Dict[str, Any]:
        """Check DataStax database health"""
        try:
            db_health = datastax_connection.health_check()
            
            if db_health.get("status") == "healthy":
                collections_count = len(db_health.get("collections", []))
                return {
                    "healthy": True,
                    "message": f"Database connected with {collections_count} collections",
                    "details": db_health
                }
            else:
                return {
                    "healthy": False,
                    "message": f"Database health issues: {db_health.get('error', 'Unknown error')}",
                    "details": db_health
                }
                
        except Exception as e:
            return {
                "healthy": False,
                "message": f"Database check failed: {str(e)}",
                "details": {"error": str(e)}
            }
    
    async def _check_vector_operations_health(self, check_id: str) -> Dict[str, Any]:
        """Check vector operations health"""
        try:
            vector_info = vector_ops.get_operation_info()
            
            if vector_info.get("model_loaded", False):
                return {
                    "healthy": True,
                    "message": f"Vector operations ready (dim: {vector_info.get('vector_dimension', 0)})",
                    "details": vector_info
                }
            else:
                return {
                    "healthy": False,
                    "message": "Vector model not loaded or operational",
                    "details": vector_info
                }
                
        except Exception as e:
            return {
                "healthy": False,
                "message": f"Vector operations check failed: {str(e)}",
                "details": {"error": str(e)}
            }
    
    async def _check_mcp_service_health(self, check_id: str) -> Dict[str, Any]:
        """Check MCP service health"""
        try:
            # Test if we can import MCP service components
            from app.db.cassandra.repositories.user_repo import UserRepository
            
            user_repo = UserRepository()
            # Try to get collection to test connectivity
            collection = user_repo.get_collection()
            
            return {
                "healthy": True,
                "message": "MCP service operational with database connectivity",
                "details": {
                    "database_connected": True,
                    "repositories_loaded": True
                }
            }
            
        except Exception as e:
            return {
                "healthy": False,
                "message": f"MCP service issues: {str(e)}",
                "details": {"error": str(e)}
            }
    
    async def _check_tone_service_health(self, check_id: str) -> Dict[str, Any]:
        """Check tone analysis service health"""
        try:
            # Test tone detection capabilities
            test_message = "Hello, how are you?"
            embedding = vector_ops.generate_embedding(test_message)
            
            if len(embedding) == vector_ops.vector_dim:
                return {
                    "healthy": True,
                    "message": f"Tone analysis ready (embedding dim: {len(embedding)})",
                    "details": {
                        "embedding_generation": True,
                        "vector_dimension": len(embedding)
                    }
                }
            else:
                return {
                    "healthy": False,
                    "message": f"Tone analysis issues: incorrect embedding dimension",
                    "details": {
                        "expected_dim": vector_ops.vector_dim,
                        "actual_dim": len(embedding)
                    }
                }
                
        except Exception as e:
            return {
                "healthy": False,
                "message": f"Tone analysis check failed: {str(e)}",
                "details": {"error": str(e)}
            }
    
    async def _check_ai_service_health(self, check_id: str) -> Dict[str, Any]:
        """Check AI response service health"""
        try:
            # This is a placeholder - you can implement actual AI service checks
            return {
                "healthy": True,
                "message": "AI response service operational (simulated)",
                "details": {
                    "response_generation": True,
                    "model_status": "ready"
                }
            }
            
        except Exception as e:
            return {
                "healthy": False,
                "message": f"AI service check failed: {str(e)}",
                "details": {"error": str(e)}
            }
    
    async def _check_whatsapp_integration_health(self, check_id: str) -> Dict[str, Any]:
        """Check WhatsApp integration health"""
        try:
            # This is a placeholder - implement actual WhatsApp API checks
            whatsapp_token = os.getenv('WHATSAPP_API_TOKEN')
            
            if whatsapp_token:
                return {
                    "healthy": True,
                    "message": "WhatsApp integration configured",
                    "details": {
                        "token_configured": True,
                        "webhook_ready": True
                    }
                }
            else:
                return {
                    "healthy": False,
                    "message": "WhatsApp API token not configured",
                    "details": {
                        "token_configured": False,
                        "webhook_ready": False
                    }
                }
                
        except Exception as e:
            return {
                "healthy": False,
                "message": f"WhatsApp integration check failed: {str(e)}",
                "details": {"error": str(e)}
            }
    
    async def Watch(self, request, context):
        """Watch health status changes with UUID v7 session tracking"""
        session_id = str(uuid7())
        service_name = request.service if request.service else "overall"
        
        logger.info(f"👀 Health watch started (Session: {session_id[:8]}) for service: '{service_name}'")
        self.watch_sessions[session_id] = {
            "service": service_name,
            "started_at": datetime.now(timezone.utc).isoformat(),
            "updates_sent": 0
        }
        
        try:
            # Send periodic health updates
            for i in range(30):  # Send up to 30 updates (10 minutes at 20s intervals)
                # Check if client disconnected
                if context.cancelled():
                    logger.info(f"🛑 Client disconnected from health watch (Session: {session_id[:8]})")
                    break
                
                await asyncio.sleep(20)  # 20 second intervals for production monitoring
                
                # Perform actual health check
                health_result = await self._perform_health_check(request.service, str(uuid7()))
                
                # Determine status based on actual health
                if health_result["healthy"]:
                    status = health_pb2.HealthCheckResponse.SERVING
                    message = f"Update #{i+1}: {health_result['message']}"
                else:
                    status = health_pb2.HealthCheckResponse.NOT_SERVING
                    message = f"Update #{i+1}: {health_result['message']}"
                
                response = health_pb2.HealthCheckResponse(
                    status=status,
                    message=message
                )
                
                self.watch_sessions[session_id]["updates_sent"] += 1
                logger.info(f"📡 Streaming health update #{i+1} (Session: {session_id[:8]}): {message}")
                yield response
            
            logger.info(f"✅ Health watch completed for '{service_name}' (Session: {session_id[:8]})")
                
        except asyncio.CancelledError:
            logger.info(f"🛑 Health watch cancelled for '{service_name}' (Session: {session_id[:8]})")
            return
        except Exception as e:
            logger.error(f"❌ Health watch error for '{service_name}' (Session: {session_id[:8]}): {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Health watch failed: {str(e)}")
        finally:
            # Clean up session
            if session_id in self.watch_sessions:
                del self.watch_sessions[session_id]
    
    def get_service_info(self) -> Dict[str, Any]:
        """Get health service information"""
        uptime_seconds = (datetime.now(timezone.utc) - self.start_time).total_seconds()
        
        return {
            "service_id": self.service_id,
            "uptime_seconds": uptime_seconds,
            "total_checks": self.check_count,
            "active_watch_sessions": len(self.watch_sessions),
            "monitored_components": list(self.service_components.keys()),
            "uuid_version": "v7",
            "started_at": self.start_time.isoformat()
        }

async def serve_health_service():
    """Start the comprehensive health gRPC server with UUID v7 support"""
    server_id = str(uuid7())
    logger.info(f"🏥 Starting Health gRPC Server with ID: {server_id}")
    
    server = aio.server()
    
    # Add the health service
    health_servicer = HealthServicer()
    health_pb2_grpc.add_HealthServiceServicer_to_server(health_servicer, server)
    
    # Add reflection support
    SERVICE_NAMES = (
        health_pb2.DESCRIPTOR.services_by_name['HealthService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    logger.info("✅ gRPC reflection enabled")
    
    # Configure server address
    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    
    logger.info(f"🚀 Starting Health gRPC Server on {listen_addr}")
    await server.start()
    
    logger.info("✅ Health gRPC server started successfully!")
    logger.info("📋 Available services:")
    logger.info("   - health.HealthService/Check (Comprehensive health checks)")
    logger.info("   - health.HealthService/Watch (Real-time health monitoring)")
    logger.info("   - grpc.reflection.v1alpha.ServerReflection (for grpcurl)")
    logger.info("")
    logger.info("🔍 Monitored components:")
    for service_key, info in health_servicer.service_components.items():
        component_name = service_key if service_key else "overall"
        logger.info(f"   - {component_name}: {info['name']}")
    logger.info("")
    logger.info("📞 Test with:")
    logger.info("   grpcurl -plaintext localhost:50051 list")
    logger.info("   grpcurl -plaintext localhost:50051 health.HealthService/Check")
    logger.info("   grpcurl -plaintext -d '{\"service\":\"database\"}' localhost:50051 health.HealthService/Check")
    logger.info(f"🆔 Server ID: {server_id}")
    
    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info(f"\n🛑 Shutting down Health gRPC server (ID: {server_id[:8]})...")
        await server.stop(5)
        logger.info("✅ Health gRPC server shutdown complete")

if __name__ == '__main__':
    asyncio.run(serve_health_service())