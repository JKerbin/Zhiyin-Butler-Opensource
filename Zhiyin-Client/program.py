import shutil
# TODO: os一定要导入，否则使用pyinstaller打包之后会报错
# TODO: 使用pycharm开发时可能会提示os未使用，忽略这个警告
import os
from utils import *


class ProgramManager:
    def __init__(self, cold_start=False):
        conf = Config()
        self.__c = 'PRO_MANAGER'
        self.mas = Massage(self.__c)
        try:
            self.system_lnk = conf.config('SYS_LNK_DIR')  # 获取系统路径
            self.current_dir = os.getcwd()  # 当前绝对路径
            self.program_dir = conf.config('PROGRAM_DIR')  # 程序管理器挂载路径
            self.program_list = []  # 维护程序列表
            # 初始化程序管理器
            if cold_start:
                Loading.waba(self.__init, module=self.__c, desc='初始化程序管理器', colour='green', directory=self.system_lnk)
            for lnk in Loading.loba(os.listdir(self.program_dir + '/lnk'), module=self.__c, desc='维护程序列表',
                                    colour='green'):
                self.program_list.append(lnk[:-4])
            with open(self.program_dir + '/plist', 'w') as file:
                for lnk in Loading.loba(self.program_list, module=self.__c, desc='本地化程序列表', colour='green'):
                    file.write(lnk + '\n')
        except Exception as e:
            self.mas.error(e)

    def __init(self, directory):
        """
        程序管理器，获取windows开始菜单下的快捷方式（除去卸载应用的快捷方式）
        :param directory: windows开始菜单路径
        """
        try:
            lnk_dir = self.program_dir + '/lnk'
            if not os.path.exists(lnk_dir):
                os.makedirs(lnk_dir)
            # 查找并复制系统目录下的快捷方式
            for item in os.listdir(directory):
                item_path = os.path.join(directory, item)
                if os.path.isfile(item_path) and item.endswith('.lnk'):
                    # 跳过所有卸载程序
                    if "卸载" in item or "Uninstall" in item or "uninstall" in item:
                        pass
                    else:
                        shutil.copy(item_path, lnk_dir)
                # 递归地处理子目录
                elif os.path.isdir(item_path):
                    self.__init(item_path)
        except Exception as e:
            self.mas.error(e)

    def start_process(self, program):
        """
        启动程序快捷方式
        :param program: 程序名称
        """
        try:
            os.startfile(f'{self.current_dir}/{self.program_dir}/lnk/{program}.lnk')
            self.mas.info(f'控制运行{program}')
        except Exception as e:
            self.mas.error(f'运行{program}失败，报错-{e}')
