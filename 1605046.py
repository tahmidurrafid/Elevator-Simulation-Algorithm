from typing import List
import numpy

class Elevator:
    def __init__(self):
        self.operation_time = 0
        self.next_available_time = 0
        self.max_load_times_count = 0
        self.stops_count = 0
        self.total_available_time = 0
        self.trip_count = 0
        self.total_load_count = 0

    def print(self):
        print("This is an elevator")

class Customer:
    def __init__(self, max_floor, arrival):
        self.floor = numpy.random.randint(2, max_floor+1)
        self.arrival = arrival
        self.delay = 0
        self.elevator_time = 0
        self.delivery_time = 0 #delay + elevator

    def print(self):
        print("This is a customer")

class Simulation:
    def __init__(self):
        self.elevator_count = 4
        self.simulation_termination = 10000
        self.floor_count = 12
        self.eleveator_capacity = 4
        self.batch_size = 6
        self.door_holding_time = 15
        self.interfloor_travelling_time = 5
        self.opening_time = 3
        self.closing_time = 3
        self.emberking_time = 3
        self.disemberking_time = 3
        self.mean_interarrival_time = 30

    def initiate(self):
        self.time = 0

    def run(self):
        print("Running Simualation")

# arr:List[Simulation] = List()

sim = Simulation()
sim.run()

print(numpy.random.randint(1, 3))