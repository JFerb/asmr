# Copyright 2026 Janosch Bajorath
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Launch turtlesim and star_node together.

turtlesim_node and star_node are started in declaration order.
No explicit sequencing is needed: star_node calls wait_for_service
in __init__ and waits up to 5 s for turtlesim to become ready.
"""
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    """Return the launch description for the turtle star demo."""
    return LaunchDescription([
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            output='screen',
        ),
        Node(
            package='turtle_star',
            executable='star_node',
            output='screen',
        ),
    ])
