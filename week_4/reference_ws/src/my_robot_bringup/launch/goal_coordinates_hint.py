# ── Hinweis: Zielkoordinaten im launch file richtig setzen ───────────────────
#
# Die Kopfzeile von obstacle_world.sdf gibt die Zielposition in WELT-
# Koordinaten (Gazebo-Frame) an:
#
#   Ziel (Welt):   (10.0, 3.0)
#   Spawn (Welt):  ( 1.0, 3.0)
#
# Das /odom-Topic startet beim Spawn des Roboters bei (0.0, 0.0) und misst
# Bewegung relativ zur Startpose — nicht relativ zum Gazebo-Weltursprung.
# goal_checker_node vergleicht die /odom-Position des Roboters mit den
# Parametern goal_x / goal_y. Diese müssen daher im /odom-Frame angegeben
# werden:
#
#   goal_x (odom) = 10.0 − 1.0 = 9.0
#   goal_y (odom) =  3.0 − 3.0 = 0.0
#
# Werden stattdessen die Weltkoordinaten (10.0, 3.0) direkt übergeben, sucht
# goal_checker_node nach dem Roboter an Weltposition (11.0, 6.0) — das liegt
# in der Wand.
#
# Empfohlene Umsetzung in sim.launch.py:

# Weltkoordinaten aus dem Kommentar in obstacle_world.sdf
SPAWN_X, SPAWN_Y = 1.0, 3.0
GOAL_X,  GOAL_Y  = 10.0, 3.0

# Umrechnung in den /odom-Frame
goal_x_odom = GOAL_X - SPAWN_X  # 9.0
goal_y_odom = GOAL_Y - SPAWN_Y  # 0.0

# Übergabe an goal_checker_node:
#
# Node(
#     package='my_robot_perception',
#     executable='goal_checker_node',
#     parameters=[{
#         'goal_x': goal_x_odom,
#         'goal_y': goal_y_odom,
#         'goal_threshold': 0.3,
#     }],
#     output='screen',
# ),
