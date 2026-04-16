#!/usr/bin/env python3
from next_seertcplist.seerTCP import API_PORT
from next_seertcplist.seerTCP import Msg_Type
from next_seertcplist.seerTCP import seerTCP

class DowloadRobotModel():
    #Reference Robokit API Protocal
    #link ====> https://seer-group.feishu.cn/wiki/SZcywRZC5ievYhkWQ8hc2ekCnod?fromScene=spaceOverview

    #/Robot Status API

    # - Download the Robot Model File
    # - Name: robot_status_model_req
    # - API number: 1500 (0x05DC)
    # - Description: download the robot model file

    def __init__(self):
        self.success = False
        # self.api_port = API_PORT.API_PORT_ROBOT_STATUS_API.value
        # self.api_number = Msg_Type.robot_status_laser_req.value
        self.api_port = 19204
        self.api_number = 1500




    def req_DowloadRobotModel(self):
        msg_dict = dict()
        return {"api_port":self.api_port, "api_number":self.api_number, "data":msg_dict}
