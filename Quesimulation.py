import sys
import math
import random
from collections import deque

# Constants
MAX_QUEUE_SIZE = 100
SERVER_BUSY = 1
SERVER_IDLE = 0

class MM1Simulator:
    def __init__(self, input_path, output_path):
        """
        Initializes the MM1 queue simulation with input and output file paths.
        """
        self.input_path = input_path
        self.output_path = output_path

        self.current_time = 0.0
        self.last_event_time = 0.0
        self.queue = deque()
        self.server_state = SERVER_IDLE
        self.total_customers_served = 0
        self.max_customers = 0
        self.customers_in_queue = 0
        self.total_delay_time = 0.0
        self.avg_queue_area = 0.0
        self.avg_server_util = 0.0

        self.arrival_mean = 0.0
        self.service_mean = 0.0

        self.event_schedule = [0.0, 0.0, float('inf')]  # [Unused, Next Arrival, Next Departure]
        self.event_type = None

    def load_input(self):
        try:
            with open(self.input_path, 'r') as f:
                data = f.readline().split()
                if len(data) != 3:
                    raise ValueError("Input file must contain 3 space-separated values.")
                self.arrival_mean = float(data[0])
                self.service_mean = float(data[1])
                self.max_customers = int(data[2])
        except Exception as err:
            print(f"[Error] Failed to load input: {err}", file=sys.stderr)
            sys.exit(1)

    def setup(self):
        self.current_time = 0.0
        self.server_state = SERVER_IDLE
        self.customers_in_queue = 0
        self.total_customers_served = 0
        self.total_delay_time = 0.0
        self.avg_queue_area = 0.0
        self.avg_server_util = 0.0

        self.event_schedule[1] = self.current_time + self.generate_exponential(self.arrival_mean)
        self.event_schedule[2] = float('inf')

    def generate_exponential(self, mean):
        return -mean * math.log(random.random())

    def determine_next_event(self):
        self.event_type = None
        next_time = float('inf')
        for i in range(1, 3):
            if self.event_schedule[i] < next_time:
                next_time = self.event_schedule[i]
                self.event_type = i

        if self.event_type is None:
            print(f"No more events. Simulation time: {self.current_time}", file=sys.stderr)
            sys.exit(1)

        self.current_time = next_time

    def process_arrival(self):
        self.event_schedule[1] = self.current_time + self.generate_exponential(self.arrival_mean)

        if self.server_state == SERVER_BUSY:
            if self.customers_in_queue >= MAX_QUEUE_SIZE:
                print(f"[Overflow] Queue exceeded at time {self.current_time}", file=sys.stderr)
                sys.exit(2)
            self.queue.append(self.current_time)
            self.customers_in_queue += 1
        else:
            self.server_state = SERVER_BUSY
            self.total_customers_served += 1
            self.event_schedule[2] = self.current_time + self.generate_exponential(self.service_mean)

    def process_departure(self):
        if self.customers_in_queue == 0:
            self.server_state = SERVER_IDLE
            self.event_schedule[2] = float('inf')
        else:
            self.customers_in_queue -= 1
            arrival_time = self.queue.popleft()
            delay = self.current_time - arrival_time
            self.total_delay_time += delay
            self.total_customers_served += 1
            self.event_schedule[2] = self.current_time + self.generate_exponential(self.service_mean)

    def update_statistics(self):
        time_elapsed = self.current_time - self.last_event_time
        self.last_event_time = self.current_time

        self.avg_queue_area += self.customers_in_queue * time_elapsed
        self.avg_server_util += self.server_state * time_elapsed

    def write_report(self):
        with open(self.output_path, 'w') as out:
            out.write("\n--- MM1 Simulation Summary ---\n")
            out.write(f"\nTotal customers served: {self.total_customers_served}")
            out.write(f"\nAverage queue delay: {self.total_delay_time / self.total_customers_served:.3f} minutes")
            out.write(f"\nAverage queue length: {self.avg_queue_area / self.current_time:.3f}")
            out.write(f"\nServer utilization: {self.avg_server_util / self.current_time:.3f}")
            out.write(f"\nSimulation ended at: {self.current_time:.3f} minutes\n")

    def simulate(self):
        self.load_input()
        self.setup()

        while self.total_customers_served < self.max_customers:
            self.determine_next_event()
            self.update_statistics()

            if self.event_type == 1:
                self.process_arrival()
            elif self.event_type == 2:
                self.process_departure()

        self.write_report()

if __name__ == "__main__":
    in_file = "mm1.in"
    out_file = "mm1.out"

    # Generate input if missing
    try:
        open(in_file, 'r').close()
    except FileNotFoundError:
        with open(in_file, 'w') as f:
            f.write("1.0 0.5 100")

    sim = MM1Simulator(in_file, out_file)
    sim.simulate()

    print(f"Simulation complete. Results saved in '{out_file}'.")
