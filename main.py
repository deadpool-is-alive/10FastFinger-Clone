import tkinter as tk
from tkinter import *
import random


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1080x720")
        self.title("Typing Master LOCAL")
        self.iconphoto(True, tk.PhotoImage(file='icon.png'))

        

        self.default_time = 60
        self.time_left = self.default_time
        self.timer_running = False
        self.characters = 0
        self.default_index = "1.0"
        self.next_index = self.default_index
        self.finished = False

        
        
        
        self.label = tk.Label(self, font=("Arial", 10))
        self.label.pack(pady=20)
        
        self.total = 0
        self.current = 0

        self.para_widget = tk.Text(
            self, 
            wrap="word", 
            font=("Arial", 15), 
            height=1
            )
        self.para_widget.pack(fill="both", expand=True, padx=10, pady=10)
        self.para_widget.config(state="disabled")
        self.para_list = self.para_func()
        self.length = len(self.para_list)
        self.color_current_word()



        self.speed = tk.Label(self, text="Typing Speed: 0 WPM", font=("Arial", 10))

        tk.Button(self, text = "Start Timer", command = self.start_timer).pack(pady=10)
        tk.Button(self, text = "Pause Timer", command = self.pause_timer).pack(pady=10)
        tk.Button(self, text = "Reset Timer", command = self.reset_timer).pack(pady=10)
        
        #tk.Label(self, text="test example").pack(side=tk.LEFT)
        self.entry = tk.Entry(self, state=tk.DISABLED, width=50, font=("Arial", 15), bd = 5)
        self.entry.pack(pady=20)

        self.entry.bind("<space>", self.check_word)

        self.countdown()

    def check_word(self, event):
        word = self.entry.get().strip()

        start = self.next_index
        end = f"{start}+{len(self.para_list[self.current])}c"

        self.para_widget.config(state="normal")

        self.para_widget.tag_remove("current", "1.0", "end")
        
        if word == self.para_list[self.current]:
            self.para_widget.tag_add("correct", start, end)
            self.total += len(word)
        else:
            self.para_widget.tag_add("wrong", start, end)
        
        self.para_widget.config(state="disabled")
        
        self.current += 1
        self.next_index = f"{end}+1c"

        self.color_current_word()
        

        if(self.current == self.length):
            self.finish()

        self.entry.delete(0, tk.END)
        return "break"
    
    def color_current_word(self):
        if(self.current >= len(self.para_list)):
            self.finish()
            return

        word = self.para_list[self.current]
        start = self.next_index
        end_index = f"{self.next_index}+{len(word)}c"

        self.para_widget.config(state="normal")

        self.para_widget.tag_remove(f"current", "1.0", "end")

        self.para_widget.tag_add(f"current", start, end_index)

        self.para_widget.tag_config(f"current", background="grey", foreground="black")
        self.para_widget.tag_config(f"correct", background="white", foreground="green")
        self.para_widget.tag_config(f"wrong", background="white", foreground="red")
        self.para_widget.config(state="disabled")

    def countdown(self):
        if self.timer_running:
            self.time_left -= 1
            if self.time_left >= 0:
                    self.update_label()
                    self.after_id = self.after(1000, self.countdown)
            else:
                self.finish()

    def update_label(self):
        mins, secs = divmod(self.time_left, 60)
        if(self.timer_running):
            self.label.config(text=f"{mins:02d}:{secs:02d}")

    def finish(self):
        self.entry.delete(0, tk.END)
        self.entry.unbind("<space>")
        self.finished = True
        print("Completed")
        print(f"Your typing speed = {self.total / (self.default_time - self.time_left) * 12}")
        self.speed.config(text=f"Typing Speed: {int(self.total / (self.default_time - self.time_left) * 12)} WPM")
        self.speed.pack(pady=10)
        self.pause_timer()
    
    def start_timer(self):
        self.entry.bind("<space>", self.check_word)
        if(not self.timer_running and not self.finished):
            self.timer_running = True
            self.update_label()
            self.after_id = self.after(1000, self.countdown)
            self.entry.config(state=tk.NORMAL)
        elif (self.finished):
            self.reset_timer()

    def pause_timer(self):
        if(self.timer_running):
            self.timer_running = False
            self.entry.config(state=tk.DISABLED)
        
    def reset_timer(self):
        self.entry.delete(0, tk.END)
        self.pause_timer()
        self.finished = False
        self.para_list = self.para_func()
        self.length = len(self.para_list)
        self.total = 0
        self.current = 0
        self.next_index = self.default_index

        if self.after_id is not None:
            self.after_cancel(self.after_id)

            self.time_left = self.default_time

    def para_func(self):
        
        with open("quotes.txt", "r", encoding="utf-8") as f:
            self.para = random.choice(f.readlines()).strip()
        # self.para_text = tk.Label(self, text = self.para,wraplength=400, justify="left", font = ("Arial", 15))
        # self.para_text.pack(pady=20)

        self.para_widget.config(state="normal")

        self.para_widget.delete("1.0", "end")

        self.para_widget.insert("1.0", self.para)

        self.para_widget.config(state="disabled")

        
        self.para_list = self.para.split()


        return self.para_list


app = App()


app.mainloop()
    
