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
except ImportError as e:
    print(f"❌ Failed to import gRPC modules: {e}")
    sys.exit(1)

async def test_health_client():
    """Test client for health service"""
    print("🔗 Connecting to gRPC Health Server...")
    
    # Create channel
    async with aio.insecure_channel('localhost:50051') as channel:
        # Create stub
        stub = health_pb2_grpc.HealthServiceStub(channel)
        
        print("\n=== Testing Health Check ===")
        
        # Test 1: Overall health
        try:
            request = health_pb2.HealthCheckRequest(service="")
            response = await stub.Check(request)
            print(f"✅ Overall Health: {response.status} - {response.message}")
        except grpc.RpcError as e:
            print(f"❌ Health check failed: {e}")
        
        # Test 2: Specific service health
        services = ["mcp", "tone", "ai", "unknown_service"]
        for service in services:
            try:
                request = health_pb2.HealthCheckRequest(service=service)
                response = await stub.Check(request)
                print(f"✅ {service} Health: {response.status} - {response.message}")
            except grpc.RpcError as e:
                print(f"❌ {service} health check failed: {e}")
        
        print("\n=== Testing Health Watch (Streaming) ===")
        
        # Test 3: Health watch streaming
        try:
            request = health_pb2.HealthCheckRequest(service="mcp")
            print(f"👀 Starting health watch for 'mcp' service...")
            
            async for response in stub.Watch(request):
                print(f"📡 Streamed: {response.status} - {response.message}")
                
        except grpc.RpcError as e:
            print(f"❌ Health watch failed: {e}")
        except KeyboardInterrupt:
            print("\n🛑 Health watch interrupted")

if __name__ == '__main__':
    asyncio.run(test_health_client())