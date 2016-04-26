# -*- coding: utf-8 -*-


class User(object):
    @staticmethod
    def login(username, passwd):
        pass

    @staticmethod
    def add(data):
        pass

    @staticmethod
    def update(uid, data):
        pass

    @staticmethod
    def get(uid):
        pass


class Finance(object):
    @staticmethod
    def add(uid, data):
        pass

    @staticmethod
    def delete(fid):
        pass

    @staticmethod
    def update(fid, data):
        pass

    @staticmethod
    def get(fid):
        pass

    @staticmethod
    def get_list(uid, type=None, start_date=None, end_date=None):
        pass
