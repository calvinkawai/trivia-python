#!/usr/bin/env python3
import tkinter as tk
from tkinter import filedialog as fd
from Team import *
from Question import *
from RoundOnePage import *

class MainPage:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(parent)
        self.frame.pack()

        # data to be passed to next page
        self.team_list = []
        self.round_one_questions = []

        self.team_name = tk.StringVar()
        label = tk.Label(self.frame, text="Please enter your team name")
        label.pack()

        entry = tk.Entry(self.frame, textvariable=self.team_name)
        entry.pack()

        submit = tk.Button(self.frame, text='Submit', command=lambda: self.add_team())
        submit.pack()

        label_current_teams = tk.Label(self.frame, text='Current teams: ')
        self.team_list_box = tk.Listbox(self.frame)
        self.team_list_box.pack()

        read_questions_file = tk.Button(self.frame, text="Find questions file", command=lambda: self.ask_question_file())
        read_questions_file.pack()

        start_round_one = tk.Button(self.frame, text='Start Round One', command=lambda: self.start_round_one())
        start_round_one.pack()

        self.warning_text = tk.StringVar()
        warning_box = tk.Label(self.frame, textvariable=self.warning_text, fg='red')
        warning_box.pack()


    def add_team(self):
        if self.team_name.get().isspace() or self.team_name.get() == "":
            self.warning_text.set("Name cannot be empty")
            return
        self.team_list.append(Team(self.team_name.get()))
        cur_num = len(self.team_list)
        self.team_list_box.insert(cur_num, f"{cur_num}: " + self.team_name.get())
        self.team_name.set("")

    def start_round_one(self):
        if len(self.team_list) < 2 or not self.round_one_questions:
            self.warning_text.set("Please check your team numbers and question sheet")
            return
        self.frame.destroy()
        RoundOne(self.parent, self.team_list, self.round_one_questions)

    def ask_question_file(self):
        name = fd.askopenfilename()
        self.round_one_questions = read_questions(name)



if __name__ == "__main__":
    window = tk.Tk()
    window.title("Ernie Bowl")
    MainPage(window)
    window.mainloop()
