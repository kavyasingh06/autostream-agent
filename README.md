AutoStream Social-to-Lead Agent

This repository contains a Conversational AI Sales Agent built for the fictional SaaS product AutoStream, as part of the ServiceHive Inflx internship assignment.

The agent converts social conversations into qualified business leads using intent detection, RAG, stateful reasoning, and tool execution.

🚀 How to Run the Project Locally
1. Clone the Repository
git clone https://github.com/your-username/autostream-agent.git
cd autostream-agent

2. Create Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Mac/Linux

3. Install Dependencies
pip install -r requirements.txt

4. Set API Key (Example for Groq / OpenAI)
setx GROQ_API_KEY "your_api_key_here"


Restart terminal after setting the key.

5. Run the Agent
python main.py

🧠 Architecture Explanation 

This project uses LangGraph to design a stateful, agentic conversational workflow instead of a simple linear chatbot. LangGraph was chosen because it allows explicit control over conversation flow using graph-based nodes, making it ideal for multi-step business logic such as intent detection, retrieval, and tool execution.

The architecture consists of multiple nodes:

Intent Node: Classifies user intent into greeting, product inquiry, or high-intent lead.

RAG Node: Retrieves pricing and policy information from a local knowledge base using vector similarity search.

Lead Node: Handles lead qualification by collecting name, email, and platform details.

Tool Node: Executes the mock lead capture API only when all required information is collected.

State management is handled using LangGraph’s built-in memory with a MemorySaver checkpointer. This allows the agent to retain conversation history and user details across multiple turns. Messages are stored using LangChain message objects, enabling consistent reasoning over previous interactions.

By separating responsibilities into nodes, the agent remains modular, interpretable, and easy to extend. This mirrors real-world production agent architectures used in customer support and sales automation systems.

📱 WhatsApp Deployment Using Webhooks

To integrate this agent with WhatsApp, the WhatsApp Business API or Twilio WhatsApp API can be used.

Workflow:

User sends a WhatsApp message.

WhatsApp sends the message to our backend via a webhook.

The webhook server forwards the message to the LangGraph agent.

The agent processes the message and generates a response.

The response is sent back to the user via WhatsApp API.

🎯 Key Capabilities

Intent detection

RAG-based knowledge retrieval

Stateful conversation memory

Conditional tool execution

Lead capture automation

Production-ready architecture

## 🎥 Demo Video
[Click here to watch the Agent in action](PASTE_YOUR_LINK_HERE)

The video demonstrates:
* RAG answering a pricing question.
* Intelligent intent shifting.
* Lead data collection and tool execution.

🏁 Conclusion


This project demonstrates a real-world, deployable agentic workflow suitable for SaaS sales automation and social lead conversion systems.
