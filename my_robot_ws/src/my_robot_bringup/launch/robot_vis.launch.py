from launch import LaunchDescription
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

    ld.add_action(
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': ParameterValue(Command(['xacro ', urdf_path]), value_type=str)}]
        )
    )

    ld.add_action(
        Node(
            package='joint_state_publisher_gui', 
            executable='joint_state_publisher_gui'
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

    

    