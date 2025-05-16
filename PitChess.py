import os
import cv2
import numpy as np
import copy
from tkinter import messagebox, simpledialog
import sys
sys.path.append("robot1.py")
sys.path.append("robot2.py")


def color(x, y, b):
    global n
    if x in range(n) and y in range(n) and b[x][y] == 0:
        b[x][y] = "u"
        color(x - 1, y, b)
        color(x, y - 1, b)
        color(x + 1, y, b)
        color(x, y + 1, b)
#染色函数：对棋盘上(x, y)处进行填充式染色，以判断其他点与该点之间是否联通

def isunblocked(x1, y1, x2, y2, b):
    bb = copy.deepcopy(b)
    color(x1, y1, bb)
    if bb[x2][y2] == "u":
        return True
    else:
        return False
#判断堵塞函数：判断棋盘上(x1,y1)与(x2, y2)之间是否联通

def onMouse1(event, x, y, flags, param):
    global mouse, pattern
    pattern = cv2.addWeighted(theme, 0.8, starttext, 0.7, 0)
    if x in range(110, 111+len(name)*50) and y in range(45):
        cv2.putText(pattern, name, (110, 37), cv2.FONT_HERSHEY_COMPLEX, 1.1, (0, 200, 200), 3, cv2.LINE_AA)
        if event == cv2.EVENT_LBUTTONDOWN:
            mouse = 13
    if x in range(308, 577) and y in range(354, 404):
        cv2.rectangle(pattern, (307, 354), (576, 403), (200, 150, 100), -1)
        if event == cv2.EVENT_LBUTTONDOWN:
            mouse = 114
    if x in range(325, 558) and y in range(424, 469):
        cv2.rectangle(pattern, (325, 424), (558, 469), (200, 150, 100), -1)
        if event == cv2.EVENT_LBUTTONDOWN:
            mouse = 112
    if x in range(302, 448) and y in range(486, 532):
        cv2.rectangle(pattern, (302, 488), (448, 530), (200, 150, 100), -1)
        if event == cv2.EVENT_LBUTTONDOWN:
            mouse = 115
    if x in range(473, 588) and y in range(488, 529):
        cv2.rectangle(pattern, (472, 488), (588, 529), (200, 150, 100), -1)
        if event == cv2.EVENT_LBUTTONDOWN:
            mouse = 104
    if x in range(222, 666) and y in range(280, 320):
        cv2.rectangle(pattern, (222, 280), (666, 320), (200, 150, 100), -1)
        if event == cv2.EVENT_LBUTTONDOWN:
            mouse = 32
#主界面鼠标回调函数：鼠标移动按钮到按钮上时显示提示，点击时生成指令

