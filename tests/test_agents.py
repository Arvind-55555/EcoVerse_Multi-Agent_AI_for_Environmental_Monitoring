# Unit Test
import pytest
import asyncio
from src.core.agent_communication import MessageBroker, Message, MessageType, MessagePriority
from src.agents.implementations import SensingAgent, AnalysisAgent

@pytest.mark.asyncio
async def test_agent_communication():
    broker = MessageBroker()
    
    sensing = SensingAgent("sensing_test", broker, ["sensor_001"])
    analysis = AnalysisAgent("analysis_test", broker)
    
    # Register agents
    broker.register_agent("sensing_test")
    broker.register_agent("analysis_test")
    
    # Test message sending
    message = Message(
        id="test_msg_1",
        sender="sensing_test",
        receiver="analysis_test",
        type=MessageType.DATA,
        priority=MessagePriority.HIGH,
        payload={"temperature": 25.5},
        timestamp="2025-01-01T00:00:00"
    )
    
    success = await broker.send_message(message)
    assert success is True
    
    # Test message receiving
    received = await broker.receive_message("analysis_test", timeout=1.0)
    assert received is not None
    assert received.payload["temperature"] == 25.5

@pytest.mark.asyncio
async def test_data_collection():
    broker = MessageBroker()
    sensing = SensingAgent("sensing_test", broker, ["sensor_001"])
    
    data = await sensing.collect_data()
    
    assert "timestamp" in data
    assert "sensor_id" in data
    assert "measurements" in data
    assert "temperature" in data["measurements"]

#Integration Test
@pytest.mark.asyncio
async def test_full_pipeline():
    """Test complete data flow from sensing to alert"""
    broker = MessageBroker()
    
    sensing = SensingAgent("sensing", broker, ["sensor_001"])
    analysis = AnalysisAgent("analysis", broker)
    alert = AlertAgent("alert", broker)
    
    # Start agents
    tasks = [
        asyncio.create_task(sensing.start()),
        asyncio.create_task(analysis.start()),
        asyncio.create_task(alert.start())
    ]
    
    # Wait for processing
    await asyncio.sleep(10)
    
    # Check statistics
    assert sensing.stats['messages_sent'] > 0
    assert analysis.stats['messages_received'] > 0
    
    # Cleanup
    await sensing.stop()
    await analysis.stop()
    await alert.stop()
    
    for task in tasks:
        task.cancel()
