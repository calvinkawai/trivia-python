#!/usr/bin/env python3
import tkinter as tk
from Question import *
from Team import *
from QuestionWindow import *

EASY = 'easy'
MEDIUM = 'medium'
HARD = 'hard'

class RoundOne:
    def __init__(self, parent, teams, questions):
        self.parent = parent
        self.frame = tk.Frame(parent)
        self.frame.pack()
        self.teams = teams
        self.vars = []
        self.all_buttons = []
        self.first_team_i = 0

        from pprint import pprint
        pprint(questions)
        current_row = 0

        # team labels to show scores
        for t in teams:
            new_text = tk.StringVar()
            new_text.set(f"{t.name}: {t.score}")
            new_label = tk.Label(self.frame, relief="sunken", textvariable=new_text, width=15).grid(row=current_row, column=0)
            self.vars.append(new_text)
            current_row += 1

        # current player labels
        self.current_player = tk.StringVar()
        self.current_player.set(f"Current Player: {self.teams[0].name}")
        c_player_label = tk.Label(self.frame, relief="sunken", textvariable=self.current_player, width=20).grid(row=0, column=1)

        current_row += 1
        count_buttons = 0
        current_col = 0
        count_cat = 0

        # question button displays
        cat_frames = []
        for category in questions:

            total_col = len(category[EASY])
            even = (total_col%2 == 0)
            self.mid_col = total_col//2

            new_frame = tk.Frame(self.frame, relief="ridge")

            # category title
            category_label = tk.Label(self.frame, text=category["name"], height=2).grid(row=current_row-1, column=current_col, pady=5)

            new_frame.grid(column=current_col, row=current_row, columnspan=5, rowspan=5, pady=5, padx=10)

            easy_questions = category[EASY]
            for eq_i in range(len(easy_questions)):
                self.all_buttons.append(
                    self.create_questions_block(new_frame, 1, eq_i, easy_questions[eq_i], "3", count_buttons)
                )
                count_buttons += 1

            med_quests = category[MEDIUM]
            for mq_i in range(len(med_quests)):
                self.all_buttons.append(
                    self.create_questions_block(new_frame, 2, mq_i, med_quests[mq_i], "5", count_buttons)
                )
                count_buttons += 1

            hard_quests = category[HARD]
            for hq_i in range(len(hard_quests)):
                self.all_buttons.append(
                    self.create_questions_block(new_frame, 3, hq_i, hard_quests[hq_i], "8",count_buttons)
                )
                count_buttons += 1

            count_cat += 1

            # change row each three categories
            if count_cat == 3:
                count_cat = 0
                current_col = 0
                current_row += 6
            current_col += 5

    def create_questions_block(self, parent, row, col, quest, point, index):
        button = tk.Button(parent, text=point, command=lambda: self.choose_quest(quest, point, index))
        button.grid(row=row, column=col)
        return button

    def choose_quest(self, quest, point, index):
        self.all_buttons[index]['state'] = 'disabled'
        if self.first_team_i == len(self.teams) - 1:
            sec_team = 0
        else:
            sec_team = self.first_team_i + 1
        qw = QuestionWindow(self.frame, quest, point, self.teams[self.first_team_i], self.teams[sec_team])
        self.update_score()

        # update current player
        self.first_team_i += 1
        if self.first_team_i == len(self.teams):
            self.first_team_i = 0
        self.current_player.set(f"Current Player: {self.teams[self.first_team_i].name}")

    def update_score(self):
        for i in range(len(self.teams)):
            self.vars[i].set(f"{self.teams[i].name}: {self.teams[i].score}")


if __name__ == "__main__":
    q = read_questions('questions/Round1.txt')
    import time
    time.sleep(3)
    window = tk.Tk('Ernie Bowl')
    team1 = Team("ABC")
    team2 = Team("BCD")
    RoundOne(window, [team1, team2], q)
    window.mainloop()
