#!/usr/bin/env python
# coding: utf-8


import numpy as np
from datetime import datetime,date,timedelta
import pandas as pd
import sys
import argparse

MAX_CAP = 10
MAX_PROJ = 3
MAX_TV = 5

################################################### ROOM CLASS ###############################################
class Room:
    def __init__(self, name, floor, capacity, projector, tv):
        self.name = name
        self.floor = floor
        self.capacity = capacity
        self.projector = projector
        self.tv = tv
        self.schedule = []
    
    def is_time_valid(self, start, end):
        start_dt = pd.to_datetime(start, format='%Y-%m-%d-%H-%M')
        end_dt = pd.to_datetime(end, format='%Y-%m-%d-%H-%M')
        for time_pair in self.schedule:
            if time > time_pair[0] and time < time_pair[1]:
                return False
        self.schedule.append((start_dt, end_dt))
        return True
    
    def is_equip_valid(self, capacity, projector, tv):
        if capacity > self.capacity or projector > self.projector or tv > self.tv:
            return False
        return True
    
    def score(self, floor, capacity, projector, tv):
        cap_score = (self.capacity - capacity) * 2
        floor_score = -(self.floor - floor) * 0.3
        proj_score = (self.projector - projector) * 0.2
        tv_score = (self.tv - tv) * 0.2
        return cap_score + floor_score + proj_score + tv_score 
    
    def check(self, start, end, floor, capacity, projector, tv):
        if not self.is_time_valid(start, end):
            return -1
        if not self.is_equip_valid(capacity, projector, tv):
            return -1
        return self.score(floor, capacity, projector, tv)

################################################### ALL ROOMS ###############################################
room1 = Room('Saturn', 1, 2, 1, 1)
room2 = Room('Earth', 2, 4, 2, 2)
room3 = Room('Jupiter', 3, 6, 3, 1)
room4 = Room('Mars', 5, 6, 1, 1)
room5 = Room('Sun', 10, 10, 1, 5)
room6 = Room('Mercury', 4, 4, 1, 1)
room7 = Room('Venus', 8, 8, 1, 2)
room8 = Room('Neptune', 5, 5, 2, 4)
rooms = [room1, room2, room3, room4, room5, room6, room7, room8]

################################################### PARSE USER INPUT ################################################
#####################################################################################################################
############################## FORMAT:                                                    ###########################
##############################    --start: start time (year-month-day-hour-minute)        ###########################
##############################    --end: end time (year-month-day-hour-minute)            ###########################
##############################    --floor: the preferred floor to be on (int)             ###########################
##############################    --capacity: how many people will be there (int)         ###########################
##############################    --projector: the number of projectors required (int)    ###########################
##############################    --tv: the number of TVs required (int)                  ###########################
#####################################################################################################################
parser = argparse.ArgumentParser(description='Create a ArcHydro schema')
parser.add_argument('--start', required=True,
                    help='the start time')
parser.add_argument('--end', required=True,
                    help='the end time')
parser.add_argument('--floor', required=True,
                    help='preferred floor')
parser.add_argument('--capacity', required=True,
                    help='size of party')
parser.add_argument('--projector', required=True,
                    help='number of projector')
parser.add_argument('--tv', required=True,
                    help='number of tv')
args = parser.parse_args()

################################################## GENERATE SCHEDULE ###############################################
def main(start, end, floor, capacity, projector, tv):
    score = []
    if not sanity_check(capacity, projector, tv):
        return
    for room in rooms:
        s = room.check(start, end, floor, capacity, projector, tv)
        score.append(s)
    if any(np.array(score) > 0):
        print('Reservation successful for', rooms[np.argmax(score)].name, 'on Floor', rooms[np.argmax(score)].floor)
    else:
        print('No available room for this period of time.')

    return

main(args.start, args.end, int(args.floor), int(args.capacity), int(args.projector), int(args.tv))


##### OTHERS #####
def sanity_check(capacity, projector, tv):
    if capacity > MAX_CAP:
        print('Too many people. Max room capacity is', MAX_CAP)
        return False
    else if projector > MAX_PROJ:
        print('Too many people. Max number of projector is', MAX_PROJ)
        return False
    else if tv > MAX_TV:
        print('Too many people. Max number of tv is', MAX_TV)
        return False
    return True
