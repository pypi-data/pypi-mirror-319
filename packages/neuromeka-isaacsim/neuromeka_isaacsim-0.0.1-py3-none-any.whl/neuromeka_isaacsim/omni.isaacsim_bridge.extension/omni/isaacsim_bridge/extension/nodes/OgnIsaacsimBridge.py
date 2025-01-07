"""
This is the implementation of the OGN node defined in OgnIsaacsimBridge.ogn
"""

# Array or tuple values are accessed as numpy arrays so you probably need this import
import numpy as np

from omni.isaac.core_nodes import BaseResetNode
from omni.isaac.core.scenes import Scene
from omni.isaac.manipulators import SingleManipulator
from neuromeka import indydcp3


class OgnIsaacsimBridgeInit(BaseResetNode):
    def __init__(self):
        super().__init__(initialize=False)
        self.scene = None
        self.initialized = False
        self.indy = None
        self.step_ip = None
        self.gripper = None
        self.manipulator = None
        self.robot_prim_path = "/World/indy7"
        self.robot_name = "indy7"
        self.ee_name = "tcp"
        self.target_positions = None

    def initialize_scene(self):
        self.scene = Scene()
        self.indy = indydcp3.IndyDCP3(robot_ip=self.step_ip)
        self.manipulator = SingleManipulator(
            prim_path=self.robot_prim_path,
            end_effector_prim_name=self.ee_name
        )
        self.scene.add(self.manipulator)
        self.manipulator.initialize()
        self.initialized = True
        return

    def custom_reset(self):
        pass


class OgnIsaacsimBridge:

    @staticmethod
    def internal_state():
        return OgnIsaacsimBridgeInit()

    @staticmethod
    def compute(db) -> bool:
        state = db.per_instance_state

        try:
            if not state.initialized:
                state.step_ip = db.inputs.step_ip
                state.initialize_scene()

            current_robot_joint_data = state.indy.get_control_state()['q']
            target_positions = np.array(np.deg2rad(current_robot_joint_data))
            state.manipulator.set_joint_positions(target_positions)

        except Exception as error:
            db.log_error(str(error))
            return False

        return True
