import pygetwindow as gw
import os

while len([window for window in gw.getWindowsWithTitle("Puxar partida no LOL") if window.title == "Puxar partida no LOL"]) > 0:
    try:
        for window in [window for window in gw.getWindowsWithTitle("Puxar partida no LOL") if window.title == "Puxar partida no LOL"]:
            window.close()
    except Exception as e:
        print(f"erro: {e}")
        input()

os.system('start "" "Puxar partida no LOL.lnk"')