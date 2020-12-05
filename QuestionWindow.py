from Question import *
from Team import *
import random
import tkinter as tk
from PIL import Image, ImageTk

class QuestionWindow:
    def __init__(self, parent, quest, point, team1, team2):
        self.count = 0
        self.buttons = []
        self.point = int(point)
        self.team1 = team1
        self.team2 = team2

        self.var = tk.StringVar()
        self.top = tk.Toplevel(parent)

        # title
        title = tk.Label(self.top, text=quest.question).pack()

        if quest.image:
            load = Image.open("images/" + quest.image)
            render = ImageTk.PhotoImage(load)
            img = tk.Label(self.top, image=render)
            img.image = render
            img.pack()

        self.window = tk.Frame(self.top)
        self.window.pack()

        # answer list and shuffle
        self.answer = quest.correctAnswer
        quest.incorrectAnswers.append(self.answer)
        random.shuffle(quest.incorrectAnswers)

        # create answer button
        self.answer_f = tk.Frame(self.window)
        self.answer_f.grid(column=0, row=1, columnspan=5, rowspan=5, pady=5)
        index = 0
        for a in quest.incorrectAnswers:
            if a == self.answer:
                self.buttons.append(self.create_answer_button(a, True, index))
            else:
                self.buttons.append(self.create_answer_button(a, False, index))
            self.buttons[index].grid()
            index += 1

        self.tool_f = tk.Frame(self.window)
        self.tool_f.grid(column=5, row=1, columnspan=5, rowspan=5, pady=5)
        # answer suggestion label
        self.answer_sug = tk.StringVar()
        answer_sug_label = tk.Label(self.tool_f, textvariable=self.answer_sug, relief="sunken", width=15, padx=5, pady=5)
        answer_sug_label.grid()

        tk.Button(self.tool_f, text="Show answer", command=lambda: self.show_answer()).grid()

        self.top.transient()
        self.top.wait_visibility()
        self.top.grab_set()
        self.top.wait_window()

    def show_answer(self):
        self.answer_sug.set(self.answer)

    def create_answer_button(self, text, correct, index):
        return tk.Button(self.answer_f, text=text, command=lambda: self.choose_answer(correct, index))

    def choose_answer(self, correct, i):
        # first click is correct
        if correct and not self.count:
            self.team1.score += self.point
            self.count = 5
            self.answer_sug.set("You are right!!!")
        # second click is correct
        elif correct and self.count == 1:
            self.team2.score += (self.point - 1)
            self.count = 5
            self.answer_sug.set("You are right!!!")
        # second click is wrong
        elif not correct and self.count == 1:
            self.team2.score -= 1
            self.count += 1
            self.answer_sug.set("Opps!!!")
        else:
            self.answer_sug.set("Opps!!!")
            self.count += 1
        self.buttons[i]['state'] = 'disabled'

        # update score
        print(self.team1.score, self.team2.score)


if __name__ == "__main__":
    q = Question()
    q.question = "what is your name"
    q.correctAnswer = "abc"
    q.incorrectAnswers = ["bca", "ca", "rand"]
    QuestionWindow(q, 3, Team("Calvin"), Team("Albert"))
