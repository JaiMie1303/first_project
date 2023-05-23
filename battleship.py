import random as rnd
import time

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return (f"x={self.x}  y={self.y}")

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))



    @staticmethod
    def convert_coord_to_point( inp_str):
        coord = inp_str.split()
        if not (coord[0].isdigit()) or not (coord[0].isdigit()):
            print("Введите числа")
            return False
        L = list(map(int, coord))
        if len(L) != 2:
            print("Введите 2 координаты")
            return False
        if L[0] <= 0 or L[0] > 6:
            print("Координата х вне допустимых значений")
            return False
        if L[1] <= 0 or L[1] > 6:
            print("Координата y вне допустимых значений")
            return False
        return Point(L[0], L[1])


class Ship:
    def __init__(self, points):
        self.points = points
        self.isalive = True
        self.hitpoints = []

    def set_state(self, isalive):
        self.isalive = isalive

    def get_state(self):
        return self.isalive

    def hit(self, _point):
        if _point in self.points:
            self.hitpoints.append(_point)
            return True
        else:
            return False

    def check_state(self):
        if set(self.points) == set(self.hitpoints):
            self.set_state(False)


class Pole:
    def __init__(self):
        self.ships = []
        self.pole = []
        for i in range(6):
            self.pole.append(['O' for j in range(6)])
        self.forbidden_zone = []
        for i in range(6):
            self.forbidden_zone.append(['O' for j in range(6)])


    def draw(self):
        print("  | 1 | 2 | 3 | 4 | 5 | 6 |")
        for i in range(6):
            line = str(i+1) + " | "
            for j in range(6):
                line += self.pole[i][j] + " | "
            print(line)

    def add_ship(self, _s):
        if self.is_available(_s):
            for point in _s.points:
                self.pole[point.y - 1][point.x - 1] = "■"
            self.ships.append(_s)
            return True
        else:
            print("Данный корабль нельзя разместить в данной точке")
            return False


    def is_available(self, _s):
        tr = []
        # self.tr.clear()
        for _point in _s.points:
            if self.forbidden_zone[_point.y - 1][_point.x - 1] == "O":
                tr.append(True)
            else:
                tr.append(False)
        a = all(tr)
        del(tr)
        return a

    def change_forbidden_zone(self, ship):
        if self.is_available(ship):
            for point in ship.points:
                _L = self.forbiden_points(point)
                for f_point in _L:
                    if 0 <= f_point.x - 1 < 6 and 0 <= f_point.y - 1 < 6:
                        self.forbidden_zone[f_point.y - 1][f_point.x - 1] = "f"


    @staticmethod
    def forbiden_points(_point):
        L = []
        L.append(_point)
        L.append(Point(_point.x + 1, _point.y))
        L.append(Point(_point.x, _point.y + 1))
        L.append(Point(_point.x - 1, _point.y))
        L.append(Point(_point.x, _point.y - 1))
        return L

    def fdraw(self):
        print("  | 1 | 2 | 3 | 4 | 5 | 6 |")
        for i in range(6):
            line = str(i+1) + " | "
            for j in range(6):
                line += self.forbidden_zone[i][j] + " | "
            print(line)

    def check_loose_condition(self):
        ships_state = [ship.get_state() for ship in self.ships]
        if True in ships_state:
            return False
        else:
            return True




