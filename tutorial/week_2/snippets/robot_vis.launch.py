# TODO: Import LaunchDescription from launch
# TODO: Import Node from launch_ros.actions
# TODO: Import Command and PathJoinSubstitution from launch.substitutions
# TODO: Import FindPackageShare from launch_ros.substitutions
# TODO: Import ParameterValue from launch_ros.parameter_descriptions


def generate_launch_description():

    # --- Paths -----------------------------------------------------------
    # PathJoinSubstitution builds a file path at launch time (not at import
    # time), so it works regardless of where the workspace is installed.
    # FindPackageShare('pkg') resolves to the share/ directory of a package.

    # TODO: Build urdf_path pointing to
    #       my_robot_description/urdf/my_robot.urdf.xacro

    # TODO: Build rviz_config pointing to
    #       my_robot_bringup/config/my_robot.rviz

    # --- Nodes -----------------------------------------------------------
    # Each Node(...) starts one ROS 2 node when the launch file runs.

    # robot_state_publisher reads the URDF and publishes TF transforms
    # for every link. It expects the full URDF XML as the robot_description
    # parameter — Command(['xacro ', urdf_path]) runs xacro at launch time
    # and passes the output string.

    # TODO: Define robot_state_publisher node
    #       package='robot_state_publisher', executable='robot_state_publisher'
    #       parameters=[{'robot_description': ParameterValue(Command(['xacro ', urdf_path]), value_type=str)}]

    # joint_state_publisher_gui opens a slider panel so you can move the
    # wheel joints interactively. It publishes /joint_states, which
    # robot_state_publisher uses to update the TF transforms.

    # TODO: Define joint_state_publisher_gui node
    #       package='joint_state_publisher_gui', executable='joint_state_publisher_gui'

    # rviz2 is the visualiser. The -d argument loads your saved config file
    # so you don't have to set up displays by hand every time.

    # TODO: Define rviz2 node
    #       package='rviz2', executable='rviz2'
    #       arguments=['-d', rviz_config]

    # TODO: Return LaunchDescription([...]) with all three nodes
    pass
