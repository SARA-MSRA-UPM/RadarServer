from threading import Thread, Event
from .monitor import Monitor
from ..actors.points.path_point import PathPoint
from ..actors.radar import Radar
from .radar_collection import RadarCollection
import socket

class SocketLector(Thread):
    def __init__(self, file_path: str, sock: socket.socket, radar_collection: RadarCollection):
        super().__init__()
        self._monitor = Monitor()
        self._point = PathPoint(file_path)
        self._radars = [
            Radar(
                name=radar.name,
                position=(radar.position_x, radar.position_y),
                orientation_initial=radar.orientation_initial,
                detection_range=radar.detection_range,
                increment=radar.increment,
                revolutions_per_second=4,
                detectable_points=[self._point],
                monitor=self._monitor
            ) for radar in radar_collection.radars
        ]
        self._sock = sock
        self._stop_event = Event()  

    def run(self):
        try:
            self._point.start()
            for radar in self._radars:
                radar.start()
                
            while self._point.is_alive() and not self._stop_event.is_set():
                detection = self._monitor.take_first_detection()
                if detection:
                    try:
                        self._sock.sendall(f"{detection}\n".encode())
                    except socket.error as e:
                        print(f"Error sending data: {e}")
                        break  
            
        finally:
            for radar in self._radars:
                radar.stop()
            self._point.stop()
            self._sock.close()

    def stop(self):
        self._stop_event.set()
