# 🧞‍♂️ AdGenie: AI-Powered Dynamic Creative Optimization (DCO)

![AdGenie Banner](https://raw.githubusercontent.com/jacknayem/AdGenie/refs/heads/main/src/generated_ad.png)

**AdGenie** is a programmatic advertising prototype that simulates real-time Dynamic Creative Optimization (DCO). Instead of serving static ads to audiences, AdGenie ingests mock user clickstream data, uses LLMs to infer the user's psychological visual preference, and generates a personalized product image and headline on the fly.

> 🎥 **[Watch the Video Demo Here]** *(https://www.loom.com/share/4a05f3d23f8c41c3922525ff60f04b09)*

## 🚀 Features

* **Real-Time Style Inference:** Reads a user's browsing history (e.g., "browsed gaming keyboards") and automatically deduces the most effective visual aesthetic (e.g., "Cyberpunk").
* **Generative AI Creative:** Bypasses static image libraries by writing highly specific prompts and generating custom product photography using open-source image models.
* **Context-Aware Copywriting:** Generates punchy, persona-specific headlines to match the inferred visual style.
* **Session State Management:** Built with Streamlit, handling robust session state to allow smooth user-switching in a live demo environment.

## 🛠️ Tech Stack

* **Frontend:** Streamlit (Python)
* **Agent Logic:** LangChain & Groq (Llama 3 70B for ultra-low latency inference)
* **Vision / Image Generation:** Pollinations AI (API-less Image Generation)
* **Data Processing:** Pandas (Ingesting user clickstream datasets)

## 🧠 Architecture: How It Works

1. **The Cache:** The app reads simulated cookie/clickstream data from a local dataset (`data/user_data.py`).
2. **The Inference (Groq/Llama 3):** The agent analyzes the user's history and acts as a Consumer Psychologist to determine the optimal visual style (Minimalist, Cyberpunk, Nature, etc.).
3. **The Director:** Llama 3 writes a high-fidelity image prompt incorporating the product and the predicted style, alongside a targeted headline.
4. **The Artist:** The prompt is sent to an open-source image generation model to render the final ad creative.

## 💻 How to Run Locally

If you want to test the DCO engine on your local machine, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/jacknayem/AdGenie.git](https://github.com/jacknayem/AdGenie.git)
   cd AdGenie
