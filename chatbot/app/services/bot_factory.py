from agno.agent import Agent, AgentKnowledge
from agno.models.openai import OpenAIChat
from agno.embedder.openai import OpenAIEmbedder
from agno.vectordb.lancedb import LanceDb
from agno.vectordb.search import SearchType

from app.core.config import settings

class BotFactory:
    def __init__(self, system_rule: str = None):
        self.table_name = settings.LANCE_DB_TABLE_NAME
        self.system_rule = system_rule if system_rule else settings.DEFAULT_SYSTEM_RULE
        self.model = settings.OPENAI_MODEL
        self.embedder = settings.OPENAI_EMBEDDER
    
    def build_knowledge_base(self):
        vector_db = LanceDb(
            table_name=self.table_name,
            uri=settings.LANCE_DB_URI,
            search_type=SearchType.vector,
            embedder=OpenAIEmbedder(
                id= self.embedder,
                api_key=settings.OPENAI_API_KEY
            )
        )
        
        knowledge_base = AgentKnowledge(vector_db=vector_db)
        return knowledge_base

    def build_agent(self):
        agent = Agent(
            model=OpenAIChat(id=self.model, api_key=settings.OPENAI_API_KEY),
            knowledge=self.build_knowledge_base(),
            description=self.system_rule,
            search_knowledge=True,
            markdown=True
        )

        return agent
