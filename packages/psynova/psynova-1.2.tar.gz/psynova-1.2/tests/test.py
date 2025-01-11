from psynova import PsynovaClient


client = PsynovaClient("SXZNq32YEkXBJM6NrQ4JXLQrNU8wqjGWxsd8L1M63M5Y2Q4Mr3w4HuJMn34HfDPK68QTYxZeCngfYmc7TJKkkv2")
# agent_id = client.create_agent(name="sdfssdf", version_id=1)
agents = client.list_agents()
for agent in agents:
    print(agent)
# res = client.chat(agent_id, message='who r u?')
# print(res)
