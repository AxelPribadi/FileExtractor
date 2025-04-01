from typing import Iterator
from agno.agent import Agent, RunResponse, AgentKnowledge
from agno.models.openai import OpenAIChat
from agno.utils.pprint import pprint_run_response
from agno.vectordb.lancedb import LanceDb
from agno.vectordb.search import SearchType
from agno.embedder.openai import OpenAIEmbedder
from chatbot.bot.config import settings


vdb = LanceDb(
    table_name="test",
    uri=settings.LANCE_DB_URI,
    search_type=SearchType.vector,
    embedder=OpenAIEmbedder(api_key=settings.OPENAI_API_KEY)
)

knowledge_base = AgentKnowledge(vector_db=vdb)

agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini", api_key=settings.OPENAI_API_KEY),
    knowledge=knowledge_base,
    description="You are a helpful assistant who knows a lot about deepfakes.",
    search_knowledge=True,
    markdown=True
)


# Run agent and return the response as a variable
# response: RunResponse = agent.run("Tell me a 5 second short story about a robot")
# Run agent and return the response as a stream
response_stream: Iterator[RunResponse] = agent.run("What is DF-GANEXT's limitations", stream=True)

# Print the response in markdown format
# pprint_run_response(response, markdown=True)
# Print the response stream in markdown format
pprint_run_response(response_stream, markdown=True)





