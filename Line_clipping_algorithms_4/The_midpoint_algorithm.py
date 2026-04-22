from main_window import Point
from Sutherland_Cohen_algorithm import Sutherlan_Cohen

class Midpoint(Sutherlan_Cohen):
    def __init__(self, x_min, y_min, x_max, y_max):
        super().__init__(x_min, y_min, x_max, y_max)
        self.created_points = []

    def clip_line(self, p1, p2, result_line=None, pixel_size = 0.1):
        if result_line is None:
            result_line = []

        # проверка длины отрезка
        length = ((p2.x - p1.x)**2 + (p2.y - p1.y)**2)**0.5

        if length < pixel_size:
            # проверка хотя бы одна точка внутри или на границе
            code1 = self.bit_code_points(p1.x, p1.y)
            code2 = self.bit_code_points(p2.x, p2.y)
            
            # если не тривиальное отсечение
            if (code1 & code2) == 0:
                result_line.append((p1, p2))
            
            return result_line
        
        # вычислить коды для точек A и B
        code1 = self.bit_code_points(p1.x, p1.y)
        code2 = self.bit_code_points(p2.x, p2.y)

        # тривиальные случаи
        # оба внутри
        if code1 == 0 and code2 == 0:
            result_line.append((p1, p2))
            return result_line
        # оба снаружи
        if (code1 & code2) != 0:
            return result_line
        
        # вычислить координаты точки С - середины отрезка
        mid_x = (p1.x + p2.x) / 2.0
        mid_y = (p1.y + p2.y) / 2.0
        mid_point = Point(mid_x, mid_y)

        self.created_points.append(mid_point)

        # рекурсивно выполнить алгоритм ядля отрезков AC и CB
        self.clip_line(p1, mid_point, result_line, pixel_size)
        self.clip_line(mid_point, p2, result_line, pixel_size)
        
        return result_line