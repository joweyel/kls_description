import os

from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node

from launch import LaunchDescription
from launch.substitutions import Command, FindExecutable


def generate_launch_description():
    """Visualize only Klaus workspace table in RViz."""

    # Get package path
    kls_description_pkg = get_package_share_directory("kls_description")

    # Paths
    xacro_file = os.path.join(kls_description_pkg, "urdf", "workspace.urdf.xacro")
    rviz_config = os.path.join(kls_description_pkg, "rviz", "view_workspace.rviz")

    # Robot description
    robot_description = {
        "robot_description": Command(
            [
                FindExecutable(name="xacro"),
                " ",
                xacro_file,
            ]
        )
    }

    # Nodes
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[robot_description],
        output="both",
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        arguments=["-d", rviz_config],
        output="log",
    )

    return LaunchDescription(
        [
            robot_state_publisher_node,
            rviz_node,
        ]
    )
