import uuid

from database import Database
from utils import *

conf = Config()


def generate_invitations(amount):
    """
    为数据库新增邀请码，邀请码使用uuid4生成
    :param amount: 新增的数量
    """
    invitations = []
    for i in range(amount):
        invitation = str(uuid.uuid4())
        print(invitation)
        invitations.append(invitation)
    db = Database(db_name=conf.config('DB_NAME'), user=conf.config('DB_USER'), pw=conf.config('DB_PASSWORD'))
    db.add_invitation(invitations)


if __name__ == '__main__':
    generate_invitations(5)
