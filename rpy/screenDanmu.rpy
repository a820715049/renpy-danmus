style danmu_text:
    size 30
    color "#fff"
    outlines [( absolute(1), "#000", absolute(0), absolute(0) )]

screen danmu_screen:
    for j in range(0, danmu.danmuLongs):
        for i in danmu.dp[j]:
            if i.move:
                add i

screen showdanmu:
    vbox:
        spacing 10
        for i in node.danmuBase:
            text "[i]":
                color "#8babfb"
            hbox:
                spacing 10
                for j in node.danmuBase[i]:
                    text "[j]":
                        color "#fff"
image blue = "#8babfb"
image white = "#fff"
define danmu_value = ''
screen input_screen:
    modal True
    zorder 49
    add "white":
        at transform:
            alpha 0.5
    vbox:
        xcenter 0.5
        ycenter 0.5
        text "请输入弹幕内容" style "dictionary_inner_name":
            xcenter 0.5
        frame:
            xsize 300
            ysize 50
            xcenter 0.5
            input value VariableInputValue("danmu_value")
        if danmu_value:
            textbutton "点击确认":
                xcenter 0.5
                style "dictionary_inner_name"
                action [Hide('input_screen'), SetVariable('danmu_value', ''), Function(node.push, danmu_value)]

style dictionary_inner_name:
        color "#fff"
        size 32
        line_spacing 4
        outlines [( absolute(1), "#666", absolute(0), absolute(0) )]
