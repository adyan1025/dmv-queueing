class Customer:
    def __init__(self, name, C, Comp, E):
        self.name = name          # Customer name
        self.C = C                # Base complexity
        self.Comp = Comp          # Complication probability
        self.E = E                # Fairness credit
        self.service_time = 0     # Will be computed later
        self.wait_time = 0        # Tracks time waited

    def update_fairness(self, alpha, beta, skipped=False, delta_t=1.0):
        self.E += alpha * delta_t
        if skipped:
            self.E += beta

    def compute_service_time(self, worker_skill, is_specialist):
        complication_penalty = self.Comp * (1 - int(is_specialist))
        self.service_time = self.C * worker_skill * (1 + complication_penalty)
        return self.service_time

    def __repr__(self):
        return f"[{self.name}] C={self.C} Comp={self.Comp} E={self.E:.3f} Wait={self.wait_time}"