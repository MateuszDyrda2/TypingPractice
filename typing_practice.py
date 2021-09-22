from tkinter import *
from random import sample,  choice
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

    def reset(self):
        self.lastspeed = 0
        self.lasttime = 0
        self.samplesize = 0
        self.started = False


class Application(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack(side='top', fill='both', expand=True)
        self.dict = Dict("resources/pop_dict.txt")
        self.stats = Statistics()
        self.create_widgets()

    def create_widgets(self):
        self.text = StringVar()
        self.text.set(self.dict.sample_words(10))

        self.text_frame = Frame(self, bg='papayawhip')
        self.text_frame.pack(ipadx=10, ipady=10, expand=True, fill='both')

        self.text_field = Label(
            self.text_frame, bg='papayawhip', fg='black', textvariable=self.text,
            font=("Courier", 16), anchor='sw', width=500, justify='left')
        self.text_field.pack(padx=(120, 120), fill='both', side='bottom')

        self.input_frame = Frame(self, bg='wheat')
        self.input_frame.pack(fill='both', expand=True)

        self.input_field = Entry(
            self.input_frame, width=40, font=("Courier", 14))
        self.input_field.pack(padx=120, fill='both', ipady=10)

        self.time_field = Label(self.input_frame, font=(
            "Times New Roman", 14), bg='wheat', text='0.00 WPM')
        self.time_field.pack(padx=10, pady=10)

        self.pause_button = Button(
            self.input_frame, command=self.pause, text="Pause", font=("Times New Roman", 14), bg='tan', activebackground='wheat')
        self.pause_button.pack(pady=5)

        self.reset_button = Button(
            self.input_frame, command=self.reset, text="Reset", font=("Times New Roman", 14), bg='tan', activebackground='wheat')
        self.reset_button.pack(pady=5)

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

    def pause(self):
        self.focus()
        self.stats.started = False

    def reset(self):
        self.focus()
        self.text.set(self.dict.sample_words(10))
        self.stats.reset()
        self.clear_text()


root = Tk()
root.title('Typing practice')
w = 720
h = 480
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
x = (ws / 2) - (w / 2)
y = (hs / 2) - (h / 2)

root.geometry('%dx%d+%d+%d' % (w, h, x, y))

app = Application(root)
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Pause", command=app.pause)
filemenu.add_command(label="Reset", command=app.reset)

filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

root.iconphoto(False, PhotoImage(file="resources/icon.png"))
root.config(menu=menubar)
app.mainloop()
