import asyncio
from src.core.agent_communication import MessageBroker
from src.agents.implementations import (
    SensingAgent, AnalysisAgent, AlertAgent, CoordinationAgent
)

class AgentManager:
    def __init__(self, config):
        self.config = config
        self.broker = MessageBroker()
        self.agents = {}
    
    async def initialize_agents(self):
        """Initialize all agents based on configuration"""
        
        # Create Sensing Agents
        if self.config['agents']['sensing']['enabled']:
            for i in range(self.config['agents']['sensing']['count']):
                agent = SensingAgent(
                    f"sensing_agent_{i}",
                    self.broker,
                    self.config['agents']['sensing']['sensor_ids']
                )
                self.agents[agent.agent_id] = agent
        
        # Create Analysis Agent
        if self.config['agents']['analysis']['enabled']:
            agent = AnalysisAgent("analysis_agent", self.broker)
            self.agents[agent.agent_id] = agent
        
        # Create Alert Agent
        if self.config['agents']['alert']['enabled']:
            agent = AlertAgent("alert_agent", self.broker)
            self.agents[agent.agent_id] = agent
        
        # Create Coordination Agent
        if self.config['agents']['coordination']['enabled']:
            agent = CoordinationAgent("coordination_agent", self.broker)
            self.agents[agent.agent_id] = agent
    
    async def start_all_agents(self):
        """Start all initialized agents"""
        tasks = [
            asyncio.create_task(agent.start())
            for agent in self.agents.values()
        ]
        return tasks
    
    async def stop_all_agents(self):
        """Stop all agents gracefully"""
        for agent in self.agents.values():
            await agent.stop()
