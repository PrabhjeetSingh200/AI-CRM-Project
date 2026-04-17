from langgraph.graph import StateGraph
from typing import TypedDict
import google.generativeai as genai
import json
import re

# 🔥 Gemini setup (PUT YOUR REAL API KEY)
genai.configure(api_key="YOUR_API_KEY_HERE")

# ✅ USE THIS MODEL (IMPORTANT)
model = genai.GenerativeModel("gemini-1.5-flash")

# ✅ State
class State(TypedDict):
    input: str
    extracted: dict
    sentiment: str
    action: str

# 🔥 Step 1: Extract Data
def extract_data(state: State):
    prompt = f"""
    Extract structured data from the text below.

    Text: {state['input']}

    Return ONLY valid JSON:
    {{
      "hcp_name": "",
      "interaction_type": "",
      "topics_discussed": "",
      "sentiment": "",
      "follow_up": ""
    }}
    """

    response = model.generate_content(prompt)
    text = response.text

    match = re.search(r"\{[\s\S]*\}", text)

    if match:
        try:
            data = json.loads(match.group())
        except:
            data = {}
    else:
        data = {}

    return {"extracted": data}

# 🔥 Step 2: Sentiment
def analyze_sentiment(state: State):
    text = state["input"]

    prompt = f"Classify sentiment as Positive, Negative or Neutral: {text}"

    response = model.generate_content(prompt)

    return {"sentiment": response.text.strip()}

# 🔥 Step 3: Action
def suggest_action(state: State):
    sentiment = state["sentiment"]

    if "Positive" in sentiment:
        action = "Schedule follow-up meeting"
    elif "Negative" in sentiment:
        action = "Send detailed info and re-engage"
    else:
        action = "Send brochure"

    return {"action": action}

# 🔥 Step 4: Final Output
def final_node(state: State):
    return {
        "extracted": state.get("extracted", {}),
        "sentiment": state.get("sentiment", ""),
        "action": state.get("action", "")
    }

# ✅ GRAPH BUILD
builder = StateGraph(State)

builder.add_node("extract", extract_data)
builder.add_node("sentiment", analyze_sentiment)
builder.add_node("action", suggest_action)
builder.add_node("final", final_node)

builder.set_entry_point("extract")

builder.add_edge("extract", "sentiment")
builder.add_edge("sentiment", "action")
builder.add_edge("action", "final")

builder.set_finish_point("final")

# ✅ COMPILE LAST
graph = builder.compile()