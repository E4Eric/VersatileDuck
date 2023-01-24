
import sys, os, copy, json, importlib
from PyQt5 import QtGui, QtWidgets
import QTPlatform, time
import AssetManager, UIEventProxy

class RuntimeContext():
    def __init__(self):
        self.eventProxy = UIEventProxy.UIEventProxy(self)

    def layout(self, available, me):
        start = time.perf_counter()
        available = self.assetManager.layout(available, me)
        end = time.perf_counter()
        print('Laayout: ', end - start)
        return available

    def drawModelElement(self, me):
        start = time.perf_counter()
        self.assetManager.drawModelElement(me)
        end = time.perf_counter()
        print('Drawt: ', end - start)

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
ctx.assetManager = AssetManager.AssetManager(ctx)
ctx.window.show()
sys.exit(ctx.app.exec_())
