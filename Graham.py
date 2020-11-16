import functools
import matplotlib.pyplot as plt
import numpy as np
import itertools
import timeit

class Point:
    """Klasa Point reprezentująca punkty na płaszczyźnie na potrzeby algorytmu Grahama"""
    def __init__(self, klucz, x, y):
        self.klucz = klucz
        self.x = x
        self.y = y

    def get_klucz(self):
        return self.klucz

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def __str__(self):
        """Zwraca ciąg zawierający infomracje o instancji"""
        f = lambda n: int(n) if n.is_integer() else n
        return str(self.klucz) + ',\t' + str(f(self.x)) + ',\t' + str(f(self.y))

    __lt__ = lambda self, other: self.y < other.y if (self.x == other.x) else self.x < other.x
    __eq__ = lambda self, other: self.x == other.x and self.y == other.y
    
    
    
def odczyt(plik):
    """
    Odczyt z plikuinput.txt współrzędnych punktów oraz ich kluczy.
    Tworzenie tablicy zbior_punktow oraz słownika slownik_punktow
    """
    zbior_punktow = []
    slownik_punktow = {}
    with open(plik, 'r') as f:
        for line in f:
            klucz, x, y = ''.join(line.split()).split(',')
            zbior_punktow.append(Point(klucz, float(x), float(y)))
            slownik_punktow[klucz] = Point(klucz, float(x), float(y))

    return zbior_punktow, slownik_punktow


def zapis(zbior_punktow, plik_zapisu):
    """
    Zapis kluczy punktow należacych do brzegu otoczki wypukłej
    do pliku zewnętrznego output.txt
    """
    plik = open(plik_zapisu,'w')
    for p in zbior_punktow:
        print(p.get_klucz(),',',p.get_x(),',',p.get_y(),',',file=plik)
    plik.close()


def sortowanie(zbior_punktow):
    """
    Sortowanie zbioru punktów rozpoczynający się od tego z najmniejszą wartością x
    i kontynuując przeciwnie do ruchu wskazówek zegara
    """
    def nachylenie(y):
        """Zwraca nachylenie prostej przechodzącej przez 2 punkty"""
        x = zbior_punktow[0]
        try:
            return (x.get_y() - y.get_y()) / \
                   (x.get_x() - y.get_x())
        except ZeroDivisionError:
            return 100

    zbior_punktow.sort()  #punkt najbardziej an lewo jest punktem pierwszym
    zbior_punktow = zbior_punktow[:1] + sorted(zbior_punktow[1:], key=nachylenie)
    return zbior_punktow


def graham_scan(zbior_punktow):
    """
    Skanuje zbior punktow.
    Zwraca zbiór punktów, które tworzą brzeg otoczki wypukłej.
    """
    
    
   
	    
    
    def cross_product_orientation(a, b, c):
        """
        Zwraca orientację trzech punktów.
        Gdy >0 to x,y,z są ułożone zgodnie z ruchem wskazówek zegara.
        Gdy <0 to x,y,z są ułożone przeciwnie do ruchu wskazówek zegara.
        Gdy =0 to x,y,z są współliniowe.
        """
        
        return (b.get_y() - a.get_y()) * \
                (c.get_x() - a.get_x()) - \
                (b.get_x() - a.get_x()) * \
                (c.get_y() - a.get_y())
        

    #otoczka_wypukla to stos punktów zaczynający się od skrajnie lewego
    otoczka_wypukla = []
    posortowane_punkty = sortowanie(zbior_punktow)
    
    for p in posortowane_punkty:
        #Jeśli zgodnie z ruchem wskazówek zegara to opuść, jeśli nie to dodaj do stosu
        while len(otoczka_wypukla) > 1 and \
                cross_product_orientation(otoczka_wypukla[-2],
                                          otoczka_wypukla[-1], p) > 0:
            otoczka_wypukla.pop()
        otoczka_wypukla.append(p)
    #Zwraca punkty tworzące brzeg otoczki wypukłej
    return otoczka_wypukla




