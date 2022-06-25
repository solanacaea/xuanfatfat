from tkinter import ttk
from tkinter import *
from single import num_key, ignore_keys, back_space_key, dd_key_map
import pydirectinput


DEF_ROW_CUR = 4
DEF_ROW_SEQ = 10
KEY_TYPE_LIST = ["键-按", "键-按住", "鼠标左键", "鼠标右键", "鼠标移动", "等待"]
KEY_LIST = ["键-按", "键-按住"]
MOUSE_LIST = ["鼠标左键", "鼠标右键", "鼠标移动"]
INTERVAL_LIST = ["键-按", "鼠标左键", "鼠标右键"]
EMPTY_INPUT = ['', ' ', '\t']


def trim_rows(rows):
    pre_index = 0
    for row in rows:
        if row.strip() == "":
            pre_index += 1
        else:
            break
    new_rows = rows[pre_index:]

    suf_index = len(new_rows)
    if len(new_rows) == 0:
        return []

    for i in range(len(new_rows), 0, -1):
        if new_rows[i - 1].strip() == "":
            suf_index -= 1
        else:
            break
    return new_rows[0:suf_index]


class AddPanel(object):
    def __init__(self, window=None, user_data=None,
                 icon=None, logo=None,
                 crud="c", uid=None, name=None, mode=None, content=None):
        self.window = window
        self.close_callback_handler = None
        self.curr_top = None
        self.curr_type = "键-按"
        self.auto_key_value = None
        self.time_value = None
        self.interval_value = None
        self.user_data = user_data
        self.icon = icon
        self.logo = logo
        self.warn_tk_var = StringVar()
        self.script_id = uid
        self.script_name_raw = name
        self.script_name = name
        self.mode = mode
        self.script_content = content

    def popup(self):
        # Create a Toplevel window
        top = Toplevel(self.window)
        top.resizable(width=False, height=False)
        top.title("按键脚本编辑")
        top.iconbitmap(self.icon)
        pos = pydirectinput.position()
        top.geometry(f"460x255+{pos[0]}+{pos[1]}")
        top.protocol("WM_DELETE_WINDOW", self._close_handler)
        self.curr_top = top
        self._init_components()
        ok_btn = ttk.Button(top, text="插入->", command=lambda: self._add_key(
            ok_btn, self.curr_type
        ), width=6)
        ok_btn.place(x=200, y=110)
        # ok_btn.pack(pady=5, side=BOTTOM)

        save_btn = ttk.Button(top, text="保存", command=lambda: self._save(), width=5)
        save_btn.place(x=330, y=220)

    def _init_components(self):
        top = self.curr_top
        # 1. 脚本名称
        name_l = Label(top, text='脚本名称:')
        name_l.place(x=20, y=10)
        name_e = Entry(top, width=13)
        if self.script_name is not None:
            name_e.insert("0", self.script_name)
        name_e.place(x=85, y=10)
        self.name_e = name_e

        # 2. 脚本类型
        name_l = Label(top, text='按键模式:')
        name_l.place(x=20, y=40)
        script_ckb = ttk.Combobox(self.curr_top, width=8, height=14)
        script_ckb["values"] = ["顺序按键", "同时按键"]

        def _select_curr_mode(evt):
            curr_mode = script_ckb.get()
            self.curr_mode = curr_mode

        script_ckb.bind("<<ComboboxSelected>>", _select_curr_mode)
        if self.mode is None:
            script_ckb.set("顺序按键")
            self.curr_mode = "顺序按键"
        else:
            script_ckb.set(self.mode)
            self.curr_mode = self.mode
        script_ckb.place(x=85, y=40)

        # 3.1 提示信息
        tip_l = Label(top, text='提示信息:')
        tip_l.place(x=20, y=220)
        insert_warn = Label(top, textvariable=self.warn_tk_var, fg='#FF0000')
        insert_warn.place(x=80, y=220)

        # 3.2 脚本内容
        name_l = Label(top, text='脚本内容:')
        name_l.place(x=258, y=10)
        script_input = Text(self.curr_top, width=25, height=13)
        self.script_input = script_input
        if self.script_content is not None:
            convert_content = "\n".join(self.script_content) + "\n"
            script_input.insert("0.0", convert_content)
        script_input.place(x=262, y=38)

        # 边框
        lb = Label(self.curr_top, borderwidth=2, width=25, height=8, relief="ridge", text="")
        lb.place(x=10, y=70)

        # 4.1 按键类型
        l2 = Label(top, text='按键类型:')
        l2.place(x=20, y=80)
        key_ckb = ttk.Combobox(top, width=8, height=14)
        key_ckb["values"] = KEY_TYPE_LIST
        key_ckb.bind("<<ComboboxSelected>>", self._select_type)
        key_ckb.set("键-按")
        self.key_type_ckb = key_ckb
        key_ckb.place(x=85, y=80)

        # 4.2 按键
        l1 = Label(top, text='自动按键:')
        self.l1 = l1
        l1.place(x=20, y=110)
        e1 = Entry(top, width=10)
        e1.place(x=85, y=110)
        self.e1 = e1
        e1.bind(sequence="<KeyPress>", func=self._key_input_event)

        # 4.3 时长
        l2 = Label(top, text='时长(秒):')
        self.l2 = l2
        l2.place(x=20, y=140)
        e2 = Entry(top, width=10)
        e2.place(x=85, y=140)
        self.e2 = e2
        e2.bind(sequence="<KeyRelease>", func=self._time_input_event)

        # 4.4 间隔
        l_interval = Label(top, text='间隔(秒):')
        self.l_interval = l_interval
        l_interval.place(x=20, y=170)
        e_interval = Entry(top, width=10)
        e_interval.place(x=85, y=170)
        self.e_interval = e_interval
        e_interval.bind(sequence="<KeyRelease>", func=self._interval_input_event)
        self.key_le = [l1, e1, l2, e2, l_interval, e_interval]

        # 4.5 鼠标坐标
        x_l = Label(top, text='X坐标:')
        x_e = Entry(top, width=10)
        y_l = Label(top, text='Y坐标:')
        y_e = Entry(top, width=10)
        self.axis = [x_l, x_e, y_l, y_e]

        # 4.6 等待
        wait_l = Label(top, text='等待时长:')
        wait_e = Entry(top, width=10)
        self.wait_le = [wait_l, wait_e]

        # init curr_type
        self._select_type(None)

    def _select_type(self, evt):
        curr_type = self.key_type_ckb.get()
        self.curr_type = curr_type
        if curr_type.startswith("键-"):
            self.l1.place(x=20, y=110)
            self.e1.place(x=85, y=110)
            self.l2.place(x=20, y=140)
            self.e2.place(x=85, y=140)
            for item in self.wait_le:
                item.place_forget()
            for axis_item in self.axis:
                axis_item.place_forget()
            if curr_type == "键-按":
                self.l_interval.place(x=20, y=170)
                self.e_interval.place(x=85, y=170)
            elif curr_type == "键-按住":
                self.l_interval.place_forget()
                self.e_interval.place_forget()
        elif curr_type.startswith("鼠标"):
            self.l1.place_forget()
            self.e1.place_forget()
            for item in self.wait_le:
                item.place_forget()
            if curr_type == "鼠标移动":
                self.l2.place_forget()
                self.e2.place_forget()
                self.l_interval.place_forget()
                self.e_interval.place_forget()
                self.axis[0].place(x=20, y=110)
                self.axis[1].place(x=85, y=110)
                self.axis[2].place(x=20, y=140)
                self.axis[3].place(x=85, y=140)
            else:
                for axis_item in self.axis:
                    axis_item.place_forget()
                self.l2.place(x=20, y=110)
                self.e2.place(x=85, y=110)
                self.l_interval.place(x=20, y=140)
                self.e_interval.place(x=85, y=140)
        elif curr_type == "等待":
            for item in self.key_le:
                item.place_forget()
            for axis_item in self.axis:
                axis_item.place_forget()
            self.wait_le[0].place(x=20, y=110)
            self.wait_le[1].place(x=85, y=110)
        self.warn_tk_var.set("")

    def _add_key(self, insert_btn, key_type):
        insert_btn.focus_set()
        x_v = 0
        y_v = 0
        wait_v = 1
        if self.curr_type in KEY_LIST:
            if self.auto_key_value is None:
                self.warn_tk_var.set("请设置自动按键！")
                return

            if self.auto_key_value.lower() not in dd_key_map:
                self.warn_tk_var.set("请换个按键！")
                return
        elif self.curr_type == "鼠标移动":
            x_v = self.axis[1].get()
            if x_v is None or str(x_v).strip() == "":
                self.warn_tk_var.set("请设置X轴坐标！")
                return
            y_v = self.axis[3].get()
            if y_v is None or str(y_v).strip() == "":
                self.warn_tk_var.set("请设置Y轴坐标！")
                return
            try:
                float(x_v)
                float(y_v)
                self.warn_tk_var.set("")
            except:
                self.warn_tk_var.set("请输入数字！")
                return
        elif self.curr_type == "等待":
            wait_v = self.wait_le[1].get()
            if wait_v is None or str(wait_v).strip() == "":
                self.warn_tk_var.set("请设置等待时长！")
                return
            try:
                float(wait_v)
                self.warn_tk_var.set("")
            except:
                self.warn_tk_var.set("请输入数字！")
                return

        if self.curr_type in INTERVAL_LIST:
            if self.time_value is None or str(self.time_value).strip() == "":
                self.warn_tk_var.set("请设置时长！")
                return

            if self.interval_value is None or str(self.time_value).strip() == "":
                self.warn_tk_var.set("请设置间隔！")
                return

        self.warn_tk_var.set("")
        if self.curr_type == "键-按":
            new_item = f"{key_type}|{self.auto_key_value}|{self.time_value}|{self.interval_value}\n"
        elif self.curr_type == "键-按住":
            new_item = f"{key_type}|{self.auto_key_value}|{self.time_value}\n"
        elif self.curr_type == "鼠标移动":
            new_item = f"{key_type}|{x_v}|{y_v}\n"
        elif self.curr_type.startswith("鼠标"):
            new_item = f"{key_type}|{self.time_value}|{self.interval_value}\n"
        elif self.curr_type == "等待":
            new_item = f"{key_type}|{wait_v}\n"
        else:
            new_item = ""
        full_content = self.script_input.get("1.0", "end")
        rough_rows = full_content.split("\n")
        rows = trim_rows(rough_rows)
        insert_row = len(rows) + 1
        self.script_input.insert(f"{insert_row}.0", new_item)

    def _save(self):
        script_name = self.name_e.get()
        if script_name is None or str(script_name).strip() == "":
            self.warn_tk_var.set("请设置脚本名称！")
            return
        script_name = str(script_name).strip()

        scripts = self.user_data["multiple"]["scripts"]
        for script_id, script_row in scripts.items():
            if script_row["name"] == script_name and script_id != self.script_id:
                self.warn_tk_var.set("脚本名称重复，请换一个！")
                return

        valid, rows = self._script_validation()
        if valid is False:
            self.warn_tk_var.set(rows)
            return

        key_valid = self._auto_key_check(rows)
        if key_valid is False:
            return

        self._complete_button_handler(rows)

    def _key_input_event(self, event):
        if event.keycode == back_space_key:
            self.auto_key_value = None
            return

        # if event.keycode in ignore_keys:
        #     return

        self.e1.delete(0, "end")
        if event.keycode not in num_key:
            if event.char in EMPTY_INPUT:
                self.e1.insert(0, event.keysym)

        if event.char in EMPTY_INPUT:
            self.auto_key_value = event.keysym
        else:
            self.auto_key_value = event.char
        self.warn_tk_var.set("")

        if self.auto_key_value.lower() not in dd_key_map:
            self.warn_tk_var.set("请换个按键！")
            return

    def _time_input_event(self, event):
        if event.keycode == back_space_key:
            self.time_value = None
            return
        try:
            self.time_value = float(self.e2.get())
            self.warn_tk_var.set("")
        except:
            self.warn_tk_var.set("请输入数字！")
            self.time_value = None
            self.e2.delete(0, "end")

    def _interval_input_event(self, event):
        if self.curr_type == "键-按住":
            return

        if event.keycode == back_space_key:
            self.interval_value = None
            return
        try:
            self.interval_value = float(self.e_interval.get())
            self.warn_tk_var.set("")
        except:
            self.warn_tk_var.set("请输入数字！")
            self.interval_value = None
            self.e_interval.delete(0, "end")

    def _script_validation(self):
        full_content = self.script_input.get("1.0", "end")
        rough_rows = full_content.split("\n")
        rows = trim_rows(rough_rows)
        if len(rows) == 0:
            return False, f"请设置脚本内容！"
        if self.curr_mode == "同时按键" and len(rows) > DEF_ROW_CUR:
            return False, f"仅支持{DEF_ROW_CUR}个同时按键！"
        elif self.curr_mode == "顺序按键" and len(rows) > DEF_ROW_SEQ:
            return False, f"仅支持{DEF_ROW_SEQ}个顺序按键！"
        return True, rows

    def _auto_key_check(self, rows):
        for row in rows:
            items = row.split("|")
            key_type = str(items[0]).strip()
            items[0] = key_type
            if key_type not in KEY_TYPE_LIST:
                self.warn_tk_var.set(f"不支持类型: <{key_type}>!")
                return False

            item_len = 3
            item_key = None
            item_digits = {}
            if key_type == "键-按":
                item_len = 4
                item_key = str(items[1]).lower()
                if self.curr_mode == "同时按键" and "+" in item_key:
                    self.warn_tk_var.set(f"同时按键不支持组合按键: <{item_key}>!")
                    return False
                item_digits = {"时长": items[2], "间隔": items[3]}
            elif key_type == "键-按住":
                if self.curr_mode == "同时按键":
                    self.warn_tk_var.set(f"同时按键不支持: <{key_type}>!")
                    return False
                item_key = str(items[1]).lower()
                item_digits = {"时长": items[2]}
            elif key_type == "鼠标左键":
                item_digits = {"时长": items[1], "间隔": items[2]}
            elif key_type == "鼠标右键":
                if self.curr_mode == "同时按键":
                    self.warn_tk_var.set(f"同时按键不支持: <{key_type}>!")
                    return False
                item_digits = {"时长": items[1], "间隔": items[2]}
            elif key_type == "鼠标移动":
                # if self.curr_mode == "同时按键":
                #     self.warn_tk_var.set(f"同时按键不支持: <{key_type}>!")
                #     return False
                item_digits = {"时长": items[1], "间隔": items[2]}
            elif key_type == "等待":
                item_len = 2

            if len(items) < item_len:
                self.warn_tk_var.set(f"请补全信息: {items}!")
                return False

            if item_key is not None:
                item_key_split = str(item_key).strip().split("+")
                for ikp in item_key_split:
                    if ikp not in dd_key_map:
                        self.warn_tk_var.set(f"不支持按键: <{ikp}>!")
                        return False

            for dig_key, dig_val in item_digits.items():
                try:
                    float(dig_val)
                except:
                    self.warn_tk_var.set(f"{dig_key}不是数字: <{dig_val}>!")
                    return False

        return True

    def _complete_button_handler(self, rows):
        self.warn_tk_var.set("")
        if self.close_callback_handler is not None:
            script_name = self.name_e.get()
            self.close_callback_handler(
                self.script_id, script_name, self.script_name_raw,
                self.curr_mode, rows
            )

    def _close_handler(self):
        self.curr_top.destroy()
        if self.close_callback_handler is not None:
            self.close_callback_handler()

    def destroy(self):
        self.curr_top.destroy()

