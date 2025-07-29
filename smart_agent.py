import os
import uuid
import sqlite3
import json
from datetime import datetime
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# ✅ Load environment variables
load_dotenv()

# ✅ Initialize GPT-4 model
llm = ChatOpenAI(temperature=0.3, model_name="gpt-4")

# ✅ Setup SQLite DB
conn = sqlite3.connect("hiring_data.db", check_same_thread = False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS structured_data (
    session_id TEXT,
    timestamp TEXT,
    industry TEXT,
    location TEXT,
    roles TEXT,
    number_of_positions INTEGER,
    urgency BOOLEAN
)''')
conn.commit()

# ✅ Function 1: Extract hiring info from client input
def extract_hiring_info(user_input):
    prompt = f"""
You are a helpful assistant that extracts structured hiring details from client conversations.

Extract these fields from the input:
- industry
- location
- roles (as array of strings)
- number_of_positions (sum of all roles)
- urgency (true if the message says urgent/immediate/asap, false if it says not urgent or no time frame or no deadline)

Return ONLY valid JSON.

Examples:
1.
Input: "We need 3 backend developers and 2 UI/UX designers urgently in Mumbai for a fintech startup."
Output:
{{
  "industry": "fintech",
  "location": "Mumbai",
  "roles": ["backend developer", "UI/UX designer"],
  "number_of_positions": 5,
  "urgency": true
}}

2.
Input: "We're hiring 4 delivery leads in Bangalore. No urgency or deadline, we’re flexible."
Output:
{{
  "industry": "",
  "location": "Bangalore",
  "roles": ["delivery lead"],
  "number_of_positions": 4,
  "urgency": false
}}

Now extract from:
\"\"\"{user_input}\"\"\"
"""
    messages = [SystemMessage(content=prompt)]
    response = llm(messages)
    try:
        return json.loads(response.content)
    except json.JSONDecodeError:
        print("❌ Failed to parse JSON from model response")
        return {}

# ✅ Function 2: Recommend hiring service
def recommend_service_gpt(data):
    """
    Uses GPT-4 to recommend the best hiring service based on extracted client data.
    """
    industry = data.get("industry", "")
    location = data.get("location", "")
    roles = data.get("roles", [])
    count = data.get("number_of_positions", 1)
    urgency = data.get("urgency", False)

    prompt = f"""
You are a smart recruiter assistant at a hiring agency.
Client Info:
- Industry: {industry}
- Location: {location}
- Roles: {roles}
- Number: {count}
- Urgent: {urgency}

Your job is to look at the client's hiring need and suggest the **most suitable service** from this list ONLY:

1. Tech Startup Hiring Pack  
2. Sales & Support Pack  
3. Enterprise Bulk Hiring Pack  
4. Custom Hiring Solution  

Read the client's extracted hiring info below and recommend **only ONE** service that best fits their needs.

Think practically, match roles, urgency, size, and type of client.

Return only the service name.
    """
    messages = [SystemMessage(content=prompt)]
    response = llm(messages)
    return response.content.strip()

# ✅ Function 3: Generate proposal
def generate_proposal(data, service):
    """
    Generate a friendly, chat-style proposal pitch that includes:
    - Why the service fits the client's needs
    - Brief overview of what the service includes
    - Invitation to schedule a call
    """
    prompt = f"""
You are an AI sales assistant at a hiring agency, chatting with a client on a business messaging platform.
Client Info:
- Industry: {data.get("industry")}
- Location: {data.get("location")}
- Roles: {', '.join(data.get("roles", []))}
- Number: {data.get("number_of_positions")}
- Urgent: {data.get("urgency")}
Based on this, you are recommending: **{service}**

Write a natural, chat-style proposal that:
1. Thanks them for reaching out
2. Clearly explains WHY this service fits their situation
3. Briefly explains WHAT the service includes (e.g. expert sourcing, speed, role-matching, dedicated recruiter, etc.)
4. Expresses confidence that your agency can deliver
5. Asks if they’d like to schedule a quick call with an expert to proceed

Don’t make it sound like a formal email. Make it a confident yet helpful 5–8 sentence **live message**.
Avoid bullet points and keep it flowing like real conversation.
    """
    messages = [SystemMessage(content=prompt)]
    response = llm(messages)
    return response.content.strip()

# ✅ Function 4: Follow-up message
def generate_follow_up_loop(user_reply, proposal, chat_history):
    prompt = f"""
You are an AI Sales Assistant at a recruitment agency. Your job is to help clients with hiring solutions only.

You should ONLY answer questions related to hiring, recruitment, or staffing needs.

If the client asks something unrelated (like coding, weather, general queries), politely respond that you specialize in recruitment and hiring, and redirect them back to hiring discussion.
Below is your chat:
{chat_history}

You had sent this proposal:
\"\"\"{proposal}\"\"\"

Client replied:
\"\"\"{user_reply}\"\"\"

Reply in a friendly, helpful, confident tone. Keep the tone chatty and natural. Be concise and suggest a suitbale proposal.  
If client sounds satisfied or ends with a goodbye, thank them and end the conversation.
    """
    messages = [SystemMessage(content=prompt)]
    response = llm(messages)
    return response.content.strip()

# ✅ Function 5: Log structured info to DB
def log_structured_data(session_id, data):
    timestamp = datetime.now().isoformat()
    industry = data.get("industry", "")
    location = data.get("location", "")
    roles = ", ".join(data.get("roles", []))
    count = data.get("number_of_positions", 0)
    urgency = data.get("urgency", False)

    cursor.execute("""
        INSERT INTO structured_data (
            session_id, timestamp, industry, location, roles, number_of_positions, urgency
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (session_id, timestamp, industry, location, roles, count, urgency))
    conn.commit()

# ✅ Function 6: Save conversation log
def save_conversation_log(history):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"conversation_log_{timestamp}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(history))
    print(f"✅ Saved: {filename}")
