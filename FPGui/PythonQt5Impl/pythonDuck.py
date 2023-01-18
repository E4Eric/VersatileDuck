
import sys, os, copy, json, importlib
from PyQt5 import QtGui, QtWidgets
import QTPlatform, time

class RuntimeContext():
    def getJsonData(self, srcDir):
        print(srcDir)

        jsonData = []
        for subdir, dirs, files in os.walk(srcDir):
            for file in files:
                if (file.endswith('json')):
                    jsonPath = os.path.join(subdir, file)
                    with open(jsonPath, 'r') as myfile:
                        jsonString = myfile.read()

                    # parse file and cache the result
                    jsonObj = json.loads(jsonString)
                    jsonData.append(jsonObj)
        return jsonData

    def cacheImage(self, name, image):
        self.imageCache[name] = image

    def extractStyle(self, sheetName, name, spec, sheetImage):
        # First extract the style's image from the sheet
        styleImage = self.window.crop(sheetImage, spec['srcX'], spec['srcY'], spec['srcW'], spec['srcH'])

    def loadStyleSheets(self, stylesDir):
        styleSheetList = self.getJsonData(stylesDir)
        for styleSheet in styleSheetList:
            self.styleCache[styleSheet['name']] = styleSheet
            print("Loaded Style: " + styleSheet['name'])
            imagePath = stylesDir + '/' + styleSheet['imagePath']
            image = self.window.loadImage(imagePath)
            self.cacheImage('Style Sheet/' + styleSheet['name'], image)

    def getStyleData(self, styleName):
        styleSheet = self.styleCache[self.appModel['curStyleSheet']]
        styleData = styleSheet['Styles'][styleName]
        return styleData

    def getStyleImage(self, styleName):
        cacheName = self.appModel['curStyleSheet']
        styleSheet = self.styleCache[self.appModel['curStyleSheet']]
        sheetImage = self.imageCache['Style Sheet/' + styleSheet['name']]
        style = styleSheet['Styles'][styleName]
        styleImage = self.window.crop(sheetImage, style['srcX'], style['srcY'], style['srcW'], style['srcH'])
        return styleImage

    def getIconImage(self, iconName):
        return self.imageCache['Icon/' + iconName]

    def offsetModelElement(self, me, dx, dy):
        me['drawRect'].x += dx
        me['drawRect'].y += dy
        if 'contents' in me:
            for kid in me['contents']:
                self.offsetModelElement(kid, dx, dy)

    def setModelElementPos(self, me, newX, newY):
        dx = newX - me['drawRect'].x
        dy = newY - me['drawRect'].y
        self.offsetModelElement(me, dx, dy)

    def inflateDrawRectForStyle(self, me):
        styleData = self.getStyleData((me['style']))
        styleExtraW = styleData['lw'] + styleData['lm'] + styleData['rm'] + styleData['rw']
        styleExtraH = styleData['th'] + styleData['tm'] + styleData['bm'] + styleData['bh']
        me['drawRect'].w += styleExtraW
        me['drawRect'].h += styleExtraH

    def adjustAvailableForStyle(self, me, available):
        styleData = self.getStyleData((me['style']))

        adjusted = copy.copy(available)
        adjusted.x += styleData['lw'] + styleData['lm']
        adjusted.y += styleData['th'] + styleData['tm']

        adjusted.w -= styleData['lw'] + styleData['lm'] + styleData['rm'] + styleData['rw']
        adjusted.h -= styleData['th'] + styleData['tm'] + styleData['bm'] + styleData['bh']
        return adjusted

    def loadIconSets(self, iconsDir):
        iconSets = self.getJsonData(iconsDir)

        self.getStyleImage("Transparent Color")
        for iconSet in iconSets:
            imagePath = iconsDir + '/' + iconSet['imagePath']
            iconGrid = self.window.loadImage(imagePath)
            self.window.setTransparentColor(iconGrid, 81, 86, 88)
            gridX = iconSet['gridX']
            gridY = iconSet['gridY']

            # now iterate over the icon name list extracting each icon from the grid
            curX = 0
            for iconName in iconSet['iconNames']:
                icon = self.window.crop(iconGrid, curX, 0, gridX, gridY)
                curX += gridX

                iconPath = 'Icon/' + iconName
                self.cacheImage(iconPath, icon)
                print("loaded Icon: ", iconPath)

    def loadDecorators(self, decoratorsDir):
        iconData = self.getJsonData(decoratorsDir)
        for icon in iconData:
            self.decoratorCache[icon['name']] = icon
            print("loaded Decorator: ", icon['name'])

    def loadLayouts(self, layoutsDir):
        layoutData = self.getJsonData(layoutsDir)
        sys.path.append(layoutsDir)
        for layout in layoutData:
            self.layoutCache[layout['name']] = layout
            print("loaded Layout: ", layout['name'])
            cp = layout['codePath']
            code = importlib.import_module(cp)
            self.codeCache[layout['name']] = code

    def loadRenderers(self, renderersDir):
        rendererData = self.getJsonData(renderersDir)
        sys.path.append(renderersDir)
        for renderer in rendererData:
            self.rendererCache[renderer['name']] = renderer
            print("loaded Renderer: ", renderer['name'])
            cp = renderer['codePath']
            code = importlib.import_module(cp)
            self.codeCache[renderer['name']] = code

    def layout(self, available, me):
        sd = self.getStyleData((me['style']))
        layoutName = sd['layout']
        layoutCode = self.codeCache[layoutName]
        available = layoutCode.layout(self, available, me)
        return available

    def drawModelElement(self, me):
        if 'drawRect' not in me:
            return   # No-op

        # auto-draw the frame if the me has a 'style' that's not already frame
        if 'style' in me and me['style'] != 'frame':
            rendererCode = self.codeCache['frame']
            rendererCode.draw(self, me)

        sd = self.getStyleData(me['style'])
        rendererName = sd['renderer']
        rendererCode = self.codeCache[rendererName]
        rendererCode.draw(self, me)
        if 'contents' in me:
            for kid in me['contents']:
                self.drawModelElement(kid)

    def loadAssets(self):
        assetDir = self.appModel['assetDir']

        # Image-based assets
        self.imageCache = {}
        self.codeCache = {}

        self.styleCache = {}
        self.loadStyleSheets(assetDir + "/Images/Styles")

        self.iconCache = {}
        self.loadIconSets(assetDir + "/Images/Icons")

        self.decoratorCache = {}
        self.loadDecorators(assetDir + "/Images/Decorators")

        # Code-based assets
        self.layoutCache = {}
        self.loadLayouts(assetDir + "/Code/Layouts")

        self.rendererCache = {}
        self.loadRenderers(assetDir + "/Code/Renderers")

    def perfTest(self, duration):
        start = time.perf_counter()
        print('start Perf test')

        count = 0
        while True:
            curtime = time.perf_counter()
            if curtime - start > 1:
                break

            self.x = 0
            self.y = 0
            self.w = 10000
            self.h = 10000
            self.layout(self, self.appModel)
            count += 1
        print('Done !! ', count)

    def startup(self):
        self.app = QtWidgets.QApplication(sys.argv) 
        self.loadAssets()
        self.graphicsEngine.runApp()

        self.perfTest(1)

# Load the model
# Startup...get the model and load the necessary assets
# HACK! parse the path(s) from the args

# filename = sys.argv[1]
modelPath = "../Models/EclipseDuck.json"
with open(modelPath, 'r') as modelData:
    appModel = json.load(modelData)

# We have a model and a graphics engine, capture them in the runtime context
ctx = RuntimeContext()
ctx.appModel = appModel

# ...time to load the assets (NOTE: from here on *always* use the context)
ctx.app = QtWidgets.QApplication(sys.argv)
ctx.window = QTPlatform.QTPlatform(ctx)
ctx.loadAssets() # load all assets to prepare for the paint
ctx.window.show()
sys.exit(ctx.app.exec_())
