# -*- coding: utf-8 -*-
from functools import partial
import Tkinter as tk
import tkMessageBox
from my_finance.model import User, Finance

current_user = None
current_finance = None

TITLE_FONT = ('Helvetica', 18, 'bold')
CONS_SEX = dict([(1, u'男'), (2, u'女')])
CONS_TYPE = dict([(1, u'收入'), (2, u'支出')])

STICKY_W_E_N_S = tk.W+tk.E+tk.N+tk.S


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.container = container
        self.frames = {}

    def set_pages(self, pages, force_update=False):
        for F in pages:
            page_name = F.__name__
            if page_name in self.frames and not force_update:
                continue
            frame = F(self.container, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky='nsew')

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Label(self, text=u'用户名:').grid(row=0, sticky=tk.W)
        tk.Label(self, text=u'密 码:').grid(row=1, sticky=tk.W)

        usernameinput = tk.Entry(self)
        usernameinput.grid(row=0, column=1, columnspan=2)
        passwdinput = tk.Entry(self, show='*')
        passwdinput.grid(row=1, column=1, columnspan=2)

        def clear_callback():
            usernameinput.delete(0, tk.END)
            passwdinput.delete(0, tk.END)

        def login_callback():
            username = usernameinput.get()
            username = username.strip()
            passwd = passwdinput.get()
            passwd = passwd.strip()

            global current_user
            current_user = User.login(username, passwd)
            if current_user:
                self.controller.set_pages([HomePage])
                self.controller.show_frame('HomePage')
            else:
                tkMessageBox.showinfo('Error', 'Login Failure!')

        tk.Button(self, text=u'登 录', command=login_callback).grid(row=2, column=1)
        tk.Button(self, text=u'清 空', command=clear_callback).grid(row=2, column=2)


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        global current_user
        tk.Label(self, text=u'姓 名: %s' % current_user.name).grid(row=0, sticky=tk.W)
        tk.Label(self, text=u'性 别: %s' % CONS_SEX[current_user.sex]).grid(row=1, sticky=tk.W)
        tk.Label(self, text=u'注册时间: %s' % current_user.create_date).grid(row=2, sticky=tk.W)

        def edit_user_callback():
            self.controller.set_pages([UserEditPage])
            self.controller.show_frame('UserEditPage')

        tk.Button(self, text='编辑', command=edit_user_callback).grid(row=0, column=1)

        finance_list = Finance.get_list(current_user.id)

        def add_finance_callback():
            self.controller.set_pages([FinanceAddPage])
            self.controller.show_frame('FinanceAddPage')

        def delete_finance_callback(fid):
            Finance.delete(fid)
            self.controller.set_pages([HomePage], force_update=True)

        def edit_finance_callback(fid):
            global current_finance
            current_finance = Finance.get(fid)
            self.controller.set_pages([FinanceEditPage], force_update=True)
            self.controller.show_frame('FinanceEditPage')

        if finance_list:
            finance_list_length = len(finance_list)
            total_input = 0
            total_output = 0

            tk.Label(self, text=u'').grid(row=4)
            tk.Label(self, text=u'添加时间', bg='green').grid(row=5, column=0, sticky=STICKY_W_E_N_S)
            tk.Label(self, text=u'类型', bg='green').grid(row=5, column=1, sticky=STICKY_W_E_N_S)
            tk.Label(self, text=u'金额', bg='green').grid(row=5, column=2, sticky=STICKY_W_E_N_S)
            tk.Label(self, text=u'注释', bg='green').grid(row=5, column=3, sticky=STICKY_W_E_N_S)
            tk.Label(self, text=u'操作', bg='green').grid(row=5, column=4, columnspan=2, sticky=STICKY_W_E_N_S)
            for idx, finance in enumerate(finance_list):
                if finance.type == 1:
                    total_input += finance.amount
                elif finance.type == 2:
                    total_output += finance.amount

                if idx % 2 == 0:
                    tk.Label(self, text=finance.create_date).grid(row=6 + idx, column=0, sticky=STICKY_W_E_N_S)
                    tk.Label(self, text=CONS_TYPE[finance.type]).grid(row=6 + idx, column=1, sticky=STICKY_W_E_N_S)
                    tk.Label(self, text=finance.amount).grid(row=6 + idx, column=2, sticky=STICKY_W_E_N_S)
                    tk.Label(self, text=finance.comments).grid(row=6 + idx, column=3, sticky=STICKY_W_E_N_S)
                    tk.Button(self, text='编辑', command=partial(edit_finance_callback, finance.id)).grid(row=6 + idx, column=4, sticky=STICKY_W_E_N_S)
                    tk.Button(self, text='删除', command=partial(delete_finance_callback, finance.id)).grid(row=6 + idx, column=5, sticky=STICKY_W_E_N_S)
                else:
                    tk.Label(self, text=finance.create_date, bg='gray').grid(row=6 + idx, column=0, sticky=STICKY_W_E_N_S)
                    tk.Label(self, text=CONS_TYPE[finance.type], bg='gray').grid(row=6 + idx, column=1, sticky=STICKY_W_E_N_S)
                    tk.Label(self, text=finance.amount, bg='gray').grid(row=6 + idx, column=2, sticky=STICKY_W_E_N_S)
                    tk.Label(self, text=finance.comments, bg='gray').grid(row=6 + idx, column=3, sticky=STICKY_W_E_N_S)
                    tk.Button(self, text='编辑', command=partial(edit_finance_callback, finance.id), bg='gray').grid(row=6 + idx, column=4, sticky=STICKY_W_E_N_S)
                    tk.Button(self, text='删除', command=partial(delete_finance_callback, finance.id), bg='gray').grid(row=6 + idx, column=5, sticky=STICKY_W_E_N_S)
            tk.Button(self, text='添加', command=add_finance_callback).grid(row=6 + finance_list_length, sticky=tk.W)
            tk.Label(self, text='总收入: %s' % total_input).grid(row=7 + finance_list_length, sticky=tk.W)
            tk.Label(self, text='总支出: %s' % total_output).grid(row=8 + finance_list_length, sticky=tk.W)
        else:
            tk.Label(self, text=u'你还没有个人财务记录', bg='red').grid(row=4, sticky=tk.W)
            tk.Button(self, text='添加', command=add_finance_callback).grid(row=5, sticky=tk.W)


class FinanceAddPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Label(self, text=u'类 型:').grid(row=0, sticky=tk.W)
        tk.Label(self, text=u'金 额:').grid(row=1, sticky=tk.W)
        tk.Label(self, text=u'注 释:').grid(row=2, sticky=tk.W)

        v = tk.StringVar()
        v.set(1)
        inputraido = tk.Radiobutton(self, text=u'收入', variable=v, value=1)
        inputraido.grid(row=0, column=1, sticky=tk.W)
        outputradio = tk.Radiobutton(self, text=u'支出', variable=v, value=2)
        outputradio.grid(row=0, column=2, sticky=tk.W)

        amountinput = tk.Entry(self)
        amountinput.grid(row=1, column=1, columnspan=2, sticky=tk.W)

        commentstext = tk.Entry(self)
        commentstext.grid(row=2, column=1, columnspan=2, sticky=tk.W)

        def save_add_callback():
            type = int(v.get())
            amount = float(amountinput.get())
            comments = commentstext.get()
            comments = comments.strip()

            data = {
                'type': type,
                'amount': amount,
                'comments': comments,
            }
            Finance.add(current_user.id, data)
            self.controller.set_pages([HomePage], force_update=True)
            self.controller.show_frame('FinanceAddPage')

        def add_back_callback():
            save_add_callback()
            self.controller.show_frame('HomePage')

        def cancel_add_callback():
            self.controller.show_frame('HomePage')

        tk.Button(self, text=u'保存&继续添加', command=save_add_callback).grid(row=3, column=0)
        tk.Button(self, text=u'添加&返回', command=add_back_callback).grid(row=3, column=1)
        tk.Button(self, text=u'返回', command=cancel_add_callback).grid(row=3, column=2)


class FinanceEditPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        global current_finance
        tk.Label(self, text=u'类 型:').grid(row=0, sticky=tk.W)
        tk.Label(self, text=u'金 额:').grid(row=1, sticky=tk.W)
        tk.Label(self, text=u'注 释:').grid(row=2, sticky=tk.W)

        v = tk.StringVar()
        v.set(current_finance.type)
        inputraido = tk.Radiobutton(self, text=u'收入', variable=v, value=1)
        inputraido.grid(row=0, column=1, sticky=tk.W)
        outputradio = tk.Radiobutton(self, text=u'支出', variable=v, value=2)
        outputradio.grid(row=0, column=2, sticky=tk.W)

        amountinput = tk.Entry(self)
        amountinput.insert(tk.END, current_finance.amount)
        amountinput.grid(row=1, column=1, columnspan=2, sticky=tk.W)

        commentstext = tk.Entry(self)
        commentstext.insert(tk.END, current_finance.comments)
        commentstext.grid(row=2, column=1, columnspan=2, sticky=tk.W)

        def save_callback():
            type = int(v.get())
            amount = float(amountinput.get())
            comments = commentstext.get()
            comments = comments.strip()

            current_finance.type = type
            current_finance.amount = amount
            current_finance.comments = comments
            Finance.update(current_finance)
            self.controller.set_pages([HomePage], force_update=True)
            self.controller.show_frame('FinanceEditPage')

        def save_back_callback():
            save_callback()
            self.controller.show_frame('HomePage')

        def cancel_edit_callback():
            self.controller.show_frame('HomePage')

        tk.Button(self, text=u'保存', command=save_callback).grid(row=3, column=0)
        tk.Button(self, text=u'保存&返回', command=save_back_callback).grid(row=3, column=1)
        tk.Button(self, text=u'返回', command=cancel_edit_callback).grid(row=3, column=2)


class UserEditPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        global current_user
        tk.Label(self, text=u'姓 名:').grid(row=0, sticky=tk.W)
        tk.Label(self, text=u'性 别:').grid(row=1, sticky=tk.W)

        nameinput = tk.Entry(self)
        nameinput.insert(tk.END, current_user.name)
        nameinput.grid(row=0, column=1, columnspan=2, sticky=tk.W)

        v = tk.StringVar()
        v.set(current_user.sex)
        maleraido = tk.Radiobutton(self, text=u'男', variable=v, value=1)
        maleraido.grid(row=1, column=1, sticky=tk.W)
        femaleradio = tk.Radiobutton(self, text=u'女', variable=v, value=2)
        femaleradio.grid(row=1, column=2, sticky=tk.W)

        def save_callback():
            name = nameinput.get()
            name = name.strip()
            sex = int(v.get())

            current_user.name = name
            current_user.sex = sex
            User.update(current_user)
            self.controller.set_pages([HomePage], force_update=True)
            self.controller.show_frame('UserEditPage')

        def save_back_callback():
            save_callback()
            self.controller.show_frame('HomePage')

        def cancel_edit_callback():
            self.controller.show_frame('HomePage')

        tk.Button(self, text=u'保存', command=save_callback).grid(row=2, column=0)
        tk.Button(self, text=u'保存&返回', command=save_back_callback).grid(row=2, column=1)
        tk.Button(self, text=u'返回', command=cancel_edit_callback).grid(row=2, column=2)


def run():
    app = App()
    app.set_pages([LoginPage])
    app.show_frame('LoginPage')

    app.title(u'个人财务管理系统')
    app.geometry('640x480')
    app.resizable(width=True, height=True)
    app.mainloop()
