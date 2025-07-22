import grpc
import pytest
from app import imagegen_pb2, imagegen_pb2_grpc
from concurrent import futures
from app.server import ImageGen

class DummyServer:
    def __init__(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        imagegen_pb2_grpc.add_ImageGenServiceServicer_to_server(ImageGen(), self.server)
        port = self.server.add_insecure_port("[::]:0")
        self.server.start()
        self.port = port
        self.channel = grpc.insecure_channel(f"localhost:{port}")
        self.stub = imagegen_pb2_grpc.ImageGenServiceStub(self.channel)

    def stop(self):
        self.server.stop(0)

@pytest.fixture(scope="module")
def grpc_stub():
    server = DummyServer()
    yield server.stub
    server.stop()

def test_valid_prompt(grpc_stub):
    response = grpc_stub.GenerateImage(imagegen_pb2.ImageRequest(prompt="sunset", steps=10))
    assert response.status == "success"
    assert response.image_base64 != ""
    assert len(response.image_base64) > 1000

def test_empty_prompt(grpc_stub):
    with pytest.raises(grpc.RpcError) as exc_info:
        grpc_stub.GenerateImage(imagegen_pb2.ImageRequest(prompt="", steps=10))
    assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT
    assert "Prompt is empty" in exc_info.value.details()

def test_invalid_steps(grpc_stub):
    with pytest.raises(grpc.RpcError) as exc_info:
        grpc_stub.GenerateImage(imagegen_pb2.ImageRequest(prompt="cat", steps=-5))
    assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT

def test_long_prompt(grpc_stub):
    long_prompt = "A beautiful futuristic city at night" * 30
    response = grpc_stub.GenerateImage(imagegen_pb2.ImageRequest(prompt=long_prompt, steps=15))
    assert response.status == "success"
    assert len(response.image_base64) > 1000
