#!/usr/bin/env python3

import rospy
import sys
import os


sys.path.append(os.path.join(os.path.dirname(__file__), "robot_status_api"))

from next_msgs.msg import SeerLaser, LaserInfo, BeamsInfo ,HeaderInfo, DeviceInfo, InstallInfo
from next_seertcplist.seerTCP import API_PORT
from next_seertcplist.seerTCP import Msg_Type
from next_seertcplist.seerTCP import seerTCP
from robot_visual_api.RobotStatusAPI_t import RobotStatusAPI

class RobotStatusAPI_ros:
    def __init__(self, ip):
        rospy.loginfo(f"[RobotStatusAPI_ros.__init__]: ROBOT IP : {ip}")
        self.robot = RobotStatusAPI(ip)

        self.pub_laser = rospy.Publisher(
            'query_robot_laser_point_cloud_data',
            SeerLaser,
            queue_size=10
        )

        rospy.loginfo('[RobotStatusAPI_ros.__init__]: Ready, Start Publishing Robot Laser API!!')

    # def req_QueryRobotLaserData(self):
    #     laser_data = self.robot.QueryRobotLaserData()
    #     msg = SeerLaser()

    #     laser_info = LaserInfo()

    #     dev = laser_data['lasers'][0]['device_info']
    #     device = DeviceInfo()
    #     device.device_name = dev.get('device_name', "Unknown")
    #     device.max_angle   = dev.get('max_angle', 0.0)
    #     device.min_angle   = dev.get('min_angle', 0.0)
    #     device.max_range   = dev.get('max_range', 0.0)
    #     device.pub_step    = dev.get('pub_step', 0.0)
    #     device.real_step   = dev.get('real_step', 0.0)
    #     device.scan_freq   = dev.get('scan_freq', 0.0)

    #     laser_info.device_info = [device]

    #     for b in laser_data['lasers'][0]['beams']:
    #         beam_msg = BeamsInfo()
    #         beam_msg.angle = b.get('angle', 0)
    #         beam_msg.dist  = b.get('dist', 0.0)
    #         beam_msg.rssi  = b.get('rssi', 0.0)
    #         beam_msg.valid = b.get('valid', True)
    #         laser_info.beams.append(beam_msg)

    #     inst = laser_data['lasers'][0]['install_info']
    #     install = InstallInfo()
    #     install.upside = inst.get('upside', True)
    #     install.x      = inst.get('x', 0.0)
    #     install.y      = inst.get('y', 0.0)
    #     install.yaw    = inst.get('yaw', 0.0)
    #     install.z      = inst.get('z', 0.0)

    #     laser_info.install_info = [install]


    #     msg.lasers.append(laser_info)

    #     msg.ret_code = laser_data.get('ret_code', -1)
    #     # laser_data = self.robot.QueryRobotLaserData()
    #     # rospy.loginfo(f"Laser response: {laser_data}")
    #     self.pub_laser.publish(msg)

    def req_QueryRobotLaserData(self):
        laser_data = self.robot.QueryRobotLaserData()
        msg = SeerLaser()

        try:
            for l in laser_data.get('lasers', []):
                laser_info = LaserInfo()

                # ---------------- Device Info ----------------
                dev = l.get('device_info', {})
                device = DeviceInfo()
                device.device_name = dev.get('device_name', "Unknown")
                device.max_angle   = dev.get('max_angle', 0.0)
                device.min_angle   = dev.get('min_angle', 0.0)
                device.max_range   = dev.get('max_range', 0.0)
                device.pub_step    = dev.get('pub_step', 0.0)
                device.real_step   = dev.get('real_step', 0.0)
                device.scan_freq   = dev.get('scan_freq', 0.0)
                laser_info.device_info = [device]

                # ---------------- Beams Info ----------------
                for b in l.get('beams', []):
                    beam_msg = BeamsInfo()
                    beam_msg.angle = int(b.get('angle', 0))    # int8
                    beam_msg.dist  = float(b.get('dist', 0.0))
                    beam_msg.rssi  = float(b.get('rssi', 0.0))
                    beam_msg.valid = bool(b.get('valid', True))
                    laser_info.beams.append(beam_msg)

                # ---------------- Install Info ----------------
                inst = l.get('install_info', {})
                install = InstallInfo()
                install.upside = inst.get('upside', True)
                install.x      = float(inst.get('x', 0.0))
                install.y      = float(inst.get('y', 0.0))
                install.yaw    = float(inst.get('yaw', 0.0))
                install.z      = float(inst.get('z', 0.0))
                laser_info.install_info = [install]

                msg.lasers.append(laser_info)

            msg.ret_code = laser_data.get('ret_code', -1)

        except Exception as e:
            rospy.logwarn(f"Failed to parse laser data: {e}")
            msg.ret_code = -1

        self.pub_laser.publish(msg)


    def publish_robot_laser(self):
        try:
            self.req_QueryRobotLaserData()
        except Exception as e:
            rospy.logwarn(f"req_QueryRobotLaserData failed: {e}")


def main(argv=sys.argv):
    rospy.init_node('next_seerlaser', anonymous=True)
    ip = os.environ.get("ip", "192.168.1.100")
    rospy.loginfo(f"Using robot IP: {ip}")
    M = RobotStatusAPI_ros(ip)
    rate = rospy.Rate(1)
    while not rospy.is_shutdown():
        M.publish_robot_laser()
        rate.sleep()


if __name__ == '__main__':
    main()

