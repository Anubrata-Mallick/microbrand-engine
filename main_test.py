import asyncio
from dotenv import load_dotenv
from src.memory import FrameworkBrandMemory
from src.graph import create_brand_engine_graph

load_dotenv()

async def main():
    print("--- 1. Setting Up Brand Memory in Backboard ---")
    memory = FrameworkBrandMemory()
    
    # Initialize a test brand assistant
    brand_assistant_id = await memory.initialize_assistant("Aura Ceramics")
    print(f"Brand Workspace Created. Assistant ID: {brand_assistant_id}")
    
    # Store explicit voice and restriction rules
    await memory.save_brand_rule(
        brand_assistant_id, 
        "Tone: Earthy, warm, mindful, and craft-centered.", 
        "tone"
    )
    await memory.save_brand_rule(
        brand_assistant_id, 
        "Forbidden: Never use hype words like 'cheap', 'crazy discount', or 'limited stock'.", 
        "forbidden"
    )
    await memory.save_brand_rule(
        brand_assistant_id, 
        "Signature: Crafted slowly by human hands.", 
        "signature"
    )
    print("Brand rules stored in memory.")

    print("\n--- 2. Executing LangGraph Copy Engine ---")
    app = create_brand_engine_graph()

    initial_state = {
        "brand_id": brand_assistant_id,
        "product_title": "Wabi-Sabi Stoneware Mug",
        "product_features": [
            "Hand-thrown on a potter's wheel using speckled clay",
            "Matte oat milk glaze finish",
            "Holds 350ml of your favorite pour-over coffee or tea",
            "Dishwasher and microwave safe"
        ],
        "target_platforms": ["shopify", "instagram"],
        "brand_profile": None,
        "generated_copies": {},
        "critique_feedback": None,
        "is_approved": False,
        "logs": []
    }

    # Run the compiled graph asynchronously
    final_state = await app.ainvoke(initial_state)

    print("\n--- 3. Pipeline Output & Execution Trace ---")
    for log in final_state["logs"]:
        print(f"[Trace] {log}")

    print("\n--- Critique Verdict ---")
    print(f"Approved: {final_state['is_approved']}")
    print(f"Feedback: {final_state['critique_feedback']}")

    print("\n--- Generated Copy per Channel ---")
    for channel, copy_text in final_state["generated_copies"].items():
        print(f"\n[{channel.upper()}]")
        print(copy_text)

if __name__ == "__main__":
    asyncio.run(main())