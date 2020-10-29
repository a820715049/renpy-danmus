label start:
    python:
        username = ""
        password = ""
        username = renpy.input("请输入用户名")
        password = renpy.input("请输入密码")
        import requests
        import json
        url = "http://122.51.92.130:3000/danmu/get"
        danmuBase = requests.get(url=url, params={"username": username.encode('utf8'),
                                                "password": password.encode('utf8')}, timeout=5).text
        danmuBase = json.loads(danmuBase)
        status = danmuBase["status"]
        danmuBase = danmuBase["data"]
        danmulist = []
        for i in danmuBase:
            list1 = [i, []]
            for j in danmuBase[i]:
                list1[1].append(j)
            danmulist.append(list1)

    "[status]"
    $ a = 0
    while(True):
        $ b = danmulist[a]
        hide screen showdanmu
        show screen showdanmu(b[1])
        "[b[0]]"
        $ a += 1
    window hide(None)
    call screen showdanmu

screen showdanmu(obj):
    vbox:
        spacing 10
        text "[obj]":
            color "#fff"
        for i in obj:
            text "[i]":
                color "#fff"
