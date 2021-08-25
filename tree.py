import inkex
from lxml import etree
from math import cos, sin, pi
import random
import sys
import re

X, Y = range(2)

class Tree(inkex.EffectExtension):
    def add_arguments(self, pars):
        pars.add_argument("--length", type=float, default=100.0, help="Длина")
        pars.add_argument("--width", type=float, default=10.0, help="Ширина")
        pars.add_argument("--depth", type=int, default=5, help="Глубина")
        pars.add_argument("--nbranches", type=int, default=2, help="Кол-во веток")
        pars.add_argument("--nleaves", type=int, default=2, help="Кол-во листьев")
        pars.add_argument("--branches", type=str, default="111111", help="Ветки")
        pars.add_argument("--leaves", type=str, default="AAAAAA", help="Листья")
        pars.add_argument("--radius", type=float, default=10.0, help="Размер листа")

    def effect(self):

        #-- Создание группы объектов
        centre = self.svg.namedview.center
        (x, y) = centre
        grp_transform = 'translate' + str(centre)

        grp_name = 'Group Name'
        grp_attribs = {inkex.addNS('label', 'inkscape'): grp_name,
                       'transform': grp_transform}
        grp = etree.SubElement(self.svg.get_current_layer(), 'g', grp_attribs)

        #-- Инициализация переменных
        l = self.svg.unittouu(str(self.options.length) + 'px')
        w = self.svg.unittouu(str(self.options.width) + 'px')
        d = self.options.depth
        nb = self.options.nbranches
        nl = self.options.nleaves
        branch = self.options.branches
        leaf = self.options.leaves
        r = self.svg.unittouu(str(self.options.radius) + 'px')

        #-- Проверка формата ввода
        if re.fullmatch("[0-9A-F]{6}", branch) and re.fullmatch("[0-9A-F]{6}", leaf):
            draw_tree(x, y, l, w, d, branch, nb, nl, leaf, r, grp)
        else:
            sys.stderr.write('Error:InvalidSpecifications.\n')  # signal an error
            error = True

#-- Рисование дерева
def draw_tree(x, y, l, w, d, branch, nb, nl, leaf, r, grp):
    if (d > 0):
        N = random.randint(1, nb) # Кол-во веток из одного конца
        for i in range(N):
            p = random.random() * 0.2 + 0.8 #Параметр для уменьшения размера ветки
            angle = (1 - random.randint(-2, 2) / 10) * pi / (N + 1) * (i + 1) #Угол наклона ветки
            draw_line(x, y, l, w, branch, angle, grp)
            draw_leaf(x + l * cos(angle), y - l * sin(angle), r, leaf, nl, grp)
            draw_tree(x + l * cos(angle), y - l * sin(angle), p * l, p * w, d - 1, branch, nb, nl, leaf, r, grp)
    else:
        draw_leaf(x, y, r, leaf, nl, grp)

#-- Рисование ветки
def draw_line(x, y, l, w, color, angle, parent):
    style = {'stroke': '#' + color,
             'stroke-width': w
             }
    elem = parent.add(inkex.PathElement())
    elem.update(**{
        'style': style,
        'd' : 'M ' + str(x) + ', ' + str(y) + ' L ' + str(x + l * cos(angle)) + ', ' + str(y - l * sin(angle))
    })

#-- Рисование листа
def draw_leaf(x, y, r, color, n, parent):

    N = random.randint(0, n) #Кол-во листьев

    for i in range(N):
        r = (random.random() * 2 - 1) * r
        style = {'stroke': 'none',
                 'fill': '#' + color,
                 }
        elem = parent.add(inkex.PathElement())
        elem.update(**{
            'style': style,
            'd' : 'M ' + str(x) + ', ' + str(y) + ' L ' + str(x + (r * random.random() * 2 - 1)) + ', ' +
                  str(y + (r * random.random() * 2 - 1)) + ' L ' + str(x + (r * random.random() * 2 - 1)) + ', ' +
                                                                      str(y + (r * random.random() * 2 - 1)) + ' z'
        })

if __name__ == '__main__':
    Tree().run()