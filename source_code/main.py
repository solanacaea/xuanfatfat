# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# set-ExecutionPolicy RemoteSigned
# pip install --upgrade pip
#

# import pyautogui
# pyautogui.press(['4','5','space'], interval=0.1)
# pyautogui.prompt(text='请输入', title='PyAutoGUI消息框', default='请输入按键')

import tkinter as tk
from tkinter import ttk
import time
import pygame
import webbrowser
import sys
import os
import pickle
from ctypes import *
from single import SinglePanel
from multiple_simple import MultiplePanel
from help import HelpPanel
from gitlab_grab import get_latest_footer, default_version
from tuopan import SysTrayIcon

pang_title = f'小胖按键 {default_version}'

window = tk.Tk()
window.resizable(width=False, height=False)
window.title(pang_title)
window.geometry('280x270+200+100')
single_panel = None
multiple_panel = None


def resource_path(relative_path, perm_temp=False):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    if perm_temp is True:
        base_path = base_path[0:base_path.rfind("\\")]
    return os.path.join(base_path, relative_path)


def _load_resource():
    start_filename = resource_path(os.path.join("data", "vuvj7-xivte.wav"))
    end_filename = resource_path(os.path.join("data", "8e6go-2nedg.wav"))
    dd_filename = resource_path(os.path.join("data", "DD94687.64.dll"))
    icon_filename = resource_path(os.path.join("data", "fat2.ico"))

    pygame.mixer.init()
    start_tracker = pygame.mixer.Sound(start_filename)
    end_tracker = pygame.mixer.Sound(end_filename)
    dd_dll = windll.LoadLibrary(dd_filename)

    time.sleep(1)
    return dd_dll, start_tracker, end_tracker, icon_filename


def _get_user_data():
    # history_filename = resource_path(os.path.join("data"), perm_temp=True)
    history_filename = "user_data.conf"
    user_data = None
    try:
        user_his = open(fr"{history_filename}", 'rb')
        user_data = pickle.load(user_his)
    except Exception as e:
        print(f"user file not exist. cur_path: {history_filename}")
        return {}, history_filename
    return user_data, history_filename


# if time.time() > 1656604800.0:
#     print("Expired")
#     sys.exit(100)


def _check_ddl(dd_dll):
    st = dd_dll.DD_btn(0)
    if st == 1:
        print("OK")
    else:
        print("驱动加载失败")
        sys.exit(101)


def _load_foot(history_path, _user_data):
    ad_title, line1, line2, curr_version = get_latest_footer(history_path, _user_data)
    ready_warn = tk.Label(window, text=ad_title)
    ready_warn.place(x=8, y=170)
    ready_warn = tk.Label(window, text=line1, fg='blue')
    ready_warn.place(x=8, y=195)
    ready_warn = tk.Label(window, text=line2, fg='blue')
    ready_warn.place(x=8, y=215)
    ready_warn = tk.Label(window, text="®不定时更新地址:", fg='blue')
    ready_warn.place(x=8, y=235)
    ready_warn = tk.Label(window, text="小胖网站", fg='blue', cursor="hand2")
    ready_warn.place(x=110, y=235)
    xp_address = "https://github.com/solanacaea/xuanfatfat"
    ready_warn.bind("<Button-1>", lambda event: webbrowser.open(xp_address))
    ready_warn = tk.Label(window, text=f"@最新版本: {curr_version}", fg='blue')
    ready_warn.place(x=160, y=235)
    # ready_warn = tkinter.Label(window, text="®玩游戏吃零食上淘宝搜索<心筑月>", fg='blue', cursor="hand2")
    # ready_warn.place(x=10, y=180)
    # xzy_url = "https://shop316822115.taobao.com/shop/view_shop.htm?spm=a230r.1.14.15.6b994a18VBoSat&user_number_id=3318437303"
    # ready_warn.bind("<Button-1>", lambda event: webbrowser.open(xzy_url))


def _close_handler():
    single_panel.close_handler()
    window.destroy()


def _init_tray(win, icon, hover_text="小胖按键"):
    menu_options = (('显示', None, _show_xiaopang), )
    tray_instance = SysTrayIcon(
        icon,
        hover_text,
        menu_options,
        on_quit=_close_handler,
        tk_window=win,
    )

    win.bind(
        "<Unmap>",
        lambda event: _hidden_window(win, tray_instance) if win.state() == 'iconic' else False
    )


def _show_xiaopang(_sysTrayIcon):
    _sysTrayIcon.destroy(exit=0)
    # _sysTrayIcon.refresh()


def _hidden_window(win, tray_instance):
    win.withdraw()
    tray_instance.activation()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    dd_dll_m, start_tracker_m, end_tracker_m, icon_m = _load_resource()
    _check_ddl(dd_dll_m)
    user_data_m, history_filename_m = _get_user_data()

    window.iconbitmap(icon_m)
    tabs = ttk.Notebook(window)
    frame1 = tk.Frame(tabs)
    tabs.add(frame1, text="单按键")
    frame2 = tk.Frame(tabs)
    tabs.add(frame2, text="多按键")
    frame3 = tk.Frame(tabs)
    tabs.add(frame3, text="帮助")
    tabs.pack(expand=True, fill=tk.BOTH)

    single_panel = SinglePanel(dd_dll_m, frame1, user_data_m, history_filename_m, start_tracker_m, end_tracker_m)
    single_panel.load_entries()

    multiple_panel = MultiplePanel(
        dd_dll=dd_dll_m, window=frame2, user_data=user_data_m,
        start_tracker=start_tracker_m, end_tracker=end_tracker_m,
        single_panel=single_panel, icon=icon_m, logo=None
    )
    multiple_panel.load()

    help_panel = HelpPanel(frame3)
    help_panel.popup()

    _load_foot(history_filename_m, user_data_m)
    _init_tray(window, icon_m)
    window.protocol("WM_DELETE_WINDOW", _close_handler)
    window.mainloop()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
