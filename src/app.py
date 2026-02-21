import streamlit as st
from agent import run_campaign_agent
from user_interest import retive_user_interest
from PIL import Image

# Page Config
st.set_page_config(page_title="AdGenie Agent", layout="wide")
st.title("AdGenie: Ad Designer")
st.markdown("### Powered by ChatGroq (Logic), Flux.1 (Vision) & FAISS (Memory)")

if 'user_history' not in st.session_state:
    st.session_state.user_history = None

# Sidebar for inputs
with st.sidebar:
    time_frequency = st.selectbox("Time Frame", ["ME", "W", "3D", "1D"])
    user_btn = st.button("Pick User History", type="primary")
    if user_btn:
       with st.spinner("Retrieving a user and finding the highest interest..."):
           st.session_state.user_history = retive_user_interest(time_frequency)
    if st.session_state.user_history is not None:
        st.success(f"The user_{st.session_state.user_history['user_id']} mostly views {st.session_state.user_history['category_code']}")

    #=============================================================
    st.header("Campaign Settings")

    # Input 1: The Persona (Triggers Retrieval)
    #persona = st.text_input("Describe the Target Audience:", "A busy college student who loves coffee")
    if st.session_state.user_history is not None:
        persona = f"The user_{st.session_state.user_history['user_id']} mostly views {st.session_state.user_history['category_code']}"
    else:
        persona = "A busy college student who loves coffee"

    # Input 2: Optional Override
    manual_prod = st.text_input("Product Override (Optional)", "")

    style = st.selectbox("Visual Style", 
        ["Cinematic (Dramatic)", 
         "Minimalist (Clean)", 
         "Cyberpunk (Neon)", 
         "Nature (Organic)"]
    )

    launch_btn = st.button("Generate Campaign", type="primary")

if launch_btn:
    with st.spinner("Agent is retrieving products and designing assets..."):
        try:
            prod_input = manual_prod if manual_prod.strip() != "" else None
            result = run_campaign_agent(persona, prod_input, style)

            # Layout
            col1, col2 = st.columns([1, 1])
            with col1:
                st.subheader("Generated Creative")
                st.image(result['image_path'], caption=f"Style: {style}", use_container_width=True)

            with col2:
                st.subheader("Campaign Strategy")
                st.success(f"**Product Selected:** {result['product_name']}")
                st.info(f"**Context:** {result['product_desc']}")
                st.markdown(f"**Headline:** *\"{result['headline']}\"*")

                with st.expander("View Agent Reasoning (Trace)"):
                    st.code(result['reasoning'], language="text")
        except Exception as e:
            st.error(f"Error: {e}")