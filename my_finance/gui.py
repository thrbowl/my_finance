# -*- coding: utf-8 -*-
import Tkinter as tk
import tkMessageBox
from my_finance.model import User, Finance

current_user = None

TITLE_FONT = ('Helvetica', 18, 'bold')
CONS_SEX = dict([(1, u'男'), (2, u'女')])
CONS_TYPE = dict([(1, u'收入'), (2, u'支出')])


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

        if finance_list:
            pass
        else:
            tk.Label(self, text=u'你还没有个人财务记录', bg='red').grid(row=4, sticky=tk.W)
            tk.Button(self, text='添加', command=add_finance_callback).grid(row=5, sticky=tk.W)


class FinanceAddPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


class FinanceEditPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


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

        def save_back_callback():
            save_callback()
            self.controller.show_frame('HomePage')

        def cancel_edit_callback():
            self.controller.show_frame('HomePage')

        tk.Button(self, text=u'保存', command=save_callback).grid(row=2, column=0)
        tk.Button(self, text=u'保存并返回', command=save_back_callback).grid(row=2, column=1)
        tk.Button(self, text=u'放弃修改', command=cancel_edit_callback).grid(row=2, column=2)


def run():
    app = App()
    app.set_pages([LoginPage])
    app.show_frame('LoginPage')

    app.title(u'个人财务管理系统')
    app.geometry('640x480')
    app.resizable(width=True, height=True)
    app.mainloop()
