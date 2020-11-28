init python:
    import math,random,time,pygame
    from threading import Timer
    import requests
    import json
    import socket
    class NodeClass(object):
        def __init__(self):
            # 基础账号密码
            self.username = "test"
            self.password = "000"
            # 服务器地址更改！
            self.comurl = "http://81.69.241.195:3000/"
            # 获取ip地址
            self.hostname = socket.gethostname()
            try:
                self.ipaddr = socket.gethostbyname(self.hostname)
            except:
                self.ipaddr = 'unknown'
            self.danmuBase = {}
            self.result = {}
        def get(self):
            self.url = self.comurl + "danmu/get"#
            self.result = requests.get(url=self.url, params={"username": self.username.encode('utf8'), "password": self.password.encode('utf8')}, timeout=5).text
            self.result = json.loads(self.result)["data"]
            self.danmuBase = self.result
        def push(self, values):
            self.url = self.comurl + "danmu/push"#
            obj = danmu.History()
            self.result = requests.get(url=self.url, params={"place": obj.encode('utf8'), "texts": values.encode('utf8'), "username": self.username.encode('utf8'), "password": self.password.encode('utf8')}, timeout=5).text
            self.result = json.loads(self.result)["data"]
            danmu.AddDanmu("{color=#7ffeff}"+ self.result +"{/color}")

    #该变量决定渲染模式，为True时更流畅但对配置要求更高
    danmuHigh = True

    def TransformRun(tran, st, at, selfs):
        tran.subpixel = True
        tran.xpos = selfs.xpos
        # tran.ypos = selfs.ypos
        selfs.xpos -= 2
        if selfs.xpos < -selfs.longs:
            selfs.move = False
            return None
        return 0.01

    class DPClass(renpy.Displayable):
        def __init__(self, child, pos, longs, alpha, **kwargs):
            # 向renpy.Displayable构造器传入额外的特性(property)。
            super(DPClass, self).__init__(**kwargs)
            # 子组件。
            self.child = renpy.displayable(child)
            # 子组件的位置。
            self.xpos = pos[0]
            self.ypos = pos[1]
            self.alpha = alpha
            self.longs = 35 * len(longs)
            if danmuHigh:
                self.move = True
            else:
                # 子组件速度
                self.redrawtime = 0.006   # 多久刷新一次位置，越大刷新得越快
                self.redrawdistance = 1      # 每次刷新的默认偏移量，越大默认误差越大

                # 子组件是否运动
                self.move = False
                self.Move()

        def render(self, width, height, st, at):
            if danmuHigh:
                t = Transform(child=self.child, function=renpy.curry(TransformRun)(selfs=self))
            else:
                t = Transform(child=self.child, alpha=self.alpha, subpixel=True, xpos=self.xpos)
            render = renpy.Render(self.ypos, self.longs)
            render.place(t, 0, self.ypos, self.longs, 35)
            return render

        def event(self, ev, x, y, st):
            return self.child.event(ev, x, y, st)

        def Move(self):
            if self.move == False:
                self.move = True
                Timer(0, self.Linear).start()

        def Linear(self):
            while(self.move and self.xpos > -self.longs):
                self.xpos -= self.redrawdistance
                renpy.redraw(self, 0)
                time.sleep(self.redrawtime)
            self.move = False

    class DanmuClass(object):
        def __init__(self):
            # 弹幕最大行数
            self.danmuLongs = 4
            # 倾斜数值
            self.lengths = 200
            self.alpha = 0.9
            self.dp = []
            self.danmuBase = {}

        def start(self):
            self.dp = []
            for i in range(0, self.danmuLongs):
                self.dp.append([])
            self.danmuBase = node.danmuBase.copy()

        def History(self):
            try:
                x = renpy.filter_text_tags(_history_list[len(_history_list)-1].what, allow=gui.history_allow_tags)
            except:
                x = ""
            return x

        def AddDanmu(self, j):
            try:
                danmuPos = 99999
                test = 0
                channel = 0
                for i in self.dp:
                    if i:
                        pos = i[len(i) - 1]
                        posx = max(pos.xpos + pos.longs, 1280)
                    else:
                        posx = 1280
                    if danmuPos - self.lengths > posx:
                        danmuPos = posx
                        channel = test
                    test += 1
                self.dp[channel].append(DPClass(Text(j, style="danmu_text"), [danmuPos, 35 * channel], j, self.alpha))
            except:
                pass

        def Show(self):
            texts = self.History()
            if texts:
                try:
                    for j in self.danmuBase[texts]:
                        self.AddDanmu(j)
                except:
                    pass

        def Clear(self):
            renpy.hide_screen('danmu_screen')
            for j in self.dp:
                for i in j:
                    i.move = False

default node = NodeClass()
default danmu = DanmuClass()
