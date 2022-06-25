import tkinter
import time
import threading
import pickle
from global_hotkeys import register_hotkey, remove_hotkey, clear_hotkeys, \
    start_checking_hotkeys, stop_checking_hotkeys
from tkinter import ttk


class Job(threading.Thread):

    def __init__(self, press_key, interval, dd_dll, *args, **kwargs):
        super(Job, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()     # 用于暂停线程的标识
        self.__flag.set()       # 设置为True
        self.__running = threading.Event()      # 用于停止线程的标识
        self.__running.set()      # 将running设置为True
        self.press_key = press_key
        self.interval = interval
        self.dd_dll = dd_dll

    def run(self):
        while self.__running.is_set():
            self.__flag.wait()      # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回
            time.sleep(self.interval)
            self.dd_dll.DD_key(self.press_key, 1)
            self.dd_dll.DD_key(self.press_key, 2)
            # print(f"pressing key={self.press_key}")
            # pydirectinput.click()

    def pause(self):
        self.__flag.clear()     # 设置3为False, 让线程阻塞

    def resume(self):
        self.__flag.set()    # 设置为True, 让线程停止阻塞

    def stop(self):
        self.__flag.set()       # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear()

    def is_active(self):
        return self.__running.is_set()


# 48-57
num_start = 48
num_key = [num_start + i for i in range(0, 10)]

# 65-90
alpha_start_1 = 65
alpha_key_1 = [alpha_start_1 + i for i in range(0, 26)]

# 97-122
# alpha_start_2 = 97
# alpha_key_2 = [alpha_start_2 + i for i in range(0, 26)]

other_key = [
    186, 187, 188, 189, 190, 191, 219, 220, 221, 222,
    45, 61, 12304, 12305, 12289, 65307, 8216, 65292, 12290, 183
]
num_key.extend(alpha_key_1)
# num_key.extend(alpha_key_2)
num_key.extend(other_key)

ignore_keys = [8, 9, 13, 18, 229]
back_space_key = 8
dd_key_map = {
    "f1": 101, "f2": 102, "f3": 103, "f4": 104, "f5": 105, "f6": 106, "f7": 107, "f8": 108, "f9": 109, "f10": 110, "f11": 111, "f12": 112,
    "`": 200, "·": 200, "1": 201, "2": 202, "3": 203, "4": 204, "5": 205, "6": 206, "7": 207, "8": 208, "9": 209, "0": 210, "-": 211, "=": 212,
    "tab": 300, "q": 301, "w": 302, "e": 303, "r": 304, "t": 305, "y": 306, "u": 307, "i": 308, "o": 309, "p": 310, "[": 311, "]": 312,
    "caps_lock": 400, "a": 401, "s": 402, "d": 403, "f": 404, "g": 405, "h": 406, "j": 407, "k": 408, "l": 409, ";": 410, "'": 411,
    "shift_l": 500, "z": 501, "x": 502, "c": 503, "v": 504, "b": 505, "n": 506, "m": 507, ",": 508, ".": 509, "/": 510, "shift_r": 511,
    "control_l": 600, "alt_l": 602, "space": 603,
    "up": 709, "left": 710, "down": 711, "right": 712
}

new_thread = None


def save_user_data(data_path, user_history_data):
    user_file = open(fr"{data_path}", 'wb')
    pickle.dump(user_history_data, user_file)
    print(f"saved new user data to {data_path}")


class SinglePanel(object):
    def __init__(self, dd_dll, window, user_data, history_filename, start_tracker, end_tracker):
        self.dd_dll = dd_dll
        self.window = window
        self.start_tracker = start_tracker
        self.end_tracker = end_tracker
        self.user_data = user_data
        self.history_filename = history_filename
        self.auto_key_value = None
        self.interval_value = None
        self.start_key_value = None
        self.end_key_value = None
        self.new_thread = None
        self.last_start_hot_key = None
        self.last_end_hot_key = None

        self.auto_tk_var = tkinter.StringVar()
        self.interval_tk_var = tkinter.StringVar()
        self.start_tk_var = tkinter.StringVar()
        self.end_tk_var = tkinter.StringVar()
        self.ready_tk_var = tkinter.StringVar()

    def load_entries(self):
        self._load_auto_entry()
        self._load_interval_entry()
        self._load_start_entry()
        self._load_end_entry()
        self._load_publish_entry()
        self._load_cache()

    def _load_auto_entry(self):
        l1 = tkinter.Label(self.window, text='自动按键:')
        l1.place(x=10, y=10)
        e1 = tkinter.Entry(self.window, width=10)
        e1.place(x=80, y=10)
        self.e1 = e1
        e1.bind(sequence="<KeyPress>", func=self._key_input_event)
        auto_warn = tkinter.Label(self.window, textvariable=self.auto_tk_var, fg='#FF0000')
        auto_warn.place(x=160, y=10)

    def _load_interval_entry(self):
        l_interval = tkinter.Label(self.window, text='间隔(秒):')
        l_interval.place(x=10, y=35)
        e_interval = tkinter.Entry(self.window, width=10)
        e_interval.place(x=80, y=35)
        self.e_interval = e_interval
        e_interval.bind(sequence="<KeyRelease>", func=self._interval_input_event)
        interval_warn = tkinter.Label(self.window, textvariable=self.interval_tk_var, fg='#FF0000')
        interval_warn.place(x=160, y=35)

    def _load_start_entry(self):
        l2 = tkinter.Label(self.window, text='开启热键:')
        l2.place(x=10, y=60)
        e2 = tkinter.Entry(self.window, width=10)
        e2.place(x=80, y=60)
        e2.bind(sequence="<KeyPress>", func=self._start_key_input)
        self.e2 = e2
        start_warn = tkinter.Label(self.window, textvariable=self.start_tk_var, fg='#FF0000')
        start_warn.place(x=160, y=60)

    def _load_end_entry(self):
        l3 = tkinter.Label(self.window, text='结束热键:')
        l3.place(x=10, y=85)
        e3 = tkinter.Entry(self.window, width=10)
        e3.place(x=80, y=85)
        e3.bind(sequence="<KeyPress>", func=self._end_key_input)
        self.e3 = e3
        end_warn = tkinter.Label(self.window, textvariable=self.end_tk_var, fg='#FF0000')
        end_warn.place(x=160, y=85)

    def _load_publish_entry(self):
        l4 = tkinter.Label(self.window, text='点击按钮完成发布:')
        l4.place(x=10, y=115)
        b1 = ttk.Button(self.window, text="完成", command=self._complete_button_handler)
        b1.place(x=136, y=125, height=28, width=40, anchor="center")
        self.b1 = b1
        ready_warn = tkinter.Label(self.window, textvariable=self.ready_tk_var, fg='#556B2F')
        ready_warn.place(x=160, y=115)

    def _load_cache(self):
        if self.user_data is not None and "auto" in self.user_data:
            self.auto_key_value = self.user_data.get("auto")
            self.start_key_value = self.user_data.get("start")
            self.end_key_value = self.user_data.get("end")
            self.interval_value = self.user_data.get("interval")

            self.e1.insert(0, self.user_data.get("auto"))
            self.e_interval.insert(0, self.user_data.get("interval"))
            self.e2.insert(0, self.user_data.get("start"))
            self.e3.insert(0, self.user_data.get("end"))

    def _key_input_event(self, event):
        if event.keycode == back_space_key:
            self.auto_key_value = None
            return

        if event.keycode in ignore_keys:
            return

        self.e1.delete(0, "end")
        if event.keycode not in num_key:
            if event.char == '':
                self.e1.insert(0, event.keysym)

        if event.char != '':
            self.auto_key_value = event.char
        else:
            self.auto_key_value = event.keysym
        self.auto_tk_var.set("")

        if self.auto_key_value.lower() not in dd_key_map:
            self.auto_tk_var.set("请换个按键！")

    def _start_key_input(self, event):
        if event.keycode == back_space_key:
            self.start_key_value = None
            return

        if event.keycode in ignore_keys:
            return

        self.e2.delete(0, "end")
        if event.keycode not in num_key:
            if event.char == '':
                self.e2.insert(0, event.keysym)
        self.start_key_value = event.keysym
        self.start_tk_var.set("")

    def _end_key_input(self, event):
        if event.keycode == back_space_key:
            self.end_key_value = None
            return

        if event.keycode in ignore_keys:
            return

        self.e3.delete(0, "end")
        if event.keycode not in num_key:
            if event.char == '':
                self.e3.insert(0, event.keysym)
        self.end_key_value = event.keysym
        self.end_tk_var.set("")

    def _interval_input_event(self, event):
        if event.keycode == back_space_key:
            self.interval_value = None
            return
        try:
            self.interval_value = float(self.e_interval.get())
            self.interval_tk_var.set("")
        except:
            self.interval_tk_var.set("请输入数字！")
            self.e_interval.delete(0, "end")

    def _complete_button_handler(self):
        print(f"auto_key_value={self.auto_key_value}, "
              f"start_key_value={self.start_key_value}, "
              f"end_key_value={self.end_key_value}")
        self.b1.focus_set()

        if self.start_key_value is None \
                or self.end_key_value is None \
                or self.auto_key_value is None\
                or self.interval_value is None:
            if self.auto_key_value is None:
                self.auto_tk_var.set("请设置按键！")
            else:
                self.auto_tk_var.set("")
            if self.start_key_value is None:
                self.start_tk_var.set("请设置按键！")
            else:
                self.start_tk_var.set("")
            if self.end_key_value is None:
                self.end_tk_var.set("请设置按键！")
            else:
                self.end_tk_var.set("")
            if self.interval_value is None:
                self.interval_tk_var.set("请设置时间！")
            else:
                self.interval_tk_var.set("")
            self.ready_tk_var.set("")
            return
        else:
            if str(self.auto_key_value).lower() not in dd_key_map:
                self.auto_tk_var.set("请换个按键！")
                self.ready_tk_var.set("")
                return

            self.auto_tk_var.set("")
            self.start_tk_var.set("")
            self.end_tk_var.set("")
            self.interval_tk_var.set("")

        if self.last_start_hot_key is not None:
            remove_hotkey(self.last_start_hot_key)
        if self.last_end_hot_key is not None:
            remove_hotkey(self.last_end_hot_key)
        stop_checking_hotkeys()
        clear_hotkeys()

        start_register_result = register_hotkey(self.start_key_value, [self.start_key_value], self._start_handler)
        end_register_result = register_hotkey(self.end_key_value, [self.end_key_value], self._stop_handler)
        print(f"单按键, start_register_result={start_register_result}, end_register_result={end_register_result}")
        start_checking_hotkeys()
        self.ready_tk_var.set("小胖已准备就绪！")

        if self.user_data is None:
            self.user_data = {}
        self.user_data["auto"] = self.auto_key_value
        self.user_data["interval"] = self.interval_value
        self.user_data["start"] = self.start_key_value
        self.user_data["end"] = self.end_key_value
        save_user_data(self.history_filename, self.user_data)

    def _start_handler(self):
        if self.new_thread is not None and self.new_thread.is_active():
            self.new_thread.stop()
        dd_key_value = dd_key_map[str(self.auto_key_value).lower()]
        self.new_thread = Job(dd_key_value, self.interval_value, self.dd_dll)
        self.new_thread.start()
        self.start_tracker.play()
        print("started")

    def _stop_handler(self):
        if self.new_thread is not None and self.new_thread.is_active():
            self.new_thread.stop()
        # clear_hotkeys()
        self.end_tracker.play()
        print("stopped")

    def close_handler(self):
        if self.new_thread is not None and self.new_thread.is_active():
            self.new_thread.stop()
        # self.window.destroy()