if __name__ == '__main__':
	
	
    plik = open('CH_Graham', 'w')
    #test 1
    t_1 = []
    punkty_1, slownik = odczyt('test1.txt')

    start_time = timeit.default_timer()
    hull_1 = graham_scan(punkty_1)
    t_1.append(timeit.default_timer() - start_time)
    print(t_1)
    
    


    slownik_otoczki = {p.klucz: 1 for p in hull_1}
    n=len(slownik_otoczki)
    xh = [p.x for p in hull_1]
    yh = [p.y for p in hull_1]
    xi = []
    yi = []
    for p in punkty_1:
        if p.klucz in slownik_otoczki:
            continue
        xi.append(p.x)
        yi.append(p.y)

    lastx =[xh[-1],xh[0]]
    lasty = [yh[-1],yh[0]]
    f1,f2,f3,f4= plt.plot(xh, yh, 'ro', xi,yi,'bo',xh,yh,'g-',lastx,lasty,'g-')

    lx=min(xh)-20
    rx=max(xh)+20
    ly=min(yh)-750
    ry=max(yh)+20
    plt.xlim(lx,rx)
    plt.ylim(ly,ry)

    plt.xlabel('Wartości x')
    plt.ylabel('Wartości y')
    plt.title('Wykres otoczki wypukłej')
    plt.legend((f1,f2,f3),('Punkty z brzegu otoczki','Punkty wewnątrz otoczki','Brzeg otoczki'),
           bbox_to_anchor=(0.01, 0.04, .98, .102), loc=3,ncol=1, mode="expand",
           borderaxespad=0.)
    plt.show()
    
    #test 2
    t_2 = []
    punkty_2, slownik = odczyt('test2.txt')

    start_time = timeit.default_timer()
    hull_2 = graham_scan(punkty_2)
    t_2.append(timeit.default_timer() - start_time)
    print(t_2)
    
    


    slownik_otoczki = {p.klucz: 1 for p in hull_2}
    n=len(slownik_otoczki)
    xh = [p.x for p in hull_2]
    yh = [p.y for p in hull_2]
    xi = []
    yi = []
    for p in punkty_2:
        if p.klucz in slownik_otoczki:
            continue
        xi.append(p.x)
        yi.append(p.y)

    lastx =[xh[-1],xh[0]]
    lasty = [yh[-1],yh[0]]
    f1,f2,f3,f4= plt.plot(xh, yh, 'ro', xi,yi,'bo',xh,yh,'g-',lastx,lasty,'g-')

    lx=min(xh)-20
    rx=max(xh)+20
    ly=min(yh)-750
    ry=max(yh)+20
    plt.xlim(lx,rx)
    plt.ylim(ly,ry)

    plt.xlabel('Wartości x')
    plt.ylabel('Wartości y')
    plt.title('Wykres otoczki wypukłej')
    plt.legend((f1,f2,f3),('Punkty z brzegu otoczki','Punkty wewnątrz otoczki','Brzeg otoczki'),
           bbox_to_anchor=(0.01, 0.04, .98, .102), loc=3,ncol=1, mode="expand",
           borderaxespad=0.)
    plt.show()
    
    
    #test 3
    t_3 = []
    punkty_3, slownik = odczyt('test3.txt')

    start_time = timeit.default_timer()
    hull_3 = graham_scan(punkty_3)
    t_3.append(timeit.default_timer() - start_time)
    print(t_3)
    
    


    slownik_otoczki = {p.klucz: 1 for p in hull_3}
    n=len(slownik_otoczki)
    xh = [p.x for p in hull_3]
    yh = [p.y for p in hull_3]
    xi = []
    yi = []
    for p in punkty_3:
        if p.klucz in slownik_otoczki:
            continue
        xi.append(p.x)
        yi.append(p.y)

    lastx =[xh[-1],xh[0]]
    lasty = [yh[-1],yh[0]]
    f1,f2,f3,f4= plt.plot(xh, yh, 'ro', xi,yi,'bo',xh,yh,'g-',lastx,lasty,'g-')

    lx=min(xh)-20
    rx=max(xh)+20
    ly=min(yh)-750
    ry=max(yh)+20
    plt.xlim(lx,rx)
    plt.ylim(ly,ry)

    plt.xlabel('Wartości x')
    plt.ylabel('Wartości y')
    plt.title('Wykres otoczki wypukłej')
    plt.legend((f1,f2,f3),('Punkty z brzegu otoczki','Punkty wewnątrz otoczki','Brzeg otoczki'),
           bbox_to_anchor=(0.01, 0.04, .98, .102), loc=3,ncol=1, mode="expand",
           borderaxespad=0.)
    plt.show()
    
    
    #test 4
    t_4 = []
    punkty_4, slownik = odczyt('test4.txt')

    start_time = timeit.default_timer()
    hull_4 = graham_scan(punkty_4)
    t_4.append(timeit.default_timer() - start_time)
    print(t_4)
    
    


    slownik_otoczki = {p.klucz: 1 for p in hull_4}
    n=len(slownik_otoczki)
    xh = [p.x for p in hull_4]
    yh = [p.y for p in hull_4]
    xi = []
    yi = []
    for p in punkty_4:
        if p.klucz in slownik_otoczki:
            continue
        xi.append(p.x)
        yi.append(p.y)

    lastx =[xh[-1],xh[0]]
    lasty = [yh[-1],yh[0]]
    f1,f2,f3,f4= plt.plot(xh, yh, 'ro', xi,yi,'bo',xh,yh,'g-',lastx,lasty,'g-')

    lx=min(xh)-20
    rx=max(xh)+20
    ly=min(yh)-750
    ry=max(yh)+20
    plt.xlim(lx,rx)
    plt.ylim(ly,ry)

    plt.xlabel('Wartości x')
    plt.ylabel('Wartości y')
    plt.title('Wykres otoczki wypukłej')
    plt.legend((f1,f2,f3),('Punkty z brzegu otoczki','Punkty wewnątrz otoczki','Brzeg otoczki'),
           bbox_to_anchor=(0.01, 0.04, .98, .102), loc=3,ncol=1, mode="expand",
           borderaxespad=0.)
    plt.show()


    #test5
    t_5 = []
    punkty_5, slownik = odczyt('test5.txt')

    start_time = timeit.default_timer()
    hull_5 = graham_scan(punkty_5)
    t_5.append(timeit.default_timer() - start_time)
    print(t_5)
    
    


    slownik_otoczki = {p.klucz: 1 for p in hull_5}
    n=len(slownik_otoczki)
    xh = [p.x for p in hull_5]
    yh = [p.y for p in hull_5]
    xi = []
    yi = []
    for p in punkty_5:
        if p.klucz in slownik_otoczki:
            continue
        xi.append(p.x)
        yi.append(p.y)

    lastx =[xh[-1],xh[0]]
    lasty = [yh[-1],yh[0]]
    f1,f2,f3,f4= plt.plot(xh, yh, 'ro', xi,yi,'bo',xh,yh,'g-',lastx,lasty,'g-')

    lx=min(xh)-20
    rx=max(xh)+20
    ly=min(yh)-750
    ry=max(yh)+20
    plt.xlim(lx,rx)
    plt.ylim(ly,ry)

    plt.xlabel('Wartości x')
    plt.ylabel('Wartości y')
    plt.title('Wykres otoczki wypukłej')
    plt.legend((f1,f2,f3),('Punkty z brzegu otoczki','Punkty wewnątrz otoczki','Brzeg otoczki'),
           bbox_to_anchor=(0.01, 0.04, .98, .102), loc=3,ncol=1, mode="expand",
           borderaxespad=0.)
    plt.show()





    print('Algorytm Grahama ', file=plik)
    print('test 1: \n ','t = ',t_1,'\nLiczba punktów wejsciowych: ', len (punkty_1), '\nLiczba punktów wyjsciowych:', len(hull_1) ,file=plik)
    print('test 2: \n ','t = ',t_2,'\nLiczba punktów wejsciowych: ', len (punkty_2), '\nLiczba punktów wyjsciowych:', len(hull_2) ,file=plik)
    print('test 3: \n','t = ',t_3,'\nLiczba punktów wejsciowych: ', len (punkty_3), '\nLiczba punktów wyjsciowych:', len(hull_3) ,file=plik)
    print('test 4: \n','t = ',t_4,'\nLiczba punktów wejsciowych: ', len (punkty_4), '\nLiczba punktów wyjsciowych:', len(hull_4) ,file=plik)
    print('test 5: \n','t = ',t_5,'\nLiczba punktów wejsciowych: ', len (punkty_5), '\nLiczba punktów wyjsciowych:', len(hull_5) ,file=plik)
    plik.close()


