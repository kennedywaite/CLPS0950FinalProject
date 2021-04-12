import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import tkinter

def q3(s, i) :  
    if (i == len(s)) :  
        tkinter.messagebox.showinfo('Answer',"REJECTED")
        return;  

    if (s[i] == 'a') : 
        q3(s, i + 1);  
    elif (s[i] == 'b'):
        q3(s, i + 1);   

root = tk.Tk()
root.withdraw()
user_inp = simpledialog.askstring(title="DFA", prompt="Enter a string within the alphabet {a,b}* Suffix must be bb")