class Gamelogic:
    def __init__(self):
        self.intro()
        self.put_ships_to_gamer_pole()
        self.put_ships_to_computer_pole()

    def start_game(self):
        while True:
            print("")
            print("Ход компьютера")
            shoot = gl.computer_shoot()
            if gl.gamer_pole.check_loose_condition():
                return print("Победил компьютер")
            while shoot:
                print("Компьютер попал в ваш корабль!!!")
                shoot = gl.computer_shoot()
                self.show_interface()
                if gl.gamer_pole.check_loose_condition():
                    return print("Победил компьютер")
            self.show_interface()
            print("")
            print("Ход игрока")
            shoot = gl.player_shoot()
            if gl.comp_pole.check_loose_condition():
                    return print("Победил игрок")
            while shoot:
                print("Вы попали в корабль компьютера!!!")
                print("Дополнительный выстрел")
                self.show_interface()
                shoot = gl.player_shoot()
                if gl.comp_pole.check_loose_condition():
                    return print("Победил игрок")
            self.show_interface()

    def intro(self):
        print("-------------------")
        print("      Игра       ")
        print("    Морской бой    ")
        time.sleep(5)
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")
        time.sleep(5)

    def put_ships_to_gamer_pole(self):
        self.gamer_pole = Pole()
        answer = input("Разместить корабли игрока случайным образом? y/n ")
        if answer == "y":
            self.gamer_pole = Gamelogic.put_random_ships_to_pole()
        elif answer == "n":
            i = 0
            points = []
            _len = 3
            print("Введите координаты трехклеточного корабля x y")
            while i < _len:
                inp_str = input()
                p = Point.convert_coord_to_point(inp_str)
                if isinstance(p, Point):
                    points.append(p)
                    i += 1

            self.gamer_pole.add_ship(Ship(points))
            self.gamer_pole.change_forbidden_zone(Ship(points))
            self.gamer_pole.ships.append(Ship(points))
            i = 0
            k = 0

            _len = 2
            while k < 2:
                points = []
                print("Введите координаты двухклеточного корабля x y")
                while i < _len:
                    inp_str = input()
                    p = Point.convert_coord_to_point(inp_str)
                    if isinstance(p, Point):
                        points.append(p)
                        i += 1
                i = 0
                if self.gamer_pole.add_ship(Ship(points)):
                    self.gamer_pole.change_forbidden_zone(Ship(points))
                    self.gamer_pole.ships.append(Ship(points))
                    k += 1

            i = 0
            k = 0
            _len = 1
            while k < 4:
                points = []
                print("Введите координаты одноклеточного корабля x y")
                while i < _len:
                    inp_str = input()
                    p = Point.convert_coord_to_point(inp_str)
                    if isinstance(p, Point):
                        points.append(p)
                        i += 1
                i = 0
                if self.gamer_pole.add_ship(Ship(points)):
                    self.gamer_pole.change_forbidden_zone(Ship(points))
                    self.gamer_pole.ships.append(Ship(points))
                    k += 1
        else:
            print("Введите y или n")
            self.put_ships_to_gamer_pole()


    def put_ships_to_computer_pole(self):
        self.comp_pole = Pole()
        self.comp_pole = Gamelogic.put_random_ships_to_pole()
        self.mask_comp_pole = Pole()

    def show_interface(self):
        print("        Поле игрока                    Поле компьютера")
        print("  | 1 | 2 | 3 | 4 | 5 | 6 |      | 1 | 2 | 3 | 4 | 5 | 6 |")
        for i in range(6):
            line = str(i + 1) + " | "
            for j in range(6):
                line += self.gamer_pole.pole[i][j] + " | "
            line += "   " + str(i + 1) + " | "
            for j in range(6):
                line += self.mask_comp_pole.pole[i][j] + " | "
            print(line)


    @staticmethod
    def put_random_ships_to_pole():
        p_pole = Pole()
        start_point = Point(rnd.randint(1, 4), rnd.randint(1, 4))
        print(start_point)
        direction = rnd.randint(0, 1)
        _points=[]
        _points.append(start_point)
        for i in range(3):
            if direction == 0:
                _points.append(Point(start_point.x+i, start_point.y))
            if direction == 1:
                _points.append(Point(start_point.x, start_point.y+i))

        p_pole.add_ship(Ship(_points))
        p_pole.change_forbidden_zone(Ship(_points))
        p_pole.ships.append(Ship(_points))

        itt = 0
        while True:
            start_point = Point(rnd.randint(1, 5), rnd.randint(1, 5))
            direction = rnd.randint(0, 1)
            _points = []
            _points.append(start_point)
            for i in range(2):
                if direction == 0:
                    _points.append(Point(start_point.x + i, start_point.y))
                if direction == 1:
                    _points.append(Point(start_point.x, start_point.y + i))

            if p_pole.add_ship(Ship(_points)):
                p_pole.change_forbidden_zone(Ship(_points))
                itt += 1
            if itt == 2:
                break


        itt = 0
        while True:
            start_point = Point(rnd.randint(1, 6), rnd.randint(1, 6))
            direction = rnd.randint(0, 1)
            _points = []
            _points.append(start_point)
            for i in range(1):
                if direction == 0:
                    _points.append(Point(start_point.x + i, start_point.y))
                if direction == 1:
                    _points.append(Point(start_point.x, start_point.y + i))

            if p_pole.add_ship(Ship(_points)):
                p_pole.change_forbidden_zone(Ship(_points))
                itt += 1
            if itt == 4:
                break

        return p_pole

    def player_shoot(self):
        output_condition = False
        while True:
            coord = input("Введите координаты выстрела x y ")
            p = Point.convert_coord_to_point(coord)
            print(p)
            if self.comp_pole.pole[p.y-1][p.x-1] == "■":
                output_condition = True
                self.comp_pole.pole[p.y-1][p.x-1] = "X"
                self.mask_comp_pole.pole[p.y-1][p.x-1] = "X"
                for ship in self.comp_pole.ships:
                    ship.hit(p)
                    ship.check_state()
                break
            elif self.comp_pole.pole[p.y-1][p.x-1] == "O":
                self.comp_pole.pole[p.y-1][p.x-1] = "T"
                self.mask_comp_pole.pole[p.y - 1][p.x - 1] = "T"
                break
            else:
                print("Сюда уже стреляли!")
        return output_condition




    def computer_shoot(self):
        output_condition = False
        while True:
            p = Point(rnd.randint(1, 6), rnd.randint(1, 6))
            if self.gamer_pole.pole[p.y-1][p.x-1] == "■":
                output_condition = True
                self.gamer_pole.pole[p.y-1][p.x-1] = "X"
                for ship in self.gamer_pole.ships:
                    ship.hit(p)
                    ship.check_state()
                break
            elif self.gamer_pole.pole[p.y-1][p.x-1] == "O":
                self.gamer_pole.pole[p.y-1][p.x-1] = "T"
                break
        return output_condition



gl = Gamelogic()
gl.start_game()







