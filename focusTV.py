#!/usr/bin/env python
import cv2
import platform
import time
import numpy as np
import os
import re

__author__ = "Amar Lakshya"
__copyright__ = "Copyright 2016"
__credits__ = ["Amar Lakshya"]
__license__ = "CC"
__version__ = "0.2"
__maintainer__ = "AmarLakshya"
__email__ = "amarlakshya1@gmail.com"
__status__ = "Production"

youtube = "YouTube"
vlc = "VLC"
VK_CODE = {'spacebar':0x20}
cascPath = os.path.dirname("./haarcascade_frontalface_alt.xml")
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")


class focus():
    """
    Creates a class named focus (so yeah, documentation.)
    """
    def getOS(self):
        """
        Params - None
        Returns - returns a very helpful string according to the current operating platform
        Does - Checks and returns the name of the current operating system.
        """
        if 'Linux' in platform.platform():
            return 'Linux'
        elif 'Windows' in platform.platform():
            return 'Windows'

    def inFocus(self,this):
        """
        Params - takes in the application to check the focus for.
        Returns - Gives a yes '1' if application in focus. (pretty much cross-platform)
        Does - Checks if an application is in focus.
        """
        focus = ""
        if self.getOS() == 'Windows':
            from win32gui import GetWindowText, GetForegroundWindow
            focus =  GetWindowText(GetForegroundWindow())
            if(this in focus):
                return 0
            else:
                return 1 if (this in focus ) else 0

        if self.getOS() == 'Linux':
            from subprocess import PIPE, Popen
            title = ''
            root_check = ''
            root = Popen(['xprop', '-root'],  stdout=PIPE)
            if root.stdout != root_check:
                root_check = root.stdout
                for i in root.stdout:
                    if '_NET_ACTIVE_WINDOW(WINDOW):' in i:
                        id_ = i.split()[4]
                        id_w = Popen(['xprop', '-id', id_], stdout=PIPE)
                for j in id_w.stdout:
                    if 'WM_NAME(STRING)' in j:
                            if title != j.split()[2]:
                                focus = j[2:]
            print focus
            if(this in focus[22:30]):
                return 0
            else:
                return 1 if (this in focus) else 0
        return -2

    def pressLin(self):
        """
        Params - None
        Returns - None
        Does - Presses space-bar key on Linux
        """
        from evdev import uinput, ecodes as e
        with uinput.UInput() as ui:
            ui.write(e.EV_KEY, e.KEY_SPACE, 1)
            ui.write(e.EV_KEY, e.KEY_SPACE, 0)
            ui.syn()


    def pressWin(self):
        """
        Params - None
        Returns - None
        Does - Presses space-bar key on Windows
        """
        import win32api,win32con
        win32api.SetCursorPos((100,100))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,100,100,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,100,100,0,0)
        time.sleep(1)
        win32api.keybd_event(VK_CODE['spacebar'], 0,0,0)
        time.sleep(.05)
        win32api.keybd_event(VK_CODE['spacebar'],0 ,win32con.KEYEVENTF_KEYUP ,0)

    def enableClickOnYouTubeHackLin(self):
        """
        Params - None
        Returns - None
        Does - A very dirty hack to get access to pausing video on youtube by pressing left-mouse key over the video first. (sorry)
        """
        if(self.inFocus(youtube)) :
            from evdev import uinput, ecodes as e
            capabilities = {
                            e.EV_ABS : (e.ABS_X, e.ABS_Y),
                            e.EV_KEY : (e.BTN_LEFT, e.BTN_RIGHT),
                            }
            with uinput.UInput(capabilities) as ui:
                ui.write(e.EV_ABS, e.ABS_X, 200)
                ui.write(e.EV_ABS, e.ABS_Y, 200)
                ui.write(e.EV_KEY, e.BTN_LEFT, 1)
                ui.write(e.EV_KEY, e.BTN_LEFT, 0)
                time.sleep(.05)
                ui.syn()

    def headtracker(self):
        """
        Params - None
        Returns - None
        Does - Pretty much does most of the stuff, face-detection and the resulting pressing stuff.
        """
        c = 0
        video_capture = cv2.VideoCapture(0)
        flag = 1
        if self.getOS() == 'Linux':
            self.enableClickOnYouTubeHackLin() # As always with binary constructions of our kind ;)
            doThis = self.pressLin
        elif self.getOS() == 'Windows':
            self.enableClickOnYouTubeHackLin() # TODOsssss for Windows
            doThis = self.pressWin

        while True:
            while ((self.inFocus(vlc) or self.inFocus(youtube))):
                # Capture frame-by-frame
                ret, frame = video_capture.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # FACES ATTRIBUTES
                gray = np.array(gray, dtype='uint8')
                faces = faceCascade.detectMultiScale(gray, 1.3, 5)
                if len(faces) == 0 and c == 0:
                    c = 1
                    try:
                        doThis()
                        # No One is sitting There
                        flag = 0
                    except:
                        pass
                elif len(faces) != 0 and flag == 0 :
                    c = 0
                    try:
                        doThis()
                        # Some One is Sitting There
                        flag = 1
                    except:
                        pass
        video_capture.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    time.sleep(2)	# Just wait a little bit for the user to catch up
    track = focus()
    track.headtracker()

