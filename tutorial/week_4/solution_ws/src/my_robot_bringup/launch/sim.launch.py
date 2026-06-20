from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    ExecuteProcess,
    GroupAction,
    OpaqueFunction,
)
from launch.conditions import IfCondition
from launch.substitutions import (
    Command,
    LaunchConfiguration,
    PathJoinSubstitution,
    PythonExpression,
)
from launch_ros.actions import Node, PushRosNamespace
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def launch_setup(context, *args, **kwargs):
    world = LaunchConfiguration('world').perform(context)

    # Spawn and goal are written here in WORLD (Gazebo) coordinates.
    # `/odom` is published relative to the robot's spawn pose (it starts at
    # (0, 0) when the robot is spawned), so we convert goals to the /odom
    # frame by subtracting the spawn. goal_checker_node compares /odom
    # against these converted values; the obstacle_nav also receives them
    # via /goal_point in the same frame.
    if world == 'maze':
        world_file = 'maze_world.sdf'
        spawn_world_x, spawn_world_y = 0.5, 0.5
        goal_world_x, goal_world_y = 0.5, 2.5
    else:
        world_file = 'obstacle_world.sdf'
        spawn_world_x, spawn_world_y = 1.0, 3.0
        goal_world_x, goal_world_y = 10.0, 3.0

    spawn_x, spawn_y = str(spawn_world_x), str(spawn_world_y)
    goal_x = goal_world_x - spawn_world_x   # in /odom frame
    goal_y = goal_world_y - spawn_world_y

    urdf_path = PathJoinSubstitution(
        [FindPackageShare('my_robot_description'), 'urdf', 'my_robot.urdf.xacro']
    )
    world_path = PathJoinSubstitution(
        [FindPackageShare('my_robot_bringup'), 'worlds', world_file]
    )
    bridge_config = PathJoinSubstitution(
        [FindPackageShare('my_robot_bringup'), 'config', 'bridge.yaml']
    )
    rviz_config = PathJoinSubstitution(
        [FindPackageShare('my_robot_bringup'), 'config', 'my_robot.rviz']
    )

    # Note: nav nodes are intentionally NOT started here. Students run
    # `ros2 run my_robot_nav obstacle_nav` (or `maze_nav`) separately so
    # they can restart their navigation logic without restarting the simulator.

    return [
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': ParameterValue(
                Command(['xacro ', urdf_path]), value_type=str
            )}],
        ),
        ExecuteProcess(
            cmd=['gz', 'sim', '-r', world_path],
        ),
        Node(
            package='ros_gz_sim',
            executable='create',
            arguments=[
                '-topic', 'robot_description',
                '-name', 'my_robot',
                '-x', spawn_x,
                '-y', spawn_y,
                '-z', '0.1',
            ],
        ),
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            parameters=[{'config_file': bridge_config}],
        ),
        # The robot's first-party nodes live under the `my_robot` namespace, so
        # their internal topics become /my_robot/set_velocity, /my_robot/goal_*,
        # /my_robot/scan_points. The Gazebo bridge publishes the sensor/actuator
        # topics at GLOBAL names (/cmd_vel, /scan, /odom), so each node that talks
        # to the bridge remaps its relative name back onto the global one.
        # Nav nodes (run via `ros2 run`) must join the namespace the same way:
        #   ros2 run my_robot_nav obstacle_nav --ros-args -r __ns:=/my_robot -r odom:=/odom
        GroupAction([
            PushRosNamespace('my_robot'),
            Node(
                package='my_robot_control',
                executable='velocity_controller',
                name='velocity_controller_node',
                remappings=[('cmd_vel', '/cmd_vel')],
                output='screen',
            ),
            Node(
                package='my_robot_perception',
                executable='goal_checker',
                name='goal_checker_node',
                parameters=[{
                    'goal_x': goal_x,
                    'goal_y': goal_y,
                    'goal_threshold': 0.3,
                }],
                remappings=[('odom', '/odom')],
                output='screen',
            ),
            Node(
                package='my_robot_perception',
                executable='scan_to_pointcloud',
                name='scan_to_pointcloud_node',
                condition=IfCondition(
                    PythonExpression(["'", LaunchConfiguration('world'), "' == 'obstacle'"])
                ),
                remappings=[('scan', '/scan')],
                output='screen',
            ),
        ]),
        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', rviz_config],
        ),
    ]


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('world', default_value='obstacle',
                              description='World to load: obstacle or maze'),
        OpaqueFunction(function=launch_setup),
    ])
