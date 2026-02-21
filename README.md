# AdGenie: AI-Powered Dynamic Creative Optimization (DCO)

![AdGenie Banner](https://raw.githubusercontent.com/jacknayem/AdGenie/refs/heads/main/src/generated_ad.png)

**AdGenie** is a programmatic advertising prototype that simulates real-time Dynamic Creative Optimization (DCO). Instead of serving static ads to audiences, AdGenie ingests mock user clickstream data, uses LLMs to infer the user's psychological visual preference, and generates a personalized product image and headline on the fly.

> **[Watch the Video Demo Here]** *(https://www.loom.com/share/4a05f3d23f8c41c3922525ff60f04b09)*

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

## How to Run Locally

If you want to test the DCO engine on your local machine, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/jacknayem/AdGenie.git](https://github.com/jacknayem/AdGenie.git)
   cd AdGenie
2. **Set up a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt`
4. **Add your HuggingFace API Key:**
   Open `generator.py` and insert your free Groq API key where indicated.
   1. **STEP1**: huggingface.co/login
   2. **STEP2**: Settings -> Access Tokens -> Create new token -> Read -> Token Name (Copy the Token)
6. **Add your Groq API Key:**
   Open `agent.py` and insert your free Groq API key where indicated.
   1. **Log in**: https://console.groq.com/login
   2. **API Key** get the GROQ_API_KEY
7. **Download Data:**
   1. **[flipkart_com-ecommerce_sample]** *(https://www.kaggle.com/datasets/atharvjairath/flipkart-ecommerce-dataset)*
   2. **[eCommerce behavior data]** *(https://www.kaggle.com/datasets/mkechinov/ecommerce-behavior-data-from-multi-category-store)*
   3. Put data in `Data Folder`
   4. Do not forget to define the path or file name in code source
8. **Run the application:**
   ```bash
   python user_interest.py
   streamlit run src/app.py`
