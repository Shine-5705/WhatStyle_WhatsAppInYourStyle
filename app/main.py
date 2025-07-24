from fastapi import FastAPI
from contextlib import asynccontextmanager
from datetime import datetime
import asyncio
import threading
import grpc
from grpc import aio
import sys
import os
from pathlib import Path

# Add project root to Python path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Add generated directory to path
generated_path = os.path.join(os.path.dirname(__file__), 'grpc_services', 'generated')
sys.path.append(generated_path)

# Global variable to store gRPC server status
grpc_server_status = {"running": False, "port": 50051, "error": None}
grpc_server_task = None

async def start_grpc_server():
    """Start gRPC server"""
    global grpc_server_status
    try:
        # Import gRPC modules
        import health_pb2
        import health_pb2_grpc
        
        class HealthServicer(health_pb2_grpc.HealthServiceServicer):
            async def Check(self, request, context):
                print(f"🔍 Health check for: {request.service}")
                return health_pb2.HealthCheckResponse(
                    status=health_pb2.HealthCheckResponse.SERVING,
                    message=f"Service '{request.service}' is healthy"
                )
            
            async def Watch(self, request, context):
                """Health watch streaming"""
                print(f"👀 Health watch for: {request.service}")
                try:
                    for i in range(5):  # 5 updates
                        if context.cancelled():
                            break
                        await asyncio.sleep(2)
                        yield health_pb2.HealthCheckResponse(
                            status=health_pb2.HealthCheckResponse.SERVING,
                            message=f"Service '{request.service}' update #{i+1} - healthy"
                        )
                except asyncio.CancelledError:
                    print("🛑 Health watch cancelled")
                    return
        
        # Create server
        server = aio.server()
        health_pb2_grpc.add_HealthServiceServicer_to_server(HealthServicer(), server)
        
        # Add port
        listen_addr = '[::]:50051'
        server.add_insecure_port(listen_addr)
        
        print(f"🚀 Starting gRPC server on {listen_addr}")
        await server.start()
        
        grpc_server_status["running"] = True
        grpc_server_status["error"] = None
        print("✅ gRPC server started successfully!")
        
        # Keep server running
        try:
            await server.wait_for_termination()
        except asyncio.CancelledError:
            print("🛑 gRPC server shutdown requested")
            await server.stop(5)
            grpc_server_status["running"] = False
        
    except Exception as e:
        error_msg = f"gRPC server error: {str(e)}"
        print(f"❌ {error_msg}")
        grpc_server_status["running"] = False
        grpc_server_status["error"] = error_msg

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown"""
    # Startup
    print("🚀 Starting services...")
    global grpc_server_task
    
    # Check if gRPC modules are available
    try:
        import health_pb2
        import health_pb2_grpc
        print("✅ gRPC modules found")
        
        # Start gRPC server as background task
        grpc_server_task = asyncio.create_task(start_grpc_server())
        
        # Give it a moment to start
        await asyncio.sleep(1)
        
        print("🎉 Services started!")
        
    except ImportError as e:
        error_msg = f"gRPC modules not found: {e}. Generate them first with protoc."
        print(f"⚠️ {error_msg}")
        grpc_server_status["running"] = False
        grpc_server_status["error"] = error_msg
    except Exception as e:
        error_msg = f"Startup error: {e}"
        print(f"❌ {error_msg}")
        grpc_server_status["running"] = False
        grpc_server_status["error"] = error_msg
    
    # Yield control to FastAPI
    yield
    
    # Shutdown
    print("🛑 Shutting down services...")
    grpc_server_status["running"] = False
    
    # Cancel gRPC server task
    if grpc_server_task and not grpc_server_task.done():
        grpc_server_task.cancel()
        try:
            await grpc_server_task
        except asyncio.CancelledError:
            print("✅ gRPC server shutdown complete")

# Create FastAPI app with lifespan
app = FastAPI(
    title="WhatsApp MCP Server with gRPC",
    description="Tone-Adaptive WhatsApp Bot with gRPC Health Service",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "WhatsApp MCP Server with gRPC is running!",
        "services": {
            "fastapi": "running",
            "grpc": grpc_server_status["running"],
            "grpc_port": grpc_server_status["port"],
            "grpc_error": grpc_server_status["error"]
        },
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """FastAPI Health check endpoint"""
    return {
        "status": "healthy",
        "service": "whatsapp-mcp-server",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "fastapi": "healthy",
            "grpc": "healthy" if grpc_server_status["running"] else "not_running",
            "grpc_port": grpc_server_status["port"],
            "grpc_error": grpc_server_status["error"]
        },
        "test_grpc": {
            "command": "python -m app.grpc_services.health_client",
            "grpcurl": f"grpcurl -plaintext localhost:{grpc_server_status['port']} health.HealthService/Check",
            "test_endpoint": f"http://localhost:8000/test-grpc"
        }
    }

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
        
        # Import here to avoid issues if not generated
        try:
            import health_pb2
            import health_pb2_grpc
        except ImportError:
            return {
                "status": "error", 
                "message": "gRPC modules not found. Run: python -m grpc_tools.protoc --proto_path=app/grpc_services/protos --python_out=app/grpc_services/generated --grpc_python_out=app/grpc_services/generated app/grpc_services/protos/health.proto"
            }
        
        stub = health_pb2_grpc.HealthServiceStub(channel)
        request = health_pb2.HealthCheckRequest(service="mcp")
        
        # Set timeout
        response = await stub.Check(request, timeout=5.0)
        
        await channel.close()
        
        return {
            "status": "success",
            "message": "gRPC connection successful",
            "grpc_response": {
                "status": response.status,
                "message": response.message
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"gRPC connection failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

@app.get("/grpc/status")
async def grpc_status():
    """Detailed gRPC server status"""
    return {
        "grpc_server": grpc_server_status,
        "task_status": "running" if grpc_server_task and not grpc_server_task.done() else "not_running",
        "task_cancelled": grpc_server_task.cancelled() if grpc_server_task else None,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=False,  # Disable reload to prevent gRPC threading issues
        log_level="info"
    )