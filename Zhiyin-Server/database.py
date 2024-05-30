import re

import pymysql

from utils import *


class Database:
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

    def __init__(self, user, pw, db_name, host='127.0.0.1', port=3306):
        """
        :param user: 用户名
        :param pw: 密码
        :param db_name: 数据库名称
        :param host: 地址（缺省值127.0.0.1）
        :param port: 端口（缺省值3306）
        """
        try:
            self.__c = 'DATABASE'
            self.mas = Massage(self.__c)
            self.__db = pymysql.connect(host=host, user=user, passwd=pw, port=port)
            self.__cursor = self.__db.cursor()
            self.__cursor.execute('USE ' + db_name)
            self.mas.info(f'建立与MySQL_{db_name}的连接，数据库用户为{user}')
        except Exception as e:
            self.mas.error(e)

    @staticmethod
    def __filter_mac_addresses(mac_list):
        """
        去除非标准17位（加上连接符）的mac地址（例如虚拟网络适配器mac地址）
        """
        def is_valid_mac(mac):
            # Regular expression to match a valid MAC address
            valid_mac_pattern = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')
            return bool(valid_mac_pattern.match(mac))

        return [mac for mac in mac_list if is_valid_mac(mac)]

    def add_invitation(self, invitations):
        """
        生成新的邀请码
        :param invitations: 新增邀请码
        """
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
        """
        用户验证
        :param mac_list: 用户mac地址列表
        """
        mac_list = self.__filter_mac_addresses(mac_list)
        try:
            # mac_list 是包含多个 MAC 地址的列表
            # 动态生成 SQL 语句中的占位符
            placeholders = ', '.join(['%s'] * len(mac_list))
            sql = f"SELECT * FROM allowed_users WHERE mac_address IN ({placeholders})"

            # 执行查询
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
        """
        用户激活
        :param mac_list: 用户mac地址列表
        :param invitation: 用户提供的邀请码
        """
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
                    # 动态生成 SQL 语句中的占位符，添加用户mac地址并删除对应邀请码
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
