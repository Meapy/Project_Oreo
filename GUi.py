#Description: This is a chat bot GUI
#Import the library
from tkinter import *
root = Tk()
root.title("Chat Bot")
root.geometry("400x500")
root.resizable(width=FALSE, height=FALSE)

main_menu = Menu(root)

# Create the submenu
file_menu = Menu(root)

# Add commands to submenu
file_menu.add_command(label="Can I have some thriller Movies")
file_menu.add_command(label="Can i see someDirectors")
file_menu.add_command(label="Can i see some Actors")
main_menu.add_cascade(label="Sample Questions", menu=file_menu)
#Add the rest of the menu options to the main menu
root.config(menu=main_menu)

chatWindow = Text(root, bd=1, bg="white",  width="50", height="8", font=("Arial", 15), foreground="black")
chatWindow.place(x=6,y=6, height=385, width=370)

messageWindow = Text(root, bd=0, bg="white",width="30", height="4", font=("Arial", 10), foreground="black")
messageWindow.place(x=128, y=400, height=88, width=260)

Button=Button(root, text="Send",  width="12", height=5,
                    bd=0, bg="#0080ff", activebackground="#00bfff",foreground='#ffffff',font=("Arial", 12))
Button.place(x=6, y=400, height=88)

#add a scroll bar
scrollbar =Scrollbar(root, command = chatWindow.yview())
scrollbar.place(x=375, y=5, height=385)

root.mainloop()