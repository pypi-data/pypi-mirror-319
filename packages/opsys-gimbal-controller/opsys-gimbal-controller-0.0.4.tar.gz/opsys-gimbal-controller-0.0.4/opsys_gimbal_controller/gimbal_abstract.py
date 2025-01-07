from abc import ABC, abstractmethod


class GimbalAbstract(ABC):
    @abstractmethod
    def home(self, axis: str, side: str):
        pass
    
    @abstractmethod
    def get_device_unit_from_angle(self, angle: float):
        pass
    
    @abstractmethod
    def get_angle_from_device_unit(self, int: int):
        pass
    
    @abstractmethod
    def set_zero(self, axis: str):
        pass
    
    @abstractmethod
    def connect(self):
        pass
    
    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def setup(self):
        pass
    
    @abstractmethod
    def get_position(self):
        pass
    
    @abstractmethod
    def get_position_encoder(self, axis: str):
        pass
    
    @abstractmethod
    def move_gimbal_abs(self, axis: str, angle: float):
        pass
    
    @abstractmethod
    def move_gimbal_rel(self, axis: str, angle: float):
        pass
    
    @abstractmethod
    def stop(self, axis: str):
        pass
    
    @abstractmethod
    def find_index(self, side: str, axis: str):
        pass
    
    @abstractmethod
    def get_velocity(self, axis: str):
        pass
    
    @abstractmethod
    def set_velocity(self, axis: str, velocity: int):
        pass
    
    @abstractmethod
    def set_acceleration(self, axis: str, acceleration: int):
        pass
    
    @abstractmethod
    def set_deceleration(self, axis: str, deceleration: int):
        pass
    
    @abstractmethod
    def set_forward_limit(self, axis: str, limit: int):
        pass
    
    @abstractmethod
    def set_backward_limit(self, axis: str, limit: int):
        pass

    @abstractmethod
    def motion_complete(self, axis: str):
        pass
