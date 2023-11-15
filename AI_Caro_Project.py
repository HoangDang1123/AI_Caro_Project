from PIL import Image, ImageTk
from tkinter import *
from time import *
import tkinter as tk
import sys

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

class GUI(Board):
    b = Board()
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("ĐỒ ÁN HỌC PHẦN - LẬP TRÌNH GAME CỜ CARO")
        self.background = tk.Canvas(
            self.window,
            width = self.window.winfo_screenwidth(),
            height = self.window.winfo_screenheight() - 100,
            background= "#b69b4c"
            )
        self.background.pack()
        self.window.state("zoomed")

        #Board Size
        self.board_size = 19
        self.frame_gap = 25
        self.width = 1000
        self.height = 1000
        
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
        self.winner = "None"

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
        self.black_piece = 1
        self.white_piece = 2
        
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
        self.title.place(x = self.board_x1 + self.frame_gap + self.board_gap_x * self.board_size + 360,
                         y = self.board_y1 - self.frame_gap + 30)

        # Label tên lớp
        self.class_name = tk.Label(self.window,
                                   text = "Lớp: ARIN330585_03CLC",
                                   font = ("Arial", 12, "bold"),
                                   fg = "navy blue",
                                   bg = "#b69b4c")
        self.class_name.place(x = self.board_x1 + self.frame_gap + self.board_gap_x * self.board_size + 150,
                              y = self.board_y1 - self.frame_gap + 75)

        # Label tên thành viên
        self.member_name = tk.Label(self.window,
                                    text = "Tên thành viên:",
                                    font = ("Arial", 12, "bold"),
                                    fg = "navy blue",
                                    bg = "#b69b4c")
        self.member_name.place(x = self.board_x1 + self.frame_gap + self.board_gap_x * self.board_size + 150,
                               y = self.board_y1 - self.frame_gap + 105)

        # Label tên thành viên 1
        self.member_1 = tk.Label(self.window,
                                 text = "Đỗ Anh Khoa          -      21110208",
                                 font = ("Arial", 12, "bold"),
                                 fg = "navy blue",
                                 bg = "#b69b4c")
        self.member_1.place(x = self.board_x1 + self.frame_gap + self.board_gap_x * self.board_size + 420, y = self.board_y1 - self.frame_gap + 105)

        # Label tên thành viên 2
        self.member_2 = tk.Label(self.window, text = "Đào Hoàng Đăng    -      21110163",
                                 font = ("Arial", 12, "bold"),
                                 fg = "navy blue",
                                 bg = "#b69b4c")
        self.member_2.place(x = self.board_x1 + self.frame_gap + self.board_gap_x * self.board_size + 420,
                            y = self.board_y1 - self.frame_gap + 145)

        # Label tên thành viên 3
        self.member_3 = tk.Label(self.window, text = "Nguyễn Anh Hào    -      21110823",
                                 font = ("Arial", 12, "bold"),
                                 fg = "navy blue",
                                 bg = "#b69b4c")
        self.member_3.place(x = self.board_x1 + self.frame_gap + self.board_gap_x * self.board_size + 420,
                            y = self.board_y1 - self.frame_gap + 185)
        
    def best_line(self):
        # Frame
        self.background.create_rectangle(self.board_x1 + self.frame_gap + self.board_gap_y * self.board_size + 100,
                                         self.board_y1 - self.frame_gap + 250,
                                         self.window.winfo_screenwidth() - 100,
                                         self.board_y1 + self.frame_gap + self.board_gap_y * self.board_size - 430,
                                         width = 3)
        
        # Label
        self.best_line_label = tk.Label(self.window,
                                        text = "BEST LINE",
                                        font = ("Arial", 12, "bold"),
                                        fg = "navy blue",
                                        bg = "#b69b4c")
        self.best_line_label.place(x = self.board_x1 + self.frame_gap + self.board_gap_x * self.board_size + 420,
                             y = self.board_y1 - self.frame_gap + 255)

        # Text
        self.best_line_text = tk.Text(self.window,
                                      bg = "#b69b4c", width = 75,
                                      height =5,
                                      borderwidth = 3,
                                      state = tk.DISABLED)
        self.best_line_text.place(x = self.board_x1 + self.frame_gap + self.board_gap_x * self.board_size + 120,
                                  y = self.board_y1 - self.frame_gap + 285)
        
    def button(self):
        # Frame
        self.background.create_rectangle(self.board_x1 + self.frame_gap + self.board_gap_x * self.board_size + 100,
                           self.board_y1 - self.frame_gap + 440,
                           self.window.winfo_screenwidth() - 100,
                           self.board_y1 + self.frame_gap + self.board_gap_y * self.board_size,
                           fill = "silver",
                           outline = "silver")

        # Frame các nút điều khiển chính
        self.background.create_rectangle(self.board_x1 + self.frame_gap + self.board_gap_x * self.board_size + 130,
                                         self.board_y1 - self.frame_gap + 470,
                                         self.board_x1 + self.frame_gap + self.board_gap_x * self.board_size + 480,
                                         self.board_y1 + self.frame_gap + self.board_gap_y * self.board_size - 190,
                                         fill = "gray",
                                         outline = "gray")
        # Button bắt đầu chơi
        self.start_button = tk.Button(self.window,
                                      text = "Start",
                                      font = "Helvetica 14 bold",
                                      command = self.start,
                                      bg = "gray",
                                      fg = "black")
        self.start_button.place(x = self.board_x1 + self.frame_gap + self.board_gap_x * self.board_size + 155,
                                y = self.board_y1 - self.frame_gap + 495,
                                width = self.chess_radius * 7,
                                height = self.chess_radius * 3)
        # Button bát đầu chơi lại
        self.restart_button = tk.Button(self.window,
                                        text = "Restart",
                                        font = "Helvetica 14 bold",
                                        command = None,
                                        bg = "gray",
                                        fg = "black")
        self.restart_button.place(x = self.board_x1 + self.frame_gap + self.board_gap_x * self.board_size + 315,
                                y = self.board_y1 - self.frame_gap + 495,
                                width = self.chess_radius * 7,
                                height = self.chess_radius * 3)
        # Button quay lại lượt trước
        self.undo_button = tk.Button(self.window,
                                        text = "Undo",
                                        font = "Helvetica 14 bold",
                                        command = None,
                                        bg = "gray",
                                        fg = "black")
        self.undo_button.place(x = self.board_x1 + self.frame_gap + self.board_gap_x * self.board_size + 155,
                                y = self.board_y1 - self.frame_gap + 575,
                                width = self.chess_radius * 7,
                                height = self.chess_radius * 3)
        # Button thoát game
        self.exit_button = tk.Button(self.window,
                                        text = "Exit",
                                        font = "Helvetica 14 bold",
                                        command = self.exit,
                                        bg = "gray",
                                        fg = "black")
        self.exit_button.place(x = self.board_x1 + self.frame_gap + self.board_gap_x * self.board_size + 315,
                                y = self.board_y1 - self.frame_gap + 575,
                                width = self.chess_radius * 7,
                                height = self.chess_radius * 3)
        
        # Frame các nút chọn chế độ chơi
        self.background.create_rectangle(self.window.winfo_screenwidth() - 480,
                                         self.board_y1 - self.frame_gap + 470,
                                         self.window.winfo_screenwidth() - 130,
                                         self.board_y1 + self.frame_gap + self.board_gap_y * self.board_size - 190,
                                         fill = "gray",
                                         outline = "gray")
        # Button AI chơi với AI
        self.ai_ai_button = tk.Button(self.window,
                               text = "AI - AI",
                               font = "Helvetica 14 bold",
                               command = None,
                               bg = "gray",
                               fg = "black")
        self.ai_ai_button.place(x = self.window.winfo_screenwidth() - 455,
                  y = self.board_y1 - self.frame_gap + 495,
                  width = self.chess_radius * 7,
                  height = self.chess_radius * 3)
        # Button AI chơi với Người
        self.ai_human_button = tk.Button(self.window,
                               text = "AI - Human",
                               font = "Helvetica 13 bold",
                               command = None,
                               bg = "gray",
                               fg = "black")
        self.ai_human_button.place(x = self.window.winfo_screenwidth() - 295,
                  y = self.board_y1 - self.frame_gap + 495,
                  width = self.chess_radius * 7,
                  height = self.chess_radius * 3)
        # Button Người chơi với Người
        self.human_human_button = tk.Button(self.window,
                               text = "Human - Human",
                               font = "Helvetica 14 bold",
                               command = None,
                               bg = "gray",
                               fg = "black")
        self.human_human_button.place(x = self.window.winfo_screenwidth() - 455,
                  y = self.board_y1 - self.frame_gap + 575,
                  width = self.chess_radius * 15,
                  height = self.chess_radius * 3)

        # Frame các nút chọn thuật toán
        self.background.create_rectangle(self.board_x1 + self.frame_gap + self.board_gap_x * self.board_size + 130,
                                         self.board_y1 - self.frame_gap + 700,
                                         self.board_x1 + self.frame_gap + self.board_gap_x * self.board_size + 480,
                                         self.board_y1 + self.frame_gap + self.board_gap_y * self.board_size - 30,
                                         fill = "gray",
                                         outline = "gray")
        # Button thuật toán Alpha-Beta
        self.ab_algorithm_button = tk.Button(self.window, text = "Alpha-Beta", font = "Helvetica 14 bold", command = None, bg = "gray", fg = "black")
        self.ab_algorithm_button.place(x = self.board_x1 + self.frame_gap + self.board_gap_x * self.board_size + 155,
                                y = self.board_y1 - self.frame_gap + 730,
                                width = self.chess_radius * 7,
                                height = self.chess_radius * 3)
        # Button thuật toán IDS
        self.ids_algorithm_button = tk.Button(self.window, text = "IDS", font = "Helvetica 14 bold", command = None, bg = "gray", fg = "black")
        self.ids_algorithm_button.place(x = self.board_x1 + self.frame_gap + self.board_gap_x * self.board_size + 315,
                                y = self.board_y1 - self.frame_gap + 730,
                                width = self.chess_radius * 7,
                                height = self.chess_radius * 3)
        
        # Frame các nút chọn ai đi trước
        self.background.create_rectangle(self.window.winfo_screenwidth() - 480,
                                         self.board_y1 - self.frame_gap + 700,
                                         self.window.winfo_screenwidth() - 130,
                                         self.board_y1 + self.frame_gap + self.board_gap_y * self.board_size - 30,
                                         fill = "gray",
                                         outline = "gray")
        # Button AI đánh trước
        self.ai_first_button = tk.Button(self.window,
                               text = "AI First",
                               font = "Helvetica 14 bold",
                               command = None,
                               bg = "gray",
                               fg = "black")
        self.ai_first_button.place(x = self.window.winfo_screenwidth() - 455,
                  y = self.board_y1 - self.frame_gap + 730,
                  width = self.chess_radius * 7,
                  height = self.chess_radius * 3)
        # Button Người đánh trước
        self.human_first_button = tk.Button(self.window,
                               text = "Human First",
                               font = "Helvetica 13 bold",
                               command = None,
                               bg = "gray",
                               fg = "black")
        self.human_first_button.place(x = self.window.winfo_screenwidth() - 295,
                  y = self.board_y1 - self.frame_gap + 730,
                  width = self.chess_radius * 7,
                  height = self.chess_radius * 3)
        
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
            self.background.create_oval(x - radius,
                                        y - radius,
                                        x + radius,
                                        y + radius,
                                        fill = "black",
                                        outline = "",
                                        width = width)
            self.background.create_text(x,
                                        y,
                                        text = count,
                                        fill = "white")
        else:
            self.background.create_oval(x - radius,
                                        y - radius,
                                        x + radius,
                                        y + radius,
                                        fill = "white",
                                        outline = "",
                                        width = width)
            self.background.create_text(x,
                                        y,
                                        text = count,
                                        fill = "black")
            
    def start(self):
        self.winner = None
        while self.winner == None:
            self.background.update()

            x = self.click_cord[0]
            y = self.click_cord[1]

            picked = self.valid_location(x, y)

            if picked:
                self.turn_label.config(text = "Turn = " + self.turn)
                self.create_circle(self.board_x1 + self.board_gap_x * (x - 1), self.board_y1 + self.board_gap_y * (y - 1), self.chess_radius, self.turn_num)
                if self.turn_num % 2 == 1:
                    self.white_cord_picked_x.append(x)
                    self.white_cord_picked_y.append(y)
                    self.board[y - 1][x - 1] = 2
                    self.turn = "black"
                elif self.turn_num % 2 == 0:
                    self.black_cord_picked_x.append(x)
                    self.black_cord_picked_y.append(y)
                    self.board[y - 1][x - 1] = 1
                    self.turn = "white"

                self.turn_num += + 1

                if self.turn == "white":
                    color_check = self.black_piece
                    win_check = "black"

                elif self.turn == "black":
                    color_check = self.white_piece
                    win_check = "white"

                self.winner = self.b.win_check(color_check, win_check, self.board)
                
        self.background.create_text(self.width / 2,
                                    self.height - self.frame_gap - 25,
                                    text = self.winner.upper() + " WINS!",
                                    font = "Helvetica 20 bold",
                                    fill = self.winner.lower())
            
    def exit(self):
        global winner
        winner = "Exit"
        self.window.destroy()
        
app = GUI()
app.mainloop()