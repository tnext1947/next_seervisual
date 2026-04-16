#!/usr/bin/env python3
import rospy
import sys
import os
import json

sys.path.append(os.path.join(os.path.dirname(__file__), "robot_status_api"))

from next_msgs.msg import SeerChassis
from robot_visual_api.RobotStatusAPI_t import RobotStatusAPI


class RobotChassisAPI_ros:
    def __init__(self, ip):
        rospy.loginfo(f"[RobotChassisAPI_ros.__init__]: ROBOT IP : {ip}")
        self.robot = RobotStatusAPI(ip)

        self.pub_chassis = rospy.Publisher(
            'query_robot_chassis_shape',
            SeerChassis,
            queue_size=10
        )

        rospy.loginfo('[RobotChassisAPI_ros.__init__]: Ready, Start Publishing Robot Chassis API!!')

    def req_QueryRobotChassis(self):
        model_data = self.robot.DowloadRobotModel()
        msg = SeerChassis()

        try:
            # rospy.loginfo(f"[RobotChassisAPI_ros] Robot Model FULL Response: {str(model_data)[:300]} ...")

            if isinstance(model_data, str):
                model_data = json.loads(model_data)

            shapes = None


            if isinstance(model_data, dict) and "deviceTypes" in model_data:
                for dev_type in model_data["deviceTypes"]:
                    if "devices" not in dev_type:
                        continue
                    for device in dev_type["devices"]:
                        if "deviceParams" not in device:
                            continue
                        for param in device["deviceParams"]:
                            if param.get("key") == "shape":
                                # rospy.loginfo(f"Found shape in device: {device.get('name')}")
                                shapes = [param]
                                break

            if shapes is None:
                raise KeyError("No shape info found in Robot Model response")

            # ------------------------------
            # parse shape params
            # ------------------------------
            for s in shapes:
                if s.get("key") == "shape":
                    combo = s["comboParam"]["childParams"]

                    for child in combo:
                        if child["key"] == "rectangle":
                            msg.type = 0
                            for p in child["params"]:
                                if p["key"] == "width":
                                    msg.width = p["doubleValue"]
                                elif p["key"] == "head":
                                    msg.head = p["doubleValue"]
                                elif p["key"] == "tail":
                                    msg.tail = p["doubleValue"]
                                elif p["key"] == "height":
                                    msg.rect_height = p["doubleValue"]

                        # elif child["key"] == "circle":
                        #     msg.type = 1
                        #     for p in child["params"]:
                        #         if p["key"] == "radius":
                        #             msg.radius = p["doubleValue"]
                        #         elif p["key"] == "height":
                        #             msg.circle_height = p["doubleValue"]

                        # elif child["key"] == "polygon":
                        #     msg.type = 2
                        #     for p in child["params"]:
                        #         if p["key"] == "polygon":
                        #             try:
                        #                 pts = json.loads(p["stringValue"])
                        #                 msg.poly_x = [pt["x"] for pt in pts]
                        #                 msg.poly_y = [pt["y"] for pt in pts]
                        #             except Exception as e:
                        #                 rospy.logwarn(f"Failed to parse polygon points: {e}")
                        #         elif p["key"] == "height":
                        #             msg.poly_height = p["doubleValue"]

            msg.ret_code = 0
            # rospy.loginfo(
            #     f"[Publish Chassis] type={msg.type}, "
            #     f"width={msg.width}, head={msg.head}, tail={msg.tail}, rect_height={msg.rect_height}, "
            #     f"radius={msg.radius}, circle_height={msg.circle_height}, "
            #     f"poly_points={len(msg.poly_x)}, ret_code={msg.ret_code}"
            # )

        except Exception as e:
            rospy.logwarn(f"Parse Robot Model failed: {e}")
            msg.ret_code = -1

        self.pub_chassis.publish(msg)

    def publish_robot_chassis(self):
        try:
            self.req_QueryRobotChassis()
        except Exception as e:
            rospy.logwarn(f"req_QueryRobotChassis failed: {e}")


def main(argv=sys.argv):
    rospy.init_node('next_seerchassis', anonymous=True)
    ip = os.environ.get("ip", "192.168.1.100")
    rospy.loginfo(f"Using robot IP: {ip}")
    M = RobotChassisAPI_ros(ip)
    rate = rospy.Rate(1)
    while not rospy.is_shutdown():
        M.publish_robot_chassis()
        rate.sleep()


if __name__ == '__main__':
    main()
