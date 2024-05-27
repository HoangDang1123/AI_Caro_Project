from PIL import Image, ImageTk
from tkinter import *
from time import *
import tkinter as tk
import sys
import time
import math
import numpy as np
import random
import asyncio

AI_turn = False

class Board():
    def __init__(self):
        self.patterns = {
            '11111': 30000000,
            '22222': -30000000,
            '011110': 20000000,
            '022220': -20000000,
            '011112': 50000,
            '211110': 50000,
            '022221': -50000,
            '122220': -50000,
            '01110': 30000,
            '02220': -30000,
            '011010': 15000,
            '010110': 15000,
            '022020': -15000,
            '020220': -15000,
            '001112': 2000,
            '211100': 2000,
            '002221': -2000,
            '122200': -2000,
            '211010': 2000,
            '210110': 2000,
            '010112': 2000,
            '011012': 2000,
            '122020': -2000,
            '120220': -2000,
            '020221': -2000,
            '022021': -2000,
            '01100': 500,
            '00110': 500,
            '02200': -500,
            '00220': -500
        }
    
    # Kiểm tra thắng
    def win_check(self, Piece_Number, Piece_Colour, board):
        point = self.points_check(board, Piece_Number)
        if point == 30000000:
            Winner = Piece_Colour
            return Winner
        
    def btsConvert(self, board, player):
        temp_board = np.array(board)
        
        cList, rList, dList = [], [], []
        board_col = len(temp_board[0])
        
        bdiag = [temp_board.diagonal(i) for i in range(board_col - 5, - board_col + 4, -1)]
        fdiag = [temp_board[::-1, :].diagonal(i) for i in range(board_col - 5, - board_col + 4, -1)]
        
        for dgd in bdiag:
            bdiagVals = ""
            for point in dgd:
                if point == 0:
                    bdiagVals += "0"
                elif point == player:
                    bdiagVals += "1"
                else:
                    bdiagVals += "2"
            dList.append(bdiagVals)
            
        for dgu in fdiag:
            fdiagVals = ""
            for point in dgu:
                if point == 0:
                    fdiagVals += "0"
                elif point == player:
                    fdiagVals += "1"
                else:
                    fdiagVals += "2"
            dList.append(fdiagVals)
            
        boardT = temp_board.copy().transpose()
        
        for col in boardT:
            colVals = ""
            for point in col:
                if point == 0:
                    colVals += "0"
                elif point == player:
                    colVals += "1"
                else:
                    colVals += "2"
            cList.append(colVals)
            
        for row in board:
            rowVals = ""
            for point in row:
                if point == 0:
                    rowVals += "0"
                elif point == player:
                    rowVals += "1"
                else:
                    rowVals += "2"
            rList.append(rowVals)
            
        return dList+cList+rList

    def points_check(self, board, player):  # evaluates
        val = 0
        player1StrArr = self.btsConvert(board, player)
        for i in range(len(player1StrArr)):
            len1 = len(player1StrArr[i])
            for j in range(len1):
                n = j+5
                if(n <= len1):
                    st = player1StrArr[i][j:n]
                    if st in self.patterns:
                        val = max(val, self.patterns[st])
            for j in range(len1):
                n = j+6
                if(n <= len1):
                    st = player1StrArr[i][j:n]
                    if st in self.patterns:
                        val = max(val, self.patterns[st])
        return val
    
    def points(self, board, player):  # evaluates
        val = 0
        player1StrArr = self.btsConvert(board, player)
        for i in range(len(player1StrArr)):
            len1 = len(player1StrArr[i])
            for j in range(len1):
                n = j+5
                if(n <= len1):
                    st = player1StrArr[i][j:n]
                    if st in self.patterns:
                        val += self.patterns[st]
            for j in range(len1):
                n = j+6
                if(n <= len1):
                    st = player1StrArr[i][j:n]
                    if st in self.patterns:
                        val += self.patterns[st]
        return val
    