def onMouse2(event, x, y, flags, param):
    global mouse, pattern
    pattern = copy.deepcopy(screen)
    if x in range(258, 258+50*len(name)) and y in range(225, 265):
        cv2.putText(pattern, name, (270, 260), cv2.FONT_HERSHEY_COMPLEX, 1.3, (0, 200, 200), 3, cv2.LINE_AA)
        cv2.putText(pattern, "Change your name?", (x, y+30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
        if event == cv2.EVENT_LBUTTONDOWN:
            mouse = 110
    if x in range(465, 850) and y in range(590, 625):
        cv2.rectangle(pattern, (465, 590), (850, 625), (200, 150, 100), -1)
        if event == cv2.EVENT_LBUTTONDOWN:
            mouse = 115
    #465590850625
#用户界面鼠标回调函数：具体效果同上

def putbrick(event, x, y, flags, boardview):
    global tpb, bricksize, a, x0, y0
    if event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
        px = (x-bx) // 50
        py = (y-by) // 50
        if bricksize == 0 and px in range(n) and py in range(n):
            tpb[px][py] = 1
            cv2.rectangle(boardview, (px * 50 + bx, py * 50 + by), (px * 50 + bx + 50, py * 50 + by + 50), (100, 200, 200), -1)
            bricksize = bricksize + 1
            x0 = px
            y0 = py
        elif bricksize == 1 and px in range(n) and py in range(n):
            if x0 == px and (y0 - py == 1 or y0 - py == -1) or y0 == py and (x0 - px == 1 or x0 - px == -1):
                tpb[px][py] = 1
                cv2.rectangle(boardview, (px * 50 + bx, py * 50 + by), (px * 50 + bx + 50, py * 50 + by + 50), (100, 200, 200), -1)
                bricksize = bricksize + 1
    if event == cv2.EVENT_LBUTTONUP and bricksize == 2:
        bricksize = -1
#放砖模式中的鼠标回调函数：拖动鼠标左键显示预览，松开完成放置

isrunning = True
if os.path.exists("data") == False:
    name = simpledialog.askstring("Welcome!", "Your name is:                             ")
    if name == None or name == "":
        name = "unnamed player"
    theme = cv2.imread(r"images\theme4.png")
    helptext = cv2.imread(r"images\Help.png")
    for i in range(8):
        screen = cv2.addWeighted(theme, 0.5, helptext, i * 0.1, 0)
        cv2.imshow("Pit Chess", screen)
        cv2.waitKey(30)
    screen = cv2.addWeighted(theme, 0.5, helptext, 0.8, 0)
    cv2.putText(screen, "Press any key to continue.", (10, 656), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (100, 200, 200), 1, cv2.LINE_AA)
    cv2.imshow("Pit Chess", screen)
    cv2.waitKey(0)
    os.mkdir("data")
    os.mkdir(fr"data\{name}")
    with open(fr"data\{name}\Record.txt", "w+") as record:
        record.write("0\n0")
    with open(fr"data\{name}\Data.txt", "w+") as data:
        data.write("10\n3\n100 40\n180 130\n4")
    gamemode = 3
    robotturn = 2
    robotmode = 1
else:
    name = os.listdir("data")[0]
    gamemode = 0
#识别是否是新手，如果是则进入新手教程

while isrunning:
    starttext = cv2.imread(r"images\Gamestart.png")
    data = list(open(fr"data\{name}\Data.txt", "r+"))
    score = list(map(int, list(open(fr"data\{name}\Record.txt", "r+"))))
    n = int(data[0])
    m = int(data[1])
    tx = int(data[2].split()[0])
    ty = int(data[2].split()[1])
    bx = int(data[3].split()[0])
    by = int(data[3].split()[1])
    t = int(data[-1])
    theme = cv2.imread(fr"images\theme{t}.png")
    cv2.putText(starttext, name+"!", (111, 38), cv2.FONT_HERSHEY_COMPLEX, 1.1, (200, 200, 200), 2, cv2.LINE_AA, )
    i = 0
    cv2.namedWindow("Pit Chess")
    start = cv2.addWeighted(theme, 0.8, starttext, 0.7, 0)
    pattern = copy.deepcopy(start)
    cv2.setMouseCallback("Pit Chess", onMouse1)
    #读取当前设置数据，生成主界面

    while gamemode == 0:
        mouse = -1
        while i < 8:
            start = cv2.addWeighted(theme, 0.5 + i * 0.05, starttext, i * 0.1, 0)
            cv2.imshow("Pit Chess", start)
            cv2.waitKey(30)
            i = i + 1
        cv2.imshow("Pit Chess", cv2.addWeighted(start, 0.5, pattern, 0.5, 0))
        order = cv2.waitKey(30)
        if order == 27:
            isrunning = False
            cv2.destroyAllWindows()
            break
        if cv2.getWindowProperty('Pit Chess', cv2.WND_PROP_VISIBLE) < 1:
            isrunning = False
            break
        #关闭主界面并退出游戏
        elif order in [114, 112, 115, 104, 13, 32] or mouse != -1:
            if max(order, mouse) == 13:
                trophy = cv2.imread(r"images\trophy.png")
                record = cv2.imread(r"images\record.png")
                screen = cv2.addWeighted(cv2.addWeighted(trophy, 0.2, theme, 1, 0), 0.8, record, 0.8, 0)
                cv2.putText(screen, name, (270, 260), cv2.FONT_HERSHEY_COMPLEX, 1.3, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(screen, str(score[0]), (400, 420), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 1.2, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(screen, str(score[1]), (400, 465), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 1.2, (255, 255, 255), 2, cv2.LINE_AA)
                pattern = copy.deepcopy(screen)
                mouse = -1
                cv2.setMouseCallback("Pit Chess", onMouse2)
                while True:
                    cv2.imshow("Pit Chess", cv2.addWeighted(screen, 0.5, pattern, 0.5, 0))
                    key = cv2.waitKey(30)
                    if cv2.getWindowProperty('Pit Chess', cv2.WND_PROP_VISIBLE) < 1:
                        break
                    if key == 110 or mouse == 110:
                        name1 = simpledialog.askstring("Change your name?", "Your new name:                                         ", initialvalue=name)
                        if name1 == None or "":
                            mouse = -1
                            continue
                        else:
                            os.rename(fr"data\{name}", fr"data\{name1}")
                            name = name1
                            break
                    elif key == 115 or mouse == 115:
                        name1 = simpledialog.askstring("Switch to your account",
                                                       "Your name:                                                        ",
                                                       initialvalue=name)
                        if name1 == None or "":
                            mouse = -1
                            continue
                        elif os.path.exists(fr"data\{name1}"):
                            name = name1
                            break
                        else:
                            assume = messagebox.askokcancel("User not existing.", "Create a new user?")
                            if not assume:
                                continue
                            name = name1
                            theme = cv2.imread(r"images\theme4.png")
                            helptext = cv2.imread(r"images\Help.png")
                            for i in range(8):
                                screen = cv2.addWeighted(theme, 0.5, helptext, i * 0.1, 0)
                                cv2.imshow("Pit Chess", screen)
                                cv2.waitKey(30)
                            screen = cv2.addWeighted(theme, 0.5, helptext, 0.8, 0)
                            cv2.putText(screen, "Press any key to continue.", (10, 656), cv2.FONT_HERSHEY_TRIPLEX, 0.7,
                                        (100, 200, 200), 1, cv2.LINE_AA)
                            cv2.imshow("Pit Chess", screen)
                            cv2.waitKey(0)
                            os.mkdir(fr"data\{name}")
                            with open(fr"data\{name}\Record.txt", "w+") as record:
                                record.write("0\n0")
                            with open(fr"data\{name}\Data.txt", "w+") as data:
                                data.write("10\n2\n100 40\n180 130\n4")
                            gamemode = 3
                            robotturn = 2
                            robotmode = 1
                            break
                    elif key != -1:
                        break
                break
            #用户界面
            order = chr(max(order, mouse))
            if order == " ":
                gamemode = 1
                i = 0
                while i < 8:
                    start = cv2.addWeighted(theme, 0.8, starttext, 0.8 - i * 0.1, 0)
                    cv2.imshow("Pit Chess", start)
                    cv2.waitKey(30)
                    i = i + 1
                break
            #开始新游戏
            elif order == "p":
                gamemode = 2
                i = 0
                while i < 8:
                    start = cv2.addWeighted(theme, 0.8, starttext, 0.8 - i * 0.1, 0)
                    cv2.imshow("Pit Chess", start)
                    cv2.waitKey(30)
                    i = i + 1
                break
            #进入存档
            elif order == "r":
                robotturn = simpledialog.askinteger("Set the robot", prompt="选择先后手：\n1表示你先手，2表示机器人先手            ",
                                                    initialvalue=1, minvalue=1, maxvalue=2)
                if robotturn == None: continue
                robotmode = simpledialog.askinteger("Set the robot", prompt="机器人难度（1-2）\n数字越大，难度越大                          ",
                                                    initialvalue=1, minvalue=1, maxvalue=2)
                if robotmode == None: continue
                gamemode = 3
                i = 0
                while i < 8:
                    start = cv2.addWeighted(theme, 0.8, starttext, 0.8 - i * 0.1, 0)
                    cv2.imshow("Pit Chess", start)
                    cv2.waitKey(30)
                    i = i + 1
                break
            #进入人机模式
            elif order == "h":
                i = 0
                while i < 8:
                    start = cv2.addWeighted(theme, 0.8 - i * 0.05, starttext, 0.8 - i * 0.1, 0)
                    cv2.imshow("Pit Chess", start)
                    cv2.waitKey(30)
                    i = i + 1
                helptext = cv2.imread(r"images\Help.png")
                i = 0
                while i < 8:
                    help = cv2.addWeighted(theme, 0.45, helptext, i * 0.1, 0)
                    cv2.imshow("Pit Chess", help)
                    cv2.waitKey(30)
                    i = i + 1
                help = cv2.addWeighted(theme, 0.5, helptext, 0.8, 0)
                cv2.imshow("Pit Chess", help)
                cv2.waitKey(0)
                if cv2.getWindowProperty('Pit Chess', cv2.WND_PROP_VISIBLE) < 1:
                    break
                i = 0
                while i < 8:
                    help = cv2.addWeighted(theme, 0.5, helptext, 0.8 - i * 0.1, 0)
                    cv2.imshow("Pit Chess", help)
                    cv2.waitKey(30)
                    i = i + 1
                i = 0
                continue
            #打开帮助
            elif order == "s":
                insetting = True
                n1 = simpledialog.askinteger("Settings", prompt="棋盘大小：", initialvalue=n, minvalue=2, maxvalue=10)
                if n1 == None:
                    insetting = False
                    i = 8
                if insetting:
                    n = n1
                    m1 = simpledialog.askinteger("Settings", prompt="先手块数：", initialvalue=m, minvalue=1, maxvalue=n//2)
                    if m1 == None:
                        insetting = False
                        i = 8
                if insetting:
                    m = m1
                    screen = copy.deepcopy(start)
                while insetting:
                    foreground = copy.deepcopy(theme)
                    cv2.rectangle(foreground, (tx - 10, ty - 25), (tx + 666, ty + 70), (50, 50, 50), -1)
                    screen1 = cv2.addWeighted(theme, 0.5, foreground, 0.5, 0)
                    cv2.putText(screen1, "Press Space to change the theme.", (tx, ty), cv2.FONT_HERSHEY_TRIPLEX,
                                0.7, (0, 200, 200), 1, cv2.LINE_AA)
                    cv2.putText(screen1, "Press Enter to move on.", (tx, ty + 30), cv2.FONT_HERSHEY_TRIPLEX, 0.7,
                                (0, 200, 200), 1, cv2.LINE_AA)
                    for i in range(10):
                        cv2.imshow("Pit Chess", cv2.addWeighted(screen1, 0.1 * i, screen, 1 - 0.1 * i, 0))
                        cv2.waitKey(30)
                    screen = copy.deepcopy(screen1)
                    cv2.imshow("Pit Chess", screen)
                    key = cv2.waitKey(0)
                    if key == -1:
                        insetting = False
                        i = 8
                        break
                    elif key == 13:
                        screen1 = copy.deepcopy(screen)
                        break
                    elif chr(key) == " ":
                        if os.path.exists(fr"images\theme{t+1}.png"):
                            theme = cv2.imread(fr"images\theme{t+1}.png")
                            t = t + 1
                        else:
                            theme = cv2.imread(r"images\theme1.png")
                            t = 1
                        continue
                if insetting:
                    bbackground = copy.deepcopy(theme)
                    cv2.rectangle(bbackground, (bx, by), (bx + 50 * n, by + 50 * n), (0, 0, 0), -1)
                    chessboard = np.zeros((666, 888, 3), np.uint8)
                    for i in range(by, n * 50 + by):
                        for j in range(bx, n * 50 + bx):
                            if (i - by) % 50 == 0 or (j - bx) % 50 == 0:
                                chessboard[i, j] = (200, 200, 200)
                            else:
                                chessboard[i, j] = (80, 80, 80)
                    foreground = copy.deepcopy(bbackground)
                    cv2.rectangle(foreground, (tx - 10, ty - 25), (tx + 666, ty + 70), (50, 50, 50), -1)
                    background = cv2.addWeighted(bbackground, 0.5, foreground, 0.5, 0)
                    screen = cv2.add(background, chessboard)
                    cv2.putText(screen, "Here's the Preview screen.", (tx, ty), cv2.FONT_HERSHEY_TRIPLEX,
                                0.7,
                                (0, 200, 200), 1, cv2.LINE_AA)
                    cv2.putText(screen, "Use the arrow keys to adjust the UI layout.", (tx, ty + 30),
                                cv2.FONT_HERSHEY_TRIPLEX, 0.7,
                                (0, 200, 200), 1, cv2.LINE_AA)
                    cv2.putText(screen, "Press enter to move on.", (tx, ty + 60), cv2.FONT_HERSHEY_TRIPLEX, 0.7,
                                (0, 200, 200), 1, cv2.LINE_AA)
                    cv2.rectangle(screen, (tx - 10, ty - 25), (tx + 666, ty + 70), (100, 200, 100), 2)
                    for i in range(8):
                        cv2.imshow("Pit Chess", cv2.addWeighted(screen1, 0.8-0.1*i, screen, 0.2+0.1*i, 0))
                        cv2.waitKey(30)
                while insetting:
                    foreground = copy.deepcopy(bbackground)
                    cv2.rectangle(foreground, (tx - 10, ty - 25), (tx + 666, ty + 70), (50, 50, 50), -1)
                    background = cv2.addWeighted(bbackground, 0.5, foreground, 0.5, 0)
                    screen = cv2.add(background, chessboard)
                    cv2.putText(screen, "Here's the Preview screen.", (tx, ty), cv2.FONT_HERSHEY_TRIPLEX,
                                0.7,
                                (0, 200, 200), 1, cv2.LINE_AA)
                    cv2.putText(screen, "Use the arrow keys to adjust the UI layout.", (tx, ty + 30), cv2.FONT_HERSHEY_TRIPLEX, 0.7,
                                (0, 200, 200), 1, cv2.LINE_AA)
                    cv2.putText(screen, "Press enter to move on.", (tx, ty + 60), cv2.FONT_HERSHEY_TRIPLEX, 0.7,
                                (0, 200, 200), 1, cv2.LINE_AA)
                    cv2.rectangle(screen, (tx-10, ty - 25), (tx + 666, ty + 70), (100, 200, 100), 2)
                    cv2.imshow("Pit Chess", screen)
                    key = cv2.waitKeyEx(0)
                    if key == -1 or key == 27:
                        insetting = False
                        i = 0
                        break
                    elif key == 2490368:
                        ty = ty - 1
                    elif key == 2621440:
                        ty = ty + 1
                    elif key == 2424832:
                        tx = tx - 1
                    elif key == 2555904:
                        tx = tx + 1
                    elif key == 13:
                        break
                    else:
                        continue
                #将固定棋盘的界面设置为background，按方向键以调整文字框位置
                bbackground = copy.deepcopy(theme)
                foreground = copy.deepcopy(theme)
                cv2.rectangle(foreground, (tx - 10, ty - 25), (tx + 666, ty + 70), (50, 50, 50), -1)
                background = cv2.addWeighted(bbackground, 0.5, foreground, 0.5, 0)
                cv2.putText(background, "Here's the Preview screen.", (tx, ty), cv2.FONT_HERSHEY_TRIPLEX,
                                0.7,
                                (0, 200, 200), 1, cv2.LINE_AA)
                cv2.putText(background, "Use the arrow keys to adjust the UI layout.", (tx, ty + 30), cv2.FONT_HERSHEY_TRIPLEX, 0.7,
                                (0, 200, 200), 1, cv2.LINE_AA)
                cv2.putText(background, "Press enter to move on.", (tx, ty + 60), cv2.FONT_HERSHEY_TRIPLEX, 0.7,
                                (0, 200, 200), 1, cv2.LINE_AA)
                while insetting:
                    chessboard = np.zeros((666, 888, 3), np.uint8)
                    for i in range(by, n * 50 + by):
                        for j in range(bx, n * 50 + bx):
                            if (i - by) % 50 == 0 or (j - bx) % 50 == 0:
                                chessboard[i, j] = (200, 200, 200)
                            else:
                                chessboard[i, j] = (80, 80, 80)
                    screen = copy.deepcopy(background)
                    cv2.rectangle(screen, (bx, by), (bx + 50 * n, by + 50 * n), (0, 0, 0), -1)
                    screen = cv2.add(screen, chessboard)
                    cv2.rectangle(screen, (bx, by), (bx + 50 * n, by + 50 * n), (100, 200, 100), 2)
                    cv2.imshow("Pit Chess", screen)
                    key = cv2.waitKeyEx(0)
                    if key == -1 or key == 27 or key == 13:
                        insetting = False
                        i = 0
                        break
                    elif key == 2490368 and by > 0:
                        by = by - 1
                    elif key == 2621440 and by + 50 * n < 666:
                        by = by + 1
                    elif key == 2424832 and bx > 0:
                        bx = bx - 1
                    elif key == 2555904 and bx + 50 * n < 888:
                        bx = bx + 1
                    else:
                        continue
                #再将固定文字框的界面设置为background，按方向键以调整棋盘位置
                with open(fr"data\{name}\Data.txt", "w") as data:
                    data.write(f"{n}\n{m}\n{tx} {ty}\n{bx} {by}\n{t}")
                break
            #进入设置
        #识别有效指令
        else:
            i = 8
            continue
        #指令无效则继续循环
    #游戏主界面

    if gamemode == 1:
        robotturn = 0
        robotmode = 0
        usingrobot = [False, False]
        chessboard = np.zeros((666, 888, 3), np.uint8)
        for i in range(by, n * 50 + by):
            for j in range(bx, n * 50 + bx):
                if (i - by) % 50 == 0 or (j - bx) % 50 == 0:
                    chessboard[i, j] = (200, 200, 200)
                else:
                    chessboard[i, j] = (80, 80, 80)
        cv2.imwrite(fr"data\{name}\chessboard.png", chessboard)
        board = [[0 for i in range(n)] for j in range(n)]
        p1 = [0, 0]
        b1 = m
        p2 = [n - 1, n - 1]
        b2 = m + 1
        turn = True
    #新游戏：新建棋盘，初始化游戏参数

    if gamemode == 2:
        previousdata = list(open(fr"data\{name}\Previous.txt", "r+"))
        turn = bool(int(previousdata[0]))
        board = []
        n = len(previousdata[1].split())
        chessboard = np.zeros((666, 888, 3), np.uint8)
        for i in range(by, n * 50 + by):
            for j in range(bx, n * 50 + bx):
                if (i - by) % 50 == 0 or (j - bx) % 50 == 0:
                    chessboard[i, j] = (200, 200, 200)
                else:
                    chessboard[i, j] = (80, 80, 80)
        for i in range(1, n+1):
            board.append(list(map(int, previousdata[i].split())))
        n = len(board)
        p1 = list(map(int, previousdata[-1].split()))
        p2 = list(map(int, previousdata[-2].split()))
        b1 = int(previousdata[-3].split()[0]); b2 = int(previousdata[-3].split()[1])
        robotturn = int(previousdata[-4].split()[0])
        robotmode = int(previousdata[-4].split()[1])
        if robotturn == 0:
            usingrobot = [False, False]
        elif robotturn == 1:
            usingrobot = [False, True]
        else:
            usingrobot = [True, False]
        if robotmode == 0:
            pass
        elif robotmode == 1:
            from robot1 import *
        else:
            from robot2 import *
        if robotmode: robot = cv2.imread(fr"images\robotthinking.png")
    #继续游戏：读取存档，turn=True表示当前轮到先手，反之轮到后手

    if gamemode == 3:
        chessboard = np.zeros((666, 888, 3), np.uint8)
        for i in range(by, n * 50 + by):
            for j in range(bx, n * 50 + bx):
                if (i - by) % 50 == 0 or (j - bx) % 50 == 0:
                    chessboard[i, j] = (200, 200, 200)
                else:
                    chessboard[i, j] = (80, 80, 80)
        cv2.imwrite(fr"data\{name}\chessboard.png", chessboard)
        board = [[0 for i in range(n)] for j in range(n)]
        p1 = [0, 0]
        b1 = m
        p2 = [n - 1, n - 1]
        b2 = m + 1
        robot = cv2.imread(fr"images\robotthinking.png")
        if robotturn == 2:
            usingrobot = [True, False]
        else:
            usingrobot = [False, True]
        if robotmode == 1:
            from robot1 import *
        else:
            from robot2 import *
        turn = True
    #人机模式：新建棋盘，选择机器人模式与先后手

    if gamemode > 0:
        with open(fr"data\{name}\Previous.txt", "w") as previous:
            previous.write("0\n")
            for line in board:
                s = ""
                for x in line:
                    s = s + str(x) + " "
                s = s[:-1]
                previous.write(s + "\n")
            previous.write(f"{robotturn} {robotmode}\n")
            previous.write(f"{b1} {b2}\n")
            previous.write(f"{p2[0]} {p2[1]}\n")
            previous.write(f"{p1[0]} {p1[1]}")
        state = True
        gamemode = 0
        foreground = copy.deepcopy(theme)
        cv2.rectangle(foreground, (tx - 10, ty - 25), (tx + 666, ty + 70), (50, 50, 50), -1)
        cv2.putText(foreground, "Press Esc to return to the main screen. Your game process will be saved automatically.", (10, 656), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.7, (255, 255, 255), 1, cv2.LINE_AA)
        i = 0
        while i < 10:
            background = cv2.addWeighted(theme, 0.8 - i * 0.03, foreground, i * 0.05, 0)
            cv2.putText(background, "Loading...", (tx, ty), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (0, 200, 200), 1, cv2.LINE_AA)
            cv2.imshow("Pit Chess", background)
            cv2.waitKey(30)
            i = i + 1
        background = cv2.addWeighted(theme, 0.5, foreground, 0.5, 0)
        screen = copy.deepcopy(background)
        cv2.rectangle(background, (bx, by), (bx + 50 * n, by + 50 * n), (0, 0, 0), -1)
        #存档并生成游戏背景
        while state:
            while state and turn:
                condition = copy.deepcopy(board)
                objects = np.zeros((666, 888, 3), np.uint8)
                cv2.circle(objects, (p1[0] * 50 + 25 + bx, p1[1] * 50 + 25 + by), 20, (0, 0, 255), -1)
                cv2.circle(objects, (p2[0] * 50 + 25 + bx, p2[1] * 50 + 25 + by), 20, (255, 0, 0), -1)
                for i in range(n):
                    for j in range(n):
                        if condition[i][j] == 1:
                            cv2.rectangle(objects, (i * 50+bx, j * 50+by), (i * 50 + 50+bx, j * 50 + 50+by), (255, 255, 255), -1)
                boardview = cv2.add(chessboard, objects)
                screen1 = cv2.add(background, boardview)
                cv2.circle(screen1, (p1[0] * 50 + 25+bx, p1[1] * 50 + 25+by), 20, (255, 255, 255), 2)
                cv2.putText(screen1, "Red 's Turn", (tx, ty), cv2.FONT_HERSHEY_TRIPLEX, 0.7,
                            (0, 200, 200), 1, cv2.LINE_AA)
                cv2.putText(screen1, f"Bricks at hand: {b1}", (tx, ty + 30), cv2.FONT_HERSHEY_TRIPLEX, 0.7,
                            (0, 200, 200), 1, cv2.LINE_AA)
                if usingrobot[0]:

                    #cv2.rectangle(screen1, (666, 0), (888, 300), (0, 0, 0), -1)
                    screen1 = cv2.add(screen1, robot)
                    cv2.putText(screen1, "I'm a robot. You'd better watch out! >v<", (tx, ty + 60), cv2.FONT_HERSHEY_TRIPLEX, 0.7,
                                (0, 200, 200), 1, cv2.LINE_AA)
                else:
                    if b1: cv2.putText(screen1, "Press Q to put brick.", (tx, ty + 60), cv2.FONT_HERSHEY_TRIPLEX, 0.7,
                            (0, 200, 200), 1, cv2.LINE_AA)
                for i in range(5):
                    loadingscreen = cv2.addWeighted(screen, 1 - 0.2 * i, screen1, 0.2 * i, 0)
                    cv2.imshow("Pit Chess", loadingscreen)
                    cv2.waitKey(10)
                screen = copy.deepcopy(screen1)
                cv2.imshow("Pit Chess", screen1)
                #显示操作前前双方棋子位置、场上砖块位置、文字提示
                if usingrobot[0]:
                    a = makedecision(p1, p2, [n-1, n-1], [0, 0], board, b1, b2)
                    if a[0]:
                        board = a[1]
                        b1 = b1 - 1
                    else:
                        p1 = a[1]
                    cv2.waitKey(300)
                    condition = copy.deepcopy(board)
                    objects = np.zeros((666, 888, 3), np.uint8)
                    cv2.circle(objects, (p1[0] * 50 + 25 + bx, p1[1] * 50 + 25 + by), 20, (0, 0, 255), -1)
                    cv2.circle(objects, (p2[0] * 50 + 25 + bx, p2[1] * 50 + 25 + by), 20, (255, 0, 0), -1)
                    for i in range(n):
                        for j in range(n):
                            if condition[i][j] == 1:
                                cv2.rectangle(objects, (i * 50 + bx, j * 50 + by), (i * 50 + 50 + bx, j * 50 + 50 + by),
                                              (255, 255, 255),
                                              -1)
                    boardview = cv2.add(chessboard, objects)
                    screen = cv2.add(boardview, background)
                    # 储存操作后界面
                    break
                try:
                    a = cv2.waitKey(0)
                    if a == -1 or a == 27:
                        with open(fr"data\{name}\Previous.txt", "w") as previous:
                            previous.write("1\n")
                            for line in board:
                                s = ""
                                for x in line:
                                    s = s + str(x) + " "
                                s = s[:-1]
                                previous.write(s+"\n")
                            previous.write(f"{robotturn} {robotmode}\n")
                            previous.write(f"{b1} {b2}\n")
                            previous.write(f"{p2[0]} {p2[1]}\n")
                            previous.write(f"{p1[0]} {p1[1]}")
                        state = False
                        if a == -1:
                            isrunning = False
                        break
                    #退出自动存档
                    a = chr(a)
                    assert a == "w" or a == "s" or a == "a" or a == "d" or a == "q"
                    p = copy.deepcopy(p1)
                    if a == "w":
                        p[1] = p1[1] - 1
                    elif a == "s":
                        p[1] = p1[1] + 1
                    elif a == "a":
                        p[0] = p1[0] - 1
                    elif a == "d":
                        p[0] = p1[0] + 1
                    #移动操作
                    elif a == "q":
                        assert b1 > 0
                        screen1 = cv2.add(boardview, background)
                        cv2.putText(screen1, f"Drag your mouse to put brick.", (tx, ty), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (0, 200, 200), 1, cv2.LINE_AA)
                        cv2.putText(screen1, f"You have {b1} at present.", (tx, ty+30), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (0, 200, 200), 1, cv2.LINE_AA)
                        cv2.putText(screen1, f"Press any key to cancel.", (tx, ty+60), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (0, 200, 200), 1, cv2.LINE_AA)
                        for i in range(5):
                            loadingscreen = cv2.addWeighted(screen, 1 - 0.2 * i, screen1, 0.2 * i, 0)
                            cv2.imshow("Pit Chess", loadingscreen)
                            cv2.waitKey(10)
                        screen = copy.deepcopy(screen1)
                        tpb = [[0 for i in range(n)] for j in range(n)]
                        b = copy.deepcopy(board)
                        bricksize = 0
                        cv2.setMouseCallback("Pit Chess", putbrick, screen)
                        while True:
                            cv2.imshow("Pit Chess", screen)
                            key = cv2.waitKey(30)
                            assert key == -1
                            if bricksize == -1:
                                break
                        for i in range(n):
                            for j in range(n):
                                if tpb[i][j] == 1:
                                    assert b[i][j] == 0 and (p1[0] != i or p1[1] != j) and (p2[0] != i or p2[1] != j)
                                    b[i][j] = 1
                        try:
                            assert isunblocked(p2[0], p2[1], 0, 0, b) and isunblocked(p1[0], p1[1], n - 1, n - 1, b)
                            board = b
                            b1 = b1 - 1
                        except:
                            messagebox.showinfo("出错了", "这里不行！")
                            continue
                    #放置砖块操作
                    assert board[p[0]][p[1]] == 0 and p[0] in range(n) and p[1] in range(n)
                    p1 = p
                    condition = copy.deepcopy(board)
                    objects = np.zeros((666, 888, 3), np.uint8)
                    cv2.circle(objects, (p1[0] * 50 + 25 + bx, p1[1] * 50 + 25 + by), 20, (0, 0, 255), -1)
                    cv2.circle(objects, (p2[0] * 50 + 25 + bx, p2[1] * 50 + 25 + by), 20, (255, 0, 0), -1)
                    for i in range(n):
                        for j in range(n):
                            if condition[i][j] == 1:
                                cv2.rectangle(objects, (i * 50 + bx, j * 50 + by), (i * 50 + 50 + bx, j * 50 + 50 + by), (255, 255, 255),
                                              -1)
                    boardview = cv2.add(chessboard, objects)
                    screen = cv2.add(boardview, background)
                    #储存操作后界面
                    break
                except:
                    continue
                #判断操作合法性，如果不合法则重启循环
            #先手回合
            if p1 == [n - 1, n - 1]:
                cv2.putText(screen, "Game Over", (tx, ty), cv2.FONT_HERSHEY_TRIPLEX,
                            0.7, (0, 200, 200), 1, cv2.LINE_AA)
                cv2.putText(screen, "Red Wins!", (tx, ty + 30), cv2.FONT_HERSHEY_TRIPLEX, 0.7,
                            (0, 200, 200), 1, cv2.LINE_AA)
                cv2.imshow("Pit Chess", screen)
                if usingrobot[1]:
                    score[robotmode-1] += 1
                    with open(fr"data\{name}\Record.txt", "w+") as rc:
                        rc.write(f"{score[0]}\n{score[1]}")
                messagebox.showinfo("Game Over", "游戏结束，先手获胜！")
                cv2.destroyAllWindows()
                break
            if p2 == [0, 0]:
                cv2.putText(screen, "Game Over", (tx, ty), cv2.FONT_HERSHEY_TRIPLEX,
                            0.7, (0, 200, 200), 1, cv2.LINE_AA)
                cv2.putText(screen, "Blue Wins!", (tx, ty + 30), cv2.FONT_HERSHEY_TRIPLEX, 0.7,
                            (0, 200, 200), 1, cv2.LINE_AA)
                cv2.imshow("Pit Chess", screen)
                if usingrobot[0]:
                    score[robotmode-1] += 1
                    with open(fr"data\{name}\Record.txt", "w+") as rc:
                        rc.write(f"{score[0]}\n{score[1]}")
                messagebox.showinfo("Game Over", "游戏结束，后手获胜！")
                cv2.destroyAllWindows()
                break
            #先手回合结束判断胜负
            while state:
                turn = True
                condition = copy.deepcopy(board)
                objects = np.zeros((666, 888, 3), np.uint8)
                cv2.circle(objects, (p1[0] * 50 + 25 + bx, p1[1] * 50 + 25 + by), 20, (0, 0, 255), -1)
                cv2.circle(objects, (p2[0] * 50 + 25 + bx, p2[1] * 50 + 25 + by), 20, (255, 0, 0), -1)
                for i in range(n):
                    for j in range(n):
                        if condition[i][j] == 1:
                            cv2.rectangle(objects, (i * 50 + bx, j * 50 + by), (i * 50  + 50 + bx, j * 50 + 50 + by),
                                          (255, 255, 255),
                                          -1)
                boardview = cv2.add(chessboard, objects)
                cv2.circle(boardview, (p2[0] * 50 + 25 + bx, p2[1] * 50 + 25 + by), 20, (255, 255, 255), 2)
                screen1 = cv2.add(boardview, background)
                cv2.putText(screen1, "Blue's Turn", (tx, ty), cv2.FONT_HERSHEY_TRIPLEX, 0.7,
                            (0, 200, 200), 1, cv2.LINE_AA)
                cv2.putText(screen1, f"Bricks at hand: {b2}", (tx, ty + 30), cv2.FONT_HERSHEY_TRIPLEX, 0.7,
                            (0, 200, 200), 1, cv2.LINE_AA)
                if usingrobot[1]:
                    #cv2.rectangle(screen1, (666, 0), (888, 300), (0, 0, 0), -1)
                    screen1 = cv2.add(screen1, robot)
                    cv2.putText(screen1, "I'm a robot. You'd better watch out! >v<", (tx, ty + 60), cv2.FONT_HERSHEY_TRIPLEX, 0.7,
                                (0, 200, 200), 1, cv2.LINE_AA)
                else:
                    if b2: cv2.putText(screen1, "Press P to put brick.", (tx, ty + 60), cv2.FONT_HERSHEY_TRIPLEX, 0.7,
                            (0, 200, 200), 1, cv2.LINE_AA)
                for i in range(5):
                    loadingscreen = cv2.addWeighted(screen, 1 - 0.2 * i, screen1, 0.2 * i, 0)
                    cv2.imshow("Pit Chess", loadingscreen)
                    cv2.waitKey(10)
                screen = copy.deepcopy(screen1)
                cv2.imshow("Pit Chess", screen)
                #显示操作前双方棋子位置、场上砖块位置、文字提示
                if usingrobot[1]:
                    a = makedecision(p2, p1, [0, 0], [n-1, n-1], board, b2, b1)
                    if a[0]:
                        board = a[1]
                        b2 = b2 - 1
                    else:
                        p2 = a[1]
                    cv2.waitKey(300)
                    condition = copy.deepcopy(board)
                    objects = np.zeros((666, 888, 3), np.uint8)
                    cv2.circle(objects, (p1[0] * 50 + 25 + bx, p1[1] * 50 + 25 + by), 20, (0, 0, 255), -1)
                    cv2.circle(objects, (p2[0] * 50 + 25 + bx, p2[1] * 50 + 25 + by), 20, (255, 0, 0), -1)
                    for i in range(n):
                        for j in range(n):
                            if condition[i][j] == 1:
                                cv2.rectangle(objects, (i * 50 + bx, j * 50 + by), (i * 50 + 50 + bx, j * 50 + 50 + by),
                                              (255, 255, 255),
                                              -1)
                    boardview = cv2.add(chessboard, objects)
                    screen = cv2.add(boardview, background)
                    # 储存操作后界面
                    break
                try:
                    a = cv2.waitKey(0)
                    if a == -1 or a == 27:
                        with open(fr"data\{name}\Previous.txt", "w") as previous:
                            previous.write("0\n")
                            for line in board:
                                s = ""
                                for x in line:
                                    s = s + str(x) + " "
                                s = s[:-1]
                                previous.write(s + "\n")
                            previous.write(f"{robotturn} {robotmode}\n")
                            previous.write(f"{b1} {b2}\n")
                            previous.write(f"{p2[0]} {p2[1]}\n")
                            previous.write(f"{p1[0]} {p1[1]}")
                        state = False
                        if a == -1:
                            isrunning = False
                        break
                    #退出自动存档
                    a = chr(a)
                    assert a == "i" or a == "k" or a == "j" or a == "l" or a == "p"
                    p = copy.deepcopy(p2)
                    if a == "i":
                        p[1] = p2[1] - 1
                    elif a == "k":
                        p[1] = p2[1] + 1
                    elif a == "j":
                        p[0] = p2[0] - 1
                    elif a == "l":
                        p[0] = p2[0] + 1
                    #移动操作
                    elif a == "p":
                        assert b2 > 0
                        screen1 = cv2.add(boardview, background)
                        cv2.putText(screen1, f"Drag your mouse to put brick.", (tx, ty), cv2.FONT_HERSHEY_TRIPLEX,
                                    0.7, (0, 200, 200), 1, cv2.LINE_AA)
                        cv2.putText(screen1, f"You have {b2} at present.", (tx, ty+30), cv2.FONT_HERSHEY_TRIPLEX, 0.7,
                                    (0, 200, 200), 1, cv2.LINE_AA)
                        cv2.putText(screen1, f"Press any key to cancel.", (tx, ty+60), cv2.FONT_HERSHEY_TRIPLEX, 0.7,
                                    (0, 200, 200), 1, cv2.LINE_AA)
                        for i in range(5):
                            loadingscreen = cv2.addWeighted(screen, 1 - 0.2 * i, screen1, 0.2 * i, 0)
                            cv2.imshow("Pit Chess", loadingscreen)
                            cv2.waitKey(10)
                        screen = copy.deepcopy(screen1)
                        tpb = [[0 for i in range(n)] for j in range(n)]
                        b = copy.deepcopy(board)
                        bricksize = 0
                        cv2.setMouseCallback("Pit Chess", putbrick, screen)
                        while True:
                            cv2.imshow("Pit Chess", screen)
                            key = cv2.waitKey(30)
                            assert key == -1
                            if bricksize == -1:
                                break
                        for i in range(n):
                            for j in range(n):
                                if tpb[i][j] == 1:
                                    assert b[i][j] == 0 and (p1[0] != i or p1[1] != j) and (p2[0] != i or p2[1] != j)
                                    b[i][j] = 1
                        try:
                            assert isunblocked(p2[0], p2[1], 0, 0, b) and isunblocked(p1[0], p1[1], n - 1, n - 1, b)
                            board = b
                            b2 = b2 - 1
                        except:
                            messagebox.showinfo("出错了", "这里不行！")
                            continue
                    #放置砖块操作
                    assert board[p[0]][p[1]] == 0 and p[0] in range(n) and p[1] in range(n)
                    p2 = p
                    condition = copy.deepcopy(board)
                    objects = np.zeros((666, 888, 3), np.uint8)
                    cv2.circle(objects, (p1[0] * 50 + 25 + bx, p1[1] * 50 + 25 + by), 20, (0, 0, 255), -1)
                    cv2.circle(objects, (p2[0] * 50 + 25 + bx, p2[1] * 50 + 25 + by), 20, (255, 0, 0), -1)
                    for i in range(n):
                        for j in range(n):
                            if condition[i][j] == 1:
                                cv2.rectangle(objects, (i * 50 + bx, j * 50 + by), (i * 50 + 50 + bx, j * 50 + 50 + by), (255, 255, 255),
                                              -1)
                    boardview = cv2.add(chessboard, objects)
                    screen = cv2.add(boardview, background)
                    #储存操作后界面
                    break
                except Exception as e:
                    continue
                #判断操作的合法性，如果不合法则重启循环
            #后手回合
            if p1 == [n - 1, n - 1]:
                cv2.putText(screen, "Game Over", (tx, ty), cv2.FONT_HERSHEY_TRIPLEX,
                            0.7, (0, 200, 200), 1, cv2.LINE_AA)
                cv2.putText(screen, "Red Wins!", (tx, ty + 30), cv2.FONT_HERSHEY_TRIPLEX, 0.7,
                            (0, 200, 200), 1, cv2.LINE_AA)
                if usingrobot[1]:
                    score[robotmode-1] += 1
                    with open(fr"data\{name}\Record.txt", "w+") as rc:
                        rc.write(f"{score[0]}\n{score[1]}")
                messagebox.showinfo("Game Over", "游戏结束，先手获胜！")
                break
            if p2 == [0, 0]:
                cv2.putText(screen, "Game Over", (tx, ty), cv2.FONT_HERSHEY_TRIPLEX,
                            0.7, (0, 200, 200), 1, cv2.LINE_AA)
                cv2.putText(screen, "Blue Wins!", (tx, ty + 30), cv2.FONT_HERSHEY_TRIPLEX, 0.7,
                            (0, 200, 200), 1, cv2.LINE_AA)
                cv2.imshow("Pit Chess", screen)
                if usingrobot[0]:
                    score[robotmode-1] += 1
                    with open(fr"data\{name}\Record.txt", "w+") as rc:
                        rc.write(f"{score[0]}\n{score[1]}")
                messagebox.showinfo("Game Over", "游戏结束，后手获胜！")
                break
            #后手回合结束判断胜负
        #进入操作回合循环
    #开始游戏
#游戏主体循环