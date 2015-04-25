from Tkinter import *
import ttk

class Application:

    def __init__(self, parent):
        self.parent = parent
        self.combo()

    def combo(self):
        self.box_value = StringVar()
        self.box = ttk.Combobox(self.parent, textvariable=self.box_value, 
                                state='readonly')
        self.box['values'] = ('A', 'B', 'C')
        self.box.current(0)
        self.box.grid(column=0, row=0)

if __name__ == '__main__':
    root = Tk()
    root.geometry("400x400")
    app = Application(root)
    root.mainloop()