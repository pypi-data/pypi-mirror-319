import pipmanager as a 
import tkinter as tk

def main():
    a.root = tk.Tk()
    a.app = a.PipManagerApp(a.root)
    a.root.mainloop()