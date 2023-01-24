import copy


def layout(ctx, available, me):
    if 'contents' not in me:
        return available   # No-op

    me['drawRect'] = copy.copy(available)
    sd = ctx.assetManager.getStyleData(me['style'])

    adjusted = ctx.assetManager.adjustAvailableForStyle(me, available)
    side = sd['side']

    # reserve the are we need for our style frame
    maxHeight = 0

    if side == 'top' or side == 'bottom':
        # reserve space now to get positioning correct
        kidAvailable = copy.copy(adjusted)
        totalHeight = 0
        startWidth = kidAvailable.w
        startX = kidAvailable.x

        spacer = None
        for kid in me['contents']:
            # right adjustment
            if kid['style'] == 'spacer':
                spacer = kid
                continue

            kidAvailable = ctx.assetManager.layout(kidAvailable, kid)
            if kidAvailable.w < 0:  # ..overflow, wrap
                kidAvailable.x = startX
                kidAvailable.w = startWidth
                kidAvailable.y += maxHeight
                kidAvailable.h -= maxHeight
                kidAvailable = ctx.assetManager.layout(kidAvailable, kid)
                totalHeight += maxHeight
                maxHeight = kid['drawRect'].h

            maxHeight = max(maxHeight, kid['drawRect'].h)

        totalHeight += maxHeight

        if spacer != None:
            dx = 0
            for kid in me['contents']:
                if kid['style'] == 'spacer':
                    dx = kidAvailable.w
                    continue

                if dx > 0:
                    ctx.assetManager.offsetModelElement(kid, dx, 0)

        # here we need to only change the height for the style
        styleData = ctx.assetManager.getStyleData(me['style'])
        totalHeight += styleData['th'] + styleData['tm'] + styleData['bh'] + styleData['bm']
        me['drawRect'].h = totalHeight

    if side == 'top':
        available.y += me['drawRect'].h
    elif side == 'bottom':
        dy = available.h - me['drawRect'].h
        ctx.assetManager.offsetModelElement(me, 0, dy)

    available.h -= me['drawRect'].h

    return available
