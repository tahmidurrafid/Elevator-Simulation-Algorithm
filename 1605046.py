from typing import List
import numpy
from numpy import floor, random

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
        self.longest = 0
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
        self.mean_interarrival_time = 90
    
    def takeInput(self):
        input = open("input.txt", "r")
        line = input.readline()
        self.simulation_termination = int(line)
        line = input.readline()
        x = line.split(" ")
        self.floor_count = int(x[0])
        self.elevator_count = int(x[1])
        self.elevator_capacity = int(x[2])
        self.batch_size = int(x[3])
        line = input.readline()
        x = line.split(" ")
        self.door_holding_time = int(x[0]) 
        self.interfloor_travelling_time = int(x[1])
        self.opening_time = int(x[2])
        self.closing_time = int(x[3])
        line = input.readline()
        x = line.split(" ")
        self.emberking_time = int(x[0])
        self.disemberking_time = int(x[1])
        line = input.readline()
        self.mean_interarrival_time = float(line)*60

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
                        customer.delivery_time = customer.elevator_time + (self.time - customer.arrival) + self.door_holding_time
                        customer.delay = customer.elevator_in_time - customer.arrival
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
                    elevator.total_load_count += elevator.current_load
                    elevator.next_available_time = self.time + self.door_holding_time + opearation_time
                    self.opened_elevator = -1
                    if(elevator.current_load == self.elevator_capacity):
                        elevator.max_load_times_count += 1
                    elevator.init_passenger_count(self.elevator_capacity)
            else:
                # print("push to queue")
                self.openQueue(self.nextElevatorTime())
        stat = Statistics(self)
        return stat

    def openQueue(self, upto_time):
        nextCustomer = self.nextCustomer()
        while upto_time >= nextCustomer.arrival:
            if(self.queue.empty()):
                self.queue.front = self.customer_count
            nextCustomer.from_queue = True
            self.queue.length += 1
            self.queue.longest = max(self.queue.longest, self.queue.length)
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
        return int(-numpy.log(random.random())*self.mean_interarrival_time)
        # return numpy.random.randint(0, 31)

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
            betweenTime = self.getBetweenTime()
            customer = Customer(self.floor_count, timeOffset + betweenTime)
            self.customers.append(customer)
            for i in range(0, self.batch_size-1):
                if(numpy.random.random() <= .5):
                    customer2 = Customer(self.floor_count, timeOffset + betweenTime)
                    self.customers.append(customer2)
        else:
            customer = self.customers[self.customer_count]
        return customer

class Statistics:
    def __init__(self, sim:Simulation):
        self.sim = sim
        self.totalCustomers = 0
        self.averageQueueLength = 0
        self.maximumQueueLength = 0
        self.averageDelayTime = 0
        self.maximumDelayTime = 0
        self.averageElevatorTime = 0
        self.maximumElevatorTime = 0
        self.averageDeliveryTime = 0
        self.maximumDeliveryTime = 0
        self.loadSize = 0
        self.operationTime = 0
        self.availableTime = 0
        self.numberOfMaxLoads = []
        self.numberOfStops = []
        self.calculate()

    def calculate(self):
        sim = self.sim
        self.totalCustomers = sim.passenger_count
        total = 0
        for i in range(0, sim.passenger_count):
            total += sim.customers[i].delay
            self.maximumDelayTime = max(self.maximumDelayTime, sim.customers[i].delay)
        self.averageDelayTime = total/self.totalCustomers
        self.averageQueueLength = total/sim.time
        self.maximumQueueLength = sim.queue.longest
        total = 0
        for i in range(0, self.totalCustomers):
            total += sim.customers[i].elevator_time
            self.maximumElevatorTime = max(self.maximumElevatorTime, sim.customers[i].elevator_time)
        self.averageElevatorTime = total/self.totalCustomers
        total = 0
        for i in range(0, self.totalCustomers):
            total += sim.customers[i].delivery_time
            self.maximumDeliveryTime = max(self.maximumDeliveryTime, sim.customers[i].delivery_time)
        self.averageDeliveryTime = total/self.totalCustomers
        self.loadSize = [elevator.total_load_count for elevator in sim.elevators]
        self.operationTime = [elevator.operation_time for elevator in sim.elevators]
        self.availableTime = [(sim.time - elevator.operation_time) for elevator in sim.elevators]
        self.numberOfMaxLoads = [elevator.max_load_times_count for elevator in sim.elevators]
        self.numberOfStops = [elevator.stops_count for elevator in sim.elevators]

    def getCSVHeading():
        return "Simulation_Number," + \
        "Total_Customers," + \
        "Avg_Queue_Size," + \
        "Max_Queue_Size," + \
        "Avg_Delay_Time," + \
        "Max_Delay_Time," + \
        "Avg_Elevator_Time," + \
        "Max_Elevator_Time," + \
        "Avg_Delivery_Time," + \
        "Max_Delivery_Time," + \
        "Load_Size," + \
        "Opeation_Time," + \
        "Available Time," + \
        "Max_Loads_Count," + \
        "Stops_Count" 
    
    def arrToStr(arr):
        x = "["
        for i in range(0, len(arr)):
            x += str(arr[i]) + " "
        x +=  "]"
        return x

    def getCSV(self, number):
        return str(number) + "," + \
        str(self.totalCustomers) + "," + \
        str(self.averageQueueLength) + "," + \
        str(self.maximumQueueLength) + "," + \
        str(self.averageDelayTime) + "," + \
        str(self.maximumDelayTime) + "," + \
        str(self.averageElevatorTime) + "," + \
        str(self.maximumElevatorTime) + "," + \
        str(self.averageDeliveryTime) + "," + \
        str(self.maximumDeliveryTime) + "," + \
        str(Statistics.arrToStr(self.loadSize)) + "," + \
        str(Statistics.arrToStr(self.operationTime)) + "," + \
        str(Statistics.arrToStr(self.availableTime)) + "," + \
        str(Statistics.arrToStr(self.numberOfMaxLoads)) + "," + \
        str(Statistics.arrToStr(self.numberOfStops))

    def print(self):
        for i in range(0, self.totalCustomers):
            if(self.sim.customers[i].arrival > self.sim.customers[i].elevator_in_time):
                print(str(i) + " == ")
        print("Total customers: " + str(self.totalCustomers))
        print("Average Queue Length: " + str(self.averageQueueLength))
        print("Maximum Queue Length: " + str(self.maximumQueueLength))
        print("Average Delay Time: " + str(self.averageDelayTime))
        print("Maximum Delay Time: " + str(self.maximumDelayTime))
        print("Average Elevator Time: " + str(self.averageElevatorTime))
        print("Maximum Elevator Time: " + str(self.maximumElevatorTime))
        print("Average Delivery Time: " + str(self.averageDeliveryTime))
        print("Maximum Delivery Time: " + str(self.maximumDeliveryTime))
        print("Average load: " + str(self.loadSize))
        print("Operation Time: " + str(self.operationTime))
        print("Available Time: " + str(self.availableTime))
        print("Max Load Time: " + str(self.numberOfMaxLoads))
        print("Number of stops: " + str(self.numberOfStops))

sim = Simulation()
sim.takeInput()
stats = []
output = Statistics.getCSVHeading() + "\n"
for i in range(0, 10):
    stat = sim.run()
    stats.append(stat)
    output += stats[i].getCSV(i+1) + "\n"
outfile = open("output2.csv", "w")
outfile.write(output)
outfile.close()