class Algorithms():
    b = Board()
    def __init__(self):
        self.MAX, self.MIN = math.inf, -math.inf
        self.save_point = 0
    
    def getCoordsAround(self, board):
        temp_board = np.array(board)
        board_size = len(temp_board)
        outTpl = np.nonzero(temp_board)  # return tuple of all non zero points on board
        potentialValsCoord = {}

        for i in range(len(outTpl[0])):
            y = outTpl[0][i]
            x = outTpl[1][i]

            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    new_x, new_y = x + dx, y + dy
                    if 0 <= new_x < board_size and 0 <= new_y < board_size and temp_board[new_y][new_x] == 0:
                        potentialValsCoord[(new_x, new_y)] = 1

        finalValsX, finalValsY = [], []
        for key in potentialValsCoord:
            finalValsY.append(key[1])
            finalValsX.append(key[0])
        
        return finalValsX, finalValsY

    def getRandomMove(self, board):
        global AI_turn
        boardSize = len(board)
        ctr = 0
        idx = boardSize//2
        while ctr < (idx/2):
            if board[idx+ctr][idx+ctr] == 0:
                AI_turn = False
                return idx+ctr, idx+ctr
            elif board[idx+ctr][idx-ctr] == 0:
                AI_turn = False
                return idx+ctr, idx-ctr
            elif board[idx+ctr][idx] == 0:
                AI_turn = False
                return idx+ctr, idx
            elif board[idx][idx+ctr] == 0:
                AI_turn = False
                return idx, idx+ctr
            elif board[idx][idx-ctr] == 0:
                AI_turn = False
                return idx, idx-ctr
            elif board[idx-ctr][idx] == 0:
                AI_turn = False
                return idx-ctr, idx
            elif board[idx-ctr][idx-ctr] == 0:
                AI_turn = False
                return idx-ctr, idx-ctr
            elif board[idx-ctr][idx+ctr] == 0:
                AI_turn = False
                return idx-ctr, idx+ctr
            ctr += 1
        for i in range(boardSize):
            for j in range(boardSize):
                if board[i][j] == 0:
                    AI_turn = False
                    return i, j

    def otherPlayerStone(self, player):
        return 2 if player==1 else 1

    def greedyAlgorithm(self, board, player):
        bestMoveRow = bestMoveCol = -1
        bestOtherMoveRow = bestOtherMoveCol = -1
        
        mostPoints = float('-inf')
        mostOtherPoints = float('-inf')
        
        potentialValsX, potentialValsY = self.getCoordsAround(board)
        for i in range(len(potentialValsX)):
            if board[potentialValsY[i]][potentialValsX[i]] == 0:
                board[potentialValsY[i]][potentialValsX[i]] = player
                movePoints = self.b.points(board, player)

                board[potentialValsY[i]][potentialValsX[i]] = self.otherPlayerStone(player)
                moveOtherPoints = self.b.points(board, self.otherPlayerStone(player))
                
                board[potentialValsY[i]][potentialValsX[i]] = 0
                
                if moveOtherPoints > mostOtherPoints:
                    bestOtherMoveRow = potentialValsY[i]
                    bestOtherMoveCol = potentialValsX[i]
                    mostOtherPoints = moveOtherPoints
                
                if movePoints > mostPoints:
                    bestMoveRow = potentialValsY[i]
                    bestMoveCol = potentialValsX[i]
                    mostPoints = movePoints

        global AI_turn
        AI_turn = False

        if mostOtherPoints >= mostPoints:
            return bestOtherMoveRow, bestOtherMoveCol
        else:
            return bestMoveRow, bestMoveCol

    def alpha_beta(self, board, isMaximizer, depth, alpha, beta, player):  # alpha, beta
        point = self.b.points(board, player)
        
        if depth == 2:
            return point
        
        if isMaximizer:  # THE MAXIMIZER
            best = self.MIN
            potentialValsX, potentialValsY = self.getCoordsAround(board)
            for i in range(len(potentialValsX)):
                if board[potentialValsY[i]][potentialValsX[i]] == 0:
                    board[potentialValsY[i]][potentialValsX[i]] = player
                    score = self.alpha_beta(board, False, depth+1, alpha, beta, player)
                    best = max(best, score)
                    alpha = max(alpha, best)  # best AI Opponent move
                    board[potentialValsY[i]][potentialValsX[i]] = 0  # undoing
                    if beta <= alpha:
                        break
            return best
        else:  # THE MINIMIZER
            best = self.MAX
            potentialValsX, potentialValsY = self.getCoordsAround(board)
            for i in range(len(potentialValsX)):
                if board[potentialValsY[i]][potentialValsX[i]] == 0:
                    otherplayer = self.otherPlayerStone(player)
                    board[potentialValsY[i]][potentialValsX[i]] = otherplayer
                    score = self.alpha_beta(board, True, depth+1, alpha, beta, player)
                    best = min(best, score)
                    beta = min(beta, best)  # best AI Opponent move
                    board[potentialValsY[i]][potentialValsX[i]] = 0  # undoing
                    if beta <= alpha:
                        break
            return best

    def alpha_beta_computer(self, board, isComputerFirst):
        mostPoints = float('-inf')
        alpha,beta = self.MIN, self.MAX
        bestMoveRow = bestMoveCol = -1
        
        potentialValsX, potentialValsY = self.getCoordsAround(board)
        for i in range(len(potentialValsX)):
            if board[potentialValsY[i]][potentialValsX[i]] == 0:
                board[potentialValsY[i]][potentialValsX[i]] = isComputerFirst
                movePoints = max(mostPoints, self.alpha_beta(
                    board, False, 1, alpha, beta, isComputerFirst))
                alpha = max(alpha, movePoints)
                board[potentialValsY[i]][potentialValsX[i]] = 0
                if beta <= alpha:
                    break
                if movePoints > mostPoints:
                    bestMoveRow = potentialValsY[i]
                    bestMoveCol = potentialValsX[i]
                    mostPoints = movePoints
                    if movePoints >= 20000000:
                        break
                elif movePoints == mostPoints:
                    rannum = random.randint(0, 1)
                    if rannum == 1:
                        bestMoveRow = potentialValsY[i]
                        bestMoveCol = potentialValsX[i]
                        mostPoints = movePoints
                        if movePoints >= 20000000:
                            break

        global AI_turn
        AI_turn = False
        return bestMoveRow, bestMoveCol
    
    def minimax(self, board, isMaximizer, depth, player):  # alpha, beta
        point = self.b.points(board, player)
        
        if depth == 2:
            return point
        
        if isMaximizer:  # THE MAXIMIZER
            best = self.MIN
            potentialValsX, potentialValsY = self.getCoordsAround(board)
            for i in range(len(potentialValsX)):
                if board[potentialValsY[i]][potentialValsX[i]] == 0:
                    board[potentialValsY[i]][potentialValsX[i]] = player
                    score = self.minimax(board, False, depth+1, player)
                    best = max(best, score)
                    board[potentialValsY[i]][potentialValsX[i]] = 0  # undoing
            return best
        else:  # THE MINIMIZER
            best = self.MAX
            potentialValsX, potentialValsY = self.getCoordsAround(board)
            for i in range(len(potentialValsX)):
                if board[potentialValsY[i]][potentialValsX[i]] == 0:
                    otherplayer = self.otherPlayerStone(player)
                    board[potentialValsY[i]][potentialValsX[i]] = otherplayer
                    score = self.minimax(board, True, depth+1, player)
                    best = min(best, score)
                    board[potentialValsY[i]][potentialValsX[i]] = 0  # undoing
            return best

    def minimax_computer(self, board, isComputerFirst):
        mostPoints = float('-inf')
        bestMoveRow = bestMoveCol = -1
        
        potentialValsX, potentialValsY = self.getCoordsAround(board)
        for i in range(len(potentialValsX)):
            if board[potentialValsY[i]][potentialValsX[i]] == 0:
                board[potentialValsY[i]][potentialValsX[i]] = isComputerFirst
                movePoints = max(mostPoints, self.minimax(
                    board, False, 1, isComputerFirst))
                board[potentialValsY[i]][potentialValsX[i]] = 0
                if movePoints > mostPoints:
                    bestMoveRow = potentialValsY[i]
                    bestMoveCol = potentialValsX[i]
                    mostPoints = movePoints
                    if movePoints >= 20000000:
                        break
                elif movePoints == mostPoints:
                    rannum = random.randint(0, 1)
                    if rannum == 1:
                        bestMoveRow = potentialValsY[i]
                        bestMoveCol = potentialValsX[i]
                        mostPoints = movePoints
                        if movePoints >= 20000000:
                            break

        global AI_turn
        AI_turn = False
        return bestMoveRow, bestMoveCol
    
    def mcts(self, board, isMaximizer, depth, player):  # alpha, beta
        point = self.b.points(board, player)
        
        if depth == 2:
            return point
        
        if isMaximizer:  # THE MAXIMIZER
            best = self.MIN
            potentialValsX, potentialValsY = self.getCoordsAround(board)
            self.save_point += len(potentialValsX)
            for i in range(len(potentialValsX)):
                if board[potentialValsY[i]][potentialValsX[i]] == 0:
                    board[potentialValsY[i]][potentialValsX[i]] = player
                    score = self.mcts(board, False, depth+1, player)
                    best = max(best, score)
                    board[potentialValsY[i]][potentialValsX[i]] = 0  # undoing
            return best
        else:  # THE MINIMIZER
            best = self.MAX
            potentialValsX, potentialValsY = self.getCoordsAround(board)
            self.save_point += len(potentialValsX)
            for i in range(len(potentialValsX)):
                if board[potentialValsY[i]][potentialValsX[i]] == 0:
                    otherplayer = self.otherPlayerStone(player)
                    board[potentialValsY[i]][potentialValsX[i]] = otherplayer
                    score = self.mcts(board, True, depth+1, player)
                    best = min(best, score)
                    board[potentialValsY[i]][potentialValsX[i]] = 0  # undoing
            return best

    def mcts_computer(self, board, isComputerFirst):
        mostPoints = float('-inf')
        bestMoveRow = bestMoveCol = -1
        
        potentialValsX, potentialValsY = self.getCoordsAround(board)
        save_x = 0
        save_x += len(potentialValsX)
        for i in range(len(potentialValsX)):
            if board[potentialValsY[i]][potentialValsX[i]] == 0:
                board[potentialValsY[i]][potentialValsX[i]] = isComputerFirst
                self.save_point = 0
                movePoints = self.mcts(board, False, 1, isComputerFirst)

                ucb = movePoints / self.save_point + 1.4 * math.sqrt(math.log(save_x) / self.save_point)
                board[potentialValsY[i]][potentialValsX[i]] = 0
                if ucb > mostPoints:
                    bestMoveRow = potentialValsY[i]
                    bestMoveCol = potentialValsX[i]
                    mostPoints = ucb
                    if ucb >= 20000000:
                        break
                elif ucb == mostPoints:
                    rannum = random.randint(0, 1)
                    if rannum == 1:
                        bestMoveRow = potentialValsY[i]
                        bestMoveCol = potentialValsX[i]
                        mostPoints = ucb
                        if ucb >= 20000000:
                            break

        global AI_turn
        AI_turn = False
        return bestMoveRow, bestMoveCol

