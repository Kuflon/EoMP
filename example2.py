import plateinteract import Plate

c=2; p=100; l=20; u=100; h=0.2; s=0.1; a=50;

#20 градусов Цельсия равномерно по всей пластине
l0 =         [[20, 20, 20, 20, 20, 20],
              [20, 20, 20, 20, 20, 20],
              [20, 20, 20, 20, 20, 20],
              [20, 20, 20, 20, 20, 20],
              [20, 20, 20, 20, 20, 20],
              [20, 20, 20, 20, 20, 20]]

l1 =         [[20, 20, 20, 20, 20, 20],
              [20, 20, 20, 20, 20, 20],
              [20, 20, 20, 20, 20, 20],
              [20, 20, 20, 20, 20, 20],
              [20, 20, 20, 20, 20, 20],
              [20, 20, 20, 20, 20, 20]]

Plate = Plate()
Plate.warm(l0, l1, c, p, l, u, h, s, a, times=20)
Plate.show_result()
