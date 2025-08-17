class Server:
    def __init__(self, name, skill=1.0, is_specialist=False):
        self.name = name
        self.skill = skill
        self.is_specialist = is_specialist
        self.current_customer = None
        self.remaining_time = 0

    def assign_customer(self, customer):
        self.current_customer = customer
        self.remaining_time = customer.compute_service_time(self.skill, self.is_specialist)

    def step(self):
        if self.current_customer:
            self.remaining_time -= 1
            if self.remaining_time <= 0:
                finished = self.current_customer
                self.current_customer = None
                self.remaining_time = 0
                return finished
        return None