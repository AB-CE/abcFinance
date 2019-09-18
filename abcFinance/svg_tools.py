class Scene:
    def __init__(self, name="svg", height=400, width=400):
        self.name = name
        self.items = []
        self.height = height
        self.width = width
        return

    def add(self, item): self.items.append(item)

    def strarray(self):
        var = ["<?xml version=\"1.0\"?>\n",
               "<svg height=\"%d\" width=\"%d\" >\n" % (
                   self.height, self.width),
               " <g style=\"fill-opacity:1.0; stroke:black;\n",
               "  stroke-width:1;\">\n"]
        for item in self.items:
            var += item.strarray()
        var += [" </g>\n</svg>\n"]
        return var

    def write_svg(self, filename=None):
        if filename:
            self.svgname = filename
        else:
            self.svgname = self.name + ".svg"
        file = open(self.svgname, 'w')
        file.writelines(self.strarray())
        file.close()
        return self.strarray()


class Line:
    def __init__(self, start, end):
        self.start = start  # xy tuple
        self.end = end  # xy tuple
        return

    def strarray(self):
        return ["  <line x1=\"%d\" y1=\"%d\" x2=\"%d\" y2=\"%d\" />\n" %
                (self.start[0], self.start[1], self.end[0], self.end[1])]


class Rectangle:
    def __init__(self, origin, height, width, color=(255, 255, 255)):
        self.origin = origin
        self.height = height
        self.width = width
        self.color = color
        return

    def strarray(self):
        return ["  <rect x=\"%d\" y=\"%d\" height=\"%d\"\n" %
                (self.origin[0], self.origin[1], self.height),
                "    width=\"%d\" style=\"fill:%s;\" />\n" %
                (self.width, colorstr(self.color))]


class Text:
    def __init__(self, origin, text, size=18, align_horizontal="middle", align_vertical="auto"):
        self.origin = origin
        self.text = text
        self.size = size
        self.align_horizontal = align_horizontal
        self.align_vertical = align_vertical
        return

    def strarray(self):
        return ["  <text x=\"%d\" y=\"%d\" font-size=\"%d\"" %
                (self.origin[0], self.origin[1],
                 self.size), " text-anchor=\"", self.align_horizontal, "\"",
                " dominant-baseline=\"", self.align_vertical, "\">\n",
                "   %s\n" % self.text,
                "  </text>\n"]


class Textbox:
    def __init__(self, origin, height, width, text, color=(255, 255, 255), text_size=18):
        self.Outer = Rectangle(origin, height, width, color)
        self.Inner = Text((origin[0]+width//2, origin[1]+height//2),
                          text, text_size, align_horizontal="middle", align_vertical="middle")
        return

    def strarray(self):
        return self.Outer.strarray() + self.Inner.strarray()


def colorstr(rgb): return "rgb({}, {}, {})".format(rgb[0], rgb[1], rgb[2])
