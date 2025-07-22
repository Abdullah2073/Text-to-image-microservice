import grpc
import threading
import time
from app import imagegen_pb2, imagegen_pb2_grpc

def send_request(prompt, steps):
    channel = grpc.insecure_channel("localhost:8080")
    stub = imagegen_pb2_grpc.ImageGenServiceStub(channel)
    response = stub.GenerateImage(imagegen_pb2.ImageRequest(prompt=prompt, steps=steps))
    print(response.status)

start_time = time.time()
threads = []
for i in range(10):  # Simulate 10 concurrent users
    t = threading.Thread(target=send_request, args=(f"castle at night {i}", 20))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

end_time = time.time()
print(f"\nTotal time: {end_time - start_time:.2f} seconds")
