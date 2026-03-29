#include <stdio.h>
#include <math.h>
#include <float.h>
#include <windows.h>

typedef struct {
    double x, y, z;
} Point;


Point vector(Point from, Point to);
Point cross_product(Point a, Point b);
double dot_product(Point a, Point b);

void is_same_side(double A, double B, double C, double x1, double y1, double x2, double y2); //1
void intersection_vector(double ax, double ay, double bx, double by, double cx, double cy, double dx, double dy); //2
int is_point_inside_angle(Point A, Point B, Point C, Point D); //3
void is_same_space(double A, double B, double C, double D, double x1, double y1, double z1, double x2, double y2, double z2);//4

Point vector(Point from, Point to) {
    Point v;
    v.x = to.x - from.x;
    v.y = to.y - from.y;
    v.z = to.z - from.z;
    return v;
}

//векторное произведение
Point cross_product(Point a, Point b) {
    Point result;
    result.x = a.y * b.z - a.z * b.y;
    result.y = a.z * b.x - a.x * b.z;
    result.z = a.x * b.y - a.y * b.x;
    return result;
}

//скалярное произведение
double dot_product(Point a, Point b) {
    return a.x * b.x + a.y * b.y + a.z * b.z;
}

//1
void is_same_side(double A, double B, double C, double x1, double y1, double x2, double y2)
{
    double check_1 = A * x1 + B * y1 + C;
    double check_2 = A * x2 + B * y2 + C;
    
    int on_line1 = 0;
    int on_line2 = 0;
    if (fabs(check_1) < DBL_EPSILON) on_line1 = 1;
    if (fabs(check_2) < DBL_EPSILON) on_line2 = 1;
    
    if (on_line1 && on_line2) 
    {
        printf("Точки A и B лежат на одной прямой\n");
    }
    else if (on_line1) 
    {
        printf("т. A лежит на прямой\n");
    }
    else if (on_line2) 
    {
        printf("т. B лежит на прямой\n");
    }
    else 
    {
        if (check_1 * check_2 > 0) 
        {
            printf("Точки A и B находятся по одну сторону\n");
        }
        else 
        {
            printf("Точки A и B находятся по разные стороны\n");
        }
    }
}

//2
void intersection_vector(double ax, double ay, double bx, double by,
                         double cx, double cy, double dx, double dy)
{   
    double vx = bx - ax;
    double vy = by - ay;
    
    double wx = dx - cx;
    double wy = dy - cy;
    
    double sonapr = vx*wx + vy*wy;
    //C относительно луча AB
    double posC = (cx - ax)*vx + (cy - ay)*vy;
    //A относительно луча CD
    double posA = (ax - cx)*wx + (ay - cy)*wy;
    
    if (sonapr > DBL_EPSILON) {
        printf("Лучи сонаправлены\n");
        printf("Лучи пересекаются\n");
    }
    else if (sonapr < -DBL_EPSILON) {
        printf("Лучи противоположно направлены\n");
        
        if (posC >= -DBL_EPSILON && posA >= -DBL_EPSILON)
            printf("Лучи пересекаются (отрезок между A и C)\n");
        else {
            printf("Лучи не пересекаются\n");
        }
    }
}


//3
int is_point_inside_angle(Point A, Point B, Point C, Point D)
{
    Point BA = vector(B, A);
    Point BC = vector(B, C);
    Point BD = vector(B, D);

    //смешанное произведение
    Point v = cross_product(BA, BC);
    double is_compl = dot_product(v, BD);

    if (fabs(is_compl) > DBL_EPSILON) {
        printf("Точки не лежат в одной плоскости, соответственно т.D лежит вне угла ABC");
        return -1;
    }

    double sign1 = dot_product(cross_product(BA, BD), v);
    
    if (sign1 <= DBL_EPSILON) {
        printf("Точка НЕ лежит внутри угла ABC");
        return -1;
    }

    double sign2 = dot_product(cross_product(BC, BD), v);
    
    if (sign2 >= DBL_EPSILON) {
        printf("Точка НЕ лежит внутри угла ABC");
        return -1;
    }

    return 1;
}



