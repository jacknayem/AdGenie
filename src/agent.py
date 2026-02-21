#from langchain_community.llms import Ollama
from langchain_groq import ChatGroq
from retrieval import get_best_product
from generator import generate_banner
import os

# Log in: https://console.groq.com/login ; get the GROQ_API_KEY
os.environ["GROQ_API_KEY"] = "PASTE HERE"
llm = ChatGroq(model_name="llama-3.3-70b-versatile")

def run_campaign_agent(user_persona, manual_product = None, visual_style="Cinematic"):

    # 1: RETRIEVAL (RAG)
    if not manual_product:
        product_data = get_best_product(user_persona)
        product_name = product_data['name']
        product_desc = product_data['desc']
    else:
        product_name = manual_product
        product_desc = "A revolutionary new product"

    # 2: PLANNING (The Agentic Reasoning)
    prompt = f"""
    Role: Senior Art Director.
    Task: Create a visual ad concept.
    
    Context:
    - Target Audience: {user_persona}
    - Product: {product_name} ({product_desc})
    - Visual Style: {visual_style}
    
    Requirements:
    1. HEADLINE: A catchy, short headline (max 6 words).
    2. PROMPT: A detailed Stable Diffusion prompt describing the product in a scene matching the '{visual_style}' style. Do NOT ask for text in the image.
    
    Output Format (Strictly):
    HEADLINE: [Your headline here]
    PROMPT: [Your visual prompt here]
    """
    response = llm.invoke(prompt).content

    # 3: PARSING
    lines = response.split('\n')
    headline = f"Discover {product_name}"
    image_prompt = f"Product shot of {product_name}, {visual_style} lighting"

    for line in lines:
        if "HEADLINE:" in line:
            headline = line.replace("HEADLINE:", "").strip().replace('"', '')
        if "PROMPT:" in line:
            image_prompt = line.replace("PROMPT:", "").strip()

    # 4: EXECUTION (Generating the Asset)
    print(f"Agent Plan -> Headline: {headline} | Prompt: {image_prompt}")
    image_path = generate_banner(image_prompt, headline)

    return {
        "product_name": product_name,
        "product_desc": product_desc,
        "headline": headline,
        "image_path": image_path,
        "reasoning": response
    }