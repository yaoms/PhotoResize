# coding=utf-8
# 2015-11-26
# yaoms
# 图片压缩,剪辑

def img_resize_crop(imname, newname="", size=(0,0), log=False, rewrite=False):
    """
    图片压缩,剪辑
    :param imname:
    :param newname:
    :param size:
    :param log:
    :param rewrite:
    :return:
    """
    from PIL import Image
    import os
    import sys

    tw, th = size
    if log:
        print imname,
    try:
        with Image.open(imname) as im:
            # print type(im)
            w, h = im.size
            if h > w:# 窄幅 颠倒宽高 便于计算最佳缩放比
                w, h = h, w

            # 计算最佳缩放比
            mode = 0
            rate = 1.0
            if w <= tw or h <= th:#小图片 跳过
                if log:
                    print
                return
            elif w / h > 4: # 长图/高图
                if log:
                    print
                return
            else:
                xr = 1.0 * w / tw # 水平缩放比
                yr = 1.0 * h / th # 垂直缩放比
                if xr > yr:
                    rate = yr
                    # 水平裁剪 四
                    mode = 0
                else:
                    rate = xr
                    # 垂直裁剪 目
                    mode = 1

            # 重新读取宽高 忽略宽高比
            w, h = im.size
            nw, nh = w / rate, h / rate
            if log:
                print "resize", (w, h), "to", (nw, nh),
            tmw, tmh = nw, nh
            tsw, tsh = tw, th
            x, y = (tmw - tsw) / 2, (tmh - tsh) / 2
            if h > w:
                tmw, tmh = tmh, tmw
                tsw, tsh = tsh, tsw
                y, x = (tmw - tsh) / 2, (tmh - tsw) / 2

            if abs(x) < 0.001:
                x = 0

            if abs(y) < 0.001:
                y = 0

            if log:
                print "crop", (x, y, tsw, tsh)
            if rewrite or not os.path.exists(newname):
                im.resize((int(nw), int(nh)), Image.ANTIALIAS).crop((int(x), int(y), int(tsw) ,int(tsh))).save(newname)
    except Exception, data:
        print >> sys.stderr, imname, "Error", data
    except SystemError, data:
        print >> sys.stderr, imname, "Error", data
    except IOError, data:
        print >> sys.stderr, imname, "Error", data