//4
void is_same_space(double A, double B, double C, double D, double x1, double y1, double z1, 
    double x2, double y2, double z2)
{
    double check_1 = A*x1 + B*y1 + C*z1 + D;
    double check_2 = A*x2 + B*y2 + C*z2 + D;
    
    int on_plane1 = 0;
    int on_plane2 = 0;
    if (fabs(check_1) < DBL_EPSILON) on_plane1 = 1;
    if (fabs(check_2) < DBL_EPSILON) on_plane2 = 1;
    
    if (on_plane1 && on_plane2) 
    {
        printf("Точки A и B лежат на одной плоскости\n");
    }
    else if (on_plane1) 
    {
        printf("т. A лежит на плоскости\n");
    }
    else if (on_plane2) 
    {
        printf("т. B лежит на плоскости\n");
    }
    else 
    {
        if (check_1 * check_2 > 0) 
        {
            printf("Точки A и B находятся по одну сторону от плоскости\n");
        }
        else 
        {
            printf("Точки A и B находятся по разные стороны от плоскости\n");
        }
    }
}


int main() 
{    
    SetConsoleOutputCP(65001);
    int num;
    
    printf("Введите номер задачи (1-4): ");
    scanf("%d", &num);
    
    switch (num)
    {
        case 1: 
        {
            double A, B, C, x1, y1, x2, y2;

            printf("Введите значения коэффициентов прямой A, B, C (Ax + By + C = 0)\n");
            scanf("%lf %lf %lf", &A, &B, &C);
            
            printf("Введите координаты точки A на плоскости (x1, y1)\n");
            scanf("%lf %lf", &x1, &y1);
            
            printf("Введите координаты точки B на плоскости (x2, y2)\n");
            scanf("%lf %lf", &x2, &y2);
            
            is_same_side(A, B, C, x1, y1, x2, y2);
            
            //по одну сторону
            printf("\nПрямая: 2x + 3y - 6 = 0\n");
            printf("Точка A(1, 1), Точка B(0, 0)\n");
            is_same_side(2, 3, -6, 1, 1, 2, 2);
            
            //по разные стороны
            printf("\nПрямая: x + y - 4 = 0\n");
            printf("Точка A(1, 1), Точка B(5, 5)\n");
            is_same_side(1, 1, -4, 1, 1, 5, 5);
            
            // точка A на прямой
            printf("\nПрямая: 3x - 2y + 1 = 0\n");
            printf("Точка A(1, 2), Точка B(3, 4)\n");
            is_same_side(3, -2, 1, 1, 2, 3, 4);
            
            //обе точки на прямой
            printf("\nПрямая: x - 2y + 3 = 0\n");
            printf("Точка A(1, 2), Точка B(3, 3)\n");
            is_same_side(1, -2, 3, 1, 2, 3, 3);
            
            break;
        }
        case 2:
        {
            double ax, ay, bx, by, cx, cy, dx, dy;
            
            printf("Введите координаты точки A (ax, ay)\n");
            scanf("%lf %lf", &ax, &ay);
            
            printf("Введите координаты точки B (bx, by)\n");
            scanf("%lf %lf", &bx, &by);
            
            printf("Введите координаты точки C (cx, cy)\n");
            scanf("%lf %lf", &cx, &cy);
            
            printf("Введите координаты точки D (dx, dy)\n");
            scanf("%lf %lf", &dx, &dy);
            
            intersection_vector(ax, ay, bx, by, cx, cy, dx, dy);
            
            // лучи пересекаются
            printf("\nA(0,0), B(2,0), C(1,0), D(3,0)\n");
            intersection_vector(0, 0, 2, 0, 1, 0, 3, 0);
            
            //лучи не пересекаются (противоположно направлены)
            printf("\nA(0,0), B(-2,0), C(3,0), D(5,0)\n");
            intersection_vector(0, 0, -2, 0, 3, 0, 5, 0);
            
            //лучи пересекаются (противоположно направлены)
            printf("\nA(0,0), B(2,0), C(1,0), D(-1,0)\n");
            intersection_vector(0, 0, 2, 0, 1, 0, -1, 0);
            
            break;
        }
        
        case 3:
        {
            Point A, B, C, D;
            printf("Введите координаты точки A в пространстве (x1, y1, z1)\n");
            scanf("%lf %lf %lf", &A.x, &A.y, &A.z);
            
            printf("Введите координаты точки B в пространстве (x2, y2, z2)\n");
            scanf("%lf %lf %lf", &B.x, &B.y, &B.z);
            
            printf("Введите координаты точки C в пространстве (x3, y3, z3)\n");
            scanf("%lf %lf %lf", &C.x, &C.y, &C.z);
            
            printf("Введите координаты точки D в пространстве (x4, y4, z4)\n");
            scanf("%lf %lf %lf", &D.x, &D.y, &D.z);

            if(is_point_inside_angle(A, B, C, D) == 1) printf("Точка D лежит внутри угла ABC\n");
            
            //точка внутри угла
            Point A1 = {1, 0, 0};
            Point B1 = {0, 0, 0};
            Point C1 = {0, 1, 0};
            Point D1 = {0.3, 0.3, 0};
            printf("\nA(1,0,0), B(0,0,0), C(0,1,0), D(0.3,0.3,0)\n");
            if(is_point_inside_angle(A1, B1, C1, D1) == 1) printf("Точка D лежит внутри угла ABC\n");
            
            //точка вне угла
            Point A2 = {1, 0, 0};
            Point B2 = {0, 0, 0};
            Point C2 = {0, 1, 0};
            Point D2 = {-0.3, -0.3, 0};
            printf("\nA(1,0,0), B(0,0,0), C(0,1,0), D(-0.3,-0.3,0)\n");
            if(is_point_inside_angle(A2, B2, C2, D2) == 1) printf("Точка D лежит внутри угла ABC\n");
            
            break;
        } 
        case 4:
        {
            double A, B, C, D, x1, y1, z1, x2, y2, z2;
            
            printf("Введите значения коэффициентов плоскости A, B, C, D (Ax + By + Cz + D = 0)\n");
            scanf("%lf %lf %lf %lf", &A, &B, &C, &D);
            
            printf("Введите координаты точки A в пространстве (x1, y1, z1)\n");
            scanf("%lf %lf %lf", &x1, &y1, &z1);
            
            printf("Введите координаты точки B в пространстве (x2, y2, z2)\n");
            scanf("%lf %lf %lf", &x2, &y2, &z2);
            
            is_same_space(A, B, C, D, x1, y1, z1, x2, y2, z2);
            
            //точки по одну сторону от плоскости
            printf("\nПлоскость: x + y + z - 3 = 0\n");
            printf("Точка A(0,0,0), Точка B(1,1,0)\n");
            is_same_space(1, 1, 1, -3, 0, 0, 0, 1, 1, 0);
            
            //точки по разные стороны от плоскости
            printf("\nПлоскость: x + y + z - 3 = 0\n");
            printf("Точка A(0,0,0), Точка B(2,2,0)\n");
            is_same_space(1, 1, 1, -3, 0, 0, 0, 2, 2, 0);
            
            //точка A на плоскости
            printf("\nПлоскость: 2x + 2y + 2z - 6 = 0\n");
            printf("Точка A(1,1,1), Точка B(0,0,0)\n");
            is_same_space(2, 2, 2, -6, 1, 1, 1, 0, 0, 0);
            
            //обе точки на плоскости
            printf("\nПлоскость: x + y + z - 3 = 0\n");
            printf("Точка A(1,1,1), Точка B(2,1,0)\n");
            is_same_space(1, 1, 1, -3, 1, 1, 1, 2, 1, 0);
            
            break;
        }
        default:
            printf("Неправильный номер\n");
    }
    return 0;
}