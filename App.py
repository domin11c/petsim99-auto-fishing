from PIL import ImageGrab
from time import sleep
import numpy as np
import win32api
import win32con
import win32gui

Width, Height = (
    win32api.GetSystemMetrics(0),
    win32api.GetSystemMetrics(1)
)
Padding = 50

class Colors:
    Bobber = (235, 0, 0)
    Wave = (203, 255, 255)
    Bar = (180, 183, 206)
    
def MouseDown() -> None:
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)

def MouseUp() -> None:
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def MouseClick() -> None:
    MouseDown()
    MouseUp()

def MouseHold(Secs: float) -> None:
    MouseDown()
    sleep(Secs)
    MouseUp()

def GetScreenshot(X: int = 0, Y: int = 0, Width: int = Width, Height: int = Height) -> list[int]:
    return np.array(ImageGrab.grab(bbox=(
        X,
        Y,
        Width,
        Height
    )))

def FindColor(Image: list[int], Color: tuple[int]):
    R, G, B = Color
    Results = np.where((Image[:, :, 0] == R) & (Image[:, :, 1] == G) & (Image[:, :, 2] == B))

    if len(Results[0]) > 0:
        return (Results[1][0], Results[0][0])

def Main():
    while True:
        sleep(0.1)

        Hwnd = win32gui.FindWindow(None, 'Roblox')
        if Hwnd == 0 or win32gui.GetForegroundWindow() != Hwnd:
            continue

        if FindColor(GetScreenshot(), Colors.Wave):
            win32gui.GetCursorPos()
            MouseClick()

            while True:
                sleep(0.1)

                if win32gui.GetForegroundWindow() != Hwnd:
                    break

                if FindColor(GetScreenshot(), Colors.Bobber) is None:
                    sleep(2)
                    MouseClick()
                    sleep(2)
                    break

                if FindColor(GetScreenshot(Height=Height // 2 - Padding), Colors.Bobber):
                    MouseDown()
                elif FindColor(GetScreenshot(Y=Height // 2 + Padding), Colors.Bobber):
                    MouseUp()
                else:
                    if not FindColor(GetScreenshot(Height=Height // 2 - Padding), Colors.Bar):
                        MouseHold(1)
                    else:
                        MouseUp()

if __name__ == '__main__':
    Main()