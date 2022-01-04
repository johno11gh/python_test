#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import tkinter as tk
from tkinter import messagebox
import random

class Application(tk.Frame):
    def __init__(self, master = None):
        #ウィンドウ##################################
        super().__init__(master)
        self.master = master
        self.master.geometry("550x625")
        self.master.title("オブジェクト化ブロック崩し")
        self.master.resizable(False, False) #x方向, y方向へのウィンドウのサイズ変更の可否
        #キャンバス初期条件##################################
        self.can_width = 400
        self.can_height = 600
        self.can_padx = 10
        self.can_pady = 10
        #ボール初期位置中心座標 初期速度################################
        self.ball_x = 120
        self.ball_y = 500
        self.ball_vx = 5
        self.ball_vy = -5
        self.ball_r = 10
        #ラケット初期位置中心座標、初期条件##################################
        self.rack_x = 210 #can_padxと考慮するとcan_padx+can_half_widthが中心点
        self.rack_y = 580
        self.rack_half_length = 50 #ラケット横長さ
        self.rack_half_height = 10 #ラケット縦長さ
        self.keyPress_R = False
        self.keyPress_L = False
        self.keyPress_U = False
        self.keyPress_D = False
        #ブロックステータス　定数定義のみ################################
        self.block_x = None
        self.block_y = None
        self.block_half_length = 35
        self.block_half_height = 15
        self.st = None
        #キャンバス生成##################################
        self.createCanvas()
        #ウィジェット生成
        self.createWidget()
        #ゲームスタート##################################
        self.createObject()
        print('gameスタート')
        self.gameLoop()

    def createCanvas(self):
        print('createCanvas')
        #キャンバス描画##################################
        self.can = tk.Canvas(bg = "#e0e0e0", width=self.can_width, height=self.can_height)
        self.can.place(x = self.can_padx, y = self.can_pady)

        #ラケット定義##################################
        print('ラケット定義')
        self.racket = Racket(self.can, self.rack_x, self.rack_y, self.rack_half_length, self.rack_half_height, self.keyPress_R, self.keyPress_L, self.keyPress_U, self.keyPress_D, self.can_width, self.can_padx)
        #ボール定義####################################
        print('ball定義')
        self.ball = Ball(self.can, self.ball_x, self.ball_y, self.ball_r, self.ball_vx, self.ball_vy, self.racket.rack_x, self.racket.rack_y, self.racket.rack_half_length, self.racket.rack_half_height, self.can_padx, self.can_pady, self.can_width, self.can_height)
        #ブロック定義##################################
        print('block定義')
        self.prepare_block()
        self.block_object_list = []
        self.color_number = 0
        for i in (self.block_list):
            self.block_x = i["block_x"]
            self.block_y = i["block_y"]
            self.st = i["st"]
            if random.randint(0, 1) == 1:
                self.color_number = random.randint(0,8)
            self.color_number += 1 #色を固定する場合は足さず指定する カラフルにする場合は+=1にする 一定数数えたら0に戻りループする
            self.block_color_pattern()
            self.block_object = Block(self.can, self.block_x, self.block_y, self.block_half_length, self.block_half_height, self.st, self.color, self.ball.ball_x, self.ball.ball_y, self.ball.ball_r, self.ball.ball_vx, self.ball.ball_vy)
            self.block_object_list.append(self.block_object)
            #print('生成情報', self.x, self.y, self.st, self.ball_x, self.ball_y, self.bx, self.by, self.rack_x)
        print(self.block_object_list)

    def createWidget(self):
        #self.startBtn = tk.Button(text = "game start")
        #self.startBtn.place(x = 430, y = 30)
        self.label1 = tk.Label(text = "(")
        self.label1.place(x = 430 , y = 60)
        self.label2 = tk.Label(textvariable = self.ball.ball_x)
        self.label2.place(x = 440, y = 61)
        self.label3 = tk.Label(text = ",")
        self.label3.place(x = 475, y = 60)
        self.label4 = tk.Label(textvariable = self.ball.ball_y)
        self.label4.place(x = 485, y=61)
        self.label5 = tk.Label(text = ")")
        self.label5.place(x = 515, y= 60)

    def createObject(self):
        self.figs = {}
        x1, y1, x2, y2 = self.ball.getCoords()
        figure = self.ball.createBall(
            self.racket.rack_x, self.racket.rack_y
        )
        self.figs[self.ball] = figure
        for self.block in self.block_object_list:
            x1, y1, x2, y2 = self.block.getCoords()
            figure = self.block.createBlock(self.ball.ball_x, self.ball.ball_y, self.ball.ball_vx, self.ball.ball_vy)
            self.figs[self.block] = figure

    def gameLoop(self):
        self.can.delete("all")
        #self.gameOver()
        self.gameClear()
        self.racket.createRacket()
        self.rack_move() #デフォルトラケットムーブがTrueの場合ここに関数を入れないと動かない
        self.ball.createBall(self.racket.rack_x, self.racket.rack_y)
        for i in self.block_object_list:
            i.createBlock(self.ball.ball_x, self.ball.ball_y, self.ball.ball_vx, self.ball.ball_vy)
        self.block_collision()
        self.after(15, self.gameLoop)
        #print(self.block) #Applicationで定義したself.blockを表示するため、ゲームループで更新されるステータスを表示するにはBlockオブジェクトのステータスを表示しなくてはいけない

    def gameOver(self):
        if self.ball.ball_y + self.ball.ball_r >= self.can_height + self.can_pady :
            messagebox.showinfo("Information", "Game Over!")
            sys.exit()

    def gameClear(self):
        if not self.block_object_list:
            messagebox.showinfo("Information", "CONGRATULATIONS!!")
            sys.exit()

    def rightKeyPress(self, event):
        self.keyPress_R = True
    def rightKeyRelease(self, event):
        self.keyPress_R = False
    def leftKeyPress(self, event):
        self.keyPress_L = True
    def leftKeyRelease(self, event):
        self.keyPress_L = False
    def upKeyPress(self, event):
        self.keyPress_U = True
    def upKeyRelease(self, event):
        self.keyPress_U = False
    def downKeyPress(self, event):
        self.keyPress_D = True
    def downKeyRelease(self, event):
        self.keyPress_D = False

    def rack_move(self):
        #ラケットの動き
        self.master.bind("<KeyPress-Right>", self.rightKeyPress)
        self.master.bind("<KeyRelease-Right>", self.rightKeyRelease) #Releaseのlは小文字
        self.master.bind("<KeyPress-Left>", self.leftKeyPress)
        self.master.bind("<KeyRelease-Left>", self.leftKeyRelease)
        self.master.bind("<KeyPress-Up>", self.upKeyPress)
        self.master.bind("<KeyRelease-Up>", self.upKeyRelease)
        self.master.bind("<KeyPress-Down>", self.downKeyPress)
        self.master.bind("<KeyRelease-Down>", self.downKeyRelease)

        if self.keyPress_R and self.racket.rack_x + self.racket.rack_half_length <= self.racket.can_width - 1:
            self.racket.rack_x += 5
        if self.keyPress_L and self.racket.rack_x - self.racket.rack_half_length >= self.can_padx:
            self.racket.rack_x -= 5
        if self.keyPress_U and self.racket.rack_y >= 500:
            self.racket.rack_y -= 5
        if self.keyPress_D and self.racket.rack_y <= 580:
            self.racket.rack_y += 5

    def prepare_block(self):
        self.block_marginx = 5
        self.block_marginy = 10
        self.block_list = []
        for_count = 0
        for self.x in range(5):
            for self.y in range(7):
                for_count += 1
                """
                if (for_count % 2 == 0):
                    for_st = 0
                elif (for_count %2 == 1):
                    for_st = 1
                """
                self.block_list.append({"block_x": self.x*80+5+self.block_half_length, "block_y": self.y*40+10+self.block_half_height, "st": 1})
                #"st"のところは基本１にすること for_stにすれば一部配置を変更可能
        """
        #内包表記ではself.x, self.yを同時にカウントし進める
        [1,1] [2,2], [3,3]と進めるので、ブロック崩しのような全行全列作るのには適さない
        ただし書き方については参考に書き記しておく
        for self.x, self.y in zip(range(5), range(7)):
            self.block_list.append({"block_x": self.x*80+5+self.block_half_length, "block_y": self.y*40+10+self.block_half_height, "st": 1})
        """
        #print(self.block_list)

    def block_color_pattern(self):
        if self.color_number == 1:
            self.color = "white"
        elif self.color_number == 2:
            self.color = "red"
        elif self.color_number == 3:
            self.color = "magenta"
        elif self.color_number == 4:
            self.color = "blue"
        elif self.color_number == 5:
            self.color = "cyan"
        elif self.color_number == 6:
            self.color = "yellow"
        elif self.color_number == 7:
            self.color = "lightgreen"
        elif self.color_number == 8:
            self.color = "orange"
        else:
            self.color_number = 0 #色定義前にnumber +=1を指定しているため0に戻させる
            self.color = "black"

    def block_collision(self):
        collided_block = None
        max_area = 0
        for block in self.block_object_list:
            #baallとblockとの当たった領域の座標を取得
            collision_rect = self.ball.getCollisionCoords(block)
            if collision_rect is not None:
                #当たった場合
                #当たった領域の面積を計算
                x1, y1, x2, y2 = collision_rect
                area = (x2 - x1)* (y2 - y1)
                if area > max_area:
                    max_area = area
                    #一番大きく当たったブロックを覚えておく
                    collided_block = block
        if collided_block is not None:
            self.ball.reflect(collided_block)
            self.block_object_list.remove(collided_block)
            #print(self.block_object_list)

