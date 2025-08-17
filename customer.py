class Customer:
    def __init__(self, name, base_complexity, complication_prob, arrival_time):
        self.name = name
        self.base_complexity = base_complexity
        self.complication_prob = complication_prob
        self.arrival_time = arrival_time
        self.fairness_credit = 0
        self.waiting_time = 0
        self.skipped_events = 0
        self.current_worker = None
        self.finished = False

    def update_fairness(self, alpha, beta, dt):
        self.fairness_credit += alpha * dt + beta * self.skipped_events
        self.skipped_events = 0