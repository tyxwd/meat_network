import matplotlib.pyplot as m_plot
import pandas
import os
import json
# 画热力图的包
import seaborn


class Meat_Network():
    meat_plot = m_plot
    current_path = None
    init_data_path = None
    treat_dirs = None
    class_index_dict = None
    class_CN_dict = None
    meat_plot_rows = 6
    meat_plot_cols = 2

    def __init__(self):
        super()

    # 获取文件路径
    @classmethod
    def get_treat_dirs(cls):
        # 获取当前路径
        cls.current_path = os.getcwd()
        cls.init_data_path = cls.current_path + "\\init_data"
        # 子文件夹：每个处理的叶子、或者根；
        cls.treat_dirs = os.listdir(cls.init_data_path)

    # 获取class的简称
    @classmethod
    def get_shorted(cls):
        # 物质class的index简称
        class_index_dict_obj = open("class_index_dict.json")
        cls.class_index_dict = json.load(class_index_dict_obj)
        class_index_dict_obj.close()

    @classmethod
    def get_CN_dict(cls):
        # 物质class的CN源分析
        class_CN_dict_obj = open("class_CN_dict.json")
        cls.class_CN_dict = json.load(class_CN_dict_obj)
        class_CN_dict_obj.close()

    # 获取list中的唯一值，返回；
    @classmethod
    def get_unique_list(cls, init_list):
        temp_list = []
        for item in init_list:
            if item not in temp_list:
                temp_list.append(item)
        return temp_list

    @classmethod
    def paint_point(cls, line_excel, Neg_Pos="Positive"):
        line_excel = line_excel
        point_y = 1
        if Neg_Pos == "Negative":
            line_excel = line_excel[line_excel["Neg_Pos"]=="Negative"]
        elif Neg_Pos == "Positive":
            line_excel = line_excel[line_excel["Neg_Pos"]=="Positive"]
        source_class_list = cls.get_unique_list(list(line_excel["Source"]))
        target_class_list = cls.get_unique_list(list(line_excel["Target"]))
        for source_or_target in ["Source", "Target"]:
            enumerate_list = None
            if source_or_target == "Source":
                point_y = 1
                enumerate_list = source_class_list
            elif source_or_target == "Target":
                point_y = 3
                enumerate_list = target_class_list
            for index, meat_class in enumerate(enumerate_list):
                # 获取该class的横坐标x值，
                meat_class_x = index
                # 该class的宽度；
                meat_class_width = line_excel[source_or_target].value_counts()[meat_class]

                # 如果是N源则为黄色，否则为蓝色
                color = "y" if cls.class_CN_dict[meat_class] == "N" else "b"

                if source_or_target == "Source":
                    cls.meat_plot.scatter(meat_class_x, point_y, color=color, linewidths=meat_class_width / 20, marker="|")
                    cls.meat_plot.text(meat_class_x, point_y - 0.05, cls.class_index_dict[meat_class], rotation="vertical",
                                horizontalalignment="center", verticalalignment="top")
                elif source_or_target == "Target":
                    cls.meat_plot.scatter(meat_class_x, point_y, color=color, linewidths=meat_class_width / 20, marker="|")
                    # verticalalignment设置垂直对齐方式：center, top, bottom, baseline
                    # horizontalalignment设置水平对齐方式：left, right, center
                    # rotation设置旋转角度：vertical, horizontal, 也可以为数字。
                    m_plot.text(meat_class_x, 3.05, cls.class_index_dict[meat_class], rotation="vertical",
                                horizontalalignment="center")

        # 返回class_list, 方便画line时获取x的值；
        return source_class_list, target_class_list

    @classmethod
    def paint_line(cls, line_excel, soure_class_list, target_class_list, Neg_Pos="Positive"):
        line_excel = line_excel
        if Neg_Pos == "Negative":
            line_excel = line_excel[line_excel["Neg_Pos"]=="Negative"]
        elif Neg_Pos == "Positive":
            line_excel = line_excel[line_excel["Neg_Pos"]=="Positive"]
        # 连线；
        for index, line in enumerate(range(line_excel.shape[0])):
            source_class = line_excel.iloc[index][0]
            target_class = line_excel.iloc[index][1]
            source_x = soure_class_list.index(source_class)
            target_x = target_class_list.index(target_class)
            line_weight = line_excel.iloc[index][6]
            cls.meat_plot.plot([source_x, target_x], [1, 3], color="r", linewidth=line_weight / 10)

    @classmethod
    def paint_network(cls, point_file_path, line_file_path, Neg_Pos, image_index):
        # point_excel = pandas.read_excel(point_file_path)
        line_excel = pandas.read_excel(line_file_path)

        cls.meat_plot.subplot(cls.meat_plot_rows, cls.meat_plot_cols, image_index)
        cls.meat_plot.axis("off")

        # 画点，
        source_class_list, target_class_list = cls.paint_point(line_excel, Neg_Pos)

        # 连线
        cls.paint_line(line_excel, source_class_list, target_class_list, Neg_Pos)

    @classmethod
    def paint_heatmap(cls, corr_excel, Neg_Pos=None, image_index=None):
        # seaborn.heatmap(corr_excel, cmap="RdYlBu_r")
        # center = 0, 中间颜色的值
        seaborn.clustermap(corr_excel, cmap="RdYlBu_r", linewidths=0.15, linecolor="k")


    @classmethod
    def start(cls):
        # 先获得文件夹位置
        cls.get_treat_dirs()
        cls.get_shorted()
        cls.get_CN_dict()
        cls.meat_plot.figure(dpi=300, figsize=(10, 10))
        for index, dir in enumerate(cls.treat_dirs):
            files = os.listdir(cls.init_data_path + "\\" + dir)
            point_file = [file for file in files if "point" in file][0]
            line_file = [file for file in files if "line" in file][0]
            point_file_path = cls.init_data_path + "\\" + dir + "\\" + point_file
            line_file_path = cls.init_data_path + "\\" + dir + "\\" + line_file
            print(point_file_path)
            cls.paint_network(point_file_path, line_file_path, "Positive", 2 * index + 1)
            cls.paint_network(point_file_path, line_file_path, "Negative", 2 * index + 2)
        cls.meat_plot.savefig("fig.eps")


if __name__ == '__main__':
    # Meat_Network.start()
    excel = pandas.read_excel("./F_R_data/Ap_negative_corr.xlsx", index_col=0)
    Meat_Network.paint_heatmap(excel)
    Meat_Network.meat_plot.show()
