class QueueEnvironment:
    def __init__(self, num_servers, max_queue_size=None):
        self.num_servers = num_servers
        self.max_queue_size = max_queue_size
        
        self.servers = [None] * num_servers   # Each slot can hold a customer
        self.queue = []                       # Waiting customers
        self.time = 0                         # Simulation clock
        self.finished_customers = []          # Record of served customers

    def reset(self):
        self.servers = [None] * self.num_servers
        self.queue = []
        self.time = 0
        self.finished_customers = []
        return self._get_state()

    def step(self, action=None):
        for customer in self.queue:
            customer.wait_time += 1

        # TODO: implement processing logic here later
        self.time += 1
        state = self._get_state()
        reward = 0.0
        done = False
        info = {}
        return state, reward, done, info

    def add_customer(self, customer):
        if self.max_queue_size is None or len(self.queue) < self.max_queue_size:
            self.queue.append(customer)
        else:
            customer.dropped = True
            self.finished_customers.append(customer)

    def _get_state(self):
        return {
            "time": self.time,
            "servers": self.servers,
            "queue_length": len(self.queue),
            "queue": self.queue
        }