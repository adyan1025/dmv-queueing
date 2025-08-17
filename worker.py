class Worker:
    def __init__(self, name, skill_multiplier, is_specialist=False):
        self.name = name
        self.skill_multiplier = skill_multiplier
        self.is_specialist = is_specialist
        self.busy_time = 0
        self.current_customer = None

    def assign_customer(self, customer, dt):
        self.current_customer = customer
        service_time = customer.base_complexity * self.skill_multiplier
        if not self.is_specialist:
            service_time *= (1 + customer.complication_prob)
        self.busy_time = service_time
        customer.current_worker = self