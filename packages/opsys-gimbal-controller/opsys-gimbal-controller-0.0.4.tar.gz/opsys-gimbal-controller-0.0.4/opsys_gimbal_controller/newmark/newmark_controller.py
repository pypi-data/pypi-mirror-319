import os, sys, re
import newmark.gclib as gclib
from ..gimbal_abstract import GimbalAbstract


sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)))


class NewmarkController(GimbalAbstract):
    """
    Newmark Gimbal Controller
    """
    
    def __init__(self):
        """
        Initialize parameters
        """
        self.set_gimbal_parameters()
        self.g = gclib.GController()
        
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
            total_step_per_round (int): steps per round.
            deg_per_round (int): Degrees per round.
            baudrate (int): Baud rate.
            velocity (int): Velocity.
            acceleration (int): Acceleration.
            deceleration (int): Deceleration.
        """
        self.__total_step_per_round = total_step_per_round
        self.__deg_per_round = deg_per_round
        self.__baudrate = baudrate
        self.__velocity = velocity
        self.__acceleration = acceleration
        self.__deceleration = deceleration
        
        self.__gimbal_steps_ratio = int(self.__total_step_per_round / self.__deg_per_round)

    def get_device_unit_from_angle(self, angle):
        """
        Input degrees and return steps for gimbal

        Args:
            angle (float): angle value

        Returns:
            str: gimbal steps
        """
        return str(int(angle * self.__gimbal_steps_ratio))
    
    def get_angle_from_device_unit(self, steps):
        """
        Input steps and return degrees for gimbal

        Args:
            steps (int): gimbal steps

        Returns:
            str: angle value
        """
        return str(int(steps / self.__gimbal_steps_ratio))
    
    def set_zero(self, axis):
        """
        Set gimbal position as zero
        
        Args:
            axis (str): axis to set as zero position - X/Y
        """
        try:
            c = self.g.GCommand  # alias the command callable

            if axis == 'X':
                c('DP 0')  # set Home as 0            
            if axis == 'Y':
                c('DP ,0')  # set Home as 0

            del c
        except gclib.GclibError as e:
            print(f'Error in <set_zero>: {e}')

    def home(self, axis, side, wait_for_completion=True):
        """
        Set gimbal homing

        Args:
            axis (str): Movement axis X/Y/XY (both).
            side (str): Motion direction clockwise and counterclockwise.
            wait_for_completion (bool, optional): True if wait for motion done.
                                                  False if not. Defaults to True.
        
        Returns:
            bool: True if homed, else False
        """
        try:
            c = self.g.GCommand  # alias the command callable
            print('\nHoming ...')

            if side == 'counterclockwise':
                c('CN 1,1,1,0,0')
            elif side == 'clockwise':
                c('CN 1,-1,1,0,0')
            
            if axis == 'X':
                c('FE')  # X-axis home
                try:
                    c('BGA')  # Homing
                    if wait_for_completion:
                        self.g.GMotionComplete('A')
                except:
                    print('X-axis reached the limit')

            if axis == 'Y':
                c('FE')  # Y-axis home
                try:
                    c('BGB')  # Homing
                    if wait_for_completion:
                        self.g.GMotionComplete('B')
                except:
                    print('Y-axis reached the limit')

            if axis == 'XY':
                c('HM')  # X-axis home
                try:
                    c('BGA')  # Homing
                except:
                    print('X-axis reached the limit')
                try:
                    c('BGB')  # Homing
                except:
                    print('Y-axis reached the limit')

                if wait_for_completion:
                    self.g.GMotionComplete('A')
                    print('Homing X Done')
                    self.g.GMotionComplete('B')
                    print('Homing Y Done')

            print('Homing Done')
            del c  # delete the alias
            return True

        except gclib.GclibError as e:
            print(f'Error in <home>: {e}')
            return False

    def connect(self):
        """
        Connect to gimbal
        
        Returns:
            bool: True if connection established,
                  else False
        """
        try:
            available = self.g.GAddresses()
            
            for a in sorted(available.keys()):
                port = a
                
                try:
                    self.g.GOpen(f'-a {port} -b {self.__baudrate} -s ALL')
                    return True
                except:
                    pass
                
            return False
        except gclib.GclibError as e:
            print(f'Error in <connect>: {e}')
            self.g.GClose()  # close connections!
            
            return False

    def disconnect(self):
        """
        Disconnect from gimbal
        """
        try:
            self.g.GClose()  # close connections!
            
        except Exception as e:
            print(f'Error in <disconnect>: {e}')

    def setup(self):
        """
        Set motor configurations
        """
        self.connect()
        
        try:
            c = self.g.GCommand  # alias the command callable
            # configures the polarity of the limit switches, home switches
            c('CN 1,1,1,0,0')
            c('PT 1,1')
            
            for axis in ['X', 'Y']:
                self.set_velocity(axis=axis, velocity=self.__velocity)
                self.set_deceleration(axis=axis, deceleration=self.__deceleration)
                self.set_acceleration(axis=axis, acceleration=self.__acceleration)

            print(self.g.GInfo())

            print(f'Motor Configuration:\nAccelerations: {self.__acceleration}[cts/sec^2] \nSpeed: {self.__velocity}[cts/sec]')
                
            del c  # delete the alias
        except gclib.GclibError as e:
            print(f'Error in <setup>: {e}')

    def get_position(self):
        """
        Read gimbal current position

        Returns:
            tuple: x, y position
        """
        try:
            c = self.g.GCommand  # alias the command callable
            output = c('DE ?,?')
            xy = [pos.lstrip() for pos in output.split(',')]
            
            del c
            return int(xy[0]) / self.__gimbal_steps_ratio, int(xy[1]) / self.__gimbal_steps_ratio
        
        except gclib.GclibError as e:
            print(f'Error in <get_position>: {e}')
            return -9999.0, -9999.0  # error value indicator
    
    def get_position_encoder(self, axis):
        """
        Read gimbal current position from encoder

        Args:
            axis (str, optional): Movement axis.

        Returns:
            float: encoder position
        """
        try:
            cmd = self.g.GCommand  # alias the command callable

            if axis == 'X':
                position_encoder = cmd('TPA')
            if axis == 'Y':
                position_encoder = cmd('TPB')

            sign = -1 if '-' in position_encoder else 1
            position_encoder = [int(s) for s in re.findall(r'\b\d+\b', position_encoder)][0] * sign

            del cmd
            return position_encoder / self.__gimbal_steps_ratio

        except gclib.GclibError as e:
            print(f'Error in <get_position_encoder>: {e}')
            return -9999.0  # error value indicator
            
    def move_gimbal_abs(self, axis, angle, wait_for_completion=True):
        """
        Move Gimbal absolute

        Args:
            axis (str): Movement axis (X/Y)
            angle (float): Movement angle
            wait_for_completion (bool, optional): True if wait for motion done.
                                                  False if not. Defaults to True.
        """
        try:
            c = self.g.GCommand  # alias the command callable
           
            if axis == 'X':
                cmd = f'PA {self.get_device_unit_from_angle(angle)};BGA'
               
            elif axis == 'Y':
                cmd = f'PA ,{self.get_device_unit_from_angle(angle)};BGB'
               
            print(f'Moving axis {axis} to {angle}; ({cmd})')
            c(cmd)  # absolute motion move
            if wait_for_completion:
                self.g.GMotionComplete('AB')
                print('Motion Done')
           
            del c  # delete the alias
        except gclib.GclibError as e:
            print(f'Error in <move_gimbal_abs>: {e}')
            if wait_for_completion:
                self.g.GMotionComplete('AB')
                print('Motion Done')
            del c  # delete the alias
    
    def move_gimbal_rel(self, axis, angle, wait_for_completion=True):
        """
        Move Gimbal relative

        Args:
            axis (str): Movement axis (X/Y)
            angle (float): Movement angle
            wait_for_completion (bool, optional): True if wait for motion done.
                                                  False if not. Defaults to True.
        """
        try:
            c = self.g.GCommand  # alias the command callable
           
            if axis == 'X':
                cmd = f'PR {self.get_device_unit_from_angle(angle)};BGA'
               
            elif axis == 'Y':
                cmd = f'PR ,{self.get_device_unit_from_angle(angle)};BGB'
               
            print(f'Moving axis {axis} to {angle}; ({cmd})')
            c(cmd)  # absolute motion move
            if wait_for_completion:
                self.g.GMotionComplete('AB')
                print('Motion Done')
           
            del c  # delete the alias
        except gclib.GclibError as e:
            print(f'Error in <move_gimbal_rel>: {e}')
            if wait_for_completion:
                self.g.GMotionComplete('AB')
                print('Motion Done')
            del c  # delete the alias

    def stop(self, axis):
        """
        Stop Gimbal
        
        Args:
            axis (str): Stop axis 'X'/'Y'/'' (stop all).
            
        Returns:
            bool: Execution status. True if succeeded, else False
        """
        try:
            c = self.g.GCommand  # alias the command callable
            print('NEWMARK: Stop')
            c(f'ST {axis}')  # Stoping
            del c  # delete the alias
            return True

        except gclib.GclibError as e:
            print(f'Error in <stop>: {e}')
            return False
        
    def find_index(self, side, axis):
        """
        Find encoder index of axes

        Args:
            side (str): clockwise/counterclockwise.
            axis (str): axis name - 'X', 'Y'.
            
        Returns:
            str: velocity value
        """ 
        try:
            c = self.g.GCommand  # alias the command callable

            if side == 'counterclockwise':
                c('CN 1,1,1,0,0')
            elif side == 'clockwise':
                c('CN 1,-1,1,0,0')

            if axis == 'X':
                velocity = c('FIA')  # velocity cts/sec
                c('BGA')
            if axis == 'Y':
                velocity = c('FIB')  # velocity cts/sec
                c('BGB')

            del c  # delete the alias
            return velocity
        except gclib.GclibError as e:
            print(f'Error in <find_index>: {e}')
            return 'Error' 
        
    def get_velocity(self, axis):
        """
        Get the slew velocity of axes

        Args:
            axis (str): axis name - 'X', 'Y'

        Returns:
            str: speed
        """ 
        try:
            cmd = self.g.GCommand  # alias the command callable

            if axis == 'X':
                velocity = cmd(f'TVA')  # velocity cts/sec
            if axis == 'Y':
                velocity = cmd('TVB')  # velocity cts/sec

            del cmd  # delete the alias
            return velocity
        except Exception as e:
            print(f'Error in <get_velocity>: {e}')
            return 'Error'
    
    def set_velocity(self, axis, velocity):
        """
        Set Gimbal velocity

        Args:
            axis (str): Gimbal axis X/Y
            velocity (int): Gimbal velocity
        """
        try:
            c = self.g.GCommand  # alias the command callable

            if axis == 'X':
                c(f'SP {velocity}')  # X-axis velocity cts/sec
            if axis == 'Y':
                c(f'SP ,{velocity}')  # Y-axis velocity cts/sec

            del c  # delete the alias
        except gclib.GclibError as e:
            print(f'Error in <set_velocity>: {e}')
    
    def set_acceleration(self, axis, acceleration):
        """
        Sets the linear acceleration rate of the
        motors for independent moves

        Args:
            axis (str): Gimbal axis X/Y
            acceleration (int): Gimbal acceleration
        """
        try:
            c = self.g.GCommand  # alias the command callable

            if axis == 'X':
                c(f'AC {acceleration}')  # velocity cts/sec
            if axis == 'Y':
                c(f'AC ,{acceleration}')  # velocity cts/sec

            del c  # delete the alias
        except gclib.GclibError as e:
            print(f'Error in <set_acceleration> {e}')
    
    def set_deceleration(self, axis, deceleration):
        """
        Sets the linear deceleration rate of the
        motors for independent moves

        Args:
            axis (str): Gimbal axis X/Y
            deceleration (int): Gimbal deceleration
        """
        try:
            c = self.g.GCommand  # alias the command callable

            if axis == 'X':
                c(f'DC {deceleration}')  # velocity cts/sec
            if axis == 'Y':
                c(f'DC ,{deceleration}')  # velocity cts/sec

            del c  # delete the alias
        except gclib.GclibError as e:
            print(f'Error in <set_deceleration>: {e}')
    
    def set_forward_limit(self, axis, limit):
        """
        Set Gimbal forward limit

        Args:
            axis (str): Gimbal axis X/Y
            limit (int): Gimbal limit
        """
        try:
            c = self.g.GCommand  # alias the command callable

            if axis == 'X':
                c(f'FL {self.get_device_unit_from_angle(limit)}')  # Set limit to counts on the axis
            if axis == 'Y':
                c(f'FL ,{self.get_device_unit_from_angle(limit)}')  # Set limit to counts on the axis

            del c  # delete the alias
        except gclib.GclibError as e:
            print(f'Error in <set_forward_limit>: {e}')

    def set_backward_limit(self, axis, limit):
        """
        Set Gimbal backward limit

        Args:
            axis (str): Gimbal axis X/Y
            limit (int): Gimbal limit
        """
        try:
            c = self.g.GCommand  # alias the command callable

            if axis == 'X':
                c(f'BL {self.get_device_unit_from_angle(limit)}')  # Set limit to counts on the axis
            if axis == 'Y':
                c(f'BL ,{self.get_device_unit_from_angle(limit)}')  # Set limit to counts on the axis

            del c  # delete the alias
        except gclib.GclibError as e:
            print(f'Error in <set_backward_limit>: {e}')
            
    def motion_complete(self, axis):
        """
        Wait for motion completion on
        selected axis/axes
        
        Args:
            axis (str): Gimbal axis X/Y/XY

        Returns:
            bool: True\False
        """
        target_axis = 'A'  # default - X axis
        if axis == 'Y':
            target_axis = 'B'
        elif axis == 'XY':
            target_axis = 'AB'
        
        try:
            self.g.GMotionComplete(target_axis)
            print(f'Homing {axis} Done')
            return True
        except gclib.GclibError as e:
            print(f'Error in <motion_complete>: {e}')
            return False
