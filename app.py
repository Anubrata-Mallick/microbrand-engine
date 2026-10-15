import os
import asyncio
import threading
import streamlit as st
import sentry_sdk
from dotenv import load_dotenv
from src.memory import FrameworkBrandMemory
from src.graph import create_brand_engine_graph
from src.audio import generate_voiceover

load_dotenv()

# --- SENTRY INITIALIZATION ---
sentry_dsn = os.getenv("SENTRY_DSN")
if sentry_dsn:
    sentry_sdk.init(
        dsn=sentry_dsn,
        traces_sample_rate=1.0,
    )

st.set_page_config(page_title="MicroBrand Voice Engine", page_icon="✨", layout="wide")

st.title("✨ MicroBrand Voice Engine")
st.caption("Agentic Multi-Platform Copy Generator with Persistent Memory, Audio Preview & Compliance Guardrails")

# Helper to run async tasks cleanly in a dedicated, isolated thread
def run_async(coro):
    """Runs an async coroutine safely inside Streamlit without closing active loops."""
    result = None
    error = None

    def target():
        nonlocal result, error
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(coro)
        except Exception as e:
            error = e
        finally:
            loop.close()

    thread = threading.Thread(target=target)
    thread.start()
    thread.join()

    if error:
        raise error
    return result

# Do NOT cache BackboardClient across global Streamlit runs to prevent stale httpx connections
def get_graph():
    return create_brand_engine_graph()

graph_app = get_graph()

# --- SIDEBAR: Brand Workspace & Memory Configuration ---
with st.sidebar:
    st.header("🏢 Brand Memory Workspace")
    
    brand_action = st.radio("Brand Configuration:", ["Select Existing Brand ID", "Create New Brand Profile"])
    
    if brand_action == "Create New Brand Profile":
        new_brand_name = st.text_input("Brand Name", placeholder="e.g. Nordic Peak Gear")
        tone_rule = st.text_area("Brand Tone & Persona", "Minimalist, adventurous, honest, quiet confidence.")
        forbidden_rules = st.text_area("Forbidden Words / Phrasing", "cheap, bargain, crazy sale, hurry")
        signature_phrase = st.text_input("Signature Tagline / Slogan", "Built for the wild.")
        
        if st.button("Save Brand to Memory", type="primary"):
            if new_brand_name:
                with st.spinner("Writing brand rules to Backboard memory..."):
                    # Fresh memory client instance for the thread
                    memory_manager = FrameworkBrandMemory()
                    assistant_id = run_async(memory_manager.initialize_assistant(new_brand_name))
                    run_async(memory_manager.save_brand_rule(assistant_id, f"Tone: {tone_rule}", "tone"))
                    run_async(memory_manager.save_brand_rule(assistant_id, f"Forbidden: {forbidden_rules}", "forbidden"))
                    run_async(memory_manager.save_brand_rule(assistant_id, f"Signature: {signature_phrase}", "signature"))
                    st.session_state["active_brand_id"] = assistant_id
                    st.success(f"Registered! Assistant ID: `{assistant_id}`")
            else:
                st.error("Please enter a brand name.")
                
        active_brand_id = st.session_state.get("active_brand_id", "")
    else:
        active_brand_id = st.text_input("Enter Assistant/Brand ID", value=st.session_state.get("active_brand_id", "d7d981ae-41ce-46a0-ac07-d4ead2c79d18"))
        st.session_state["active_brand_id"] = active_brand_id

    st.divider()
    st.markdown("**Sponsors Integrated:**")
    st.markdown("- 💾 **Backboard**: Persistent Agent Memory")
    st.markdown("- 🔊 **ElevenLabs**: Social Voiceover Synthesis")
    st.markdown("- 📡 **Sentry**: Trace & Latency Telemetry")
    st.markdown("- ☁️ **Render**: Cloud Agent Runtime")

# --- MAIN WORKSPACE: Inputs & Execution ---
col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    st.subheader("📦 Product Details")
    product_title = st.text_input("Product Title", placeholder="e.g. Wabi-Sabi Stoneware Mug")
    
    features_input = st.text_area(
        "Key Features / Specifications (one per line)",
        placeholder="Hand-thrown ceramic\n120ml capacity\nMatte charcoal glaze\nMicrowave safe",
        height=150
    )
    
    platforms = st.multiselect(
        "Target Platforms",
        options=["shopify", "instagram", "amazon", "x"],
        default=["shopify", "instagram"]
    )
    
    generate_btn = st.button("Generate On-Brand Copy", type="primary", use_container_width=True)

with col2:
    st.subheader("📋 Output & Compliance")
    
    # Preserve generated outputs in Streamlit session state across button clicks (audio reruns)
    if "latest_state" not in st.session_state:
        st.session_state["latest_state"] = None

    if generate_btn:
        if not active_brand_id:
            st.error("Please provide or create an active Brand ID in the sidebar.")
        elif not product_title:
            st.error("Please enter a product title.")
        elif not platforms:
            st.error("Please select at least one target platform.")
        else:
            features = [f.strip() for f in features_input.split("\n") if f.strip()]
            
            initial_state = {
                "brand_id": active_brand_id,
                "product_title": product_title,
                "product_features": features,
                "target_platforms": platforms,
                "brand_profile": None,
                "generated_copies": {},
                "critique_feedback": None,
                "is_approved": False,
                "logs": []
            }
            
            with st.spinner("Executing LangGraph pipeline with Backboard memory..."):
                final_state = run_async(graph_app.ainvoke(initial_state))
                st.session_state["latest_state"] = final_state

    # Render results from session state
    active_result = st.session_state.get("latest_state")
    if active_result:
        if active_result.get("is_approved"):
            st.success(f"✅ {active_result.get('critique_feedback')}")
        else:
            st.warning(f"⚠️ {active_result.get('critique_feedback')}")
        
        copies = active_result.get("generated_copies", {})
        if copies:
            channels = list(copies.keys())
            tabs = st.tabs([p.upper() for p in channels])
            for idx, channel in enumerate(channels):
                copy_text = copies[channel]
                with tabs[idx]:
                    st.text_area(f"{channel.capitalize()} Copy", value=copy_text, height=180, key=f"text_{channel}")
                    
                    # ElevenLabs Audio Preview Button
                    if st.button(f"🔊 Listen to {channel.capitalize()} Voiceover", key=f"audio_btn_{channel}"):
                        with st.spinner("Synthesizing voiceover with ElevenLabs..."):
                            try:
                                audio_bytes = generate_voiceover(copy_text)
                                st.audio(audio_bytes, format="audio/mp3")
                            except Exception as e:
                                st.error(f"Audio generation error: {e}")
        
        with st.expander("🔍 View Execution Logs & Memory Retrieval"):
            for log in active_result.get("logs", []):
                st.write(f"- {log}")