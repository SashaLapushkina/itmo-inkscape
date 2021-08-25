import inkex
from lxml import etree

X, Y = range(2)

class Ornament(inkex.EffectExtension):
    def add_arguments(self, pars):
        pars.add_argument("--width", type=float, default=100.0, help="Ширина")
        pars.add_argument("--height", type=float, default=100.0, help="Высота")
        pars.add_argument("--replay", type=int, default=5, help="Повторы")

    def effect(self):
        #-- Создание группы
        centre = self.svg.namedview.center
        grp_transform = 'translate' + str(centre)
        grp_name = 'Group Name'
        grp_attribs = {inkex.addNS('label', 'inkscape'): grp_name,
                       'transform': grp_transform}
        grp = etree.SubElement(self.svg.get_current_layer(), 'g', grp_attribs)

        w = self.svg.unittouu(str(self.options.width) + 'px')
        h = self.svg.unittouu(str(self.options.height) + 'px')
        r = self.options.replay
        draw_ornament(w, h, r, grp)

def draw_ornament(w, h, r, parent):
    x = 0;
    y = h;
    w0 = w / r
    for i in range(r):
        draw_line(x, y, w0, h, parent)
        draw_rect(x + (w0 / 2), h / 2, min(h / 6, w0 / 12), parent)
        x = x + w0

#Рисование линии одного раппорта
def draw_line(x, y, w0, h, parent):
    style = {'stroke': '#000000',
             'stroke-width': '1px',
             'fill': 'none'
             }
    elem = parent.add(inkex.PathElement())
    elem.update(**{
        'style': style,
        'd' : 'M ' + str(x) + ', ' + str(y) + ' L ' + str(x + w0 / 2) + ', ' + str(y - h) + ' L ' + str(x + w0 * 3 / 4) + ', ' + str(y - h / 2) +
            ' M ' + str(x + w0 / 4) + ', ' + str(y - h / 2) + ' L ' + str(x + w0 / 2) + ', ' + str(y) + ' L ' + str(x + w0) + ', ' + str(y - h) +
            ' L ' + str(x + w0) + ', ' + str(y)
    })
    return elem

#-- Рисование квадрата
def draw_rect(cx, cy, r, parent):
    style = {'stroke': 'none',
             'stroke-width': '1px',
             'fill': '#000000'
             }

    elem = parent.add(inkex.PathElement())
    elem.update(**{
        'style': style,
        'd' : 'M ' + str(cx - r) + ', ' + str(cy - r) + ' L ' + str(cx + r) + ', ' + str(cy - r) + ' L ' + str(cx + r) +
              ', ' + str(cy + r) + 'L' + str(cx - r) + ', ' + str(cy + r) + ' z'
    })


if __name__ == '__main__':
    Ornament().run()