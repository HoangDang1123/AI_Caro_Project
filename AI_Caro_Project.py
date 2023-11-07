# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 01:34:47 2023

@author: daoho
"""

import tkinter as tk
from PIL import Image, ImageTk, ImageDraw

class CaroBoard(tk.Frame):
    def __init__(self, window, board_size):
        self.create_dot()
        self.window = window
        self.board_size = board_size
        self.create_frame()
        self.create_board()
        self.create_button()
        
    def create_dot(self):
        # Tạo hình ảnh chấm tròn
        circle_radius = 10
        circle_black_color = "black"
        black_image = Image.new("RGBA", (circle_radius * 10, circle_radius * 10), (0, 0, 0, 0))
        draw = ImageDraw.Draw(black_image)
        draw.ellipse((0, 0, circle_radius * 10, circle_radius * 10), fill=circle_black_color)
        
        # Chuyển đổi hình ảnh thành đối tượng hình ảnh tkinter
        self.black = ImageTk.PhotoImage(black_image)
        
        circle_white_color = "white"
        white_image = Image.new("RGBA", (circle_radius * 10, circle_radius * 10), (0, 0, 0, 0))
        draw = ImageDraw.Draw(white_image)
        draw.ellipse((0, 0, circle_radius * 10, circle_radius * 10), fill=circle_white_color)
        
        # Chuyển đổi hình ảnh thành đối tượng hình ảnh tkinter
        self.white = ImageTk.PhotoImage(white_image)
        
    def create_frame(self):
        self.button_frame = tk.Frame(self.window, bg = "blue")
        self.button_frame.grid(row = 0, column = 0)
        
        self.board_frame = tk.Frame(self.window, bg = "black")
        self.board_frame.grid(row = 0, column = 1)
        
    def create_board(self):
        self.tiles = []
        for i in range(self.board_size):
            row = []
            for j in range(self.board_size):
                tile = tk.Button(self.board_frame, width=3, height=1, relief=tk.RAISED, borderwidth=1, highlightbackground="black", bg = "orange", state = tk.DISABLED)
                tile.grid(row=i, column=j)
                row.append(tile)
            self.tiles.append(row)
            
    def create_button(self):
        self.start_button = tk.Button(self.button_frame, text = "Start", font = ("Arial", 14, "bold"), bg = "red", borderwidth = 2, width = 8, command = self.start)
        self.start_button.grid(row = 0, padx = 30, pady = 2)
        
        self.reset_button = tk.Button(self.button_frame, text = "Reset", font = ("Arial", 14, "bold"), bg = "red", borderwidth = 2, width = 8, command = self.reset)
        self.reset_button.grid(row = 1, padx = 30, pady = 2)
        
    def click(self, i, j):
        if self.count % 2 != 0:
            self.tiles[i][j].config(image = self.black, compound = tk.CENTER, text = self.count, fg = "black")
        else:
            self.tiles[i][j].config(image = self.white, compound = tk.CENTER, text = self.count, fg = "white")
        self.count += 1
        
    def start(self):
        self.count = 1
        for i in range(self.board_size):
            for j in range(self.board_size):
                button_command = lambda x=i, y=j: self.click(x, y)
                self.tiles[i][j].config(command = button_command, state=tk.NORMAL)
                
    def reset(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.tiles[i][j].config(text = "", bg = "orange", state = tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Caro Board")
    
    board_size = 19
    caro_board = CaroBoard(root, board_size)
    
    root.mainloop()