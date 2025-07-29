# ai-sales-agent
An AI-powered sales assistant that engages clients, understands hiring needs, and delivers tailored recruitment proposals with conversational follow-ups.

\# 🤖 Smart Hiring Agent



An AI-powered assistant for recruiting agencies that chats with clients, understands their hiring needs, recommends suitable hiring solutions, and logs structured data — all through a conversational interface.



---



\## 🚀 Features



\- \*\*Natural Language Input\*\*: Clients can describe their hiring needs casually.

\- \*\*Automatic Extraction\*\*: Extracts roles, location, number of positions, and urgency from client input.

\- \*\*Smart Recommendations\*\*: Suggests the most suitable hiring service based on extracted data.

\- \*\*Proposal Generation\*\*: Drafts a friendly, human-like proposal message.

\- \*\*Follow-up Handling\*\*: Engages in back-and-forth conversation, redirects if off-topic.

\- \*\*Persistent Logging\*\*:

&nbsp; - Structured hiring details logged into a SQLite database

&nbsp; - Full chat conversation saved as `.txt` logs with timestamps

\- \*\*Streamlit Interface\*\*: Clean and chat-like UI for demo and testing

\- \*\*Modular Codebase\*\*: Separated backend and frontend (`smart\_agent.py` \& `smart\_agent\_app.py`)



---



\## 🧠 How It Works



1\. Client enters hiring requirements.

2\. The agent extracts structured data and suggests a matching hiring service.

3\. A proposal is generated and shown.

4\. The client can chat further, and the agent responds conversationally.

5\. The session is logged both in `.txt` and `.db` format.



---



\## Project Structure

┣ 📜 smart\_agent.py # Core logic: extraction, proposal, follow-up, logging

┣ 📜 smart\_agent\_app.py # Streamlit UI for chat interface

┣ 📜 view\_structured\_log.py #code to view the structured log

┣ 📜 hiring\_data.db# SQLite DB storing structured hiring data

┣ 📜 conversation\_log\_\*.txt # Text logs of each client conversation

┣ 📜 README.md




