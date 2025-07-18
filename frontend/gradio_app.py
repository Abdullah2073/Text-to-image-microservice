import grpc
import base64
from PIL import Image
from io import BytesIO
import gradio as gr
from app import imagegen_pb2, imagegen_pb2_grpc

# gRPC Client for interacting with the server
def generate_image_from_grpc(prompt, steps=50):
    try:
        # Establish connection to gRPC server
        channel = grpc.insecure_channel('localhost:8080')
        stub = imagegen_pb2_grpc.ImageGenServiceStub(channel)
        
        # Prepare request
        request = imagegen_pb2.ImageRequest(prompt=prompt, steps=steps)
        
        # Make the gRPC call to generate the image
        response = stub.GenerateImage(request)
        
        if response.status == "success":
            # Decode the base64 image and return as a PIL image
            img_data = base64.b64decode(response.image_base64)
            image = Image.open(BytesIO(img_data))
            return image, "✅ Image generated successfully!"
        else:
            return None, f"❌ Error: {response.status}"
    except Exception as e:
        print(f"Error in gRPC call: {e}")
        return None, "❌ Error in generating image."

# Gradio Interface
with gr.Blocks() as demo:
    # Cute theme with modern design
    gr.Markdown("""
        <h1 style="text-align: center; color: #ff69b4;">🎨 AI Image Generator</h1>
        <p style="text-align: center; font-size: 18px; color: #555;">Enter a prompt, and let the magic happen! ✨</p>
    """)

    with gr.Row():
        # Prompt input (Removed style argument)
        prompt_input = gr.Textbox(
            label="Enter a Prompt", 
            placeholder="Describe your dream image here!", 
            lines=2, 
            max_lines=5,
            interactive=True,
            elem_id="prompt-input",  # Custom styling via external CSS
        )

        # Slider for steps (Removed style argument)
        steps_input = gr.Slider(
            minimum=1, 
            maximum=100, 
            value=50, 
            label="Inference Steps", 
            interactive=True,
            elem_id="steps-input"  # Custom styling via external CSS
        )

    # Generate button with an icon
    generate_btn = gr.Button(
        "Generate Image 🌟", 
        variant="primary", 
        elem_id="generate-btn",  # Custom styling via external CSS
    )

    # Image display area
    image_display = gr.Image(
        type="pil", 
        label="Generated Image", 
        elem_id="image-display", 
        interactive=True,
    )

    # Status label
    status = gr.Label(
        value="ℹ️ Enter a prompt and click Generate.",
        elem_id="status-label",
    )

    # When the button is clicked, call the generate_image_from_grpc function
    generate_btn.click(generate_image_from_grpc, inputs=[prompt_input, steps_input], outputs=[image_display, status])

# Launch Gradio interface and generate a public link
demo.launch(share=True, inbrowser=True)
