# !/usr/bin/env python3
# -*- coding: utf-8 -*-

try :
    import sys
    from src.widget.mainWindow import MainWindows
    from PySide6.QtWidgets import QApplication
    from PySide6.QtGui import QScreen

    game_size = {"X": 3, "Y": 3, "Z": 3, "W": 3}
    bombs = 5


    app = QApplication(sys.argv)

    main_window = MainWindows(game_size, bombs)
    main_window.show()

    center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
    geo = main_window.frameGeometry()
    geo.moveCenter(center)
    main_window.move(geo.topLeft())

    sys.exit(app.exec())
    
except ModuleNotFoundError as e:
    # tinker message for the user
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Error", f"ModuleNotFoundError : {e}\n\nPlease install the required modules with the command :\npip install -r requirements.txt")
    root.destroy()
    sys.exit(1)
    
except Exception as e:
    # tinker message for the user
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Error", f"An error occured : {e}")
    root.destroy()
    sys.exit(1)
