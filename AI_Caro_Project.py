from PIL import Image, ImageTk
from tkinter import *
from time import *
import tkinter as tk
import sys
import time
import math
import numpy as np
import random

class Board():
    # Kiểm tra thắng
    def win_check(self, Piece_Number, Piece_Colour, board):
        if self.rowCheck(Piece_Number, board) or self.rowCheck(Piece_Number, self.transpose(board)) or self.rowCheck(Piece_Number, self.transposeDiagonalInc(board)) or self.rowCheck(Piece_Number, self.transposeDiagonalDec(board)):
            Winner = Piece_Colour
            return Winner

    def rowCheck(self, Piece_Number, board):
        for i in range(len(board)):
            if board[i].count(Piece_Number) >= 5:
                
                for z in range(len(board) - 3):
                    Connection = 0

                    for c in range(5):
                        if board[i][z + c] == Piece_Number:
                            Connection += 1

                        else:
                            break

                        if Connection == 5:
                            return True

    # Đường chéo giảm
    def getDiagonalDec(self, loa, digNum):
        lst=[]
        if digNum <= len(loa) - 1:
            index = len(loa) - 1
            for i in range(digNum, -1, -1):
                lst.append(loa[i][index])
                index -= 1
            return lst
        else:
            index = (len(loa) * 2 - 2) - digNum
            for i in range(len(loa) - 1, digNum - len(loa), -1):
                lst.append(loa[i][index])
                index -= 1
            return lst

    def transposeDiagonalDec(self, loa):
        lst = []
        for i in range(len(loa) * 2 - 1):
            lst.append(self.getDiagonalDec(loa, i))
        return lst

    # Đường chéo tăng
    def getDiagonalInc(self, loa, digNum):
        lst=[]
        if digNum <= len(loa) - 1:
            index = 0
            for i in range(digNum, -1, -1):
                lst.append(loa[i][index])
                index += 1
            return lst
        else:
            index =  digNum - len(loa) + 1
            for i in range(len(loa) - 1, digNum - len(loa), -1):
                lst.append(loa[i][index])
                index += 1
            return lst

    def transposeDiagonalInc(self, loa):
        lst = []
        for i in range(len(loa) * 2 - 1):
            lst.append(self.getDiagonalInc(loa, i))
        return lst

    def transpose(self, loa):
        lst = []
        for i in range(len(loa)):
            lst.append(self.getCol(loa, i))
        return lst
        
    def getCol(self, loa, colNum):
        lst = []
        for i in range(len(loa)):
            lst.append(loa[i][colNum])
        return lst
    
