import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import chainlit as cl
from agno.agent import RunResponse
from typing import Iterator

from app.services.bot_factory import BotFactory

# Initialize Factory and Bot
factory = BotFactory()
agent = factory.build_agent()

@cl.on_message
async def on_message(message: cl.Message):
    """Handles incoming messages from the user in Chainlit with streaming response."""

    # Create a new message for streaming response
    msg = cl.Message(content="")
    await msg.send()
    
    # Stream response
    response_stream: Iterator[RunResponse] = agent.run(message.content, stream=True)
    for chunk in response_stream:
        await msg.stream_token(chunk.content)
    
    # Complete the message stream
    await msg.update()
