from tkintertable import TableCanvas, TableModel
from tkinter import ttk
from tkinter import *


'''
1.遍历表格
t = treeview.get_children()
for i in t:
    print(treeview.item(i,'values'))
2.绑定单击离开事件
def treeviewClick(event):  # 单击
    for item in tree.selection():
        item_text = tree.item(item, "values")
        print(item_text[0:2])  # 输出所选行的第一列的值
tree.bind('<ButtonRelease-1>', treeviewClick)  
------------------------------
鼠标左键单击按下1/Button-1/ButtonPress-1 
鼠标左键单击松开ButtonRelease-1 
鼠标右键单击3 
鼠标左键双击Double-1/Double-Button-1 
鼠标右键双击Double-3 
鼠标滚轮单击2 
鼠标滚轮双击Double-2 
鼠标移动B1-Motion 
鼠标移动到区域Enter 
鼠标离开区域Leave 
获得键盘焦点FocusIn 
失去键盘焦点FocusOut 
键盘事件Key 
回车键Return 
控件尺寸变Configure
------------------------------
'''


class MultiplePanel(object):
    def __init__(self, dd_dll, window, user_data, start_tracker, end_tracker):
        self.dd_dll = dd_dll
        self.window = window
        self.start_tracker = start_tracker
        self.end_tracker = end_tracker
        self.user_data = user_data
        self.columns = ("按键", "时长", "")

    def _load_btn_entry(self):
        newb = ttk.Button(self.window, text='+', command=self._insert)
        newb.place(x=30, y=20, height=28, width=40, anchor="center")
        # newb.grid(row=0, column=4)

    def _load_auto_entry(self):
        treeview = ttk.Treeview(self.window, height=18, show="headings", columns=self.columns)
        self.treeview = treeview
        treeview.bind('<Double-1>', self._set_cell_value)  # 双击左键进入编辑

        treeview.column("按键", width=80, anchor='center')
        treeview.column("时长", width=80, anchor='center')
        treeview.column("", width=50, anchor='center')

        treeview.heading("按键", text="按键")
        treeview.heading("时长", text="时长")
        treeview.heading("", text="")
        # treeview.place(x=10, y=40)
        treeview.pack(side=RIGHT, fill=BOTH)

    def _insert(self):
        children_len = len(self.treeview.get_children())
        self.treeview.insert('', children_len, values=("按键", "时长", "-"))
        self.treeview.update()
        # self.newb.place(x=120, y=(len(name) - 1) * 20 + 45)

    def _set_cell_value(self, event):  # 双击进入编辑状态
        for item in self.treeview.selection():
            # item = I001
            item_text = self.treeview.item(item, "values")
            # print(item_text[0:2])  # 输出所选行的值
        column = self.treeview.identify_column(event.x)  # 列
        row = self.treeview.identify_row(event.y)  # 行
        cn = int(str(column).replace('#', ''))
        rn = int(str(row).replace('I', ''))
        entryedit = Text(self.window, width=10 + (cn - 1) * 16, height=1)
        entryedit.place(x=16 + (cn - 1) * 130, y=6 + rn * 20)

        def saveedit():
            self.treeview.set(item, column=column, value=entryedit.get(0.0, "end"))
            entryedit.destroy()
            okb.destroy()

        okb = ttk.Button(self.window, text='OK', width=4, command=saveedit)
        okb.place(x=90 + (cn - 1) * 242, y=2 + rn * 20)

    def _sort(self):
        for col in self.columns:  # 绑定函数，使表头可排序
            self.treeview.heading(
                col, text=col,
                command=lambda _col=col: self._treeview_sort_column(
                    self.treeview, _col, False
                )
            )

    def _treeview_sort_column(self, tv, col, reverse):  # Treeview、列名、排列方式
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)  # 排序方式
        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):  # 根据排序后索引移动
            tv.move(k, '', index)
        tv.heading(col, command=lambda: self._treeview_sort_column(tv, col, not reverse))  # 重写标题，使之成为再点倒序的标题
