#!/usr/bin/env python3

from typing import List

import pytermgui as ptg
import subprocess
import json
from threading import Thread
import time
from tkinter import Toplevel, Label
from PIL import Image, ImageTk



class RelicReward():
    def __init__(self, name, platinum, ducats, best) -> None:
        self.name = name
        self.platinum = platinum
        self.ducats = ducats
        self.best = best

def holding_splash() -> None:
    with ptg.WindowManager() as manager:
        manager.layout.add_slot('Body')
        manager.add(
            ptg.Window(
                "Waiting for Relic-Detection",
                )
            .set_title('Relic Companion')
            .center()
        )

def show_relic_loot(relicList: List) -> None:
    with ptg.WindowManager() as manager:
        manager.layout.add_slot('Body')
        relicContainers = []
        for relicLoot in relicList:
            container = ptg.Container(
                    f'{relicLoot.name}',
                    '',
                    f'{relicLoot.platinum} Platinum',
                    f'{relicLoot.ducats} Ducats',
                )
            if relicLoot.best:
                container.box = 'DOUBLE'
            relicContainers.append(
                container
            )

        window = (
            ptg.Window(
                ptg.Splitter(
                    *relicContainers
                    
                ),
                box="DOUBLE"
            )
            .set_title('Relic Companion')
            .center()
            
        )
        manager.add(window)

def run_wfinfo():
    wfinfo_path = '/home/jonas/code/wfinfo-ng-fork' # TODO fix paths being hardcoded
    command = '~/.cargo/bin/wfinfo ~/.steam/steam/steamapps/compatdata/230410/pfx/drive_c/users/steamuser/AppData/Local/Warframe/EE.log' # TODO fix path being hardcoded
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=wfinfo_path)
    return process

def read_output(process):
    relicList = []
    for line in process.stdout:
        # try to parse the line from json
        try:
            reward = json.loads(line)
            relic = RelicReward(reward['name'], reward['platinum'], reward['ducats'], reward['best'])
            relicList.append(relic)
            if len(relicList) == 4:
                show_relic_loot(relicList)
                relicList = []
        except json.JSONDecodeError:
            if line.decode().strip() == 'begin JSON':
                print('relic detected')
            elif line.decode().strip() == 'end JSON':
                print('relic ended')
                show_relic_loot(relicList)
                relicList = []
            continue
    for line in process.stderr:
        raise Exception(line.decode().strip())

def start():
    process = run_wfinfo()

    thread = Thread(target=read_output, args=(process,))
    thread.start()

    holding_splash()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        process.terminate()
        thread.join()

def start_debug():
    # spawn the test window in a thread
    test_window = Thread(target=TestWindow, args=(1,))
    test_window.start()
    time.sleep(1)

    wfinfo_process = run_wfinfo()

    wfinfo_thread = Thread(target=read_output, args=(wfinfo_process,))
    wfinfo_thread.start()

    holding_splash()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        wfinfo_process.terminate()
        wfinfo_thread.join()

class TestWindow(Toplevel):
    def __init__(self, image_number: int):
        Toplevel.__init__(self)
        self.title('Warframe')
        self.resizable(False, False)
        # embedd the image
        imageFile = f"tests/{image_number}.png"
        self.image1 = ImageTk.PhotoImage(Image.open(imageFile))

        # get the image size
        w = self.image1.width()
        h = self.image1.height()

        # position coordinates of root 'upper left corner'
        x = 0
        y = 0

        # make the root window the size of the image
        self.geometry("%dx%d+%d+%d" % (w, h, x, y))

        # root has no image argument, so use a label as a panel
        Label(self, image=self.image1).pack(fill='both', expand=True)
        print("Display image1")
        self.update()

    def callback(self):
        return True
