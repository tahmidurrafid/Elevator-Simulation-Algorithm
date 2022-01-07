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
        self.current_load = 0
    def print(self):
        print("This is an elevator")
    def init_passenger_count(self, capacity):
        self.passenger_count = []
        for i in range(0, capacity+1):
            self.passenger_count.append(0)

class Customer:
    def __init__(self, max_floor, arrival):
        self.floor = numpy.random.randint(2, max_floor+1)
        self.arrival = arrival
        self.elevator_in_time = 0
        self.delay = 0
        self.elevator_time = 0
        self.delivery_time = 0 #delay + elevator
        self.from_queue = False

    def print(self):
        print("Customer: arrival - " + str(self.arrival)) 


class Queue:
    def __init__(self):
        self.front = 0
        self.length = 0
        self.start_time = 0
        self.total_time = 0
        self.total_customer_time = 0
        
    def empty(self):
        return self.length == 0

    def print(self):
        print("This is queue")


class Simulation:
    def __init__(self):
        self.elevator_count = 4
        self.simulation_termination = 10000
        self.floor_count = 12
        self.elevator_capacity = 12
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
        self.customer_count = 0
        self.queue = Queue()
        self.customers:List[Customer] = list()
        self.elevators:List[Elevator] = list()
        self.opened_elevator = -1
        for i in range(0, self.elevator_count):
            self.elevators.append(Elevator())

    def run(self):
        print("Running Simualation")
        self.initiate()
        print(self.nextCustomer().arrival)
        print(self.getAvailableElevetorIndex())
        iteration = 0
        while(self.time < self.simulation_termination and iteration < 10):
            iteration += 1
            print(str(iteration) + "========================")
            nextEventTime = 0
            availableElevatorIndex = self.getAvailableElevetorIndex()
            if(self.queue.empty() and availableElevatorIndex != -1):
                print("Straight to the elevator")
                customer = self.nextCustomer()
                elevator = self.elevators[availableElevatorIndex]
                customer.print()
                self.customer_count += 1
                elevator.current_load += 1
                self.time = customer.arrival
                if elevator.current_load == self.elevator_capacity or self.nextCustomer().arrival > self.time + self.door_holding_time:
                    print("Elevator is full")

            else:
                print("push to queue")

            continue
            elevatorIndex = self.getAvailableElevetorIndex()
            if elevatorIndex != -1:
                elevator = self.elevators[elevatorIndex]
                elevator.current_load += 1
                customer = self.nextCustomer()
                self.time = customer.arrival
                customer.elevator_in_time = self.time
                self.customer_count += 1
                # if self.nextCustomer().arrival > self.time + self.door_holding_time
            else:
                self.queue.print()

    def getAvailableElevetorIndex(self):
        if self.opened_elevator != -1:
            return self.opened_elevator
        for i in range(0, self.elevator_count):
            if(self.elevators[i].next_available_time <= self.time):
                self.opened_elevator = i
                return i
        return -1
    def nextElevatorTime(self):
        minTime = numpy.Inf
        for i in range(0, self.elevator_count):
            minTime = min(minTime, self.elevators[i].next_available_time)
        return minTime

    def nextCustomer(self)->Customer:
        customer = None
        if self.customer_count == len(self.customers):
            timeOffset = self.customers[self.customer_count-1].arrival if self.customer_count > 0 else 0
            customer = Customer(self.floor_count, timeOffset + numpy.random.randint(0, self.mean_interarrival_time+1))
            self.customers.append(customer)
        else:
            customer = self.customers[self.customer_count]
        return customer

# arr:List[Simulation] = List()

sim = Simulation()
sim.run()