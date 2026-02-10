import torch
from diffusers import FluxPipeline

# Load the model
pipe = FluxPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-schnell",
    torch_dtype=torch.bfloat16
)

# Move to GPU (cuda) or Mac (mps)
device = "mps" if torch.backends.mps.is_available() else "cuda"
pipe.to(device)

def generate_banner(prompt_text, filename = "generated_ad.png"):
    image = pipe(
        prompt_text,
        guidance_scale=0.0,
        num_inference_steps = 4,
        max_sequence_length=256,
        generator=torch.Generator("cpu").manual_seed(42)
    ).images[0]

    image.save(filename)
    return filename