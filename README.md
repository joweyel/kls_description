# klaus_description

Robot and workspace description for Klaus project (igus ReBeL 6-DOF arm).

## Contents

- [`urdf/`](urdf/) - Robot and workspace URDF models
- [`meshes/`](meshes/) - Collision and visual meshes
- [`launch/`](launch/) - Visualization launch files
- [`rviz/`](rviz/) - RViz configurations

## Build

```bash
colcon build --packages-select klaus_description
```

## Quick Start

Visualize robot and Workspace (without gripper):
```bash
ros2 launch klaus_description view_klaus.launch.py
```

Visualize robot and Workspace (with gripper):
```bash
ros2 launch klaus_description view_klaus.launch.py gripper_type:=rebel
```

**With camera** (recommended tilt: -17°):
```bash
ros2 launch klaus_description view_klaus.launch.py \
  gripper_type:=rebel \
  use_camera:=true \
  camera_tilt_degrees:=-17
```

**Workspace only**:
```bash
ros2 launch klaus_description view_workspace.launch.py
```

## Arguments

### view_klaus.launch.py
- `gripper_type`: `none` (default), `rebel`
- `use_camera`: `true`/`false` (default: `false`)
- `camera_tilt_degrees`: Tilt angle in degrees (default: 0.0)

### view_workspace.launch.py
No arguments (workspace only visualization)