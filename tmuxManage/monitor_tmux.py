# encoding: utf-8
"""

"""

import os
import libtmux
import pandas as pd
import time
from pathlib import Path
from datetime import datetime

session_name = ""



def get_datetime(format="%Y-%m-%d %H:%M:%S"):
    return datetime.now().strftime(format=format)


class MonitorTmux(object):
    def __init__(self):
        pass

    def execute_monitor(self):
        """监控每个进程"""
        global session_name
        log_result = open("process_tmux.log", "a")
        # 查询所有进程
        linux_cmd = f'ps -aux | grep "python3 run.py --env_id"'
        cmd_res = os.popen(linux_cmd)
        process_result_list = cmd_res.readlines()

        port_file_df = pd.read_csv("port_reference.csv", encoding="utf-8")
        # 判断哪些进程死了
        need_reset_process = {}
        for idx, data in port_file_df.iterrows():
            env_id_list = data.env_id.split(", ") if ", " in str(data.env_id) else [data.env_id]
            for env_id_idx, env_id in enumerate(env_id_list):
                python_cmd = f"python3 run.py --env_id {env_id}"
                exist_process = [ii for ii in process_result_list if python_cmd in ii]
                if exist_process:
                    continue

                need_reset_process.update({
                    f"{data[0]}_{str(env_id)}_{str(env_id_idx)}": python_cmd
                })
                print_info = f"{get_datetime()} {data[0]} {python_cmd} reset excute"
                print(print_info, file=log_result)


        # 开始监控
        libserver = libtmux.Server()
        tmux_session = libserver.find_where({"session_name": session_name})
        window_list = tmux_session.list_windows()
        window_name_list = [ii.name for ii in window_list]

        for window_name, cmd_python in need_reset_process.items():
            pane_idx, port_num, window_obj = window_name.split("_")[-1], window_name.split("_")[-2], "_".join(window_name.split("_")[:-2]),
            if window_obj in window_name_list:
                panes_obj = window_list[window_name_list.index(window_obj)].list_panes()[int(pane_idx)]
                panes_obj.send_keys(cmd_python, enter=True)

        pass

def main():
    """

    """
    while True:
        MonitorTmux().execute_monitor()
        time.sleep(60)

main()


