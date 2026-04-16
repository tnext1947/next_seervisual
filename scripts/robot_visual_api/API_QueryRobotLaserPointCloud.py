#!/usr/bin/env python3
from next_seertcplist.seerTCP import API_PORT
from next_seertcplist.seerTCP import Msg_Type
from next_seertcplist.seerTCP import seerTCP

class QueryRobotLaserData():
    #Reference Robokit API Protocal
    #link ====> https://seer-group.feishu.cn/wiki/SZcywRZC5ievYhkWQ8hc2ekCnod?fromScene=spaceOverview

    #/Robot Status API

    # - Query Robot Laser Point Cloud Data
    # - Name: robot_status_laser_req
    # - API number: 1009 (0x03F1)
    # - Description: Robot laser status inquiry

    def __init__(self):
        self.success = False
        self.api_port = API_PORT.API_PORT_ROBOT_STATUS_API.value
        self.api_number = Msg_Type.robot_status_laser_req.value




    def req_QueryRobotLaserData(self):
        msg_dict = dict()
        return {"api_port":19204, "api_number":1009, "data":msg_dict}

a = QueryRobotLaserData()
print(a.req_QueryRobotLaserData())