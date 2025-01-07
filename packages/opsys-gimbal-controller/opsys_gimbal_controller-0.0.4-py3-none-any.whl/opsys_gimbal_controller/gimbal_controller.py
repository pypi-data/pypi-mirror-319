from .gimbal_abstract import GimbalAbstract
from .gimbal_types import GimbalTypes


class GimbalController(GimbalAbstract):
    """
    Gimbal Controller main class
    """
    
    def __init__(self, motor_type):
        """
        Initialize parameters

        Args:
            motor_type (str): gimbal motor type
        """
        self.motor_type = motor_type
        self.gimbal = None  # gimbal connection
        
    def set_gimbal_parameters(self,
                              total_step_per_round=3600000,
                              deg_per_round=360,
                              baudrate=19200,
                              velocity=50000,
                              acceleration=200000,
                              deceleration=150000):
        """
        Set gimbal parameter value

        Args:
            total_step_per_round (int, optional): steps per round. Defaults to 3600000.
            deg_per_round (int, optional): Degrees per round. Defaults to 360.
            baudrate (int, optional): Baud rate. Defaults to 19200.
            velocity (int, optional): Velocity. Defaults to 50000.
            acceleration (int, optional): Acceleration. Defaults to 200000.
            deceleration (int, optional): Deceleration. Defaults to 150000.
        """
        self.gimbal.set_gimbal_parameters(total_step_per_round,
                                          deg_per_round,
                                          baudrate,
                                          velocity,
                                          acceleration,
                                          deceleration)
        
    def get_device_unit_from_angle(self, angle):
        """
        Input degrees and return steps for gimbal

        Args:
            angle (float): angle value

        Returns:
            str: gimbal steps
        """
        return self.gimbal.get_device_unit_from_angle(angle)
    
    def get_angle_from_device_unit(self, steps):
        """
        Input steps and return degrees for gimbal

        Args:
            steps (int): gimbal steps

        Returns:
            str: angle value
        """
        return self.gimbal.get_angle_from_device_unit(steps)
    
    def set_zero(self, axis):
        """
        Set gimbal position as zero
        
        Args:
            axis (str): axis to set as zero position - X/Y
        """
        self.gimbal.set_zero(axis)

    def connect(self):
        """
        Connect to gimbal
        
        Returns:
            bool: True if connection established,
                  else False
        """
        if self.motor_type.upper() == GimbalTypes.NEWMARK:
            from .newmark.newmark_controller import NewmarkController
            
            self.gimbal = NewmarkController()
            
        elif self.motor_type.upper() == GimbalTypes.THORLABS:
            # *** Currentrly unsupported ***
            # from .thorlabs.thorlabs_controller import ThorlabsController
            
            # self.gimbal = ThorlabsController()
            return False
            
        elif self.motor_type.upper() == GimbalTypes.MANUF:
            return
        
        else:
            raise ValueError("Can't find motor type")
        
        return self.gimbal.connect()

    def disconnect(self):
        """
        Disconnect from Gimbal
        """
        self.gimbal.disconnect()

    def setup(self):
        """
        Set motor configurations
        """
        self.gimbal.setup()

    def get_position(self):
        """
        Read gimbal current position

        Returns:
            tuple: x, y position
        """
        if self.motor_type.upper() == GimbalTypes.NEWMARK:
            x, y = self.gimbal.get_position()
            
        elif self.motor_type.upper() == GimbalTypes.THORLABS:
            y = -999  # single axis
            x = self.gimbal.get_position()
            
        return x, y
    
    def get_position_encoder(self, axis='X'):
        """
        Read gimbal current position from encoder

        Args:
            axis (str, optional): Movement axis. Defaults to 'X'.

        Returns:
            float: encoder position
        """
        return self.gimbal.get_position_encoder(axis)

    def home(self, axis='XY', side='clockwise', wait_for_completion=True):
        """
        Set gimbal homing

        Args:
            axis (str, optional): Movement axis X/Y/XY (both). Defaults to 'XY'.
            side (str, optional): Motion direction clockwise and counterclockwise.
                                  Defaults to 'clockwise'.
            wait_for_completion (bool, optional): True if wait for motion done.
                                                  False if not. Defaults to True.
        
        Returns:
            bool: True if homed, else False
        """
        return self.gimbal.home(axis, side, wait_for_completion)

    def move_gimbal_abs(self, axis, angle, wait_for_completion=True):
        """
        Move Gimbal absolute

        Args:
            axis (str): Movement axis (X/Y)
            angle (float): Movement angle
            wait_for_completion (bool, optional): True if wait for motion done.
                                                  False if not. Defaults to True.
        """
        self.gimbal.move_gimbal_abs(axis, angle, wait_for_completion)

    def move_gimbal_rel(self, axis, angle, wait_for_completion=True):
        """
        Move Gimbal relative

        Args:
            axis (str): Movement axis (X/Y)
            angle (float): Movement angle
            wait_for_completion (bool, optional): True if wait for motion done.
                                                  False if not. Defaults to True.
        """
        self.gimbal.move_gimbal_rel(axis, angle, wait_for_completion)

    def stop(self, axis=''):
        """
        Stop Gimbal
        
        Args:
            axis (str): Stop axis 'X'/'Y'/'' (stop all). Defaults to ''.
            
        Returns:
            bool: Execution status. True if succeeded, else False
        """
        return self.gimbal.stop(axis)
    
    def find_index(self, side='clockwise', axis='X'):
        """
        Find encoder index of axes

        Args:
            side (str): clockwise/counterclockwise.
                        Defaults to 'clockwise'.
            axis (str): axis name - 'X', 'Y'. Defaults to 'X'.
            
        Returns:
            str: velocity value
        """ 
        return self.gimbal.find_index(side, axis)
    
    def get_velocity(self, axis):
        """
        Get the slew velocity of axes

        Args:
            axis (str): axis name - 'X', 'Y'

        Returns:
            str: speed
        """ 
        return self.gimbal.get_velocity(axis)
    
    def set_velocity(self, axis, velocity):
        """
        Set Gimbal velocity

        Args:
            axis (str): Gimbal axis X/Y
            velocity (int): Gimbal velocity
        """
        self.gimbal.set_velocity(axis, velocity)
    
    def set_acceleration(self, axis, acceleration):
        """
        Set Gimbal acceleration

        Args:
            axis (str): Gimbal axis X/Y
            acceleration (int): Gimbal acceleration
        """
        self.gimbal.set_acceleration(axis, acceleration)
    
    def set_deceleration(self, axis, deceleration):
        """
        Set Gimbal deceleration

        Args:
            axis (str): Gimbal axis X/Y
            deceleration (int): Gimbal deceleration
        """
        self.gimbal.set_deceleration(axis, deceleration)
    
    def set_forward_limit(self, axis, limit):
        """
        Set Gimbal forward limit

        Args:
            axis (str): Gimbal axis X/Y
            limit (int): Gimbal limit
        """
        self.gimbal.set_forward_limit(axis, limit)
    
    def set_backward_limit(self, axis, limit):
        """
        Set Gimbal reverse limit

        Args:
            axis (str): Gimbal axis X/Y
            limit (int): Gimbal limit
        """
        self.gimbal.set_backward_limit(axis, limit)
        
    def motion_complete(self, axis):
        """
        Wait for motion completion on
        selected axis/axes
        
        Args:
            axis (str): Gimbal axis X/Y/XY

        Returns:
            bool: True\False
        """
        return self.gimbal.motion_complete(axis)
