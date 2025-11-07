# Agent wiring using OpenAI Agents SDK
instructions="""
You are GreenMind Coordinator. Orchestrate: DataIngestor -> Analyzer -> Planner -> Executor -> Reporter.
Given user goal, call the appropriate agents and return a JSON summary.
"""
)


# For simple prototype we'll represent other agents as thin wrappers


data_ingestor_agent = Agent(
name="DataIngestor",
instructions="""
Fetch data for a given region using the data_ingestor.fetch_forest_cover function.
Return a compact JSON with fields required by Analyzer.
""",
tools=[fetch_forest_cover]
)


analyzer_agent = Agent(
name="Analyzer",
instructions="""
Analyze metrics and detect anomalies. Return analysis with keys: is_anomaly, percent_change.
""",
tools=[detect_anomaly]
)


planner_agent = Agent(
name="Planner",
instructions="""
Create a mitigation plan from analysis output.
""",
tools=[build_plan]
)


executor_agent = Agent(
name="Executor",
instructions="""
Execute plan actions (create ticket, notify Slack) and return execution results.
""",
tools=[execute_actions]
)


reporter_agent = Agent(
name="Reporter",
instructions="""
Generate a human-friendly report (markdown or plain text) summarizing metrics, analysis, plan, execution.
""",
tools=[make_report]
)


# Wire handoffs
coordinator.handoffs = [data_ingestor_agent, analyzer_agent, planner_agent, executor_agent, reporter_agent]