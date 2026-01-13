import uuid
from agent.graph import app
from langchain_core.messages import HumanMessage

print("🤖 AutoStream AI Agent Started (Type 'exit' to quit)")

# GENERATE A NEW THREAD ID to avoid loading corrupted memory
thread_id = str(uuid.uuid4())
config = {"configurable": {"thread_id": thread_id}}

while True:
    try:
        user_input = input("\nUser: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            break
        if not user_input:
            continue

        # Prepare the input for the graph
        inputs = {"messages": [HumanMessage(content=user_input)]}

        # Run the graph
        output = app.invoke(inputs, config=config)

        # Get the last message (the agent's reply)
        last_msg = output["messages"][-1].content
        print(f"\nAgent: {last_msg}")

    except Exception as e:
        print(f"❌ Error details: {e}")
        # If it crashes, generate a new ID to reset state
        thread_id = str(uuid.uuid4())
        config = {"configurable": {"thread_id": thread_id}}
        print("🔄 Resetting conversation memory...")