import re
import pymysql
from utils import *

"""
# 邀请码表 #
CREATE TABLE invitation_codes (
    invitation VARCHAR(255)
);
+------------+--------------+------+-----+---------+-------+
| Field      | Type         | Null | Key | Default | Extra |
+------------+--------------+------+-----+---------+-------+
| invitation | varchar(255) | YES  |     | NULL    |       |
+------------+--------------+------+-----+---------+-------+
# 用户mac表 #
CREATE TABLE allowed_users (
    mac_address VARCHAR(17)
);
+-------------+-------------+------+-----+---------+-------+
| Field       | Type        | Null | Key | Default | Extra |
+-------------+-------------+------+-----+---------+-------+
| mac_address | varchar(17) | YES  | UNI | NULL    |       |
+-------------+-------------+------+-----+---------+-------+
"""


class Database:
    def __init__(self, user, pw, db_name, host='127.0.0.1', port=3306):
        """
        :param user: 用户名
        :param pw: 密码
        :param db_name: 数据库名称
        :param host: 地址（缺省值127.0.0.1）
        :param port: 端口（缺省值3306）
        """
        self.user = user
        self.pw = pw
        self.db_name = db_name
        self.host = host
        self.port = port
        self.__connect_to_db()

    def __connect_to_db(self):
        try:
            self.__c = 'DATABASE'
            self.mas = Massage(self.__c)
            self.__db = pymysql.connect(
                host=self.host,
                user=self.user,
                passwd=self.pw,
                port=self.port,
                db=self.db_name
            )
            self.__cursor = self.__db.cursor()
            self.mas.info(f'建立与MySQL_{self.db_name}的连接，数据库用户为{self.user}')
        except Exception as e:
            self.mas.error(e)

    def __ping_db(self):
        try:
            self.__db.ping(reconnect=True)
        except pymysql.MySQLError as e:
            self.mas.warning(e)
            self.__connect_to_db()

    @staticmethod
    def __filter_mac_addresses(mac_list):
        def is_valid_mac(mac):
            valid_mac_pattern = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')
            return bool(valid_mac_pattern.match(mac))

        return [mac for mac in mac_list if is_valid_mac(mac)]

    def add_invitation(self, invitations):
        self.__ping_db()
        try:
            for invitation in invitations:
                sql = "INSERT INTO invitation_codes (invitation) VALUES (%s)"
                val = invitation
                self.__cursor.execute(sql, val)
            self.__db.commit()
            self.mas.info('新增邀请码')
        except Exception as e:
            self.mas.error(e)

    def user_verification(self, mac_list):
        self.__ping_db()
        mac_list = self.__filter_mac_addresses(mac_list)
        try:
            placeholders = ', '.join(['%s'] * len(mac_list))
            sql = f"SELECT * FROM allowed_users WHERE mac_address IN ({placeholders})"
            self.__cursor.execute(sql, mac_list)
            result = self.__cursor.fetchone()
            if result:
                self.mas.info(f'用户{mac_list}已注册')
                return 'success'
            else:
                self.mas.info(f'用户{mac_list}未注册')
                return 'fail'
        except Exception as e:
            self.mas.error(e)
            return 'fail'

    def user_activation(self, mac_list, invitation):
        self.__ping_db()
        mac_list = self.__filter_mac_addresses(mac_list)
        state = self.user_verification(mac_list)
        if state == 'success':
            self.mas.warning(f'用户{mac_list}已经注册过')
            return 'exist'
        else:
            try:
                sql = "SELECT * FROM invitation_codes WHERE invitation = %s"
                self.__cursor.execute(sql, (invitation,))
                result = self.__cursor.fetchone()
                if result:
                    placeholders = ', '.join(['(%s)'] * len(mac_list))
                    sql = f"INSERT INTO allowed_users (mac_address) VALUES {placeholders} " \
                          f"ON DUPLICATE KEY UPDATE mac_address=VALUES(mac_address)"
                    self.__cursor.execute(sql, mac_list)
                    sql = "DELETE FROM invitation_codes WHERE invitation = %s"
                    self.__cursor.execute(sql, (invitation,))
                    self.__db.commit()
                    self.mas.info(f'用户{mac_list}注册成功')
                    return 'success'
                else:
                    self.mas.info('无效的邀请码')
                    return 'fail'
            except Exception as e:
                self.mas.error(e)
                return 'fail'
