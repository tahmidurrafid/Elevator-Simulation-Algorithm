from typing import List
import numpy
from numpy import random
from numpy.core.fromnumeric import cumprod

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
        print(self.passenger_count)

    def init_passenger_count(self, capacity):
        self.passenger_count = []
        self.first_customer = -1
        self.current_load = 0
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

    def pop(self):
        self.length -= 1
        if self.length != 0:
            self.front += 1
        else:
            self.front = 0

    def print(self):
        print("This is queue")


class Simulation:
    def __init__(self):
        self.elevator_count = 4
        self.simulation_termination = 4800
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
        self.passenger_count = 0
        self.queue = Queue()
        self.customers:List[Customer] = list()
        self.elevators:List[Elevator] = list()
        self.opened_elevator = -1
        for i in range(0, self.elevator_count):
            elevator = Elevator()
            self.elevators.append(elevator)
            elevator.init_passenger_count(self.elevator_capacity)

    def run(self):
        self.initiate()
        iteration = 0
        while(self.time < self.simulation_termination):
            iteration += 1
            print(str(iteration) + "========================")
            availableElevatorIndex = self.getAvailableElevetorIndex()
            if(availableElevatorIndex != -1):
                customer = self.nextPassenger()
                elevator = self.elevators[availableElevatorIndex]
                if elevator.current_load == 0:
                    elevator.first_customer = self.passenger_count
                elevator.current_load += 1
                self.passenger_count += 1
                self.customer_count = max(self.passenger_count, self.customer_count)
                if(customer.from_queue):
                    self.queue.pop()
                    next_time = self.time + self.emberking_time
                    self.openQueue(next_time)
                    self.time = next_time
                else:
                    self.time = customer.arrival
                customer.elevator_in_time = self.time
                elevator.passenger_count[customer.floor] += 1

                if elevator.current_load == self.elevator_capacity or self.nextPassenger().arrival > self.time + self.door_holding_time:
                    for k in range(elevator.first_customer, elevator.first_customer + elevator.current_load):
                        customer = self.customers[k]
                        N = customer.floor - 1
                        floor_open_before = 0
                        passenger_drop_before = 0
                        for i in range(0, customer.floor):
                            floor_open_before += 1 if elevator.passenger_count[i] > 0 else 0
                            passenger_drop_before +=  elevator.passenger_count[i]
                        customer.elevator_time = self.interfloor_travelling_time*N + \
                            (floor_open_before + 1)*self.opening_time + floor_open_before*self.closing_time + \
                                (passenger_drop_before+1)*self.disemberking_time
                        customer.delivery_time = customer.elevator_time + (self.time - customer.elevator_in_time) + self.door_holding_time
                    max_floor = 1
                    total_stops = 0
                    for i in range(0, self.floor_count+1):
                        if elevator.passenger_count[i] > 0:
                            max_floor = i
                            total_stops += 1
                    elevator.trip_count += 1
                    elevator.stops_count += total_stops
                    opearation_time = (max_floor-1)*2*self.interfloor_travelling_time + total_stops*(self.opening_time + self.closing_time) + \
                        elevator.current_load*self.disemberking_time
                    elevator.operation_time += opearation_time
                    elevator.next_available_time = self.time + self.door_holding_time + opearation_time
                    self.opened_elevator = -1
                    print("Elevator will go: " + str(availableElevatorIndex))
                    elevator.init_passenger_count(self.elevator_capacity)
            else:
                print("push to queue")
                self.openQueue(self.nextElevatorTime())
            print(self.passenger_count)

    def openQueue(self, upto_time):
        nextCustomer = self.nextCustomer()
        while upto_time >= nextCustomer.arrival:
            if(self.queue.empty()):
                self.queue.front = self.customer_count
            nextCustomer.from_queue = True
            self.queue.length += 1
            self.customer_count += 1
            nextCustomer = self.nextCustomer()
        if(self.getAvailableElevetorIndex() == -1):
            self.time = self.nextElevatorTime()

    def getAvailableElevetorIndex(self):
        if self.opened_elevator != -1:
            return self.opened_elevator
        for i in range(0, self.elevator_count):
            if(self.elevators[i].next_available_time <= self.time):
                self.opened_elevator = i
                return i
        return -1
    def getBetweenTime(self) -> int:
        # return int(-numpy.log(random.random())*self.mean_interarrival_time)
        return numpy.random.randint(0, 31)

    def nextElevatorTime(self):
        minTime = numpy.Inf
        for i in range(0, self.elevator_count):
            minTime = min(minTime, self.elevators[i].next_available_time)
        return minTime

    def nextPassenger(self)->Customer:
        if(self.customer_count == self.passenger_count):
            return self.nextCustomer()
        return self.customers[self.passenger_count]

    def nextCustomer(self)->Customer:
        customer = None
        if self.customer_count == len(self.customers):
            timeOffset = self.customers[self.customer_count-1].arrival if self.customer_count > 0 else 0
            customer = Customer(self.floor_count, timeOffset + self.getBetweenTime() )
            self.customers.append(customer)
        else:
            customer = self.customers[self.customer_count]
        return customer

# arr:List[Simulation] = List()

sim = Simulation()
sim.run()