class Minimax():
    def __init__(self):
        self.MAX, self.MIN = math.inf, -math.inf
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
    
    def getCoordsAround(self, board_size, board):
        '''
        get points around placed stones
        '''
        outTpl = np.nonzero(board)  # return tuple of all non zero points on board
        potentialValsCoord = {}
        for i in range(len(outTpl[0])):
            y = outTpl[0][i]
            x = outTpl[1][i]
            if y > 0:
                potentialValsCoord[(x, y-1)] = 1
                if x > 0:
                    potentialValsCoord[(x-1, y-1)] = 1
                if x < (board_size-1):
                    potentialValsCoord[(x+1, y-1)] = 1
            if x > 0:
                potentialValsCoord[(x-1, y)] = 1
                if y < (board_size-1):
                    potentialValsCoord[(x-1, y+1)] = 1
            if y < (board_size-1):
                potentialValsCoord[(x, y+1)] = 1
                if x < (board_size-1):
                    potentialValsCoord[(x+1, y+1)] = 1
                if x > 0:
                    potentialValsCoord[(x-1, y+1)] = 1
            if x < (board_size-1):
                potentialValsCoord[(x+1, y)] = 1
                if y > 0:
                    potentialValsCoord[(x+1, y-1)] = 1
        finalValsX, finalValsY = [], []
        for key in potentialValsCoord:
            finalValsX.append(key[0])
            finalValsY.append(key[1])
        return finalValsX, finalValsY


    def convertArrToMove(self, row, col):
        '''
        col goes to letter of number plus 1
        row is number but plus 1
        '''
        colVal = chr(col+ord('a'))  # 97
        rowVal = str(row+1)
        return colVal+rowVal


    def convertMoveToArr(self, col, row):
        '''
        convert move ex: a4 to be converted to col and row integers for array
        '''
        colVal = ord(col)-ord('a')  # double check
        rowVal = int(row)-1
        return colVal, rowVal


    def convertKeyToArr(self, key):
        '''
        convert key in getcoordsaround func to array indexes
        '''
        colVal = ord(key[0])-ord('a')  # double check
        rowVal = int(key[1:])-1
        return colVal, rowVal


    def getRandomMove(self, board, boardSize):
        '''
        For choosing random move when can't decide propogated to center
        '''
        ctr = 0
        idx = boardSize//2
        while ctr < (idx/2):
            if board[idx+ctr][idx+ctr] == 0:
                return idx+ctr, idx+ctr
            elif board[idx+ctr][idx-ctr] == 0:
                return idx+ctr, idx-ctr
            elif board[idx+ctr][idx] == 0:
                return idx+ctr, idx
            elif board[idx][idx+ctr] == 0:
                return idx, idx+ctr
            elif board[idx][idx-ctr] == 0:
                return idx, idx-ctr
            elif board[idx-ctr][idx] == 0:
                return idx-ctr, idx
            elif board[idx-ctr][idx-ctr] == 0:
                return idx-ctr, idx-ctr
            elif board[idx-ctr][idx+ctr] == 0:
                return idx-ctr, idx+ctr
            ctr += 1
        for i in range(boardSize):
            for j in range(boardSize):
                if board[i][j] == 0:
                    return i, j

    def btsConvert(self, board, player):
        '''
        convert board to col,row,and diag string arrays for easier interpreting 
        '''
        temp_board = np.array(board)
        cList, rList, dList = [], [], []
        board_col = len(board[0])
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


    def points(self, board, player):  # evaluates
        '''
        assigns points for moves
        '''
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

    def otherPlayerStone(self, player):
        '''
        Stones are 1 or 2 based on player. Just gets other player's stone
        '''
        return 2 if player==1 else 1

    def minimax(self, board, isMaximizer, depth, alpha, beta, player):  # alpha, beta
        '''
        Minimax with Alpha-Beta pruning (also computer is 1st Max in this implementation)
        alpha is best already explored option along path to root for maximizer(AI)
        beta is best already explored option along path to root for minimizer(AI Opponent)
        '''
        
        point = self.points(board, player)
        if depth == 2 or point>=20000000 or point<=-20000000:
            return point
        size = len(board)
        if isMaximizer:  # THE MAXIMIZER
            best = self.MIN
            potentialValsX, potentialValsY = self.getCoordsAround(size, board)
            for i in range(len(potentialValsX)):
                if board[potentialValsY[i]][potentialValsX[i]] == 0:
                    board[potentialValsY[i]][potentialValsX[i]] = player
                    score = self.minimax(board, False, depth+1, alpha, beta, player)
                    best = max(best, score)
                    alpha = max(alpha, best)  # best AI Opponent move
                    board[potentialValsY[i]][potentialValsX[i]] = 0  # undoing
                    if beta <= alpha:
                        break
            return best
        else:  # THE MINIMIZER
            best = self.MAX
            potentialValsX, potentialValsY = self.getCoordsAround(size, board)
            for i in range(len(potentialValsX)):
                if board[potentialValsY[i]][potentialValsX[i]] == 0:
                    otherplayer = self.otherPlayerStone(player)
                    board[potentialValsY[i]][potentialValsX[i]] = otherplayer
                    score = self.minimax(board, True, depth+1, alpha, beta, player)
                    best = min(best, score)
                    beta = min(beta, best)  # best AI Opponent move
                    board[potentialValsY[i]][potentialValsX[i]] = 0  # undoing
                    if beta <= alpha:
                        break
                    if movePoints > mostPoints:
                        bestMoveRow = potentialValsY[i]
                        bestMoveCol = potentialValsX[i]
                        mostPoints = movePoints
                        if movePoints >= 20000000:
                            break
            if bestMoveRow == -1 or bestMoveCol == -1:  # ' when still -1
                bestMoveRow, bestMoveCol = self.getRandomMove(board, boardSize)
            board[bestMoveRow][bestMoveCol] = mark
            return bestMoveRow, bestMoveCol
            return best

    def computer(self, board_size, board, isComputerFirst):
        '''
        Chooses best move for computer
        Max that gives index and calls min in minimax 
        '''
        mostPoints = float('-inf')
        alpha,beta = self.MIN, self.MAX
        if isComputerFirst:
            mark = 1
        else:
            mark = 2
        bestMoveRow = bestMoveCol = -1
        boardSize = len(board)
        potentialValsX, potentialValsY = self.getCoordsAround(board_size, board)
        for i in range(len(potentialValsX)):
            if board[potentialValsY[i]][potentialValsX[i]] == 0:
                board[potentialValsY[i]][potentialValsX[i]] = mark
                movePoints = max(mostPoints, self.minimax(
                    board, False, 1, alpha, beta, mark))
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
        if bestMoveRow == -1 or bestMoveCol == -1:  # ' when still -1
            bestMoveRow, bestMoveCol = self.getRandomMove(board, boardSize)
        board[bestMoveRow][bestMoveCol] = mark
        return bestMoveRow, bestMoveCol

