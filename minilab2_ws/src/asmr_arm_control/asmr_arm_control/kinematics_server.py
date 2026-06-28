import math
import rclpy
import yaml
import os

from ament_index_python.packages import get_package_share_directory

from rclpy.node import Node
from asmr_arm_interfaces.srv import ComputeFK, ComputeIK

class KinematicsNode(Node):
    def __init__(self):
        super().__init__('kinematics_node')
        self.fk_server = self.create_service(ComputeFK, 'compute_fk', self.compute_fk)
        self.ik_server = self.create_service(ComputeIK, 'compute_ik', self.compute_ik)
        dims_path = os.path.join(
            get_package_share_directory('asmr_arm_description'),
            'config',
            'arm_dimensions_pedestal.yaml',
        )
        with open(dims_path) as f:
            dims = yaml.safe_load(f)
        self.l1 = dims['l1']
        self.l2 = dims['l2']

    def compute_fk(self, request, response):
        if not self._joints_valid(request.theta1, request.theta2):
            response.success = False
            return response
        t1, t2 = request.theta1, request.theta2
        response.x = self.l1 * math.sin(t1) + self.l2 * math.sin(t1 + t2)
        response.y = self.l1 * math.cos(t1) + self.l2 * math.cos(t1 + t2)
        response.success = True
        return response
        
    def compute_ik(self, request, response):
        x, y = request.x, request.y
        D = (x**2 + y**2 - self.l1**2 - self.l2**2)/(2 * self.l1 * self.l2)
        if D > 1 or D < -1:
            response.success = False
            return response
        t2 = math.atan2(-math.sqrt(1 - D**2), D)
        t1 = math.atan2(x, y) - math.atan2(self.l2 * math.sin(t2), self.l1 + self.l2 * math.cos(t2))
        response.theta1 = t1
        response.theta2 = t2
        response.success = True 
        return response
        

    def _joints_valid(self, t1, t2):
        if not all(math.isfinite(a) for a in (t1, t2)):
            return False
        lim = math.pi
        return -lim <= t1 <= lim and -lim <= t2 <= lim

def main(args=None):
    rclpy.init(args=args)
    node = KinematicsNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
        
    