class GUI():
    b = Board()
    m = Algorithms()
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("ĐỒ ÁN HỌC PHẦN - LẬP TRÌNH GAME CỜ CARO")
        self.background = tk.Canvas(
            self.window,
            width = self.window.winfo_screenwidth(),
            height = self.window.winfo_screenheight(),
            background= "#b69b4c"
            )
        self.background.pack()
        self.window.state("zoomed")

        #Board Size
        self.board_size = 19
        self.frame_gap = 25
        self.width = 0.52 * self.window.winfo_screenwidth()
        self.height = 0.93 * self.window.winfo_screenheight()
        
        self.board_x1 = self.width / 10
        self.board_y1 = self.height / 10
        self.board_gap_x = (self.width - self.board_x1 * 2) / (self.board_size - 1)
        self.board_gap_y = (self.height - self.board_y1 * 2) / (self.board_size - 1)
        
        #Chess Piece
        self.chess_radius = (self.board_gap_x * (9 / 10)) / 2
        
        #Turn
        self.turn_num = 1
        self.turn = "white"
        self.winner = None
        self.circles = []
        self.texts = []

        #Cord List
        self.black_cord_picked_x = []
        self.black_cord_picked_y = []
        self.white_cord_picked_x = []
        self.white_cord_picked_y = []

        #Click Detection Cord
        self.game_cord_x = []
        self.game_cord_y = []
        self.actual_cord_x_1 = []
        self.actual_cord_y_1 = []
        self.actual_cord_x_2 = []
        self.actual_cord_y_2 = []
        
        #2D Board List
        self.board = []
        for i in range(self.board_size):
            self.board.append([0] * (self.board_size))
            
        self.unfilled = 0
        self.white_piece = 1
        self.black_piece = 2
        
        self.playwith = False
        self.gofirst = False
        self.AIfirst = False
        
        self.AI = False
        self.ab_algorithm = False
        self.g_algorithm = False
        self.mm_algorithm = False
        self.mcts_algorithm = False
        
        #Fills Empty List
        for z in range(1, self.board_size + 1):
            for i in range(1, self.board_size + 1):
                self.game_cord_x.append(z)
                self.game_cord_y.append(i)
                self.actual_cord_x_1.append((z - 1) * self.board_gap_x + self.board_x1 - self.chess_radius)
                self.actual_cord_y_1.append((i - 1) * self.board_gap_y + self.board_y1 - self.chess_radius)
                self.actual_cord_x_2.append((z - 1) * self.board_gap_x + self.board_x1 + self.chess_radius)
                self.actual_cord_y_2.append((i - 1) * self.board_gap_y + self.board_y1 + self.chess_radius)
        
        self.introduction()
        self.best_line()
        self.button()
        self.game_board()
        self.turn_label()
        
        self.background.bind("<Button-1>", self.mouse_click)
        self.click_cord = [None, None]
        
    def mainloop(self):
        self.window.mainloop()
        
    def introduction(self):
        # Label tiêu đề
        self.title = tk.Label(self.window,
                              text = "ĐỒ ÁN CUỐI KỲ",
                              font = ("Arial", 20, "bold"),
                              fg = "navy blue",
                              bg = "#b69b4c")
        self.title.place(x = self.board_x1 + self.frame_gap + self.board_gap_x * (self.board_size - 1) + 0.1875 * self.window.winfo_screenwidth(),
                         y = self.board_y1 - self.frame_gap - 0.028 * self.window.winfo_screenheight())

        # Label tên lớp
        self.class_name = tk.Label(self.window,
                                   text = "Lớp: ARIN330585_03CLC",
                                   font = ("Arial", 12, "bold"),
                                   fg = "navy blue",
                                   bg = "#b69b4c")
        self.class_name.place(x = self.board_x1 + self.frame_gap + self.board_gap_x * (self.board_size - 1) + 0.078125 * self.window.winfo_screenwidth(),
                              y = self.board_y1 - self.frame_gap + 0.015 * self.window.winfo_screenheight())

        # Label tên thành viên
        self.member_name = tk.Label(self.window,
                                    text = "Tên thành viên:",
                                    font = ("Arial", 12, "bold"),
                                    fg = "navy blue",
                                    bg = "#b69b4c")
        self.member_name.place(x = self.board_x1 + self.frame_gap + self.board_gap_x * (self.board_size - 1) + float(150 / 1920) * self.window.winfo_screenwidth(),
                               y = self.board_y1 - self.frame_gap + float(50 / 1080) * self.window.winfo_screenheight())

        # Label tên thành viên 1
        self.member_1 = tk.Label(self.window,
                                 text = "Đỗ Anh Khoa          -      21110208",
                                 font = ("Arial", 12, "bold"),
                                 fg = "navy blue",
                                 bg = "#b69b4c")
        self.member_1.place(x = self.board_x1 + self.frame_gap + self.board_gap_x * (self.board_size - 1) + float(420 / 1920) * self.window.winfo_screenwidth(),
                            y = self.board_y1 - self.frame_gap + float(50 / 1080) * self.window.winfo_screenheight(),)

        # Label tên thành viên 2
        self.member_2 = tk.Label(self.window, text = "Đào Hoàng Đăng    -      21110163",
                                 font = ("Arial", 12, "bold"),
                                 fg = "navy blue",
                                 bg = "#b69b4c")
        self.member_2.place(x = self.board_x1 + self.frame_gap + self.board_gap_x * (self.board_size - 1) + float(420 / 1920) * self.window.winfo_screenwidth(),
                            y = self.board_y1 - self.frame_gap + float(90 / 1080) * self.window.winfo_screenheight(),)

        # Label tên thành viên 3
        self.member_3 = tk.Label(self.window, text = "Nguyễn Anh Hào    -      21110823",
                                 font = ("Arial", 12, "bold"),
                                 fg = "navy blue",
                                 bg = "#b69b4c")
        self.member_3.place(x = self.board_x1 + self.frame_gap + self.board_gap_x * (self.board_size - 1) + float(420 / 1920) * self.window.winfo_screenwidth(),
                            y = self.board_y1 - self.frame_gap + float(130 / 1080) * self.window.winfo_screenheight())
        
    def best_line(self):
        # Frame
        self.background.create_rectangle(self.board_x1 + self.frame_gap + self.board_gap_y * (self.board_size - 1) + float(100 / 1920) * self.window.winfo_screenwidth(),
                                         self.board_y1 - self.frame_gap + float(170 / 1080) * self.window.winfo_screenheight(),
                                         self.window.winfo_screenwidth() - float(100 / 1920) * self.window.winfo_screenwidth(),
                                         self.board_y1 + self.frame_gap + self.board_gap_y * (self.board_size - 1) - float(510 / 1080) * self.window.winfo_screenheight(),
                                         width = 3)
        
        # Label
        self.best_line_label = tk.Label(self.window,
                                        text = "BEST LINE",
                                        font = ("Arial", 12, "bold"),
                                        fg = "navy blue",
                                        bg = "#b69b4c")
        self.best_line_label.place(x = self.board_x1 + self.frame_gap + self.board_gap_x * (self.board_size - 1) + float(420 / 1920) * self.window.winfo_screenwidth(),
                                   y = self.board_y1 - self.frame_gap + float(180 / 1080) * self.window.winfo_screenheight())

        # Text
        self.best_line_text = tk.Text(self.window,
                                      bg = "#b69b4c", width = 75,
                                      height =5,
                                      borderwidth = 3,
                                      state = tk.DISABLED)
        self.best_line_text.place(x = self.board_x1 + self.frame_gap + self.board_gap_x * (self.board_size - 1) + float(120 / 1920) * self.window.winfo_screenwidth(),
                                  y = self.board_y1 - self.frame_gap + float(210 / 1080) * self.window.winfo_screenheight())
        
    def button(self):
        # Frame
        self.background.create_rectangle(self.board_x1 + self.frame_gap + self.board_gap_x * (self.board_size - 1) + float(100 / 1920) * self.window.winfo_screenwidth(),
                           self.board_y1 - self.frame_gap + float(370 / 1080) * self.window.winfo_screenheight(),
                           self.window.winfo_screenwidth() - float(100 / 1920) * self.window.winfo_screenwidth(),
                           self.board_y1 + self.frame_gap + self.board_gap_y * (self.board_size - 1),
                           fill = "silver",
                           outline = "silver")

        # Frame các nút điều khiển chính
        self.background.create_rectangle(self.board_x1 + self.frame_gap + self.board_gap_x * (self.board_size - 1) + float(130 / 1920) * self.window.winfo_screenwidth(),
                                         self.board_y1 - self.frame_gap + float(400 / 1080) * self.window.winfo_screenheight(),
                                         self.board_x1 + self.frame_gap + self.board_gap_x * (self.board_size - 1) + float(480 / 1920) * self.window.winfo_screenwidth(),
                                         self.board_y1 + self.frame_gap + self.board_gap_y * (self.board_size - 1) - float(260 / 1080) * self.window.winfo_screenheight(),
                                         fill = "gray",
                                         outline = "gray")
        # Button bắt đầu chơi
        self.start_button = tk.Button(self.window,
                                      text = "Start",
                                      font = "Helvetica 14 bold",
                                      command = self.start,
                                      bg = "gray",
                                      fg = "black")
        self.start_button.place(x = self.board_x1 + self.frame_gap + self.board_gap_x * (self.board_size - 1) + float(155 / 1920) * self.window.winfo_screenwidth(),
                                y = self.board_y1 - self.frame_gap + float(425 / 1080) * self.window.winfo_screenheight(),
                                width = self.chess_radius * 7,
                                height = self.chess_radius * 3)
        # Button bát đầu chơi lại
        self.restart_button = tk.Button(self.window,
                                        text = "Restart",
                                        font = "Helvetica 14 bold",
                                        command = None,
                                        bg = "gray",
                                        fg = "black")
        self.restart_button.place(x = self.board_x1 + self.frame_gap + self.board_gap_x * (self.board_size - 1) + float(315 / 1920) * self.window.winfo_screenwidth(),
                                y = self.board_y1 - self.frame_gap + float(425 / 1080) * self.window.winfo_screenheight(),
                                width = self.chess_radius * 7,
                                height = self.chess_radius * 3)
        # Button quay lại lượt trước
        self.undo_button = tk.Button(self.window,
                                        text = "Undo",
                                        font = "Helvetica 14 bold",
                                        command = self.undo,
                                        bg = "gray",
                                        fg = "black")
        self.undo_button.place(x = self.board_x1 + self.frame_gap + self.board_gap_x * (self.board_size - 1) + float(155 / 1920) * self.window.winfo_screenwidth(),
                                y = self.board_y1 - self.frame_gap + float(505 / 1080) * self.window.winfo_screenheight(),
                                width = self.chess_radius * 7,
                                height = self.chess_radius * 3)
        # Button thoát game
        self.exit_button = tk.Button(self.window,
                                        text = "Exit",
                                        font = "Helvetica 14 bold",
                                        command = self.exit,
                                        bg = "gray",
                                        fg = "black")
        self.exit_button.place(x = self.board_x1 + self.frame_gap + self.board_gap_x * (self.board_size - 1) + float(315 / 1920) * self.window.winfo_screenwidth(),
                                y = self.board_y1 - self.frame_gap + float(505 / 1080) * self.window.winfo_screenheight(),
                                width = self.chess_radius * 7,
                                height = self.chess_radius * 3)
        
        # Frame các nút chọn chế độ chơi
        self.background.create_rectangle(self.window.winfo_screenwidth() - float(480 / 1920) * self.window.winfo_screenwidth(),
                                         self.board_y1 - self.frame_gap + float(400 / 1080) * self.window.winfo_screenheight(),
                                         self.window.winfo_screenwidth() - float(130 / 1920) * self.window.winfo_screenwidth(),
                                         self.board_y1 + self.frame_gap + self.board_gap_y * (self.board_size - 1) - float(260 / 1080) * self.window.winfo_screenheight(),
                                         fill = "gray",
                                         outline = "gray")
        # Button AI chơi với Người
        self.ai_human_button = tk.Button(self.window,
                               text = "AI - Human",
                               font = "Helvetica 14 bold",
                               command = self.set_AI,
                               bg = "gray",
                               fg = "black")
        self.ai_human_button.place(x = self.window.winfo_screenwidth() - float(455 / 1920) * self.window.winfo_screenwidth(),
                  y = self.board_y1 - self.frame_gap + float(425 / 1080) * self.window.winfo_screenheight(),
                  width = self.chess_radius * 15,
                  height = self.chess_radius * 3)
        # Button Người chơi với Người
        self.human_human_button = tk.Button(self.window,
                               text = "Human - Human",
                               font = "Helvetica 14 bold",
                               command = self.unset_AI,
                               bg = "gray",
                               fg = "black")
        self.human_human_button.place(x = self.window.winfo_screenwidth() - float(455 / 1920) * self.window.winfo_screenwidth(),
                  y = self.board_y1 - self.frame_gap + float(505 / 1080) * self.window.winfo_screenheight(),
                  width = self.chess_radius * 15,
                  height = self.chess_radius * 3)

        # Frame các nút chọn thuật toán
        self.background.create_rectangle(self.board_x1 + self.frame_gap + self.board_gap_x * (self.board_size - 1) + float(130 / 1920) * self.window.winfo_screenwidth(),
                                         self.board_y1 - self.frame_gap + float(615 / 1080) * self.window.winfo_screenheight(),
                                         self.board_x1 + self.frame_gap + self.board_gap_x * (self.board_size - 1) + float(480 / 1920) * self.window.winfo_screenwidth(),
                                         self.board_y1 + self.frame_gap + self.board_gap_y * (self.board_size - 1) - float(30 / 1080) * self.window.winfo_screenheight(),
                                         fill = "gray",
                                         outline = "gray")
        
        # Button thuật toán Alpha-Beta
        self.ab_algorithm_button = tk.Button(self.window, text = "Alpha-Beta", font = "Helvetica 14 bold", command = self.set_ab_algorithm, bg = "gray", fg = "black")
        self.ab_algorithm_button.place(x = self.board_x1 + self.frame_gap + self.board_gap_x * (self.board_size - 1) + float(155 / 1920) * self.window.winfo_screenwidth(),
                                y = self.board_y1 - self.frame_gap + float(650 / 1080) * self.window.winfo_screenheight(),
                                width = self.chess_radius * 7,
                                height = self.chess_radius * 3)
        # Button thuật toán Greedy
        self.g_algorithm_button = tk.Button(self.window, text = "Greedy", font = "Helvetica 14 bold", command = self.set_g_algorithm, bg = "gray", fg = "black")
        self.g_algorithm_button.place(x = self.board_x1 + self.frame_gap + self.board_gap_x * (self.board_size - 1) + float(315 / 1920) * self.window.winfo_screenwidth(),
                                y = self.board_y1 - self.frame_gap + float(650 / 1080) * self.window.winfo_screenheight(),
                                width = self.chess_radius * 7,
                                height = self.chess_radius * 3)
        
        # Button thuật toán Minimax
        self.mm_algorithm_button = tk.Button(self.window, text = "Minimax", font = "Helvetica 14 bold", command = self.set_mm_algorithm, bg = "gray", fg = "black")
        self.mm_algorithm_button.place(x = self.board_x1 + self.frame_gap + self.board_gap_x * (self.board_size - 1) + float(155 / 1920) * self.window.winfo_screenwidth(),
                                y = self.board_y1 - self.frame_gap + float(730 / 1080) * self.window.winfo_screenheight(),
                                width = self.chess_radius * 7,
                                height = self.chess_radius * 3)
        # Button thuật toán Monte Carlo Search Tree
        self.mcts_algorithm_button = tk.Button(self.window, text = "MCTS", font = "Helvetica 14 bold", command = self.set_mcts_algorithm, bg = "gray", fg = "black")
        self.mcts_algorithm_button.place(x = self.board_x1 + self.frame_gap + self.board_gap_x * (self.board_size - 1) + float(315 / 1920) * self.window.winfo_screenwidth(),
                                y = self.board_y1 - self.frame_gap + float(730 / 1080) * self.window.winfo_screenheight(),
                                width = self.chess_radius * 7,
                                height = self.chess_radius * 3)
        
        # Frame các nút chọn ai đi trước
        self.background.create_rectangle(self.window.winfo_screenwidth() - float(480 / 1920) * self.window.winfo_screenwidth(),
                                         self.board_y1 - self.frame_gap + float(615 / 1080) * self.window.winfo_screenheight(),
                                         self.window.winfo_screenwidth() - float(130 / 1920) * self.window.winfo_screenwidth(),
                                         self.board_y1 + self.frame_gap + self.board_gap_y * (self.board_size - 1) - float(30 / 1080) * self.window.winfo_screenheight(),
                                         fill = "gray",
                                         outline = "gray")
        # Button AI đánh trước
        self.ai_first_button = tk.Button(self.window,
                               text = "AI First",
                               font = "Helvetica 14 bold",
                               command = self.set_AI_turn,
                               bg = "gray",
                               fg = "black")
        self.ai_first_button.place(x = self.window.winfo_screenwidth() - float(455 / 1920) * self.window.winfo_screenwidth(),
                  y = self.board_y1 - self.frame_gap + float(650 / 1080) * self.window.winfo_screenheight(),
                  width = self.chess_radius * 15,
                  height = self.chess_radius * 3)
        # Button Người đánh trước
        self.human_first_button = tk.Button(self.window,
                               text = "Human First",
                               font = "Helvetica 14 bold",
                               command = self.unset_AI_turn,
                               bg = "gray",
                               fg = "black")
        self.human_first_button.place(x = self.window.winfo_screenwidth() - float(455 / 1920) * self.window.winfo_screenwidth(),
                  y = self.board_y1 - self.frame_gap + float(730 / 1080) * self.window.winfo_screenheight(),
                  width = self.chess_radius * 15,
                  height = self.chess_radius * 3)
        
    def set_AI(self):
        self.AI = True
        self.ai_human_button.config(bg = "white")
        self.human_human_button.config(bg = "gray")
        self.playwith = True
        
    def unset_AI(self):
        self.AI = False
        self.ai_human_button.config(bg = "gray")
        self.human_human_button.config(bg = "white")
        self.playwith = True
    
    def set_AI_turn(self):
        if self.AI == False:
            tk.messagebox.showerror("Error!!!","Please select AI vs Human!")
        else:
            global AI_turn
            AI_turn = True
            self.ai_first_button.config(bg = "white")
            self.human_first_button.config(bg = "gray")
            self.gofirst = True
            self.AIfirst = True
        
    def unset_AI_turn(self):
        if self.AI == False:
            tk.messagebox.showerror("Error!!!","Please select AI vs Human!")
        else:
            global AI_turn
            AI_turn = False
            self.ai_first_button.config(bg = "gray")
            self.human_first_button.config(bg = "white")
            self.gofirst = True
            self.AIfirst = False
        
    def set_ab_algorithm(self):
        if self.AI == False:
            tk.messagebox.showerror("Error!!!","Please select AI vs Human!")
        else:
            self.ab_algorithm = True
            self.g_algorithm = False
            self.mm_algorithm = False
            self.mcts_algorithm = False
            
            self.ab_algorithm_button.config(bg = "white")
            self.g_algorithm_button.config(bg = "gray")
            self.mm_algorithm_button.config(bg = "gray")
            self.mcts_algorithm_button.config(bg = "gray")

    def set_g_algorithm(self):
        if self.AI == False:
            tk.messagebox.showerror("Error!!!","Please select AI vs Human!")
        else:
            self.ab_algorithm = False
            self.g_algorithm = True
            self.mm_algorithm = False
            self.mcts_algorithm = False  
            
            self.ab_algorithm_button.config(bg = "gray")
            self.g_algorithm_button.config(bg = "white")
            self.mm_algorithm_button.config(bg = "gray")
            self.mcts_algorithm_button.config(bg = "gray")
            
    def set_mm_algorithm(self):
        if self.AI == False:
            tk.messagebox.showerror("Error!!!","Please select AI vs Human!")
        else:
            self.ab_algorithm = False
            self.g_algorithm = False
            self.mm_algorithm = True
            self.mcts_algorithm = False  
            
            self.ab_algorithm_button.config(bg = "gray")
            self.g_algorithm_button.config(bg = "gray")
            self.mm_algorithm_button.config(bg = "white")
            self.mcts_algorithm_button.config(bg = "gray")
            
    def set_mcts_algorithm(self):
        if self.AI == False:
            tk.messagebox.showerror("Error!!!","Please select AI vs Human!")
        else:
            self.ab_algorithm = False
            self.g_algorithm = False
            self.mm_algorithm = False
            self.mcts_algorithm = True  
            
            self.ab_algorithm_button.config(bg = "gray")
            self.g_algorithm_button.config(bg = "gray")
            self.mm_algorithm_button.config(bg = "gray")
            self.mcts_algorithm_button.config(bg = "white")
        
    def game_board(self):
        # Tạo bàn cờ
        self.background.create_rectangle(self.board_x1 - self.frame_gap,
                                         self.board_y1 - self.frame_gap,
                                         self.board_x1 + self.frame_gap + self.board_gap_x * (self.board_size - 1),
                                         self.board_y1 + self.frame_gap + self.board_gap_y * (self.board_size - 1),
                                         width = 3)
        
        letter = 64
        for f in range(self.board_size):
            self.background.create_line(self.board_x1,
                          self.board_y1 + f * self.board_gap_y,
                          self.board_x1 + self.board_gap_x * (self.board_size - 1),
                          self.board_y1 + f * self.board_gap_y)
            self.background.create_line(self.board_x1 + f * self.board_gap_x,
                          self.board_y1,
                          self.board_x1 + f * self.board_gap_x,
                          self.board_y1 + self.board_gap_y * (self.board_size - 1))

            self.background.create_text(self.board_x1 - self.frame_gap * 1.7,
                                        self.board_y1 + f * self.board_gap_y,
                                        text = chr(letter + 1),
                                        font = "Helvetica 10 bold",
                                        fill = "black")
            self.background.create_text(self.board_x1 + f * self.board_gap_x,
                                        self.board_y1 - self.frame_gap * 1.7,
                                        text = f + 1,
                                        font = "Helvetica 10 bold",
                                        fill = "black")
            letter += 1
    
    def turn_label(self):
        self.turn_label = tk.Label(self.window,
                                   text = "Turn = " + self.turn,
                                   font = "Helvetica 20 bold",
                                   fg = self.turn)
        self.turn_label.place(x = 100, y = self.window.winfo_height() - 100)
            
    def mouse_click(self, event):
        x_click = event.x
        y_click = event.y
        self.click_cord = self.piece_location(x_click, y_click)
        picked = self.valid_location(self.click_cord[0], self.click_cord[1])
        if picked:
            global AI_turn
            AI_turn = True
    
    # Tọa độ chấm caro
    def piece_location(self, x_click, y_click):    
        x = None
        y = None
        for i in range(len(self.actual_cord_x_1)):
            if x_click > self.actual_cord_x_1[i] and x_click < self.actual_cord_x_2[i]:
                x = self.game_cord_x[i]
            if y_click > self.actual_cord_y_1[i] and y_click < self.actual_cord_y_2[i]:
                y = self.game_cord_y[i]
        return x, y
    
    # Kiểm tra tọa độ hợp lệ
    def valid_location(self, x, y):
        if x == None or y == None:
            return False
        elif self.board[y - 1][x - 1] == 0:
            return True
        
    def create_circle(self, x, y, radius, count, width = 2):
        if count % 2 != 0:
            circle_id = self.background.create_oval(x - radius,
                                        y - radius,
                                        x + radius,
                                        y + radius,
                                        fill = "white",
                                        outline = "",
                                        width = width)
            text_id = self.background.create_text(x,
                                        y,
                                        text = count,
                                        fill = "black")
        else:
            circle_id = self.background.create_oval(x - radius,
                                        y - radius,
                                        x + radius,
                                        y + radius,
                                        fill = "black",
                                        outline = "",
                                        width = width)
            text_id = self.background.create_text(x,
                                        y,
                                        text = count,
                                        fill = "white")
        self.background.addtag_withtag("circle", circle_id)
        self.background.addtag_withtag("text", text_id)
        self.circles.append(circle_id)
        self.texts.append(text_id)
            
    def start(self):
        if self.playwith == False:
            tk.messagebox.showerror("Error!!!", "Please select AI vs Human or Human vs Human")
        else:
            if self.AI == True and self.gofirst == False:
                tk.messagebox.showerror("Error!!!", "Please select AI First or Human First")
            else:
                self.start_button.config(bg = "white")
                
                self.click_cord = [None, None]
                if(AI_turn):
                    self.piece_num = self.white_piece
                else:
                    self.piece_num = self.black_piece

                while self.winner == None:
                    #self.restart_button.config(command = self.restart)
                    
                    x = 0
                    y = 0
                    if(self.AI):
                        if(AI_turn):
                            if(self.ab_algorithm):
                                if self.turn_num <= 1:
                                    y, x = self.m.getRandomMove(self.board)
                                else:
                                    y, x = self.m.alpha_beta_computer(self.board, self.piece_num)
                            elif(self.g_algorithm):
                                if self.turn_num <= 1:
                                    y, x = self.m.getRandomMove(self.board)
                                else:
                                    y, x = self.m.greedyAlgorithm(self.board, self.piece_num)
                                    
                            elif(self.mm_algorithm):
                                if self.turn_num <= 1:
                                    y, x = self.m.getRandomMove(self.board)
                                else:
                                    y, x = self.m.minimax_computer(self.board, self.piece_num)
                                    
                            elif(self.mcts_algorithm):
                                if self.turn_num <= 1:
                                    y, x = self.m.getRandomMove(self.board)
                                else:
                                    y, x = self.m.mcts_computer(self.board, self.piece_num)
                            x += 1
                            y += 1
                        else:
                            self.background.update()
                            x = self.click_cord[0]
                            y = self.click_cord[1]
                    else:
                        self.background.update()
                        x = self.click_cord[0]
                        y = self.click_cord[1]
                        
                    picked = self.valid_location(x, y)
                    if picked:
                        self.create_circle(self.board_x1 + self.board_gap_x * (x - 1), self.board_y1 + self.board_gap_y * (y - 1), self.chess_radius, self.turn_num)
                        if self.turn_num % 2 == 1:
                            self.white_cord_picked_x.append(x)
                            self.white_cord_picked_y.append(y)
                            self.board[y - 1][x - 1] = self.white_piece
                            self.turn = "black"
                            
                        elif self.turn_num % 2 == 0:
                            self.black_cord_picked_x.append(x)
                            self.black_cord_picked_y.append(y)
                            self.board[y - 1][x - 1] = self.black_piece
                            self.turn = "white"
                        self.turn_num += 1
                        
                        if self.turn == "black":
                            color_check = self.white_piece
                            win_check = "white"
                            
                        elif self.turn == "white":
                            color_check = self.black_piece
                            win_check = "black"
                            
                        self.winner = self.b.win_check(color_check, win_check, self.board)
                if self.AI == True:
                    win = ""
                    if self.AIfirst == True:
                        if self.turn == "black":
                            win = "AI"
                        else:
                            win = "Human"
                    else:
                        if self.turn == "white":
                            win = "AI"
                        else:
                            win = "Human"
                            
                    winner_text = self.background.create_text(self.width / 2,
            	                                    self.height - self.frame_gap - 25,
            	                                    text = win + " WINS!",
            	                                    font = "Helvetica 20 bold",
                                                    fill = self.winner)
                else:
                    winner_text = self.background.create_text(self.width / 2,
            	                                    self.height - self.frame_gap - 25,
            	                                    text = self.winner.upper() + " WINS!",
            	                                    font = "Helvetica 20 bold",
                                                    fill = self.winner)
                
                self.background.addtag_withtag("winnertext", winner_text)
        
    def restart(self):
        self.winner = "0"
        circle_g = self.background.find_withtag("circle")
        self.background.delete(*circle_g)
        
        text_g = self.background.find_withtag("text")
        self.background.delete(*text_g)
        
        winner_text = self.background.find_withtag("winnertext")
        self.background.delete(*winner_text)
        
        self.start_button.config(bg = "gray")
        self.ai_human_button.config(bg = "gray")
        self.human_human_button.config(bg = "gray")
        self.ai_first_button.config(bg = "gray")
        self.human_first_button.config(bg = "gray")
        self.ab_algorithm_button.config(bg = "gray")
        self.g_algorithm_button.config(bg = "gray")
        
        self.playwith = False
        self.gofirst = False
        self.AIfirst = False
        self.AI = False
        self.AI_turn = False
        self.ab_algorithm = False
        self.g_algorithm = False
        self.mm_algorithm = False
        self.mcts_algorithm = False
        
        self.turn_num = 1
        self.turn = "white"
        self.winner = None
        #Cord List
        self.black_cord_picked_x = []
        self.black_cord_picked_y = []
        self.white_cord_picked_x = []
        self.white_cord_picked_y = []

        #Click Detection Cord
        self.game_cord_x = []
        self.game_cord_y = []
        self.actual_cord_x_1 = []
        self.actual_cord_y_1 = []
        self.actual_cord_x_2 = []
        self.actual_cord_y_2 = []
        
        #2D Board List
        self.board = []
        for i in range(self.board_size):
            self.board.append([0] * (self.board_size))
            
        self.unfilled = 0
        self.white_piece = 1
        self.black_piece = 2
        
        self.AI = False
        
        self.ab_algorithm = False
        
        #Fills Empty List
        for z in range(1, self.board_size + 1):
            for i in range(1, self.board_size + 1):
                self.game_cord_x.append(z)
                self.game_cord_y.append(i)
                self.actual_cord_x_1.append((z - 1) * self.board_gap_x + self.board_x1 - self.chess_radius)
                self.actual_cord_y_1.append((i - 1) * self.board_gap_y + self.board_y1 - self.chess_radius)
                self.actual_cord_x_2.append((z - 1) * self.board_gap_x + self.board_x1 + self.chess_radius)
                self.actual_cord_y_2.append((i - 1) * self.board_gap_y + self.board_y1 + self.chess_radius)
        
        self.background.bind("<Button-1>", self.mouse_click)
        self.click_cord = [None, None]
        
    def delete_circle(self):
        circle = self.circles.pop()
        self.background.delete(circle)
        text = self.texts.pop()
        self.background.delete(text)
        
    def undo(self):
        if len(self.circles) > 0 and len(self.texts) > 0 and self.turn_num > 0:
            self.delete_circle()
            
            """
            if self.turn_num % 2 == 0 and len(self.white_cord_picked_x) > 0:
                x = self.white_cord_picked_x[-1] - 1
                y = self.white_cord_picked_y[-1] - 1
                self.board[y][x] = 0
            elif self.turn_num % 2 == 1 and len(self.black_cord_picked_y) > 0:
                x = self.black_cord_picked_x[-1] - 1
                y = self.black_cord_picked_y[-1] - 1
                self.board[y][x] = 0
            
            """
            self.turn_num -= 1
            
    def exit(self):
        self.window.destroy()
        
app = GUI()
app.mainloop()