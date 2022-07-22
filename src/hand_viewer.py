#!/usr/bin/python3
"""Script for testing the generated robot manipulators in a simply pybullet enviroment."""

# Author: Josh Campbell, campbjos@oregonstate.edu
# Date: 3-14-2022


import pybullet as p
import time
import pybullet_data
# import os
import json
from numpy import pi
import pathlib

class sim_tester():
    """Simulator class to test different hands in."""

    def __init__(self, gripper_name, gripper_loc=None):
        """Initialize the sim_tester class.

        Args:
            gripper_name (str): The name of the gripper to be pulled into the simulator enviroment
            gripper_loc (str): The location of the top hand directory in the output directory
        """
        self.gripper_name = gripper_name
        self.gripper_loc = gripper_loc
        
        # self.directory = os.path.dirname(__file__)
        self.directory = str(pathlib.Path(__file__).parent.resolve())


    def main(self):
        """Run the simulator."""           
        physicsClient = p.connect(p.GUI)  # or p.DIRECT for non-graphical version
        p.setAdditionalSearchPath(pybullet_data.getDataPath())  # optionally
        p.setGravity(0, 0, -10)
        LinkId = []
        cubeStartPos = [0, 0, 1]
        cubeStartOrientation = p.getQuaternionFromEuler([0, 0, 0])
        plane_id = p.loadURDF("plane.urdf")
        hand_id = p.loadURDF(self.gripper_name, useFixedBase=1, basePosition=[0,0,0.04])#, baseOrientation=p.getQuaternionFromEuler([0, pi/2, pi/2]))


        p.resetDebugVisualizerCamera(cameraDistance=.02, cameraYaw=0, cameraPitch=-89.9999,
                                cameraTargetPosition=[0, 0.1, 0.5])
        joint_angles = [-.695, 1.487, 0.695, -1.487]
        for i in range(0, p.getNumJoints(hand_id)):
            p.resetJointState(hand_id, i, joint_angles[i])
            
            p.setJointMotorControl2(hand_id, i, p.POSITION_CONTROL, targetPosition=joint_angles[i], force=0)
            linkName = p.getJointInfo(hand_id, i)[12].decode("ascii")
            if "sensor" in linkName:
                LinkId.append("skip")
            else:
                LinkId.append(p.addUserDebugParameter(linkName, -3.14, 3.14, joint_angles[i]))

        # box_id = p.loadURDF(f"{self.directory}/resources/object_models/2v2_mod/2v2_mod_cuboid_small.urdf", basePosition=[0,0.1067,.04])


        while p.isConnected():

            p.stepSimulation()
            time.sleep(1. / 240.)

            for i in range(0, len(LinkId)):
                if LinkId[i] != "skip":
                    linkPos = p.readUserDebugParameter(LinkId[i])
                    p.setJointMotorControl2(hand_id, i, p.POSITION_CONTROL, targetPosition=linkPos)


        p.disconnect()
    
def read_json(file_loc):
    """Read contents of a given json file.

    Args:
        file_loc (str): Full path to the json file including the file name.

    Returns:
        dictionary: dictionary that contains the content from the json.
    """
    with open(file_loc, "r") as read_file:
        file_contents = json.load(read_file)
    return file_contents


if __name__ == '__main__':

    directory = str(pathlib.Path(__file__).parent.resolve()) #os.getcwd()

    # file_content = read_json("./../src/.user_info.json")
    folders = []
    hand_names = []
    # for folder in glob.glob(f'{directory}/resources/*/'):
    #     folders.append(folder)

    folders = sorted(pathlib.Path(f'{directory}/resources/').glob('**/*.urdf'))
    # print(urdfs)
    for i, hand in enumerate(folders):
        temp_hand = str(hand).split('/')
        # print(temp_hand)
        hand_names.append(str(hand))
        print(f'{i}:   {temp_hand[-1][:-5]}')

    input_num = input("\033[92mEnter the number of the hand you want loaded:   \033[0m")
    num = int(input_num)

    hand_name = hand_names[num]

    if input("\033[92m Do you want to load a second model? (y/n) \033[0m" ) == "y":
        num2 = input("\032[91m Enter the number of the model you want loaded:   \033[0m")
        print("Enter the position and orientation of the second model: ")
        pose_list = ['x', 'y', 'z', 'roll', 'pitch', 'yaw']
        pose_model2 = []
        for i in pose_list:
            pose_model2.append(int(input(f'\032[91mEnter value for {i}:   \032[0m'))

    print(hand_name)
    # hand_loc = folders[num]

    sim_test = sim_tester(hand_name)
    sim_test.main()