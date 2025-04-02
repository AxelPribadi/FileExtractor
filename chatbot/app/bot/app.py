
import chainlit as cl
from agno.agent import Agent, AgentKnowledge, RunResponse
from agno.models.openai import OpenAIChat
from agno.vectordb.lancedb import LanceDb
from agno.vectordb.search import SearchType
from agno.embedder.openai import OpenAIEmbedder
from app.core.config import settings

# Initialize the AGNO Agent
knowledge_base = AgentKnowledge(
    vector_db = LanceDb(
        table_name="test",
        uri=settings.LANCE_DB_URI,
        search_type=SearchType.vector,
        embedder=OpenAIEmbedder(api_key=settings.OPENAI_API_KEY)
    )
)

agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini", api_key=settings.OPENAI_API_KEY),
    knowledge=knowledge_base,
    description="You are a helpful assistant who knows a lot about deepfakes.",
    search_knowledge=True,
    markdown=True
)

@cl.on_message
async def on_message(message: cl.Message):
    """Handles incoming messages from the user in Chainlit."""

    # Get user input
    user_input = message.content

    # Run the agent and get the response (no streaming)
    response: RunResponse = agent.run(user_input)

    # Extract the response content (use the correct attribute)
    response_text = response.content

    # Send response back to the user
    await cl.Message(content=response_text).send()
