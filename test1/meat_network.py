import matplotlib.pyplot as m_plot
import pandas
import os
import json


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
    def paint_excel(cls, point_file_path, line_file_path, Neg_Pos, image_index):
        # point_excel = pandas.read_excel(point_file_path)
        line_excel = pandas.read_excel(line_file_path)

        cls.meat_plot.subplot(cls.meat_plot_rows, cls.meat_plot_cols, image_index)
        cls.meat_plot.axis("off")

        # 画点，
        source_class_list, target_class_list = cls.paint_point(line_excel, Neg_Pos)

        # 连线
        cls.paint_line(line_excel, source_class_list, target_class_list, Neg_Pos)

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
            cls.paint_excel(point_file_path, line_file_path, "Positive", 2 * index + 1)
            cls.paint_excel(point_file_path, line_file_path, "Negative", 2 * index + 2)
        cls.meat_plot.savefig("fig.eps")
# 获取当前路径
# current_path = os.getcwd()
# init_data_path = current_path + "\\init_data"
# # 子文件夹：每个处理的叶子、或者根；
# treat_dirs = os.listdir(init_data_path)
#
#
# # 物质class的index简称
# class_index_dict_obj = open("class_index_dict.json")
# class_index_dict = json.load(class_index_dict_obj)
# class_index_dict_obj.close()
#
# # 物质class的CN源分析
# class_CN_dict_obj = open("class_CN_dict.json")
# class_CN_dict = json.load(class_CN_dict_obj)
# class_CN_dict_obj.close()


# def paint_one_excel(point_file_path, line_file_path, Pos_Neg, final_name):
#     point_excel = pandas.read_excel(point_file_path)
#     # 获取Excel中包含的所有class信息；
#     all_classes = list(point_excel["Id"])
#
#     m_plot.figure(dpi=300, figsize=(10, 10))
#     line_excel = pandas.read_excel(line_file_path)
#     x_ratio = 1
#     # 画点；
#     for index, line in enumerate(range(point_excel.shape[0])):
#         compound_class = point_excel.iloc[index][0]
#         # 物质在list中的index
#         class_index = all_classes.index(compound_class)
#         positive_count = point_excel.iloc[index][4]
#         negative_count = point_excel.iloc[index][5]
#         line_weight_count = None
#         if Pos_Neg == "Positive":
#             line_weight_count = positive_count
#         elif Pos_Neg == "Negative":
#             line_weight_count = negative_count
#         x = class_index * x_ratio
#
#         # 如果是N源则为黄色，否则为蓝色
#         color = "y" if class_CN_dict[compound_class] == "N" else "b"
#         m_plot.scatter(x, 1, color=color, linewidths=line_weight_count / 20, marker="|")
#         m_plot.text(x, 0.95, class_index_dict[compound_class], rotation="vertical", horizontalalignment="center", verticalalignment="top")
#         m_plot.scatter(x, 3, color=color, linewidths=line_weight_count / 20, marker="|")
#         # verticalalignment设置垂直对齐方式：center, top, bottom, baseline
#         # horizontalalignment设置水平对齐方式：left, right, center
#         # rotation设置旋转角度：vertical, horizontal, 也可以为数字。
#         m_plot.text(x, 3.05, class_index_dict[compound_class], rotation="vertical", horizontalalignment="center")
#
#     # 连线；
#     if Pos_Neg == "Positive":
#         for index, line in enumerate(range(line_excel.shape[0])):
#             source_class = line_excel.iloc[index][0]
#             target_class = line_excel.iloc[index][1]
#             source_x = all_classes.index(source_class) * x_ratio
#             target_x = all_classes.index(target_class)
#             line_weight = line_excel.iloc[index][6]
#             if line_excel.iloc[index][7] == "Positive":
#                 # plot的前两参数是x的list和y的list;
#                 m_plot.plot([source_x, target_x], [1, 3], color="r", linewidth=line_weight / 10)
#     elif Pos_Neg == "Negative":
#         for index, line in enumerate(range(line_excel.shape[0])):
#             source_class = line_excel.iloc[index][0]
#             target_class = line_excel.iloc[index][1]
#             source_x = all_classes.index(source_class) * x_ratio
#             target_x = all_classes.index(target_class)
#             line_weight = line_excel.iloc[index][6]
#             if line_excel.iloc[index][7] == "Negative":
#                 # plot的前两参数是x的list和y的list;
#                 m_plot.plot([source_x, target_x], [1, 3], color="c", linewidth=line_weight / 10, linestyle=":")
#
#
#     # 坐标轴不显示，
#     m_plot.axis("off")
#
#     # 边框调整
#     m_plot.subplots_adjust(top=0.7, bottom=0.3, left=0.1, right=0.9, hspace=0, wspace=0)
#     m_plot.show()
#
#     # m_plot.savefig("./out_data/%s_%s.eps" % (final_name, Pos_Neg))
#     # 清除所有之前的信息；
#     # m_plot.clf()


# for dir in treat_dirs:
#     files = os.listdir(init_data_path + "\\" + dir)
#     point_file = [file for file in files if "point" in file][0]
#     line_file = [file for file in files if "line" in file][0]
#     point_file_path = init_data_path + "\\" + dir + "\\" + point_file
#     line_file_path = init_data_path + "\\" + dir + "\\" + line_file
#     paint_one_excel(point_file_path, line_file_path, "Positive", files[0].split("_")[0])
#     paint_one_excel(point_file_path, line_file_path, "Negative", files[0].split("_")[0])
#     # m_plot.show()
#
#     break

if __name__ == '__main__':
    Meat_Network.start()