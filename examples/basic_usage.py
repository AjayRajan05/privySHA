from privysha import Agent

agent = Agent(
    model="mock",
    privacy=True,
    token_budget=1200
)

query = "Hey bro can you analyze this dataset for anomalies?"

response = agent.run(query, trace=True)

print(response)