# encoding: utf-8
"""
使用tmux 启动每个测试版本
# run.py 中最好默认 env_id 是 0
"""

import os
import libtmux
import pandas as pd
import time
from pathlib import Path
from datetime import datetime


# 每个版本 需要启动的个数
PROCESS_NUM = 2
docker_id_list = list(range(0, 0))
root_path = r"*/"
session_name = ""
# 是否清除docker
docker_remove_flag = False

# test
# root_path = r"/home/cetc28/lixbi/code2/"
code_config2 = {
    # 复赛第一轮
    # root_path + "battle-framework_1030": "from agent.amscadre_1120.amscadre_blue1030.blue_agent import BlueAgent",  # 测试1
    # root_path + "battle-framework_1102": "from agent.amscadre_1120.amscadre_blue1102.blue_rule_agent_20201102_yuding import BlueAgent",# 测试2
    root_path + "battle-framework_1107": "from agent.amscadre_1120.amscadre_blue1107.blue_rule_agent_20201106_old_awacs import BlueAgent",  # 测试3
    # 复赛第二轮开发版本
    root_path + "battle-framework_likai1209": "from agent.amscadre_1120.amscadre_blue1125submit.yuding_blue_1209likai import BlueAgent",  # 测试8
    root_path + "battle-framework_yuding1209": "from agent.amscadre_1120.amscadre_blue1125submit.yuding_blue1209 import BlueAgent ",  # 测试9
    # root_path + "battle-framework_yuding1211": "from agent.amscadre_1120.amscadre_blue1210.blue_agent_20201211_develop_bom_JT import BlueAgent",  # 测试10
    # root_path + "battle-framework_yuding1212": "from agent.amscadre_1120.amscadre_blue1212.blue_agent_20201212_develop_bom_JT_1_airBack import BlueAgent",  # 测试11

    # 1215 复赛第二轮提交版的三种拆分模式,歼击机点位,驱逐舰点位
    root_path + "battle-framework_air_logic": "from agent.amscadre_1120.amscadre_blue1215sumbit.entities_blue.air_logic import BlueAgent", # 正常
    root_path + "battle-framework_acwacs_logic": "from agent.amscadre_1120.amscadre_blue1215sumbit.entities_blue.ship_acwacs_logic import BlueAgent", # 极限

    root_path + "battle-framework_curve_fight": "from agent.amscadre_1120.amscadre_blue1215sumbit.air_logic_curve_fight import BlueAgent",
    # 蓝方决赛开发版本
    root_path + "battle-framework_blue0104": "from agent.amscadre_1120.amscadre_blue0104.blue_20210101_dev1111 import BlueAgent",
    root_path + "battle-framework_blue0105": "from agent.amscadre_1120.amscadre_blue0105.blue_20210104_dev import BlueAgent",
    root_path + "battle-framework_blue0105JT": "from agent.amscadre_1120.amscadre_blue0105JT.blue_20210105_dev import BlueAgent",
    root_path + "battle-framework_blue0106": "from agent.amscadre_1120.amscadre_blue0106.blue_20210106_dev import BlueAgent",
    root_path + "battle-framework_blue0107": "from agent.amscadre_1120.amscadre_blue_0107.blue_20210107_dev import BlueAgent",
    root_path + "battle-framework_yuding0108": "from agent.amscadre_1120.amscadre_blue0108.blue_20210108_dev_yuding import BlueAgent",
    root_path + "battle-framework_blue0108": "from agent.amscadre_1120.amscadre_blue0108.blue_20210108_dev import BlueAgent",
    # root_path + "battle-framework_hzh0109": "from agent.amscadre_1120.amscadre_blue0109.blue_20210108_hzh import BlueAgent",
    root_path + "battle-framework_dev0109": "from agent.amscadre_1120.amscadre_blue0109.blue_20210109_dev import BlueAgent",
    root_path + "battle-framework_yuding0109": "from agent.amscadre_1120.amscadre_blue0109.blue_20210109_yuding import BlueAgent",
    root_path + "battle-framework_attackJam0109_hzh": "from agent.amscadre_1120.amscadre_blue_attackJam0109.blue_20210109_hzh import BlueAgent",
    root_path + "battle-framework_attackJam0109_hzh_30_line": "from agent.amscadre_1120.amscadre_blue_attackJam0109.blue_20210109_hzh_30_line import BlueAgent",
    root_path + "battle-framework_attackJam0110_hzh": "from agent.amscadre_1120.amscadre_blue0110attackJam.blue_20210110_hzh import BlueAgent",
    root_path + "battle-framework_attackJam0110_hzh_30_line": "from agent.amscadre_1120.amscadre_blue0110attackJam.blue_20210110_hzh_30_line import BlueAgent",
    root_path + "battle-framework_hzhAfternoon_0111": "from agent.amscadre_1120.amscadre_blue0111.blue_20210111_dev import BlueAgent",
    root_path + "battle-framework_blue0111": "from agent.amscadre_1120.amscadre_blue0111.blue_20210111_hzh_afternoon import BlueAgent",

}

code_config = {
root_path + "blue_28_v2": "from agent.amscadre_1120.amscadre_blue_28_v2.blue_agent_28_v2 import BlueAgent",
root_path + "blue_32_v2": "from agent.amscadre_1120.amscadre_blue_32_v2.blue_agent_32_v2 import BlueAgent"

}


