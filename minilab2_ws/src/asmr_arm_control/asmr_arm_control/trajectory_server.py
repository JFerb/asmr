import math
import threading
import time
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from control_msgs.msg import MultiDOFCommand
from sensor_msgs.msg import JointState
from asmr_arm_interfaces.action import ExecuteTrajectory
from asmr_arm_interfaces.srv import ComputeIK, ComputeFK

STEPS = 50        # Interpolationsschritte zwischen Waypoints
STEP_DELAY = 0.05 # Sekunden zwischen Schritten
SETTLE_TOL = 0.05 # Toleranz in Radians zum Einrasten

class TrajectoryServer(Node):
    def __init__(self):
        super().__init__('trajectory_server')
        self._lock = threading.Lock()
        self._current_theta1 = 0.0
        self._current_theta2 = 0.0

        cb_group = ReentrantCallbackGroup()

        self.create_subscription(
            JointState, '/joint_states', self._joint_states_cb, 10,
            callback_group=cb_group)

        self._ref_pub = self.create_publisher(
            MultiDOFCommand, '/arm_pid_controller/reference', 10)

        self._ik_client = self.create_client(
            ComputeIK, 'compute_ik', callback_group=cb_group)
        self._fk_client = self.create_client(
            ComputeFK, 'compute_fk', callback_group=cb_group)

        self._action_server = ActionServer(
            self, ExecuteTrajectory, 'execute_trajectory',
            execute_callback=self._execute_cb,
            goal_callback=self._goal_cb,
            cancel_callback=self._cancel_cb,
            callback_group=cb_group)

        self.get_logger().info('TrajectoryServer bereit.')

    def _sleep(self, seconds):
        start = self.get_clock().now()
        while (self.get_clock().now() - start).nanoseconds < seconds * 1e9:
            time.sleep(0.001)

    def _joint_states_cb(self, msg: JointState):
        with self._lock:
            for i, name in enumerate(msg.name):
                if name == 'shoulder':
                    self._current_theta1 = msg.position[i]
                elif name == 'elbow':
                    self._current_theta2 = msg.position[i]

    def _goal_cb(self, goal_request):
        if len(goal_request.x) == 0 or len(goal_request.x) != len(goal_request.y):
            return GoalResponse.REJECT
        return GoalResponse.ACCEPT

    def _cancel_cb(self, goal_handle):
        return CancelResponse.ACCEPT

    async def _execute_cb(self, goal_handle):
        goal = goal_handle.request
        feedback = ExecuteTrajectory.Feedback()

        with self._lock:
            theta1 = self._current_theta1
            theta2 = self._current_theta2

        for idx, (wx, wy) in enumerate(zip(goal.x, goal.y)):
            ik_req = ComputeIK.Request()
            ik_req.x = wx
            ik_req.y = wy
            ik_res = await self._ik_client.call_async(ik_req)

            if not ik_res.success:
                self.get_logger().warn(f'Waypoint {idx} nicht erreichbar, überspringe.')
                continue

            target_t1 = ik_res.theta1
            target_t2 = ik_res.theta2

            # Smooth interpolation zum Ziel
            for step in range(1, STEPS + 1):
                if goal_handle.is_cancel_requested:
                    goal_handle.canceled()
                    result = ExecuteTrajectory.Result()
                    result.success = False
                    with self._lock:
                        result.theta1 = self._current_theta1
                        result.theta2 = self._current_theta2
                    return result

                alpha = step / STEPS
                t1 = theta1 + alpha * (target_t1 - theta1)
                t2 = theta2 + alpha * (target_t2 - theta2)

                cmd = MultiDOFCommand()
                cmd.dof_names = ['shoulder', 'elbow']
                cmd.values = [t1, t2]
                self._ref_pub.publish(cmd)

                self._sleep(STEP_DELAY)

            # Warten bis Arm eingerastet
            for _ in range(50):
                with self._lock:
                    e1 = abs(self._current_theta1 - target_t1)
                    e2 = abs(self._current_theta2 - target_t2)
                if e1 < SETTLE_TOL and e2 < SETTLE_TOL:
                    break
                self._sleep(STEP_DELAY)

            # FK für Feedback
            fk_req = ComputeFK.Request()
            with self._lock:
                fk_req.theta1 = self._current_theta1
                fk_req.theta2 = self._current_theta2
            fk_res = await self._fk_client.call_async(fk_req)

            feedback.waypoint_index = idx
            feedback.ee_x = fk_res.x
            feedback.ee_y = fk_res.y
            goal_handle.publish_feedback(feedback)

            with self._lock:
                theta1 = self._current_theta1
                theta2 = self._current_theta2

        goal_handle.succeed()
        result = ExecuteTrajectory.Result()
        result.success = True
        with self._lock:
            result.theta1 = self._current_theta1
            result.theta2 = self._current_theta2
        return result


def main(args=None):
    rclpy.init(args=args)
    node = TrajectoryServer()
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()