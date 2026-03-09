#include <stdio.h>
#include <math.h>
#include <float.h>
#include <windows.h>

typedef struct {
    double x, y, z;
} Vector;

// Разность векторов
Vector sub(Vector a, Vector b) {
    Vector v = {a.x - b.x, a.y - b.y, a.z - b.z};
    return v;
}

// Скалярное произведение
double dot(Vector v, Vector w) {
    return v.x * w.x + v.y * w.y + v.z * w.z;
}

// Векторное произведение
Vector cross(Vector v, Vector w) {
    Vector r = {
        v.y * w.z - v.z * w.y,
        v.z * w.x - v.x * w.z,
        v.x * w.y - v.y * w.x
    };
    return r;
}

// Длина вектора
double len(Vector v) {
    return sqrt(v.x * v.x + v.y * v.y + v.z * v.z);
}

// Проверка на ноль
int is_zero(double x) {
    return fabs(x) < DBL_EPSILON;
}

void is_same_side(double A, double B, double C, double x1, double y1, double x2, double y2); //1
void intersection(double ax, double ay, double bx, double by, double cx, double cy, double dx, double dy);
void is_same_space(double A, double B, double C, double D, double x1, double y1, double z1, double x2, double y2, double z2);//4

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
        printf("Точки A и B лежат на одной прямой");
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

void intersection(double ax, double ay, double bx, double by, double cx, double cy, double dx, double dy)
{

}


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
    scanf("%d", &num);
    switch (num)
    {
        //Определить положение двух точек относительно прямой
        //по одну сторону от прямой, по разные, на прямой. Прямая задана своими коэффициентами
        case 1: 
        {
            double A, B, C, x1, y1, x2, y2;
            
            printf("Введите значения коэффициентов прямой A, B, C (Ax + By + C = 0)\n");
            scanf("%lf %lf %lf", &A, &B, &C);
            
            printf("Введите координаты точки A на плоскости (x1, y1)\n");
            scanf("%lf %lf", &x1, &y1);
            
            printf("Введите координаты точки B на плоскости  (x2, y2)\n");
            scanf("%lf %lf", &x2, &y2);
            
            is_same_side(A, B, C, x1, y1, x2, y2);
            break;
        }
        case 2:
        {
            double ax, ay, bx, by, cx, cy, dx, dy;
            
            printf("Enter the coordinates of the A point on the line (ax, ay)\n");
            scanf("%lf %lf", &ax, &ay);
            
            printf("Enter the coordinates of the B point on the line (bx, by)\n");
            scanf("%lf %lf", &bx, &by);
            
            printf("Enter the coordinates of the C point on the line (cx, cy)\n");
            scanf("%lf %lf", &cx, &cy);
            
            printf("Enter the coordinates of the D point on the line (dx, dy)\n");
            scanf("%lf %lf", &dx, &dy);
            
            // Здесь нужно добавить реализацию для case 2
            printf("Case 2 is not implemented yet\n");
            break;
        }
        
        case 3:
        {
            // Здесь нужно добавить реализацию для case 3
            printf("Case 3 is not implemented yet\n");
            break;
        }
        
        case 4:
        {
            //Определить положение двух точек относительно плоскости
            //по одну сторону от плоскости, по разные, на плоскости.  Плоскость задана своими коэффициентами.
            double A, B, C, D, x1, y1, z1, x2, y2, z2;
            
            printf("Введите значения коэффициентов плоскости A, B, C, D (Ax + By + Cz + D = 0)\n");
            scanf("%lf %lf %lf %lf", &A, &B, &C, &D);
            
            printf("Введите координаты точки A в пространстве (x1, y1, z1)\n");
            scanf("%lf %lf %lf", &x1, &y1, &z1);
            
            printf("Введите координаты точки B в пространстве (x2, y2, z2)\n");
            scanf("%lf %lf %lf", &x2, &y2, &z2);
            
            is_same_space(A, B, C, D, x1, y1, z1, x2, y2, z2);
            break;
        }
        default:
            printf("Invalid task number\n");
    }
    return 0;
}