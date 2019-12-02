from Tkinter import Button, Tk

from PyQt5.QtWidgets import QApplication, QPushButton, QWidget



class Button:
    root = Tk()
    root.title("Interface!")
    root.geometry("300x150+50+50")

    # Create a button that will print the contents of the entry
    start = Button(root, text='Fish', command='fish')
    stop = Button(root, text='Stop', command='stop')
    start.grid()
    stop.grid()

    root.mainloop()


# class Button(QWidget):
#     def __init__(self):
#         super().__init__()
#
#         start = QPushButton('Start!', self)
#         start.move(30, 5)
#
#         stop = QPushButton('Stop!', self)
#         stop.move(100, 5)
#
#         start.clicked.connect(self.Start_Bot)
#         stop.clicked.connect(self.exit_bot)
#
#         self.setGeometry(0,595,800,50)
#         self.setWindowTitle("Interface!")
#
#     def Start_Bot(self):
#         print('Starting a Thread with Main')
#         Thread(target=main).start()
#
#
#     def exit_bot(self):
#         print('Exiting the Client')
#         exit()


app = QApplication([])
button = Button()
button.show()
#app.exec()
#https://www.devdungeon.com/content/gui-programming-python

"""
window.move(0,555)
window.resize(800,100)
window.setLayout(layout)
window.show()
"""