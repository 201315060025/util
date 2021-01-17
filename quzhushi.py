# encoding:utf-8
"""
代码去注释， 规则 # 号后面全部去掉； 三个引号全部去掉
"""
import os
import shutil
import re
import sys
# 获取路径
def show_files(path, all_files):
    # 首先遍历当前目录所有文件及文件夹
    file_list = os.listdir(path)
    # 准备循环判断每个元素是否是文件夹还是文件，是文件的话，把名称传入list，是文件夹的话，递归
    for file in file_list:
        # 利用os.path.join()方法取得路径全名，并存入cur_path变量，否则每次只能遍历一层目录
        cur_path = os.path.join(path, file)
        # 判断是否是文件夹
        if os.path.isdir(cur_path):
            show_files(cur_path, all_files)
        else:
            all_files.append(cur_path)
    return all_files

# 删除某一目录下的所有文件或文件夹
def del_file(filepath):

    del_list = os.listdir(filepath)
    for f in del_list:
        file_path = os.path.join(filepath, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    shutil.rmtree(filepath)

if __name__ == '__main__':
    # _path = sys.argv[1]
    _path = r'E:\project_code\add_remark_code\academy_of_military_sciences\battle-framework\agent\amscadre_1120\amscadre_red0109'
    new_path = _path + '_new'
    new_path = new_path.replace("\\", "/")
    index = len(new_path.split('/'))
    files  = show_files(_path,[])
    # 删除文件夹
    if os.path.exists(new_path):
        del_file(new_path)
    # 重新创建文件夹
    os.makedirs(new_path)
    for f in files:
        f = f.replace("\\", "/")
        arrs = f.split('/')
        new_path2 = new_path + '/' + '/'.join(arrs[index:])
        if not os.path.exists('/'.join(new_path2.split('/')[:-1])):
            os.makedirs('/'.join(new_path2.split('/')[:-1]))
        new_py = open(new_path2, mode='a', encoding='utf-8')

        # 一行一行读
        pys = open(f, mode='r', encoding="utf-8").readlines()

        # 去注释规则，1：方法的说明规则删除， 2：带有# 号的删除
        remark_flag = None
        for p in pys:
            # 规则1
            if p.count("'''") == 2 or p.count('"""') == 2:
                continue
            # 规则2
            if ("'''" in p or '"""' in p) and remark_flag is None:
                # start
                remark_flag = "first"
                continue

            elif remark_flag == "first":
                if "'''" in p or '"""' in p:
                    remark_flag = None
                continue
            else:
                pass

            # 规则3
            last_idx, space_line = [len(p), ""] if p.find('#') == -1 else [p.find('#'), '\n']
            new_py.write(p[0:last_idx] + space_line)

        new_py.close()
