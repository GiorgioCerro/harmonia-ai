import chainlit as cl
from harmonia_ai.harmonia import HarmoniA

# Initialize HarmoniA
harmonia = HarmoniA()

@cl.step(type="tool")
async def tool():
    # Fake tool
    await cl.sleep(2)
    return "Response from the tool!"


@cl.on_message  # this function will be called every time a user inputs a message in the UI
async def main(message: cl.Message):
    """
    This function is called every time a user inputs a message in the UI.
    It sends back an intermediate response from the tool, followed by the final answer.

    Args:
        message: The user's message.

    Returns:
        None.
    """

    # Send an intermediate message
    await cl.Message(content="Thinking...").send()

    # Get response from HarmoniA
    response = await harmonia.ask_harmonia(message.content)

    # Send the final response
    await cl.Message(content=response).send()
