from abc import ABC, abstractmethod
import airsim
import cv2
import numpy as np
from pymavlink import mavutil
import time


class IDroneApi(ABC):
    def __init__(self, connect_uri = None):
        self.client = None
        self.connect_uri = connect_uri

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def get_image(self, max_attempts=10):
        pass


class AirSimAPI(IDroneApi):
    def connect(self):
        self.client = airsim.MultirotorClient()
        self.client.confirmConnection()
        return "Подключение через AirSim установлено"

    def get_image(self, max_attempts=10):
        responses = self.client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)])

        if responses:
            response = responses[0]

            img_1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8)
            img_rgb = img_1d.reshape(response.height, response.width, 3)

            cv2.imwrite('test.jpg', img_rgb)
            print("Image saved")
        else:
            print("No images found")


class MavLinkAPI(IDroneApi):
    def connect(self):
        self.client = mavutil.mavlink_connection(self.connect_uri)
        self.client.wait_heartbeat()
        print("Соединение через MavLink установлено")

    def get_image(self, max_attempts=10, delay=1):
        self.client.mav.command_long_send(
            self.client.target_system,
            self.client.target_component,
            mavutil.mavlink.MAV_CMD_IMAGE_START_CAPTURE,
            0,
            0,  # зарезервирована ли камера
            0,  # какая задержка между снимками
            1,  # общее кол-во изображений для захвата
            0,
            0, 0, 0  # дополнительные параметры
        )

        for _ in range(max_attempts):  # _ название переменной, которую мы не хотим использовать
            response = self.client.recv_match(type='CAMERA_IMAGE_CAPTURED', blocking=True, timeout=5)
            if response:
                print(f"Путь до файла: {response.file_path}")
                break
            else:
                print(f"Ожидание камеры...")
            time.sleep(delay)


class DroneAPIFactory:
    @staticmethod
    def get_drone_api(api_type, connect_uri):
        if api_type == 'airsim':
            return AirSimAPI(connect_uri)
        elif api_type == 'mavlink':
            return MavLinkAPI(connect_uri)
        else:
            raise ValueError("Такое API не реализовано")


if __name__ == '__main__':
    api_type = 'airsim'
    connect_uri = "tcp://127.0.0.1:5555"
    drone = DroneAPIFactory.get_drone_api(api_type, connect_uri)
    drone.connect()
    drone.get_image()



