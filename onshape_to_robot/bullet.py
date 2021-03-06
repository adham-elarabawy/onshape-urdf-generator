#!/usr/bin/env python
import math
import sys
import os
import time
import argparse
import pybullet as p
from .simulation import Simulation

parser = argparse.ArgumentParser(prog="onshape-to-robot-bullet")
parser.add_argument('-f', '--fixed', action='store_true')
parser.add_argument('directory')
args = parser.parse_args()

sim = Simulation(args.directory+'/robot.urdf', gui=True, panels=True, fixed=args.fixed)

controls = {}
for name in sim.getJoints():
    if name.endswith('_speed'):
        controls[name] = p.addUserDebugParameter(name, -math.pi*3, math.pi*3, 0)
    else:
        infos = sim.getJointsInfos(name)
        low = -math.pi
        high = math.pi
        if 'lowerLimit' in infos:
            low = infos['lowerLimit']
        if 'upperLimit' in infos:
            high = infos['upperLimit']
        controls[name] = p.addUserDebugParameter(name, low, high, 0)

lastPrint = 0
while True:
    targets = {}
    for name in controls.keys():
        targets[name] = p.readUserDebugParameter(controls[name])
    sim.setJoints(targets)

    if time.time() - lastPrint > 0.05:
        lastPrint = time.time()
        os.system("clear")
        frames = sim.getFrames()
        for frame in frames:
            print(frame)
            print("- x=%f\ty=%f\tz=%f" % frames[frame][0])
            print("- r=%f\tp=%f\ty=%f" % frames[frame][1])
            print("")
            print("Center of mass:")
            print(sim.getCenterOfMassPosition())

    sim.tick()

