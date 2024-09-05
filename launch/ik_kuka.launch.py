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
            "bt_config_kuka.yaml"        # load the behavior tree plugins and the tree
          ]),
          "--path-to-file",
          PathJoinSubstitution([
            config_folder,
            "skills_config_kuka.yaml"    # load the parameters of each skill plugin
          ]),
          "--path-to-file",
          PathJoinSubstitution([
            config_folder,
            "trajectories_kuka.yaml"    # load the parameters of each skill plugin
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
         launch_arguments={'config': PathJoinSubstitution([config_folder,"ik_solver_config_kuka.yaml"])}.items()
         )
      ]
    )
])
