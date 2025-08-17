from customer import Customer
from server import Server
from environment import QueueEnvironment

servers = [
    Server("Alice", skill=1.0, is_specialist=False),
    Server("Bob", skill=1.2, is_specialist=True)
]

env = QueueEnvironment(servers, max_queue_size=5)

env.add_customer(Customer("A", 4.0, 0.2, 1.0))
env.add_customer(Customer("B", 8.0, 0.5, 2.0))
env.add_customer(Customer("C", 2.0, 0.1, 1.0))
env.add_customer(Customer("D", 10.0, 0.6, 0.0))
env.add_customer(Customer("E", 6.0, 0.3, 3.0))

for _ in range(10):
    state, reward, done, info = env.step()
    
    print(f"Time={state['time']}")
    print("Servers:")
    for server in state['servers']:
        if server.current_customer:
            print(f"  {server.name} serving {server.current_customer.name}, remaining_time={server.remaining_time}")
        else:
            print(f"  {server.name} is idle")
    
    print("Queue:", [c.name for c in state['queue']])
    print("-" * 40)