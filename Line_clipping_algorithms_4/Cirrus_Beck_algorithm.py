from main_window import Point

class Cyrus_Beck:
    def __init__(self, polygon):
        self.polygon = polygon
        self.edges = []
        
        n = len(polygon.points)
        cx = sum(p.x for p in polygon.points) / n
        cy = sum(p.y for p in polygon.points) / n
        centroid = Point(cx, cy) # геометрический центр многоугольника

        for i in range(n):
            p1 = polygon.points[i]
            p2 = polygon.points[(i + 1) % n]

            dx = p2.x - p1.x
            dy = p2.y - p1.y
            
            mid_x = (p1.x + p2.x) / 2
            mid_y = (p1.y + p2.y) / 2
            
            to_center_x = cx - mid_x
            to_center_y = cy - mid_y
            
            # перпендикуляр
            n_cand1 = (-dy, dx)
            dot_center = to_center_x * n_cand1[0] + to_center_y * n_cand1[1]
            
            # нормаль к центру многоугольника
            if dot_center > 0:
                n_vec = (-n_cand1[0], -n_cand1[1])
            else:
                n_vec = n_cand1
                
            self.edges.append({
                'point': p1,
                'vector': (dx, dy),
                'normal': n_vec 
            })

    def clip_line(self, p1, p2):
        P_napravlen = (p2.x - p1.x, p2.y - p1.y)
        
        t_entering = 0.0
        t_leaving = 1.0
        
        for edge in self.edges:
            # значения по ключу
            Vi = edge['point'] 
            Ni = edge['normal']
            
            w_x = p1.x - Vi.x
            w_y = p1.y - Vi.y
            numer = -(w_x * Ni[0] + w_y * Ni[1]) # -((P1 - Vi), Ni)

            denom = P_napravlen[0] * Ni[0] + P_napravlen[1] * Ni[1] # ((P2 - V1), Ni)
            
            # параллельность прямой
            if abs(denom) < 1e-9:
                if numer < 0:
                    return None # вне полуплоскости
                continue
            
            t = numer / denom
            
            if denom < 0: # ПВ
                t_entering = max(t_entering, t)
            else: # ПП
                t_leaving = min(t_leaving, t)
            
            if t_entering > t_leaving:
                return None
        
        # отрезок видим 
        res_p1 = Point(p1.x + t_entering * P_napravlen[0], p1.y + t_entering * P_napravlen[1])
        res_p2 = Point(p1.x + t_leaving * P_napravlen[0], p1.y + t_leaving * P_napravlen[1])
        
        return (res_p1, res_p2)
    

    def get_all_intersections(self, p1, p2):
        intersections = []
        P_napravlen = (p2.x - p1.x, p2.y - p1.y)
        
        for edge in self.edges:
            Vi = edge['point']
            Ni = edge['normal']
            
            w_x = p1.x - Vi.x
            w_y = p1.y - Vi.y
            numer = -(w_x * Ni[0] + w_y * Ni[1])
            denom = P_napravlen[0] * Ni[0] + P_napravlen[1] * Ni[1]
            
            if abs(denom) < 1e-9:
                continue
            
            t = numer / denom
            
            inter_x = p1.x + t * P_napravlen[0]
            inter_y = p1.y + t * P_napravlen[1]
            
            intersections.append(Point(inter_x, inter_y))
        
        return intersections