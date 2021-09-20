from collections import deque
from tkinter import *
from random import sample, shuffle, choice
from timeit import default_timer as timer


class Dict:
    def __init__(self, filename):
        self.words = []
        with open(filename) as file:
            self.words = [line.strip() for line in file]

    def get_next(self):
        return choice(self.words)

    def sample_words(self, count):
        return " ".join(sample(self.words, count))


class Statistics:
    def __init__(self):
        self.lasttime = 0
        self.lastspeed = 0
        self.samplesize = 0
        self.started = False

    def start(self):
        self.lasttime = timer()
        self.started = True

    def record(self, str):
        newtime = timer()
        difference = newtime - self.lasttime
        self.lasttime = newtime

        speed = 60 / (difference * (5 / (len(str) + 1)))
        self.samplesize += 1
        self.lastspeed += (speed - self.lastspeed) / self.samplesize

    def get_mean(self):
        return self.lastspeed


class Application(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack(side='top', fill='both', expand=True)
        self.dict = Dict("pop_dict.txt")
        self.stats = Statistics()
        self.create_widgets()

    def create_widgets(self):
        self.text = StringVar()
        self.text.set(self.dict.sample_words(10))

        self.text_field = Message(
            self, bg='papayawhip', fg='black', textvariable=self.text,
            font=("Courier", 14), anchor='s', width=500, justify='left')
        self.text_field.pack(ipadx=10, ipady=10, expand=True, fill='both')

        self.input_frame = Frame(self)
        self.input_frame.pack(fill='both', expand=True)

        self.input_field = Entry(
            self.input_frame, width=40, font=("Courier", 14))
        self.input_field.pack(ipadx=10, ipady=10)

        self.time_field = Label(self.input_frame, font=("Times New Roman", 14))
        self.time_field.pack(padx=10, pady=10)

        self.input_field.bind("<space>", self.space_pressed)
        self.input_field.bind("<BackSpace>", self.backspace_pressed)
        self.input_field.bind("<Key>", self.key_pressed)

        self.input_field.focus()

    def space_pressed(self, event):
        (first, rest) = self.text.get().split(maxsplit=1)

        if first != self.input_field.get():
            self.flash_red()
        else:
            self.stats.record(first)
            self.text.set(rest + ' ' + self.dict.get_next())
            self.time_field["text"] = "{:.2f}".format(
                self.stats.get_mean()) + " WPM"
            self.clear_text()
        return "break"

    def backspace_pressed(self, event):
        if event.state & 0x0004:
            self.clear_text()
            return "break"

    def key_pressed(self, event):
        if(self.stats.started == False):
            self.stats.start()

    def clear_text(self):
        self.input_field.delete(0, 'end')

    def change_back(self):
        self.input_field["bg"] = "white"

    def flash_red(self):
        self.input_field["bg"] = "red"

        self.after(500, self.change_back)


root = Tk()
root.title('Typing practice')
root.geometry("720x480")

app = Application(root)
app.mainloop()
