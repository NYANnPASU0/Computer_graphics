from main_window import Point

class Sutherlan_Cohen:
    def __init__(self, x_min, y_min, x_max, y_max):
            self.x_min = x_min
            self.y_min = y_min
            self.x_max = x_max
            self.y_max = y_max
            
            self.INSIDE = 0  # 0000 - внутри
            self.LEFT = 1    # 0001 - слева
            self.RIGHT = 2   # 0010 - справа
            self.BOTTOM = 4  # 0100 - снизу
            self.TOP = 8     # 1000 - сверху

    def bit_code_points(self, x, y): # кодирование точек битами(побитовое или)
        code = self.INSIDE
        if x < self.x_min:
            code |= self.LEFT
        elif x > self.x_max:
            code |= self.RIGHT

        if y < self.y_min:
            code |= self.BOTTOM
        elif y > self.y_max:
            code |= self.TOP

        return code
    
    def clip_line(self, p1, p2):

        code_point1 = self.bit_code_points(p1.x, p1.y)
        code_point2 = self.bit_code_points(p2.x, p2.y)

        while True:
            # если точка A внутри окна, поменять точки местами
            

            # тривиальные случаи
            # 1 - отрезок полностью внутри
            if code_point1 == 0 and code_point2 == 0:
                return p1, p2
            
            # 2 - отрезок полностью снаружи(общий бит 1)
            if (code_point1 & code_point2) != 0:
                return None
            

