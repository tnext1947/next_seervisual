#!/usr/bin/env python3

import rospy
import sys
import os
from next_seertcplist.seerTCP import API_PORT
from next_seertcplist.seerTCP import Msg_Type
from next_seertcplist.seerTCP import seerTCP
from robot_visual_api.API_QueryRobotLaserPointCloud import QueryRobotLaserData
from robot_visual_api.API_DownloadRobotModel import DowloadRobotModel



class RobotStatusAPI:
    def __init__(self, ip):
        self.robot = seerTCP()
        print(f"[RobotStatusAPI.__init__]: ROBOT IP : {ip}")
        self.robot.set_ip(ip)

    def QueryRobotLaserData(self):
        reqLaser = QueryRobotLaserData()
        msg = reqLaser.req_QueryRobotLaserData()
        response_ = self.sendToRobot(msg)
        # print(response_)
        return response_

    def DowloadRobotModel(self):
        reqFile = DowloadRobotModel()
        msg = reqFile.req_DowloadRobotModel()
        response_ = self.sendToRobot(msg)
        # print(response_)
        return response_

    def sendToRobot(self, msg=dict()):
        # print(f"[RobotNavigationAPI.sendToRobot]: sendToRobot ==> {msg}")
        self.robot.set_port(msg['api_port'])
        robot_res = self.robot.query(1, msg['api_number'], msg['data'])
        return robot_res


# a = RobotStatusAPI("192.168.10.62")
# b = a.QueryRobotAlarmStatus()
# print(b)