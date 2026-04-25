# Swarm Coordination of Ground Robots

**MARS Mini Project — PES University Bengaluru**  
**Team:** Shashank (PES1UG23CS709) | Vinaya P (PES1UG23CS688) | Vikhyath N (PES1UG23CS686) | Vishal Naik (PES1UG23CS695)

## Overview
Simulation of 3 autonomous TurtleBot3 Waffle robots coordinating to navigate a shared Gazebo environment using ROS2 Jazzy. Each robot operates independently with Nav2, AMCL localization, and LiDAR perception. A custom Task Allocator node automatically assigns zones and dispatches goals to all 3 robots simultaneously.

## Tech Stack
- ROS2 Jazzy + Gazebo Harmonic + Ubuntu 24.04
- Nav2 (A* global planner + DWA local planner)
- AMCL (Adaptive Monte Carlo Localization)
- SLAM Toolbox + CycloneDDS + RViz2

## How to Run

**Terminal 1:**
```bash
ros2 launch tb3_multi_robot tb3_world.launch.py
```

**Terminal 2:**
```bash
ros2 launch tb3_multi_robot tb3_nav2.launch.py
```

**Terminal 3:**
```bash
python3 multi_robot_scripts/task_allocator.py
```

## Result
All 3 robots autonomously navigate to assigned zones simultaneously without collisions.
