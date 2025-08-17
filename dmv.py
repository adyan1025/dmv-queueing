import random
from customer import Customer
from worker import Worker

def priority_score(customer, w1, w2, worker):
    service_time = customer.base_complexity * worker.skill_multiplier
    if not worker.is_specialist:
        service_time *= (1 + customer.complication_prob)
    return w1 * customer.fairness_credit - w2 * service_time

def compute_reward(customers, served_customers):
    # Fairness: average fairness of all customers
    avg_fairness = sum(c.fairness_credit for c in customers) / len(customers)
    
    # Efficiency: number of customers served weighted by inverse service time
    efficiency = 0
    for c, service_time in served_customers:
        efficiency += 1 / service_time

    # Total reward
    lambda_fairness = 1.0
    lambda_efficiency = 1.0
    total_reward = lambda_fairness * avg_fairness + lambda_efficiency * efficiency
    return total_reward, avg_fairness, efficiency

def step(customers, workers, current_time, alpha, beta, dt, w1, w2):
    served_customers = []

    # update workers
    for worker in workers:
        if worker.current_customer:
            worker.busy_time -= dt
            if worker.busy_time <= 0:
                # record served customer for reward
                service_time = worker.current_customer.base_complexity * worker.skill_multiplier
                if not worker.is_specialist:
                    service_time *= (1 + worker.current_customer.complication_prob)
                served_customers.append((worker.current_customer, service_time))

                worker.current_customer.finished = True
                worker.current_customer.current_worker = None
                worker.current_customer = None

    # active customers
    active_customers = [c for c in customers if c.arrival_time <= current_time and not c.finished]

    # update fairness
    for customer in active_customers:
        if customer.current_worker is None:
            customer.waiting_time += dt
            customer.skipped_events += 1
            customer.update_fairness(alpha, beta, dt)

    # assign free workers
    free_workers = [w for w in workers if w.current_customer is None]
    waiting_customers = [c for c in active_customers if c.current_worker is None]

    for worker in free_workers:
        if waiting_customers:
            print(f"\nWorker {worker.name} evaluating waiting customers at time {current_time}:")
            for c in waiting_customers:
                service_time = c.base_complexity * worker.skill_multiplier
                if not worker.is_specialist:
                    service_time *= (1 + c.complication_prob)
                score = priority_score(c, w1, w2, worker)
                print(f"  {c.name}: fairness={c.fairness_credit:.2f}, "
                      f"service_time={service_time:.2f}, priority={score:.2f}")
            
            chosen_customer = max(waiting_customers, key=lambda c: priority_score(c, w1, w2, worker))
            worker.assign_customer(chosen_customer, dt)
            waiting_customers.remove(chosen_customer)

    # compute reward
    total_reward, avg_fairness, efficiency = compute_reward(customers, served_customers)
    print(f"\n--- Reward at time {current_time} ---")
    print(f"Average fairness: {avg_fairness:.2f}")
    print(f"Efficiency (served weighted by 1/service_time): {efficiency:.2f}")
    print(f"Total reward: {total_reward:.2f}\n")
    return total_reward

# CUSTOMERS: short low-fairness and long high-fairness to see the effect
customers = [
    Customer("A", 12, 0.2, arrival_time=0),  # long, high complexity
    Customer("B", 2, 0.1, arrival_time=0),   # short, low complexity
    Customer("C", 5, 0.3, arrival_time=1),
    Customer("D", 6, 0.4, arrival_time=2)
]

# WORKERS: only 2 to force queueing
workers = [
    Worker("Alice", 1.0, False),
    Worker("Charlie", 1.2, False)
]

alpha = 1
beta = 2
# tweak weights to favor service time strongly
w1, w2 = 1, 10
dt = 1

for t in range(30):
    reward = step(customers, workers, t, alpha, beta, dt, w1, w2)
    active_customers = [c for c in customers if c.arrival_time <= t and not c.finished]
    if not active_customers and all(c.finished or c.arrival_time > t for c in customers):
        print(f"All customers finished by time {t+1}")
        break
    print(f"Time {t+1}")
    for c in active_customers:
        worker_name = c.current_worker.name if c.current_worker else "None"
        print(f"{c.name}: fairness={c.fairness_credit:.2f}, worker={worker_name}")
    print("-"*40)