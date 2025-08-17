class QueueEnvironment:
    def __init__(self, servers, max_queue_size=None):
        self.servers = servers
        self.max_queue_size = max_queue_size
        self.queue = []
        self.time = 0
        self.finished_customers = []

    # not sure how to fix this just yet
    # def reset(self):
    #     self.servers = [None] * self.num_servers
    #     self.queue = []
    #     self.time = 0
    #     self.finished_customers = []
    #     return self._get_state()

    def step(self, action=None):
        for customer in self.queue:
            customer.wait_time += 1

        for server in self.servers:
            finished = server.step()
            if finished:
                self.finished_customers.append(finished)

        for server in self.servers:
            if server.current_customer is None and self.queue:
                next_customer = self.queue.pop(0)
                server.assign_customer(next_customer)

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