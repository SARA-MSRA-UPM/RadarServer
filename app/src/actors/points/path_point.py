# external imports
from svgpathtools import svg2paths
import logging

# internal imports
from .point import Point

class PathPoint(Point):

    def __init__(self,
                 svg_path_file: str,
                 x: float = 0,
                 y: float = 0):
        super().__init__(x, y)
        
        # Extraer y transformar los paths usando `svgpathtools`
        if svg_path_file[-1] == "2":
            paths = self._load_and_transform_paths(svg_path_file, (200,200), (700,700))
        elif svg_path_file[-1] == "3":
            paths = self._load_and_transform_paths(svg_path_file, (-50,-50), (50,50))
        elif svg_path_file[-1] == "4":
            paths = self._load_and_transform_paths(svg_path_file, (-100,100), (300,500))
        else:
            paths = self._load_and_transform_paths(svg_path_file, (0,0),(100,100))

        
        # Generar puntos interpolados a partir de los paths transformados
        self.path_points = self._extract_points_from_paths(paths)

        # Configuración de los índices de seguimiento del recorrido
        self.path_index = 0
        self.loop = True
        self.path_segment_index = 0

        # Ajustar la velocidad para cubrir todos los puntos en 1 minuto (60 segundos)
        total_points = sum(len(points) for points in self.path_points)
        self.speed = 60 / total_points  # Ajuste para completar en 60 segundos

        # Mostrar el bounding box inicial
        self._display_bounding_box()
        self.update()

    def _load_and_transform_paths(self, svg_path_file, target_min=(0, 0), target_max=(100, 100)):
        """
        Carga los paths desde un archivo SVG y aplica escalado y traslación para ajustarlos
        a un bounding box específico.
        """
        paths, _ = svg2paths(svg_path_file)

        # Calcular el bounding box actual de los paths
        min_x = min(seg.start.real for path in paths for seg in path)
        max_x = max(seg.start.real for path in paths for seg in path)
        min_y = min(seg.start.imag for path in paths for seg in path)
        max_y = max(seg.start.imag for path in paths for seg in path)

        # Calcular escala y traslación para ajustar al bounding box deseado
        scale_x = (target_max[0] - target_min[0]) / (max_x - min_x)
        scale_y = (target_max[1] - target_min[1]) / (max_y - min_y)
        scale = min(scale_x, scale_y)  # Mantener la relación de aspecto

        # Escalar y trasladar cada path
        transformed_paths = []
        for path in paths:
            path = path.scaled(scale)  # Escalado uniforme
            path = path.translated(complex(target_min[0] - min_x * scale, target_min[1] - min_y * scale))
            transformed_paths.append(path)

        return transformed_paths

    def _extract_points_from_paths(self, paths, num_segments=1000):
        """
        Extrae puntos interpolados de cada path en el archivo SVG.
        
        :param paths: Paths cargados y transformados.
        :param num_segments: Número total de puntos objetivo.
        :return: Lista de listas, cada sublista contiene (x, y) puntos de un path.
        """
        path_segments = []
        for path in paths:
            points = []
            path_length = path.length()
            segment_points = max(10, int(path_length * (num_segments / sum(p.length() for p in paths))))
            
            for i in range(segment_points + 1):
                t = i / segment_points
                point = path.point(t)
                points.append((point.real, point.imag))

            path_segments.append(points)
        
        return path_segments

    def _display_bounding_box(self):
        all_points = [p for segment in self.path_points for p in segment]
        x_values = [p[0] for p in all_points]
        y_values = [p[1] for p in all_points]
        min_x, max_x = min(x_values), max(x_values)
        min_y, max_y = min(y_values), max(y_values)
        
        logging.info(
            f"Bounding Box: Min X: {min_x}, Max X: {max_x}, Min Y: {min_y}, Max Y: {max_y}"
        )

    def update(self):
        """
        Avanza en el trayecto del SVG punto por punto.
        """
        if self.path_segment_index < len(self.path_points):
            current_segment = self.path_points[self.path_segment_index]
            
            if self.path_index < len(current_segment) - 1:
                self.x, self.y = current_segment[self.path_index]
                self.path_index += 1
            else:
                self.path_index = 0
                self.path_segment_index += 1
        else:
            if self.loop:
                self.path_segment_index = 0
                self.path_index = 0
                self.loop = False
            else:
                super().stop()
