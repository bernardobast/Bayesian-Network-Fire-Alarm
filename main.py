#!/usr/bin/env python

import probability
from itertools import product

T = True
F = False

class Problem:

    def __init__(self, fh):

        # Place here your code to load problem from opened file object fh
        # and use probability.BayesNet() to create the Bayesian network

        self.rooms = []
        self.corridors = {}
        self.prop_prob = 0
        #List that sensors and its values
        self.sensors =[]
        #dictionary storing every sensor per room
        self.sensor_room = {}
        #Every measurement
        self.measurements = {}
        #Stores the baysian net
        self.bayesnet = 0
        #Counts the numberm or measures/time isinstances
        self.time_intances = 0
        info = fh.readlines()

        for i in range(len(info)):

            # Reads the first character
            data_type = info[i][0]
            # String containing all the needed data
            data = info[i]

            # If its an room
            if data_type == 'R':
                str_ = data.split()
                #print(str)
                for k in range(1, len(str_)):
                    self.rooms.append(str_[k])

            # If its a corridor
            if data_type == 'C':
                str_ = data.split()
                aux = []
                aux2 = []
                #print(str)
                for k in range(1, len(str_)):
                    str_2 = str_[k].split(',')
                    #If room not in corridors
                    if str_2[0] not in self.corridors:
                        self.corridors[str_2[0]] = []
                    if str_2[1] not in self.corridors:
                        self.corridors[str_2[1]] = []
                    self.corridors[str_2[0]].append(str_2[1])
                    self.corridors[str_2[1]].append(str_2[0])


            # If its a sensor
            if data_type == 'S':
                str_ = data.split()
                for k in range(1, len(str_)):
                    str_2 = str_[k].split(':')
                    #Iniates the list for each room
                    if str_2[1] not in self.sensor_room.keys():
                        self.sensor_room[str_2[1]] = []
                    self.sensors.append([str_2[0], str_2[1], float(str_2[2]), float(str_2[3])])
                    self.sensor_room[str_2[1]].append([str_2[0], float(str_2[2]), float(str_2[3])])

            # If data is a measurement
            if data_type == 'M':
                #Increments time instances
                self.time_intances += 1
                #Gets individual measures
                str_ = data.split()
                #self.measurements[l] = []
                for k in range(1, len(str_)):
                    str_2 = str_[k].split(':')
                    #Converts sting into boolean
                    if(str_2[1] == 'T'):
                        sensor_measure = T
                    else:
                        sensor_measure = F
                    #Sensor name + Time instance, with given value
                    self.measurements[str_2[0]+'_'+str(self.time_intances)]= sensor_measure

            # If data is a probability
            if data_type == 'P':
                str_ = data.split()
                self.prop_prob = float(str_[1])

    def solve(self):
        # Place here your code to determine the maximum likelihood solution
        # returning the solution room name and likelihood
        # use probability.elimination_ask() to perform probabilistic inference

        #Initiates the bays net
        self.bayesnet = probability.BayesNet()
        #Creates the first rooms
        for room in self.rooms:
            #name + time instance
            room = room + '_1'
            self.bayesnet.add([room,'',0.5])

        #Creates the first sensors
        for sensor in self.sensors:
            #name + time instance
            son = sensor[0] + '_1'
            #name + time instance
            parent =  sensor[1]+'_1'
            self.bayesnet.add([son,parent,{T:sensor[2], F:sensor[3]}])

        #Time instance 1 is already created other instances
        for time in range(2, self.time_intances+1):
            #Gets the previous time instance
            previous_time = time-1
            #Creates a node for each room for each time instance
            for room in self.rooms:
                #Number of corridors
                n_corridors = 1
                #Son node
                son = room + '_' + str(time)
                #Stores the parents nodes
                parents = [room + '_' + str(previous_time)]
                #Returns the room connections
                if room in self.corridors.keys():
                    corridors = self.corridors[room]
                    #Number of corridors
                    n_corridors = len(corridors)+1
                    #Creates the parent node
                    for corridor in corridors:
                        parents += [corridor +'_' + str(previous_time)]
                #Returns the possible combinations and probabilities
                prob = return_probabilities(n_corridors, self.prop_prob)
                #Adds into the baysian Net
                parents = list_to_string(parents)
                self.bayesnet.add([son,parents,prob])

                #Returns the room sensors
                if room in self.sensor_room.keys():
                    for sensors in self.sensor_room[room]:
                        son = sensors[0] + '_' + str(time)
                        parent = room + '_' + str(time)
                        self.bayesnet.add([son,parent,{T: sensors[1], F: sensors[2]}])
        #Probability to be returned
        likelihood=0.0
        #Calculates the probability for each room
        for room_ in self.rooms:
            son = room_ + '_' + str(self.time_intances)
            #Uses elimination ask to return the probability
            prob = probability.elimination_ask(son, self.measurements, self.bayesnet).show_approx('{:}')
            pre_str = prob.split()
            if float(prob.split()[3])>likelihood:
                likelihood = float(prob.split()[3])
                room_pre=room_
        #Return the final solution
        room = room_pre.split('_')[0]
        return (room, likelihood)

#Returns the probabilities dictionary depending on the number of conections and propagation probability
def return_probabilities(n_corridors, P):
    probability = {}
    #If the room is only connected to itself
    if n_corridors == 1:
        probability = {T: 1, F: 0}
    else:
        combinations = product([T, F], repeat=n_corridors)
        for combination in combinations:
            #The same room in previous time instance is always the first one
            if(combination[0]==T):
                probability[combination] = 1
                continue
            #If any other room is True, the probability is P
            if(combination[0]==F) and (T in combination[1:]):
                probability[combination] = P
            else:
                probability[combination] = 0
    return probability

#Converts lists to strings 
def list_to_string(list):
    #Checks is string was already created
    declared =  F
    for item in list:
        #If not declared
        if declared == F:
            string_final = str(item)
            declared = T
            continue
        aux = string_final
        string_final = aux + ' ' + str(item)
    return string_final

def solver(input_file):
    return Problem(input_file).solve()

