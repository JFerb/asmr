import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from asmr_arm_interfaces.action import ExecuteTrajectory

# Waypoints in Arm-Koordinaten (x=seitlich, y=höhe relativ zur Schulter)
# Block liegt bei y=0.6m vor dem Arm, Höhe ca. -0.10m relativ zur Schulter
WAYPOINTS = [
    {'name': 'home',     'x': 0.9,  'y': 0.0},   # Arm senkrecht nach oben
    {'name': 'approach', 'x': -0.1, 'y': 0.5},   # vor dem Block auf Blockhöhe
    {'name': 'push',     'x': -0.1, 'y': 0.85},  # deutlich weiter schieben
]

class PushBlockMission(Node):
    def __init__(self):
        super().__init__('push_block_mission')
        self._client = ActionClient(self, ExecuteTrajectory, 'execute_trajectory')

    def run(self):
        self.get_logger().info('Warte auf TrajectoryServer...')
        self._client.wait_for_server()

        goal = ExecuteTrajectory.Goal()
        goal.x = [wp['x'] for wp in WAYPOINTS]
        goal.y = [wp['y'] for wp in WAYPOINTS]

        self.get_logger().info('Sende Trajectory Goal...')
        send_goal_future = self._client.send_goal_async(
            goal, feedback_callback=self._feedback_cb)
        rclpy.spin_until_future_complete(self, send_goal_future)

        goal_handle = send_goal_future.result()
        if not goal_handle.accepted:
            self.get_logger().error('Goal abgelehnt!')
            return

        self.get_logger().info('Goal akzeptiert, warte auf Ergebnis...')
        result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self, result_future)

        result = result_future.result().result
        if result.success:
            self.get_logger().info(
                f'Mission erfolgreich! theta1={result.theta1:.3f}, theta2={result.theta2:.3f}')
        else:
            self.get_logger().error('Mission fehlgeschlagen!')

    def _feedback_cb(self, feedback_msg):
        fb = feedback_msg.feedback
        self.get_logger().info(
            f'Waypoint {fb.waypoint_index} erreicht: '
            f'ee_x={fb.ee_x:.3f}, ee_y={fb.ee_y:.3f}')


def main(args=None):
    rclpy.init(args=args)
    node = PushBlockMission()
    node.run()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()