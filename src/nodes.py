import os
import json
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq
from src.state import AgentState
from src.memory import FrameworkBrandMemory

# Initialize our memory framework instance
memory_manager = FrameworkBrandMemory()

def get_llm():
    """Initializes the chat model backend."""
    # Reads Groq API key or swaps cleanly with other providers
    api_key = os.getenv("GROQ_API_KEY")
    return ChatGroq(
        model_name="openai/gpt-oss-120b",
        temperature=0.3,
        groq_api_key=api_key
    )

async def recall_memory_node(state: AgentState) -> AgentState:
    """Node 1: Retrieves brand guidelines and rules from persistent memory."""
    brand_id = state.get("brand_id", "default_brand")
    
    # Initialize fresh instance per graph call to prevent event loop connection reuse
    memory_manager = FrameworkBrandMemory()
    rules = await memory_manager.get_brand_context(assistant_id=brand_id)
    
    # Categorize and populate brand profile in state
    state["brand_profile"] = {
        "brand_id": brand_id,
        "brand_name": brand_id.replace("_", " ").title(),
        "tone": [r for r in rules if "tone:" in r.lower()],
        "forbidden_words": [r for r in rules if "forbidden:" in r.lower() or "never:" in r.lower()],
        "target_audience": "Defined in persistent memory profile",
        "signature_phrase": next((r for r in rules if "signature:" in r.lower()), "")
    }
    
    state["logs"].append(f"Successfully retrieved {len(rules)} memory rules for brand '{brand_id}'.")
    return state

async def generate_copy_node(state: AgentState) -> AgentState:
    """Node 2: Generates channel-specific copy conditioned on brand memory."""
    llm = get_llm()
    brand_rules = state.get("brand_profile", {})
    features_list = state.get("product_features", [])
    features_text = "\n- ".join(features_list) if features_list else "Standard specifications"
    platforms = ", ".join(state.get("target_platforms", ["shopify", "instagram"]))
    
    prompt = f"""
    You are an expert e-commerce copywriter.
    
    BRAND GUIDELINES FROM PERSISTENT MEMORY:
    - Tone rules: {brand_rules.get('tone', ['Authentic and direct'])}
    - Forbidden words: {brand_rules.get('forbidden_words', ['None'])}
    - Signature phrase: {brand_rules.get('signature_phrase', '')}
    
    PRODUCT DETAILS:
    - Product: {state.get('product_title')}
    - Key Features:
    - {features_text}
    
    TARGET CHANNELS:
    {platforms}
    
    INSTRUCTIONS:
    Write copy specifically tailored to each requested channel while strictly obeying all brand guidelines.
    Return ONLY a valid JSON object where keys are the channel names (e.g. "shopify", "instagram") and values are the generated copy strings.
    """
    
    messages = [
        SystemMessage(content="You generate platform-specific e-commerce copy adhering strictly to brand memory constraints. Output valid JSON only."),
        HumanMessage(content=prompt)
    ]
    
    response = await llm.ainvoke(messages)
    
    try:
        # Strip potential markdown code block markers
        cleaned = response.content.replace("```json", "").replace("```", "").strip()
        state["generated_copies"] = json.loads(cleaned)
    except Exception:
        # Fallback if raw text returned
        state["generated_copies"] = {"raw_output": response.content}
        
    state["logs"].append("Draft copy generated for requested platforms.")
    return state

async def brand_critique_node(state: AgentState) -> AgentState:
    """Node 3: Validates drafts against forbidden vocabulary and brand rules."""
    copies = state.get("generated_copies", {})
    forbidden = state.get("brand_profile", {}).get("forbidden_words", [])
    
    violations = []
    combined_text = " ".join(str(v) for v in copies.values()).lower()
    
    for rule in forbidden:
        clean_word = (
            rule.replace("forbidden:", "")
                .replace("never:", "")
                .strip()
                .lower()
        )
        if clean_word and clean_word in combined_text:
            violations.append(clean_word)
            
    if violations:
        state["is_approved"] = False
        state["critique_feedback"] = f"Forbidden terms detected: {', '.join(violations)}. Needs revision."
        state["logs"].append(f"Critique flagged violations: {violations}")
    else:
        state["is_approved"] = True
        state["critique_feedback"] = "Approved: Perfectly aligned with brand memory."
        state["logs"].append("Critique passed: Output compliant.")
        
    return state