def get_datetime(format="%Y-%m-%d %H:%M:%S"):
    return datetime.now().strftime(format=format)


class ManageTmux(object):
    def __init__(self, session_name="test_session", process_num=2):
        self.session_name = session_name
        self.process_num = process_num
        self.server = None
        self._init_server()
        pass

    def _init_server(self):
        self.server = libtmux.Server()

    def create_session(self, start_directory=None, window_name=None):
        """

        """
        if not self.server:
            self.server = self._init_server()

        # 创建session
        session_exist = self.server.has_session(self.session_name)
        if not session_exist:
            self.server.new_session(self.session_name)

    def create_window(self, start_directory, window_name):
        """"""
        # 创建session
        self.create_session()

        tmux_session = self.server.find_where({"session_name": f"{self.session_name}"})
        if not tmux_session:
            self.create_session()
            tmux_session = self.server.find_where({"session_name": f"{self.session_name}"})

        # 查看已经窗口
        del_window_idx = [total_w.id for total_w in tmux_session.list_windows() if total_w.name == window_name]
        for del_window in del_window_idx:
            tmux_session.get_by_id(del_window).kill_window()

        return tmux_session.new_window(window_name=window_name, start_directory=start_directory)

    def create_pane(self, window_session, start_directory, env_id_list=[]):
        """

        """
        pane_list = window_session.list_panes()
        if len(pane_list) >= self.process_num:
            pass
        else:
            for process_n in range(self.process_num):
                window_session.split_window("", start_directory=start_directory, attach=False, vertical=False)
                if len(window_session.list_panes()) >= self.process_num:
                    pane_list = window_session.list_panes()
                    break

        #
        for idx, pane_obj in enumerate(pane_list):
            cmd = f"python3 run.py --env_id {str(env_id_list[idx])}"
            pane_obj.send_keys(cmd, enter=True)


class ProjectTool(object):
    def __init__(self):
        pass

    @staticmethod
    def remove_docker(env_id_list):
        """
        清除原来创建的docker容器
        :param env_id_list:
        :return:
        """
        for env_id in env_id_list:
            docker_name = f"env_{str(env_id)}"
            docker_stop = 'docker stop {}'.format(docker_name)
            print(docker_stop)
            os.system(docker_stop)
            time.sleep(1)

            docker_rm = 'docker rm {}'.format(docker_name)
            print(docker_rm)
            os.system(docker_rm)
            time.sleep(1)

    @staticmethod
    def clear_log(code_list):
        for code in code_list:
            if not os.path.exists(code):
                raise (f"{code} 路径不存在")
            # 清楚所有的log 文件
            remove_file = list(Path(code).glob("*.log")) + list(Path(code).glob("*.txt"))
            [os.remove(remove_f) for remove_f in remove_file]

    @staticmethod
    def agent_code_modify(code_config):
        """

        """
        for code_path, insert_word in code_config.items():
            run_file = os.path.join(code_path, "run.py")
            with open(run_file, "r") as f:
                data_list = f.readlines()

            # 找到最后一个导入
            last_idx = 0
            for idx, word in enumerate(data_list):
                if "def connect_loop(rpyc_port)" in word:
                    last_idx = idx
                    break

            data_list.insert(last_idx - 1, insert_word + "\n")

            with open(run_file, "w") as f:
                for word in data_list:
                    f.writelines(word)

    @staticmethod
    def copy_direct(code_config):
        """
        复制目标文件
        """
        source_dir = os.path.join(root_path, "battle-framework")
        # source_dir == /home/cetc28/lixbi/code2/battle-framework
        for code_path, _ in code_config.items():
            # run_file = os.path.join(code_path, "run.py")
            cmd = fr"cp -r {source_dir} {code_path}"
            os.system(cmd)
        pass






def main():
    """"""

    # 首先清除docker  和日志
    # code_con  = code_config
    # # 已知
    global docker_id_list
    global session_name

    # copy 文件
    ProjectTool.copy_direct(code_config)

    #
    # if docker_remove_flag: ProjectTool.remove_docker(docker_id_list)
    # # 清除日志
    ProjectTool.clear_log(list(code_config.keys()))
    # 替换代码
    ProjectTool.agent_code_modify(code_config)

    # tmux 启动
    tmux_obj = ManageTmux(session_name=session_name, process_num=PROCESS_NUM)
    #
    # # 开始生成
    begin_idx = 0
    port_df_list = []
    for code_path, _ in code_config.items():
        name = os.path.basename(code_path)
        tmux_window = tmux_obj.create_window(code_path, name)
        env_id_list = docker_id_list[begin_idx*PROCESS_NUM: (begin_idx+1)*PROCESS_NUM]
        port_list = [[6100 + env_id * 10 + i for i in range(4)][1] for env_id in env_id_list]
        port_df_list.append([name, ", ".join(list(map(lambda x:str(x), env_id_list))), ", ".join(list(map(lambda x:str(x), port_list)))])
        tmux_obj.create_pane(tmux_window, code_path, env_id_list)
        begin_idx += 1
    pd.DataFrame(port_df_list, columns=["name", "env_id", "port"]).to_csv("port_reference.csv", index=False, encoding="utf-8")




if __name__ == "__main__":
    main()
    pass













