from customer import Customer
from environment import QueueEnvironment
from server import Server

servers = [
    Server("Alice", skill=1.0, is_specialist=False),
    Server("Bob", skill=1.2, is_specialist=True),
    Server("Charlie", skill=0.8, is_specialist=False),
    Server("Diana", skill=1.5, is_specialist=True)
]

env = QueueEnvironment(servers, max_queue_size=5)

# just dummy customers for testing, they will be created in the for loop with randomized parameters for the RL model
env.add_customer(Customer("A", 4.0, 0.2, 1.0))
env.add_customer(Customer("B", 8.0, 0.5, 2.0))
env.add_customer(Customer("C", 2.0, 0.1, 1.0))
env.add_customer(Customer("D", 10.0, 0.6, 0.0))
env.add_customer(Customer("E", 6.0, 0.3, 3.0))

for _ in range(5):
    state, reward, done, info = env.step()

    print(f"Time={state['time']}")
    print(f"Queue length: {state['queue_length']}")
    print("Queue:", state['queue'])
    print("-" * 40)
