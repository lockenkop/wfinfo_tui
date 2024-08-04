from wfinfo_tui import main
from PIL import Image, ImageTk
from tkinter import Toplevel, Label, Tk, TOP, BOTH, YES
from time import sleep


def test_detection():
    test_window = main.TestWindow(1)
    print('test')
    main.start()
