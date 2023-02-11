import time

class DisplayManager():
    def __init__(self, ctx):
        self.ctx = ctx
        self.layers = {}

    def layout(self, available, me):
        start = time.perf_counter()
        available = self.ctx.assetManager.layout(available, me)
        end = time.perf_counter()
        print('Layout: ', end - start)
        return available

    def drawModelElement(self, me):
        start = time.perf_counter()
        self.ctx.assetManager.drawModelElement(me)
        end = time.perf_counter()
        print('Draw: ', end - start)

    def pick(self, me, x ,y):
        if 'drawRect' not in me:
            return None

        dr = me['drawRect']
        if x < dr.x:
            return None
        if x > (dr.x + dr.w):
            return None
        if y < dr.y:
            return None
        if y > (dr.y + dr.h):
            return None

        # drill down
        if 'contents' in me:
            for kid in me['contents']:
                found = self.pick(kid, x,y)
                if found != None:
                    return found

        return me

    def drawModelElement(self, me):
        if 'drawRect' not in me:
            return   # No-op

        # auto-draw the frame if the me has a 'style' that's not already frame
        if 'style' in me and me['style'] != 'frame':
            self.ctx.assetManager.draw('frame', me)

        sd = self.ctx.assetManager.getStyleData(me['style'])
        rendererName = sd['renderer']
        self.ctx.assetManager.draw(rendererName, me)
        if 'contents' in me:
            for kid in me['contents']:
                self.drawModelElement(kid)
