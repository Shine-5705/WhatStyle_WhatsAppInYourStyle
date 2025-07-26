# ===== app/grpc_services/server.py =====
import asyncio
import logging
import signal
import sys
import os
from datetime import datetime, timezone
from uuid6 import uuid7
from typing import Dict, Any
import time

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('grpc_server.log')
    ]
)
logger = logging.getLogger(__name__)

# Import services
from app.grpc_services.services.mcp_service import serve as serve_mcp
from app.grpc_services.services.tone_service import serve_tone_service
from app.grpc_services.services.health_service import serve_health_service
from app.db.cassandra.connection import datastax_connection
from app.db.vector.vector_operations import vector_ops

class GRPCServerManager:
    """Comprehensive gRPC server manager with UUID v7 tracking"""
    
    def __init__(self):
        self.manager_id = str(uuid7())
        self.start_time = datetime.now(timezone.utc)
        self.servers = {}
        self.shutdown_requested = False
        
        logger.info(f"🚀 GRPC Server Manager initialized with ID: {self.manager_id}")
    
    async def initialize_dependencies(self):
        """Initialize all dependencies with comprehensive error handling"""
        init_id = str(uuid7())
        logger.info(f"🔧 Initializing dependencies (ID: {init_id[:8]})")
        
        try:
            # Initialize DataStax connection
            logger.info("📊 Connecting to DataStax Astra...")
            datastax_connection.connect()
            logger.info("✅ DataStax connection established")
            
            # Test database health
            db_health = datastax_connection.health_check()
            logger.info(f"💊 Database health: {db_health['status']}")
            
            # Initialize vector operations
            logger.info("🤖 Initializing vector operations...")
            vector_info = vector_ops.get_operation_info()
            logger.info(f"✅ Vector operations ready: {vector_info}")
            
            # Log successful initialization
            connection_info = datastax_connection.get_connection_info()
            logger.info(f"📋 Available collections: {connection_info['collections']}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize dependencies (ID: {init_id[:8]}): {e}")
            logger.warning("⚠️ Continuing with limited functionality")
            return False
    
    async def start_all_services(self):
        """Start all gRPC services concurrently"""
        startup_id = str(uuid7())
        logger.info(f"🚀 Starting all gRPC services (startup: {startup_id[:8]})")
        
        # Define services to start
        services = [
            {
                "name": "MCP Service",
                "port": 50052,
                "serve_function": serve_mcp,
                "description": "Main WhatsApp message processing service"
            },
            {
                "name": "Tone Service", 
                "port": 50053,
                "serve_function": serve_tone_service,
                "description": "Advanced tone analysis service"
            },
            {
                "name": "Health Service",
                "port": 50051,
                "serve_function": serve_health_service,
                "description": "System health monitoring service"
            }
        ]
        
        # Start services concurrently
        service_tasks = []
        for service in services:
            logger.info(f"🎯 Starting {service['name']} on port {service['port']}")
            task = asyncio.create_task(
                service["serve_function"](),
                name=f"{service['name']}_server"
            )
            service_tasks.append(task)
            self.servers[service["name"]] = {
                "task": task,
                "port": service["port"],
                "description": service["description"],
                "started_at": datetime.now(timezone.utc).isoformat(),
                "service_id": str(uuid7())
            }
        
        logger.info(f"✅ All {len(services)} services started successfully!")
        logger.info("=" * 60)
        logger.info("📋 GRPC SERVICES OVERVIEW")
        logger.info("=" * 60)
        
        for name, info in self.servers.items():
            logger.info(f"🔸 {name}")
            logger.info(f"   📍 Port: {info['port']}")
            logger.info(f"   📝 Description: {info['description']}")
            logger.info(f"   🆔 Service ID: {info['service_id']}")
            logger.info(f"   ⏰ Started: {info['started_at']}")
        
        logger.info("=" * 60)
        logger.info(f"🆔 Manager ID: {self.manager_id}")
        logger.info(f"⏱️ Total startup time: {(datetime.now(timezone.utc) - self.start_time).total_seconds():.2f}s")
        logger.info("=" * 60)
        
        return service_tasks
    
    async def monitor_services(self, service_tasks):
        """Monitor service health and handle failures"""
        monitor_id = str(uuid7())
        logger.info(f"👁️ Starting service monitoring (ID: {monitor_id[:8]})")
        
        while not self.shutdown_requested:
            try:
                # Check if any service has failed
                for task in service_tasks:
                    if task.done():
                        exception = task.exception()
                        if exception:
                            logger.error(f"❌ Service {task.get_name()} failed: {exception}")
                        else:
                            logger.warning(f"⚠️ Service {task.get_name()} completed unexpectedly")
                
                # Wait before next check
                await asyncio.sleep(30)  # Check every 30 seconds
                
                # Log periodic health status
                uptime = (datetime.now(timezone.utc) - self.start_time).total_seconds()
                logger.info(f"💊 Service manager health check - Uptime: {uptime:.0f}s, Services: {len([t for t in service_tasks if not t.done()])}/{len(service_tasks)} running")
                
            except asyncio.CancelledError:
                logger.info("🛑 Service monitoring cancelled")
                break
            except Exception as e:
                logger.error(f"❌ Error in service monitoring: {e}")
                await asyncio.sleep(10)
    
    def setup_signal_handlers(self):
        """Setup graceful shutdown signal handlers"""
        def signal_handler(signum, frame):
            logger.info(f"🛑 Received signal {signum}, initiating graceful shutdown...")
            self.shutdown_requested = True
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        logger.info("🔧 Signal handlers configured")
    
    async def graceful_shutdown(self, service_tasks):
        """Perform graceful shutdown of all services"""
        shutdown_id = str(uuid7())
        logger.info(f"🛑 Starting graceful shutdown (ID: {shutdown_id[:8]})")
        
        try:
            # Cancel all service tasks
            for task in service_tasks:
                if not task.done():
                    logger.info(f"🛑 Stopping {task.get_name()}...")
                    task.cancel()
            
            # Wait for all tasks to complete
            if service_tasks:
                logger.info("⏳ Waiting for services to shutdown...")
                await asyncio.wait(service_tasks, timeout=10.0)
            
            # Disconnect from database
            logger.info("📊 Disconnecting from DataStax...")
            datastax_connection.disconnect()
            
            # Log final statistics
            total_uptime = (datetime.now(timezone.utc) - self.start_time).total_seconds()
            logger.info(f"📊 Shutdown complete - Total uptime: {total_uptime:.2f}s")
            logger.info(f"🆔 Manager {self.manager_id[:8]} shutdown successfully")
            
        except Exception as e:
            logger.error(f"❌ Error during shutdown: {e}")
    
    async def run(self):
        """Main run method - orchestrates the entire server lifecycle"""
        try:
            logger.info("🚀 Starting WhatsApp MCP gRPC Server Suite")
            logger.info(f"🆔 Manager ID: {self.manager_id}")
            logger.info(f"⏰ Start time: {self.start_time.isoformat()}")
            
            # Setup signal handlers
            self.setup_signal_handlers()
            
            # Initialize dependencies
            deps_initialized = await self.initialize_dependencies()
            if not deps_initialized:
                logger.warning("⚠️ Some dependencies failed to initialize")
            
            # Start all services
            service_tasks = await self.start_all_services()
            
            # Create monitoring task
            monitor_task = asyncio.create_task(
                self.monitor_services(service_tasks),
                name="service_monitor"
            )
            
            # Wait for shutdown signal or service failure
            all_tasks = service_tasks + [monitor_task]
            
            try:
                # Wait until shutdown is requested or a critical task fails
                while not self.shutdown_requested:
                    done, pending = await asyncio.wait(all_tasks, timeout=1.0, return_when=asyncio.FIRST_COMPLETED)
                    
                    # Check if any critical service failed
                    for task in done:
                        if task in service_tasks:
                            logger.error(f"❌ Critical service {task.get_name()} stopped unexpectedly")
                            self.shutdown_requested = True
                            break
                    
                    if done:
                        break
                        
            except KeyboardInterrupt:
                logger.info("🛑 Keyboard interrupt received")
                self.shutdown_requested = True
            
            # Perform graceful shutdown
            await self.graceful_shutdown(service_tasks + [monitor_task])
            
        except Exception as e:
            logger.error(f"❌ Fatal error in server manager: {e}")
            raise

async def main():
    """Main entry point"""
    try:
        # Create and run server manager
        server_manager = GRPCServerManager()
        await server_manager.run()
        
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        sys.exit(1)

def create_health_service():
    """Create a simple health service for the health port"""
    # This is a placeholder - you might want to implement a proper health service
    pass

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Application interrupted")
    except Exception as e:
        logger.error(f"❌ Application failed: {e}")
        sys.exit(1)