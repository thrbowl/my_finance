# -*- coding: utf-8 -*-
from my_finance import db


class User(object):
    def __init__(self, record):
        self.id = record[0]
        self.username = record[1]
        self.passwd = record[2]
        self.name = record[3]
        self.age = record[4]
        self.sex = record[5]
        self.create_date = record[6]

    @staticmethod
    def login(username, passwd):
        sql = "SELECT * FROM users WHERE username=? and passwd=?"
        result = db.select(sql, (username, passwd), is_fetchone=True)
        if result:
            return User(result)

    @staticmethod
    def add(data):
        pass

    @staticmethod
    def update(user):
        sql = "UPDATE users SET name=?, sex=? WHERE id=?"
        db.execute(sql, (user.name, user.sex, user.id))

    @staticmethod
    def get(uid):
        sql = "SELECT * FROM users WHERE id=?"
        result = db.select(sql, (uid,), is_fetchone=True)
        if result:
            return User(result)


class Finance(object):
    def __init__(self, record):
        self.id = record[0]
        self.user_id = record[1]
        self.type = record[2]
        self.amount = record[3]
        self.comments = record[4]
        self.create_date = record[5]

    @staticmethod
    def add(uid, data):
        sql = "INSERT INTO finances VALUES (null, ?, ?, ?, ?, datetime())"
        db.execute(sql, (uid, data['type'], data['amount'], data['comments']))

    @staticmethod
    def delete(fid):
        sql = "DELETE FROM finances WHERE id=?"
        db.execute(sql, (fid, ))

    @staticmethod
    def update(finance):
        sql = "UPDATE finances SET type=?, amount=?, comments=? WHERE id=?"
        db.execute(sql, (finance.type, finance.amount, finance.comments, finance.id))

    @staticmethod
    def get(fid):
        sql = "SELECT * FROM finances WHERE id=?"
        result = db.select(sql, (fid,), is_fetchone=True)
        if result:
            return Finance(result)

    @staticmethod
    def get_list(uid):
        sql = "SELECT * FROM finances WHERE user_id=? ORDER BY create_date DESC"
        resultset = db.select(sql, (uid,))
        if resultset:
            return [Finance(result) for result in resultset]
