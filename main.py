import asyncio
import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
import yaml

from src.api.main import app
from src.agents.agent_manager import AgentManager
from src.pipelines.data_pipeline import DataPipeline

# Global instances
agent_manager = None
data_pipeline = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global agent_manager, data_pipeline
    
    # Load configuration
    with open('config/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Initialize components
    print("Starting EcoVerse...")
    
    # Start data pipeline
    data_pipeline = DataPipeline(
        batch_size=config['data_pipeline']['batch_size']
    )
    pipeline_task = asyncio.create_task(data_pipeline.start_processing())
    
    # Initialize and start agents
    agent_manager = AgentManager(config)
    await agent_manager.initialize_agents()
    agent_tasks = await agent_manager.start_all_agents()
    
    print("EcoVerse system started successfully!")
    
    yield
    
    # Shutdown
    print("Shutting down EcoVerse...")
    await data_pipeline.stop_processing()
    await agent_manager.stop_all_agents()
    
    pipeline_task.cancel()
    for task in agent_tasks:
        task.cancel()
    
    print("EcoVerse system stopped.")

app.router.lifespan_context = lifespan

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )# main.py
