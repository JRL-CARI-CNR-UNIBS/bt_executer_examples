# This Python file uses the following encoding: utf-8
from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from launch.substitutions import FindExecutable, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
  config_folder = PathJoinSubstitution([FindPackageShare("bt_executer_examples"),"config"])

  return LaunchDescription([
    ExecuteProcess(
        cmd = [
          FindExecutable(name="cnr_param_server"),
          "--path-to-file",
          PathJoinSubstitution([
            config_folder,
            "bt_config.yaml"        # load the behavior tree plugins and the tree
          ]),
          "--path-to-file",
          PathJoinSubstitution([
            config_folder,
            "skills_config.yaml"    # load the parameters of each skill plugin
          ]),
          "--path-to-file",
          PathJoinSubstitution([
            config_folder,
            "trajectories.yaml"    # load the parameters of each skill plugin
          ])
        ],
        shell=False
      ),
      
   
    TimerAction(
      period=1.0,  # delay in seconds
      actions=[
      IncludeLaunchDescription(
      PythonLaunchDescriptionSource(
        PathJoinSubstitution([FindPackageShare('ik_solver'),"launch","ik_solver.launch.py"])),
         launch_arguments={'file': PathJoinSubstitution([config_folder,"ik_solver_config.yaml"])}.items()
         )
      ]
    ),

    #Foo tf to use move_to_skill
    TimerAction(
      period=1.0,  # delay in seconds
      actions=[
         Node(
           package="tf2_ros",
           executable="static_transform_publisher",
           name="foo_static_tf",
           arguments=["0.3","0","0","0","0","0","comau_link_6","foo_location"],
           output="screen")
      ]
    ),
     
    TimerAction(
      period=5.0,  # delay in seconds
      actions=[
        Node(
          package="bt_executer",
          executable="bt_executer_node",
          output="screen",
          namespace="bt_executer",
          ros_arguments=["--log-level", "info"]
        )
      ]
    )
])