class Block():
    def __init__(self, canvas, block_x, block_y, block_half_length, block_half_height, st, color, ball_x, ball_y, ball_r, ball_vx, ball_vy):
        self.canvas = canvas
        self.block_x = block_x
        self.block_y = block_y
        self.block_half_length = block_half_length
        self.block_half_height = block_half_height
        self.st = st
        self.color = color
        self.ball_x = ball_x
        self.ball_y = ball_y
        self.ball_r = ball_r
        self.ball_vx = ball_vx
        self.ball_vy = ball_vy

    def getCoords(self):
        return (self.block_x - self.block_half_length, self.block_y - self.block_half_height, self.block_x + self.block_half_length, self.block_y + self.block_half_height)

    def createBlock(self, ball_x, ball_y, ball_vx, ball_vy):
        #print('createBlock')
        self.ball_x = ball_x
        self.ball_y = ball_y
        self.ball_vx = ball_vx
        self.ball_vy = ball_vy
        if self.st:
            self.canvas.create_rectangle(
                self.block_x - self.block_half_length,
                self.block_y - self.block_half_height,
                self.block_x + self.block_half_length,
                self.block_y + self.block_half_height,
                fill = self.color
                )
        #ブロックとボールのぶつかり判定及びぶつかった時のブロックの処理
        #上下にぶつかったときの判定
        #ボールがブロックの縦方向にある、x軸の範囲内にある時
        if (self.ball_x >= self.block_x - self.block_half_length and self.ball_x <= self.block_x + self.block_half_length):
            #ボールがブロックの下にある場合
            if(self.ball_y >= self.block_y + self.block_half_height):
                if (self.ball_y - self.ball_r <= self.block_y + self.block_half_height) and self.st:
                    self.st = 0
            elif (self.ball_y <= self.block_y - self.block_half_height):
                #ボールがブロックの上にある場合
                if (self.ball_y + self.ball_r >= self.block_y - self.block_half_height) and self.st:
                    self.st = 0
        elif (self.ball_y >= self.block_y - self.block_half_height and self.ball_y <= self.block_y + self.block_half_height):
        #ボールが左右に当たった時の判定
            if (self.ball_x <= self.block_x - self.block_half_length):
                #ボールが左から当たった場合の判定
                if (self.ball_x + self.ball_r >= self.block_x - self.block_half_length) and self.st:
                    self.st = 0
            elif (self.ball_x >= self.block_x + self.block_half_length):
                #ボールが右から当たった時の判定
                if self.ball_x - self.ball_r <= self.block_x + self.block_half_length and self.st:
                    self.st = 0

