from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from launch.substitutions import PathJoinSubstitution, Command
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    ld = LaunchDescription()

    description_share = FindPackageShare('my_robot_description')
    bringup_share = FindPackageShare('my_robot_bringup')
    
    urdf_path = PathJoinSubstitution([description_share, 'urdf', 'my_robot.urdf.xacro'])
    rviz_config = PathJoinSubstitution([bringup_share, 'config', 'my_robot.rviz'])
    world_path = PathJoinSubstitution([bringup_share, 'worlds', 'wall_world.sdf'])
    bridge_config = PathJoinSubstitution([bringup_share, 'config', 'bridge.yaml'])

    ld.add_action(
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': ParameterValue(Command(['xacro ', urdf_path]), value_type=str)}]
        )
    )
    ld.add_action(
        ExecuteProcess(cmd=['gz', 'sim', '-r', '-s', world_path], output='screen')
    )
    
    ld.add_action(
        Node(
            package='ros_gz_sim',
            executable='create',
            arguments=['-topic', 'robot_description', '-name', 'my_robot', '-z', '0.1']
        )
    )

    ld.add_action(
        Node(
            package='ros_gz_bridge', 
            executable='parameter_bridge',
            parameters=[{'config_file': bridge_config}]
        )
    )

    ld.add_action(
        Node(
            package='rviz2', 
            executable='rviz2',
            arguments=['-d', rviz_config]
        )
    )

    return ld

    

    