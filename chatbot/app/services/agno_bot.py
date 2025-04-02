
from agno.agent import Agent, AgentKnowledge, RunResponse
from agno.models.openai import OpenAIChat
from agno.vectordb.lancedb import LanceDb
from agno.vectordb.search import SearchType
from agno.embedder.openai import OpenAIEmbedder

from app.core.config import settings

class AgnoFactory:
    def __init__(self, vector_table: str = "test", system_rule: str = None):
        self.vector_table = vector_table
        self.system_rule = system_rule

    def get_knowledge(self):
        vector_db = LanceDb(
            table_name=self.vector_table,
            uri=settings.LANCE_DB_URI,
            search_type=SearchType.vector,
            embedder=OpenAIEmbedder(api_key=settings.OPENAI_API_KEY)
        )

        knowledge_base = AgentKnowledge(vector_db=vector_db)
        return knowledge_base
    
    async def get_agent(self):
        agent = Agent(
            model=OpenAIChat(id="gpt-4o-mini", api_key=settings.OPENAI_API_KEY),
            description=self.system_rule,
            knowledge=self.get_knowledge(),
            add_history_to_messages=True,
            markdown=True
        )

        return agent
    

    