# from typing import Iterator
# from agno.agent import Agent, RunResponse
# import chainlit as cl
# from chatbot.bot.agno_bot import AgnoFactory
# from chatbot.core.config import settings

# @cl.on_message
# async def on_message(message: cl.Message):

#     # send message to AGNO Agent (connected to lanceDB for context) + chat history
#     current_user = cl.user_session.get("user")
#     current_session = message.thread_id

#     factory = AgnoFactory()
#     agent = factory.get_agent(
#         user_id=current_user,
#         session_id=current_session
#     )

#     response_stream: Iterator[RunResponse] = agent.run(message.content, stream=True)
#     response_message = cl.Message(content="")

#     # send response to chainlit
#     async for chunk in response_stream:
#         response_message.content += chunk.text
#         await response_message.update()

#     await response_message.send()


import sys
import subprocess

def run_chainlit():
    subprocess.run()
