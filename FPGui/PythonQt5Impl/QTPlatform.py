
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPixmap, QColor, QFont, QFontMetrics, QPainter

class R():
    def __init__(self, x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def __str__(self):
        return f'({self.x},{self.y},{self.w},{self.h})'

class QTPlatform(QtWidgets.QWidget):
    def __init__(self, ctx):
        self.ctx = ctx
        self.fontCache = {}
        self.painter = None
        super().__init__()
        print("init !!")

    def resizeEvent(self, event):
        size = event.size()
        available = R(0,0, size.width(), size.height())
        self.ctx.layout(available, self.ctx.appModel)

    def paintEvent(self, event): 
        self.painter = QPainter()   # Cache for callbacks...rebderers don't need to know
        self.painter.begin(self)

        self.ctx.drawModelElement(self.ctx.appModel)
        
        self.painter.end()
        self.painter = None

    def setTransparentColor(self, pixmap, r, g, b):
        # Create a mask from the pixmap that matches the color you want to make transparent
        mask = pixmap.createMaskFromColor(QColor(r, g, b))

        # Set the mask on the pixmap
        pixmap.setMask(mask)

    def loadImage(self, path):
        return QPixmap(path)

    def getImageWidth(self, pixmap):
        return pixmap.rect().width()

    def getImageHeight(self, pixmap):
        return pixmap.rect().height()


    def getFontFromSpec(self, fontSpec):
        if fontSpec in self.fontCache:
            font, palette = self.fontCache[fontSpec]
            return font

        font = QFont()

        # set transparent background in the palette
        font.setStyleHint(QFont.SansSerif)  # default style hint

        textColor = QColor(0,0,0,)
        for attr, value in self.parseStyleSheet(fontSpec):
            if attr == "font-family":
                font.setFamily(value)
            elif attr == "color":
                textColor = QColor(value)
            elif attr == "font-size":
                font.setPointSize(int(value))
            elif attr == "font-weight":
                font.setWeight(int(value))
            elif attr == "font-style":
                if value == "italic":
                    font.setItalic(True)
                if value == "bold":
                    font.setBold(True)

        self.fontCache[fontSpec] = (font, textColor)
        return font

    def parseStyleSheet(self, fontSpec: str):
        """
        Parse a style sheet string into a list of (property, value) tuples.
        """
        properties = []
        for rule in fontSpec.split(";"):
            if not rule:
                continue
            attr, value = rule.split(":")
            properties.append((attr.strip(), value.strip()))
        return properties

    def getTextWidth(self, text, fontSpec):
        font = self.getFontFromSpec(fontSpec)
        font_metrics = QFontMetrics(font)
        bounding_rect = font_metrics.boundingRect(text)
        return bounding_rect.width()

    def getTextHeight(self, text, fontSpec):
        font = self.getFontFromSpec(fontSpec)
        font_metrics = QFontMetrics(font)
        bounding_rect = font_metrics.boundingRect(text)
        return bounding_rect.height()

    def drawText(self, x, y, text, fontSpec):
        font, textColor = self.fontCache[fontSpec]
        self.painter.setFont(font)
        self.painter.setPen(QColor(textColor))

        print(x, y, text)
        r = QRect(x, y, 1000, 1000)
        self.painter.drawText(r, Qt.AlignTop | Qt.AlignLeft,  text)

    def drawImage(self, dx,dy,dw,dh, image, sx,sy,sw,sh):
        dstRect = QRect(dx,dy,dw,dh)
        srcRect = QRect(sx,sy,sw,sh)
        self.painter.drawPixmap(srcRect, image, dstRect)

    def crop(self, srcMap, x,y,w,h):
        return srcMap.copy(QRect(x,y,w,h))

