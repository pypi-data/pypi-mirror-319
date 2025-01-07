import unittest
from unittest.mock import patch, MagicMock
from opsys_gimbal_controller.gimbal_controller import GimbalController


GIMBAL_TYPE = 'Newmark'


class Test(unittest.TestCase):
    @ classmethod
    def setUp(self):
        pass

    @ classmethod
    def setUpClass(cls):
        pass

    @ classmethod
    def tearDownClass(cls):
        pass
    
    @ patch.object(GimbalController, 'set_gimbal_parameters')
    def test_set_gimbal_parameters(self, gimbal_mock: MagicMock):
        gimbal = GimbalController(motor_type=GIMBAL_TYPE)
        total_step_per_round = 3600000
        deg_per_round = 360
        baudrate = 19200
        velocity = 50000
        acceleration = 200000
        deceleration = 150000
        gimbal.set_gimbal_parameters(total_step_per_round=total_step_per_round,
                                     deg_per_round=deg_per_round,
                                     baudrate=baudrate,
                                     velocity=velocity,
                                     acceleration=acceleration,
                                     deceleration=deceleration)
        gimbal_mock.assert_called_once_with(total_step_per_round=3600000,
                                            deg_per_round=360,
                                            baudrate=19200,
                                            velocity=50000,
                                            acceleration=200000,
                                            deceleration=150000)
        
    @ patch.object(GimbalController, 'get_device_unit_from_angle')
    def test_get_device_unit_from_angle(self, gimbal_mock: MagicMock):
        gimbal = GimbalController(motor_type=GIMBAL_TYPE)
        angle = 0
        gimbal.get_device_unit_from_angle(angle=angle)
        gimbal_mock.assert_called_once_with(angle=0)
        
    @ patch.object(GimbalController, 'get_angle_from_device_unit')
    def test_get_angle_from_device_unit(self, gimbal_mock: MagicMock):
        gimbal = GimbalController(motor_type=GIMBAL_TYPE)
        steps = 0
        gimbal.get_angle_from_device_unit(steps=steps)
        gimbal_mock.assert_called_once_with(steps=0)
        
    @ patch.object(GimbalController, 'set_zero')
    def test_set_zero(self, gimbal_mock: MagicMock):
        gimbal = GimbalController(motor_type=GIMBAL_TYPE)
        axis = 'X'
        gimbal.set_zero(axis=axis)
        gimbal_mock.assert_called_once_with(axis='X')

    @ patch.object(GimbalController, 'connect')
    def test_connect(self, gimbal_mock: MagicMock):
        gimbal = GimbalController(motor_type=GIMBAL_TYPE)
        gimbal.connect()
        gimbal_mock.assert_called_once_with()

    @ patch.object(GimbalController, 'disconnect')
    def test_disconnect(self, gimbal_mock: MagicMock):
        gimbal = GimbalController(motor_type=GIMBAL_TYPE)
        gimbal.disconnect()
        gimbal_mock.assert_called_once_with()

    @ patch.object(GimbalController, 'setup')
    def test_setup(self, gimbal_mock: MagicMock):
        gimbal = GimbalController(motor_type=GIMBAL_TYPE)
        gimbal.setup()
        gimbal_mock.assert_called_once_with()

    @ patch.object(GimbalController, 'get_position')
    def test_get_position(self, gimbal_mock: MagicMock):
        gimbal = GimbalController(motor_type=GIMBAL_TYPE)
        gimbal.get_position()
        gimbal_mock.assert_called_once_with()
        
    @ patch.object(GimbalController, 'get_position_encoder')
    def test_get_position(self, gimbal_mock: MagicMock):
        gimbal = GimbalController(motor_type=GIMBAL_TYPE)
        axis = 'X'
        gimbal.get_position_encoder(axis=axis)
        gimbal_mock.assert_called_once_with(axis='X')

    @ patch.object(GimbalController, 'home')
    def test_home(self, gimbal_mock: MagicMock):
        gimbal = GimbalController(motor_type=GIMBAL_TYPE)
        axis = 'XY'
        side = 'clockwise'
        gimbal.home(axis=axis, side=side)
        gimbal_mock.assert_called_once_with(axis='XY', side='clockwise')

    @ patch.object(GimbalController, 'move_gimbal_abs')
    def test_move_gimbal_abs(self, gimbal_mock: MagicMock):
        gimbal = GimbalController(motor_type=GIMBAL_TYPE)
        axis = 'X'
        angle = 50
        gimbal.move_gimbal_abs(axis=axis, angle=angle)
        gimbal_mock.assert_called_once_with(axis='X', angle=50)

    @ patch.object(GimbalController, 'move_gimbal_rel')
    def test_move_gimbal_rel(self, gimbal_mock: MagicMock):
        gimbal = GimbalController(motor_type=GIMBAL_TYPE)
        axis = 'X'
        angle = 50
        gimbal.move_gimbal_rel(axis=axis, angle=angle)
        gimbal_mock.assert_called_once_with(axis='X', angle=50)
        
    @ patch.object(GimbalController, 'stop')
    def test_stop(self, gimbal_mock: MagicMock):
        gimbal = GimbalController(motor_type=GIMBAL_TYPE)
        axis = ''
        gimbal.stop(axis=axis)
        gimbal_mock.assert_called_once_with(axis='')
        
    @ patch.object(GimbalController, 'find_index')
    def test_find_index(self, gimbal_mock: MagicMock):
        gimbal = GimbalController(motor_type=GIMBAL_TYPE)
        axis = 'X'
        side = 'clockwise'
        gimbal.find_index(side=side, axis=axis)
        gimbal_mock.assert_called_once_with(side='clockwise', axis='X')
        
    @ patch.object(GimbalController, 'get_velocity')
    def test_get_velocity(self, gimbal_mock: MagicMock):
        gimbal = GimbalController(motor_type=GIMBAL_TYPE)
        axis = 'X'
        gimbal.get_velocity(axis=axis)
        gimbal_mock.assert_called_once_with(axis='X')
        
    @ patch.object(GimbalController, 'set_velocity')
    def test_set_velocity(self, gimbal_mock: MagicMock):
        gimbal = GimbalController(motor_type=GIMBAL_TYPE)
        axis = 'X'
        velocity = 2500
        gimbal.set_velocity(axis=axis, velocity=velocity)
        gimbal_mock.assert_called_once_with(axis='X', velocity=2500)
        
    @ patch.object(GimbalController, 'set_acceleration')
    def test_set_acceleration(self, gimbal_mock: MagicMock):
        gimbal = GimbalController(motor_type=GIMBAL_TYPE)
        axis = 'X'
        acceleration = 2500
        gimbal.set_acceleration(axis=axis, acceleration=acceleration)
        gimbal_mock.assert_called_once_with(axis='X', acceleration=2500)
        
    @ patch.object(GimbalController, 'set_deceleration')
    def test_set_deceleration(self, gimbal_mock: MagicMock):
        gimbal = GimbalController(motor_type=GIMBAL_TYPE)
        axis = 'X'
        deceleration = 2500
        gimbal.set_deceleration(axis=axis, deceleration=deceleration)
        gimbal_mock.assert_called_once_with(axis='X', deceleration=2500)
        
    @ patch.object(GimbalController, 'set_forward_limit')
    def test_set_forward_limit(self, gimbal_mock: MagicMock):
        gimbal = GimbalController(motor_type=GIMBAL_TYPE)
        axis = 'X'
        limit = -45
        gimbal.set_forward_limit(axis=axis, limit=limit)
        gimbal_mock.assert_called_once_with(axis='X', limit=-45)
        
    @ patch.object(GimbalController, 'set_backward_limit')
    def test_set_backward_limit(self, gimbal_mock: MagicMock):
        gimbal = GimbalController(motor_type=GIMBAL_TYPE)
        axis = 'X'
        limit = -45
        gimbal.set_backward_limit(axis=axis, limit=limit)
        gimbal_mock.assert_called_once_with(axis='X', limit=-45)


if __name__ == '__main__':
    unittest.main()