class GUI(Board, Minimax):
    b = Board()
    m = Minimax()
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("ĐỒ ÁN HỌC PHẦN - LẬP TRÌNH GAME CỜ CARO")
        self.background = tk.Canvas(
            self.window,
            width = self.window.winfo_screenwidth(),
            height = self.window.winfo_screenheight() - float(100 / 1080) * self.window.winfo_screenheight(),
            background= "#b69b4c"
            )
        self.background.pack()
        self.window.state("zoomed")

        #Board Size
        self.board_size = 19
        self.frame_gap = 25
        self.width = 0.52 * self.window.winfo_screenwidth()
        self.height = 0.93 * self.window.winfo_screenheight()
        
        self.board_size = self.board_size - 1
        self.board_x1 = self.width / 10
        self.board_y1 = self.height / 10
        self.board_gap_x = (self.width - self.board_x1 * 2) / self.board_size
        self.board_gap_y = (self.height - self.board_y1 * 2) / self.board_size
        
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
        for i in range(self.board_size + 1):
            self.board.append([0] * (self.board_size + 1))
            
        self.unfilled = 0
        self.white_piece = 1
        self.black_piece = 2
        
        self.AI = False
        self.AI_turn = False
        self.AI_algorithm = False
        
        #Fills Empty List
        for z in range(1, self.board_size + 2):
            for i in range(1, self.board_size + 2):
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
        # LabelHCMUTE logo
        """
        logo = tk.PhotoImage(file="./image/hcmute.png")
        self.university_logo = tk.Label(self.window,
                                        image = logo,
                                        bg = "#b69b4c")
        self.university_logo.image = logo
        self.university_logo.place(x = self.board_x1 + self.frame_gap + self.board_gap_x * self.board_size + 230,
                                   y = self.board_y1 - self.frame_gap - 70)
        """

        # Label tiêu đề
        self.title = tk.Label(self.window,
                              text = "ĐỒ ÁN CUỐI KỲ",
                              font = ("Arial", 20, "bold"),
                              fg = "navy blue",
                              bg = "#b69b4c")
        self.title.place(x = self.board_x1 + self.frame_gap + self.board_gap_x * self.board_size + 0.1875 * self.window.winfo_screenwidth(),
                         y = self.board_y1 - self.frame_gap + 0.028 * self.window.winfo_screenheight())

        # Label tên lớp
        self.class_name = tk.Label(self.window,
                                   text = "Lớp: ARIN330585_03CLC",
                                   font = ("Arial", 12, "bold"),
                                   fg = "navy blue",
                                   bg = "#b69b4c")
        self.class_name.place(x = self.board_x1 + self.frame_gap + self.board_gap_x * self.board_size + 0.078125 * self.window.winfo_screenwidth(),
                              y = self.board_y1 - self.frame_gap + 0.069 * self.window.winfo_screenheight())

        # Label tên thành viên
        self.member_name = tk.Label(self.window,
                                    text = "Tên thành viên:",
                                    font = ("Arial", 12, "bold"),
                                    fg = "navy blue",
                                    bg = "#b69b4c")
        self.member_name.place(x = self.board_x1 + self.frame_gap + self.board_gap_x * self.board_size + float(150 / 1920) * self.window.winfo_screenwidth(),
                               y = self.board_y1 - self.frame_gap + float(105 / 1080) * self.window.winfo_screenheight())

        # Label tên thành viên 1
        self.member_1 = tk.Label(self.window,
                                 text = "Đỗ Anh Khoa          -      21110208",
                                 font = ("Arial", 12, "bold"),
                                 fg = "navy blue",
                                 bg = "#b69b4c")
        self.member_1.place(x = self.board_x1 + self.frame_gap + self.board_gap_x * self.board_size + float(420 / 1920) * self.window.winfo_screenwidth(),
                            y = self.board_y1 - self.frame_gap + float(105 / 1080) * self.window.winfo_screenheight(),)

        # Label tên thành viên 2
        self.member_2 = tk.Label(self.window, text = "Đào Hoàng Đăng    -      21110163",
                                 font = ("Arial", 12, "bold"),
                                 fg = "navy blue",
                                 bg = "#b69b4c")
        self.member_2.place(x = self.board_x1 + self.frame_gap + self.board_gap_x * self.board_size + float(420 / 1920) * self.window.winfo_screenwidth(),
                            y = self.board_y1 - self.frame_gap + float(145 / 1080) * self.window.winfo_screenheight(),)

        # Label tên thành viên 3
        self.member_3 = tk.Label(self.window, text = "Nguyễn Anh Hào    -      21110823",
                                 font = ("Arial", 12, "bold"),
                                 fg = "navy blue",
                                 bg = "#b69b4c")
        self.member_3.place(x = self.board_x1 + self.frame_gap + self.board_gap_x * self.board_size + float(420 / 1920) * self.window.winfo_screenwidth(),
                            y = self.board_y1 - self.frame_gap + float(185 / 1080) * self.window.winfo_screenheight())
        
    def best_line(self):
        # Frame
        self.background.create_rectangle(self.board_x1 + self.frame_gap + self.board_gap_y * self.board_size + float(100 / 1920) * self.window.winfo_screenwidth(),
                                         self.board_y1 - self.frame_gap + float(250 / 1080) * self.window.winfo_screenheight(),
                                         self.window.winfo_screenwidth() - float(100 / 1920) * self.window.winfo_screenwidth(),
                                         self.board_y1 + self.frame_gap + self.board_gap_y * self.board_size - float(430 / 1080) * self.window.winfo_screenheight(),
                                         width = 3)
        
        # Label
        self.best_line_label = tk.Label(self.window,
                                        text = "BEST LINE",
                                        font = ("Arial", 12, "bold"),
                                        fg = "navy blue",
                                        bg = "#b69b4c")
        self.best_line_label.place(x = self.board_x1 + self.frame_gap + self.board_gap_x * self.board_size + float(420 / 1920) * self.window.winfo_screenwidth(),
                                   y = self.board_y1 - self.frame_gap + float(255 / 1080) * self.window.winfo_screenheight())

        # Text
        self.best_line_text = tk.Text(self.window,
                                      bg = "#b69b4c", width = 75,
                                      height =5,
                                      borderwidth = 3,
                                      state = tk.DISABLED)
        self.best_line_text.place(x = self.board_x1 + self.frame_gap + self.board_gap_x * self.board_size + float(120 / 1920) * self.window.winfo_screenwidth(),
                                  y = self.board_y1 - self.frame_gap + float(285 / 1080) * self.window.winfo_screenheight())
        
    def button(self):
        # Frame
        self.background.create_rectangle(self.board_x1 + self.frame_gap + self.board_gap_x * self.board_size + float(100 / 1920) * self.window.winfo_screenwidth(),
                           self.board_y1 - self.frame_gap + float(440 / 1080) * self.window.winfo_screenheight(),
                           self.window.winfo_screenwidth() - float(100 / 1920) * self.window.winfo_screenwidth(),
                           self.board_y1 + self.frame_gap + self.board_gap_y * self.board_size,
                           fill = "silver",
                           outline = "silver")

        # Frame các nút điều khiển chính
        self.background.create_rectangle(self.board_x1 + self.frame_gap + self.board_gap_x * self.board_size + float(130 / 1920) * self.window.winfo_screenwidth(),
                                         self.board_y1 - self.frame_gap + float(470 / 1080) * self.window.winfo_screenheight(),
                                         self.board_x1 + self.frame_gap + self.board_gap_x * self.board_size + float(480 / 1920) * self.window.winfo_screenwidth(),
                                         self.board_y1 + self.frame_gap + self.board_gap_y * self.board_size - float(190 / 1080) * self.window.winfo_screenheight(),
                                         fill = "gray",
                                         outline = "gray")
        # Button bắt đầu chơi
        self.start_button = tk.Button(self.window,
                                      text = "Start",
                                      font = "Helvetica 14 bold",
                                      command = self.start,
                                      bg = "gray",
                                      fg = "black")
        self.start_button.place(x = self.board_x1 + self.frame_gap + self.board_gap_x * self.board_size + float(155 / 1920) * self.window.winfo_screenwidth(),
                                y = self.board_y1 - self.frame_gap + float(495 / 1080) * self.window.winfo_screenheight(),
                                width = self.chess_radius * 7,
                                height = self.chess_radius * 3)
        # Button bát đầu chơi lại
        self.restart_button = tk.Button(self.window,
                                        text = "Restart",
                                        font = "Helvetica 14 bold",
                                        command = self.restart,
                                        bg = "gray",
                                        fg = "black")
        self.restart_button.place(x = self.board_x1 + self.frame_gap + self.board_gap_x * self.board_size + float(315 / 1920) * self.window.winfo_screenwidth(),
                                y = self.board_y1 - self.frame_gap + float(495 / 1080) * self.window.winfo_screenheight(),
                                width = self.chess_radius * 7,
                                height = self.chess_radius * 3)
        # Button quay lại lượt trước
        self.undo_button = tk.Button(self.window,
                                        text = "Undo",
                                        font = "Helvetica 14 bold",
                                        command = self.undo,
                                        bg = "gray",
                                        fg = "black")
        self.undo_button.place(x = self.board_x1 + self.frame_gap + self.board_gap_x * self.board_size + float(155 / 1920) * self.window.winfo_screenwidth(),
                                y = self.board_y1 - self.frame_gap + float(575 / 1080) * self.window.winfo_screenheight(),
                                width = self.chess_radius * 7,
                                height = self.chess_radius * 3)
        # Button thoát game
        self.exit_button = tk.Button(self.window,
                                        text = "Exit",
                                        font = "Helvetica 14 bold",
                                        command = self.exit,
                                        bg = "gray",
                                        fg = "black")
        self.exit_button.place(x = self.board_x1 + self.frame_gap + self.board_gap_x * self.board_size + float(315 / 1920) * self.window.winfo_screenwidth(),
                                y = self.board_y1 - self.frame_gap + float(575 / 1080) * self.window.winfo_screenheight(),
                                width = self.chess_radius * 7,
                                height = self.chess_radius * 3)
        
        # Frame các nút chọn chế độ chơi
        self.background.create_rectangle(self.window.winfo_screenwidth() - float(480 / 1920) * self.window.winfo_screenwidth(),
                                         self.board_y1 - self.frame_gap + float(470 / 1080) * self.window.winfo_screenheight(),
                                         self.window.winfo_screenwidth() - float(130 / 1920) * self.window.winfo_screenwidth(),
                                         self.board_y1 + self.frame_gap + self.board_gap_y * self.board_size - float(190 / 1080) * self.window.winfo_screenheight(),
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
                  y = self.board_y1 - self.frame_gap + float(495 / 1080) * self.window.winfo_screenheight(),
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
                  y = self.board_y1 - self.frame_gap + float(575 / 1080) * self.window.winfo_screenheight(),
                  width = self.chess_radius * 15,
                  height = self.chess_radius * 3)

        # Frame các nút chọn thuật toán
        self.background.create_rectangle(self.board_x1 + self.frame_gap + self.board_gap_x * self.board_size + float(130 / 1920) * self.window.winfo_screenwidth(),
                                         self.board_y1 - self.frame_gap + float(700 / 1080) * self.window.winfo_screenheight(),
                                         self.board_x1 + self.frame_gap + self.board_gap_x * self.board_size + float(480 / 1920) * self.window.winfo_screenwidth(),
                                         self.board_y1 + self.frame_gap + self.board_gap_y * self.board_size - float(30 / 1080) * self.window.winfo_screenheight(),
                                         fill = "gray",
                                         outline = "gray")
        # Button thuật toán Alpha-Beta
        self.ab_algorithm_button = tk.Button(self.window, text = "Alpha-Beta", font = "Helvetica 14 bold", command = self.set_AI_algorithm, bg = "gray", fg = "black")
        self.ab_algorithm_button.place(x = self.board_x1 + self.frame_gap + self.board_gap_x * self.board_size + float(155 / 1920) * self.window.winfo_screenwidth(),
                                y = self.board_y1 - self.frame_gap + float(730 / 1080) * self.window.winfo_screenheight(),
                                width = self.chess_radius * 7,
                                height = self.chess_radius * 3)
        # Button thuật toán IDS
        self.ids_algorithm_button = tk.Button(self.window, text = "IDS", font = "Helvetica 14 bold", command = self.unset_AI_algorithm, bg = "gray", fg = "black")
        self.ids_algorithm_button.place(x = self.board_x1 + self.frame_gap + self.board_gap_x * self.board_size + float(315 / 1920) * self.window.winfo_screenwidth(),
                                y = self.board_y1 - self.frame_gap + float(730 / 1080) * self.window.winfo_screenheight(),
                                width = self.chess_radius * 7,
                                height = self.chess_radius * 3)
        
        # Frame các nút chọn ai đi trước
        self.background.create_rectangle(self.window.winfo_screenwidth() - float(480 / 1920) * self.window.winfo_screenwidth(),
                                         self.board_y1 - self.frame_gap + float(700 / 1080) * self.window.winfo_screenheight(),
                                         self.window.winfo_screenwidth() - float(130 / 1920) * self.window.winfo_screenwidth(),
                                         self.board_y1 + self.frame_gap + self.board_gap_y * self.board_size - float(30 / 1080) * self.window.winfo_screenheight(),
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
                  y = self.board_y1 - self.frame_gap + float(730 / 1080) * self.window.winfo_screenheight(),
                  width = self.chess_radius * 7,
                  height = self.chess_radius * 3)
        # Button Người đánh trước
        self.human_first_button = tk.Button(self.window,
                               text = "Human First",
                               font = "Helvetica 13 bold",
                               command = self.unset_AI_turn,
                               bg = "gray",
                               fg = "black")
        self.human_first_button.place(x = self.window.winfo_screenwidth() - float(295 / 1920) * self.window.winfo_screenwidth(),
                  y = self.board_y1 - self.frame_gap + float(730 / 1080) * self.window.winfo_screenheight(),
                  width = self.chess_radius * 7,
                  height = self.chess_radius * 3)
        
    def set_AI(self):
        self.AI = True
        
    def unset_AI(self):
        self.AI = False
    
    def set_AI_turn(self):
        self.AI_turn = True
        
    def unset_AI_turn(self):
        self.AI_turn = False
        
    def set_AI_algorithm(self):
        self.AI_algorithm = True

    def unset_AI_algorithm(self):
        self.AI_algorithm = False    
        
    def game_board(self):
        # Tạo bàn cờ
        self.background.create_rectangle(self.board_x1 - self.frame_gap,
                                         self.board_y1 - self.frame_gap,
                                         self.board_x1 + self.frame_gap + self.board_gap_x * self.board_size,
                                         self.board_y1 + self.frame_gap + self.board_gap_y * self.board_size,
                                         width = 3)
        
        letter = 64
        for f in range(self.board_size + 1):
            self.background.create_line(self.board_x1,
                          self.board_y1 + f * self.board_gap_y,
                          self.board_x1 + self.board_gap_x * self.board_size,
                          self.board_y1 + f * self.board_gap_y)
            self.background.create_line(self.board_x1 + f * self.board_gap_x,
                          self.board_y1,
                          self.board_x1 + f * self.board_gap_x,
                          self.board_y1 + self.board_gap_y * self.board_size)

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
        if(self.AI_turn):
            self.piece_num = self.white_piece
        else:
            self.piece_num = self.black_piece
            
            
        while self.winner == None:
            x = 0
            y = 0
            if(self.AI):
                if(self.AI_turn):
                    if(self.AI_algorithm):
                        x, y = self.m.computer(self.board_size, self.board, self.AI_turn)
                        print(x, y)
                    else:
                        # Thuật toán 2
                        x = 0
                        y = 0
                    self.AI_turn = False
                else:
                    self.background.update()
                    x = self.click_cord[0]
                    y = self.click_cord[1]
                    self.AI_turn = True 
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
                
        winner_text = self.background.create_text(self.width / 2,
	                                    self.height - self.frame_gap - 25,
	                                    text = self.winner.upper() + " WINS!",
	                                    font = "Helvetica 20 bold",
	                                    fill = self.winner.lower())
        
        self.background.addtag_withtag("winnertext", winner_text)

    
        
    def restart(self):
        circle_ids = self.background.find_withtag("circle")
        self.background.delete(*circle_ids)
        
        text_ids = self.background.find_withtag("text")
        self.background.delete(*text_ids)
        
        winner_text = self.background.find_withtag("winnertext")
        self.background.delete(*winner_text)
        
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
        for i in range(self.board_size + 1):
            self.board.append([0] * (self.board_size + 1))
            
        self.unfilled = 0
        self.white_piece = 1
        self.black_piece = 2
        
        #Fills Empty List
        for z in range(1, self.board_size + 2):
            for i in range(1, self.board_size + 2):
                self.game_cord_x.append(z)
                self.game_cord_y.append(i)
                self.actual_cord_x_1.append((z - 1) * self.board_gap_x + self.board_x1 - self.chess_radius)
                self.actual_cord_y_1.append((i - 1) * self.board_gap_y + self.board_y1 - self.chess_radius)
                self.actual_cord_x_2.append((z - 1) * self.board_gap_x + self.board_x1 + self.chess_radius)
                self.actual_cord_y_2.append((i - 1) * self.board_gap_y + self.board_y1 + self.chess_radius)
                
    def undo(self):
        circle = self.circles.pop()
        self.background.delete(circle)
        
        text = self.texts.pop()
        self.background.delete(text)
        
        self.turn_num -= 1
            
    def exit(self):
        self.window.destroy()
        
app = GUI()
app.mainloop()