import grpc
from concurrent import futures
import base64
import torch
from diffusers import AutoPipelineForText2Image
from app import imagegen_pb2, imagegen_pb2_grpc

from PIL import Image
import io
import logging

logging.basicConfig(level=logging.INFO)

class ImageGen(imagegen_pb2_grpc.ImageGenServiceServicer):
    def __init__(self):
        try:
            logging.info("Loading model...")
            self.pipe = AutoPipelineForText2Image.from_pretrained(
                r"F:\model\Dreamshaper 8", torch_dtype=torch.float32
            ).to("cpu")
            logging.info("Model loaded successfully.")
        except Exception as e:
            logging.error(f"Failed to load model: {e}")
            raise e

    def GenerateImage(self, request, context):
        if not request.prompt.strip():
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Prompt is empty.")
            return imagegen_pb2.ImageResponse(status="error: prompt is empty", image_base64="")

        if request.steps <= 0 or request.steps > 100:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Steps must be between 1 and 100.")
            return imagegen_pb2.ImageResponse(status="error: invalid steps", image_base64="")

        try:
            logging.info(f"Generating image for prompt: {request.prompt} with steps={request.steps}")
            image = self.pipe(request.prompt, num_inference_steps=request.steps).images[0]

            buf = io.BytesIO()
            image.save(buf, format="PNG")
            img_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')

            return imagegen_pb2.ImageResponse(status="success", image_base64=img_b64)

        except Exception as e:
            logging.error(f"Inference error: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error during inference: {str(e)}")
            return imagegen_pb2.ImageResponse(status=f"error: {str(e)}", image_base64="")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    imagegen_pb2_grpc.add_ImageGenServiceServicer_to_server(ImageGen(), server)
    
    PORT = 8080
    server.add_insecure_port(f"[::]:{PORT}")
    print(f"\n✅ gRPC server is running on port {PORT}...\n")
    
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
