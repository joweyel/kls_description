import os

from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import (
    Command,
    FindExecutable,
    LaunchConfiguration,
    TextSubstitution,
)


def generate_launch_description():
    """Launch-file to visualize Klaus robot and workspace in RViz.
    Uses joint_state_publisher_gui for interactive joint control.
    Shows both robot (/robot_description) and workspace table (/workspace/robot_description).
    """

    # Get package path
    klaus_description_pkg = get_package_share_directory("klaus_description")
    xacro_file = os.path.join(klaus_description_pkg, "urdf", "klaus.urdf.xacro")
    workspace_file = os.path.join(klaus_description_pkg, "urdf", "workspace.urdf.xacro")
    rviz_config_file = os.path.join(klaus_description_pkg, "rviz", "view_klaus.rviz")

    # Launch Arguments

    name_arg = DeclareLaunchArgument(
        "name", default_value="klaus", description="Name of 'robot'"
    )

    gripper_type_arg = DeclareLaunchArgument(
        "gripper_type",
        default_value="none",
        choices=["none", "rebel"],
        description="Type of gripper to visualize (is attached to the robot)",
    )

    use_camera_arg = DeclareLaunchArgument(
        "use_camera",
        default_value="false",
        choices=["true", "false"],
        description="Enable camera holder integration on workspace",
    )

    camera_tilt_degrees_arg = DeclareLaunchArgument(
        "camera_tilt_degrees",
        default_value="0.0",
        description="Camera tilt angle in degrees (positive = down, negative = up)",
    )

    prefix_arg = DeclareLaunchArgument(
        "prefix",
        default_value="workspace_",
        description="Prefix for use in workspace urdf file",
    )

    launch_arguments = [
        name_arg,
        gripper_type_arg,
        use_camera_arg,
        camera_tilt_degrees_arg,
        prefix_arg,
    ]

    name = LaunchConfiguration("name", default="klaus")
    gripper_type = LaunchConfiguration("gripper_type", default=None)
    use_camera = LaunchConfiguration("use_camera", default=False)
    camera_tilt_degrees = LaunchConfiguration("camera_tilt_degrees")
    prefix = LaunchConfiguration("prefix")

    # Build robot description using xacro

    robot_description = {
        "robot_description": ParameterValue(
            Command(
                [
                    FindExecutable(name="xacro"),
                    " ",
                    xacro_file,
                    " name:=",
                    name,
                    " gripper_type:=",
                    gripper_type,
                    " use_camera:=",
                    use_camera,
                    " camera_tilt_degrees:=",
                    camera_tilt_degrees,
                ]
            ),
            value_type=str,
        )
    }

    workspace_description = {
        "robot_description": ParameterValue(
            Command(
                [
                    FindExecutable(name="xacro"),
                    " ",
                    workspace_file,
                    " prefix:=",  # for disambiguation of base_link when joining bases of urdfs
                    prefix,
                ]
            ),
            value_type=str,
        )
    }

    # Additional setup needed for loading 2 different urdfs

    # Joint state publisher GUI - allows interactive joint control
    joint_state_publisher_gui_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        name="joint_state_publisher_gui",
        output="screen",
    )

    # Robot state publisher (publishes to /joint_states)
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="both",
        parameters=[robot_description],
    )

    # Workspace state publisher (publishes to /workspace/joint_states)
    workspace_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="workspace_state_publisher",
        namespace="workspace",
        output="both",
        parameters=[workspace_description],
    )

    # RViz visualization
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="log",
        arguments=["-d", rviz_config_file],
    )

    # Static transform to connect robot and workspace frames (2 seperate urdfs)
    static_tf_node = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="workspace_to_robot_tf",
        arguments=[
            "0",
            "0",
            "0",
            "0",
            "0",
            "0",
            "world",
            [prefix, TextSubstitution(text="base_link")],
        ],
        output="log",
    )

    # Nodes to launch
    nodes_to_start = [
        joint_state_publisher_gui_node,
        robot_state_publisher_node,
        workspace_state_publisher_node,
        static_tf_node,
        rviz_node,
    ]

    return LaunchDescription(launch_arguments + nodes_to_start)
