# app/grpc_services/health_server.py
import asyncio
import grpc
from grpc import aio
import sys
import os

# Add generated directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'generated'))

try:
    import health_pb2
    import health_pb2_grpc
    print("✅ Successfully imported gRPC health modules")
except ImportError as e:
    print(f"❌ Failed to import gRPC modules: {e}")
    print("Please run: python -m grpc_tools.protoc --proto_path=app/grpc_services/protos --python_out=app/grpc_services/generated --grpc_python_out=app/grpc_services/generated app/grpc_services/protos/health.proto")
    sys.exit(1)

class HealthServicer(health_pb2_grpc.HealthServiceServicer):
    def __init__(self):
        self.service_status = {
            "": "Overall system",
            "mcp": "MCP Protocol service", 
            "tone": "Tone analysis service",
            "ai": "AI response service",
            "whatsapp": "WhatsApp integration service"
        }
    
    async def Check(self, request, context):
        """Health check for a specific service"""
        service_name = request.service if request.service else "overall system"
        print(f"🔍 Health check requested for service: '{service_name}'")
        
        # All services are healthy in this demo
        status = health_pb2.HealthCheckResponse.SERVING
        
        if request.service in self.service_status:
            description = self.service_status[request.service]
            message = f"{description} is healthy and serving"
        else:
            message = f"Service '{request.service}' is healthy (unknown service)"
        
        response = health_pb2.HealthCheckResponse(
            status=status,
            message=message
        )
        
        print(f"✅ Responding with status: {status}, message: {message}")
        return response
    
    async def Watch(self, request, context):
        """Watch health status changes (streaming)"""
        service_name = request.service if request.service else "overall system"
        print(f"👀 Health watch started for service: '{service_name}'")
        
        try:
            # Send periodic health updates
            for i in range(10):  # Send 10 updates
                # Check if client disconnected
                if context.cancelled():
                    print("🛑 Client disconnected from health watch")
                    break
                
                await asyncio.sleep(2)  # 2 second intervals
                
                # Simulate some status variation
                if i == 3:
                    # Simulate a brief degraded state
                    status = health_pb2.HealthCheckResponse.NOT_SERVING
                    message = f"Service '{request.service}' temporarily degraded (update #{i+1})"
                elif i == 4:
                    # Back to healthy
                    status = health_pb2.HealthCheckResponse.SERVING
                    message = f"Service '{request.service}' recovered and healthy (update #{i+1})"
                else:
                    status = health_pb2.HealthCheckResponse.SERVING
                    message = f"Service '{request.service}' check #{i+1} - All systems operational!"
                
                response = health_pb2.HealthCheckResponse(
                    status=status,
                    message=message
                )
                
                print(f"📡 Streaming health update #{i+1}: {message}")
                yield response
                
            print(f"✅ Health watch completed for '{service_name}'")
                
        except asyncio.CancelledError:
            print(f"🛑 Health watch cancelled for '{service_name}'")
            return
        except Exception as e:
            print(f"❌ Health watch error for '{service_name}': {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Health watch failed: {str(e)}")

async def serve():
    """Start the gRPC server"""
    server = aio.server()
    
    # Add the health service
    health_servicer = HealthServicer()
    health_pb2_grpc.add_HealthServiceServicer_to_server(health_servicer, server)
    
    # Configure server address
    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    
    print(f"🚀 Starting gRPC Health Server on {listen_addr}")
    await server.start()
    
    print("✅ gRPC server started successfully!")
    print("📋 Available services:")
    print("   - health.HealthService/Check")
    print("   - health.HealthService/Watch")
    print("📞 Test with:")
    print("   grpcurl -plaintext localhost:50051 health.HealthService/Check")
    print("   python app/grpc_services/health_client.py")
    
    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down gRPC server...")
        await server.stop(5)
        print("✅ gRPC server shutdown complete")

if __name__ == '__main__':
    asyncio.run(serve())