class Ball():
    def __init__(self, canvas, ball_x, ball_y, ball_r, ball_vx, ball_vy, rack_x, rack_y, rack_half_length, rack_half_height, can_padx, can_pady, can_width, can_height):
        self.canvas = canvas
        self.ball_x = ball_x
        self.ball_y = ball_y
        self.ball_r = ball_r
        self.ball_vx = ball_vx #ボールのx軸方向への速度
        self.ball_vy = ball_vy #y軸方向への速度
        self.rack_x = rack_x
        self.rack_y = rack_y
        self.rack_half_length = rack_half_length
        self.rack_half_height = rack_half_height
        self.can_padx = can_padx
        self.can_pady = can_pady
        self.can_width = can_width
        self.can_height = can_height

    def createBall(self, rack_x, rack_y):
        #print('createBall')
        #print('self.ball_x, ball_y',self.ball_x, self.ball_y,  'self.ball_vx, self.ball_vy',self.ball_vx, self.ball_vy, 'self.rack_x', self.rack_x, 'self.rack_y', self.rack_y)
        self.canvas.create_oval(
            self.ball_x - self.ball_r,
            self.ball_y - self.ball_r,
            self.ball_x +  self.ball_r,
            self.ball_y + self.ball_r,
            fill = "#5b5b5b"
            )

        #ボールを動かす ボールの座標を遷移させていく
        self.ball_x += self.ball_vx
        self.ball_y += self.ball_vy
        self.rack_x = rack_x
        self.rack_y = rack_y
        #ボールが壁にぶつかる時の判定
        if self.ball_x - self.ball_r <= 0 and self.ball_vx <= 0:
            self.ball_vx *= -1 #壁にぶつかった時速度を*-1して逆向きにする
        elif self.ball_x + self.ball_r >= self.can_padx + self.can_width and self.ball_vx >= 0:
            self.ball_vx *= -1
            #self.ball_x = self.can_padx + self.can_width
        if self.ball_y - self.ball_r <= 0 and self.ball_vy <= 0:
            self.ball_vy *= -1 #ボールが天井にぶつかった時　反射する
        #ボールが底に着いた時の処理
        if self.ball_y + self.ball_r >= self.can_height + self.can_pady and self.ball_vy > 0:
            self.ball_vy *= -1 #ボールが底についた時　反射する
            #ここでself.gameOver()を入れてもここはボールクラスの中なので起動しない
        #ボールがラケットにぶつかったときの判定及び処理
        #ボールが上からラケットにぶつかる判定
        if self.ball_y <= self.rack_y:
            if (self.ball_x >= self.rack_x - self.rack_half_length and self.ball_x <= self.rack_x + self.rack_half_length) and self.ball_y + self.ball_r >= self.rack_y - self.rack_half_height and self.ball_vy > 0:
                self.ball_vy *= -1
        #ボールが下からラケットにぶつかる判定
        if self.ball_y > self.rack_y:
            if (self.ball_x >= self.rack_x - self.rack_half_length and self.ball_x <= self.rack_x + self.rack_half_length) and self.ball_y - self.ball_r <= self.rack_y + self.rack_half_height and self.ball_vy < 0 and 2*self.ball_r < (self.can_height - self.rack_y + self.rack_half_height):
                self.ball_vy *= -1
        #ボールが横からラケットにぶつかる判定 まず高さがラケットと同程度の高さにある判定
        if (self.ball_y > self.rack_y - self.rack_half_height and self.ball_y <= self.rack_y + self.rack_half_height):
            #ボールがラケットの左にある判定
            if (self.ball_x <= self.rack_x):
                #左からぶつかる判定
                if (self.ball_x + self.ball_r >= self.rack_x - self.rack_half_length) and self.ball_vx > 0:
                    self.ball_vx *= -1
            #ボールがラケットの右側にある判定
            elif (self.ball_x >= self.rack_x):
                #右からぶつかる判定
                if (self.ball_x - self.ball_r <= self.rack_x + self.rack_half_length) and self.ball_vx < 0:
                    self.ball_vx *= -1

    def getCoords(self):
        return (self.ball_x - self.ball_r, self.ball_y - self.ball_r, self.ball_x + self.ball_r, self.ball_y + self.ball_r)

    def getCollisionCoords(self, object):
        #オブジェクトと当たった領域の座標の取得
        #各オブジェクトの座標を取得
        ball_x1, ball_y1, ball_x2, ball_y2 = self.getCoords()
        object_x1, object_y1, object_x2, object_y2 = object.getCoords()
        #新しい矩形の座標を取得
        x1 = max(ball_x1, object_x1)
        y1 = max(ball_y1, object_y1)
        x2 = min(ball_x2, object_x2)
        y2 = min(ball_y2, object_y2)
        if x1 < x2 and y1 < y2:
            #始点が終点より左上にある
            #当たった領域の左上座標と右上座標を返却
            return (x1, y1, x2, y2)
        else:
            #当たってない場合Noneを返却
            return None

    def reflect(self, object):
        #オブジェクトの座標を取得
        object_x1, object_y1, object_x2, object_y2 = object.getCoords()
        x1, y1, x2, y2 = self.getCollisionCoords(object)
        if self.ball_vx < 0:
            #ボールが左方向に移動中
            if x2 == object_x2:
                self.ball_vx *= -1
        else:
            if x1 == object_x1:
                self.ball_vx *= -1
        if self.ball_vy < 0:
            #ボールが上方向に移動中
            if y2 == object_y2:
                self.ball_vy *= -1
        else:
            if y1 == object_y1:
                self.ball_vy *= -1
class Racket():
    def __init__(self, canvas, rack_x, rack_y, rack_half_length, rack_half_height, keyPress_R, keyPress_L, keyPress_U, keyPress_D, can_width, can_padx):
        self.can = canvas
        self.rack_x = rack_x
        self.rack_y = rack_y
        self.rack_half_length = rack_half_length
        self.rack_half_height = rack_half_height
        self.keyPress_R = keyPress_R
        self.keyPress_L = keyPress_L
        self.keyPress_U = keyPress_U
        self.keyPress_D = keyPress_D
        self.can_width = can_width
        self.can_padx = can_padx

    def createRacket(self):
        #print('createRacket')
        self.can.create_rectangle(
            self.rack_x - self.rack_half_length,
            self.rack_y - self.rack_half_height,
            self.rack_x + self.rack_half_length,
            self.rack_y + self.rack_half_height,
            fill = "white"
            )

if __name__ ==  "__main__":
    root = tk.Tk()
    app = Application(master = root)
    app.mainloop()
