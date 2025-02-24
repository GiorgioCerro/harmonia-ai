import chainlit as cl
from harmonia_ai.harmonia import HarmoniA

# Initialize HarmoniA
harmonia = HarmoniA()

@cl.on_message
async def main(message: cl.Message):
    """
    Handles user messages in Chainlit while maintaining memory.
    """

    # Retrieve stored messages (initialize if empty)
    stored_messages = cl.user_session.get("messages", [])
    stored_messages.append(message.content)  # Add new message

    

    try:
        # Stream responses from HarmoniA
        async for response in harmonia.ask_harmonia("\n".join(stored_messages)):  
            await cl.Message(content=response).send()

            # Store updated memory back into the session
            stored_messages.append(response)
            cl.user_session.set("messages", stored_messages)
        print("---")
        print(stored_messages)
        print("---")
    except Exception as e:
        await cl.Message(content=f"Error: {str(e)}").send()