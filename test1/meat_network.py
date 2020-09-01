import matplotlib.pyplot as m_plot
import pandas
import os
import json

# 获取当前路径
current_path = os.getcwd()
init_data_path = current_path + "\\init_data"
# 子文件夹：每个处理的叶子、或者根；
treat_dirs = os.listdir(init_data_path)


# 物质class的index简称
class_index_dict_obj = open("class_index_dict.json")
class_index_dict = json.load(class_index_dict_obj)
class_index_dict_obj.close()

# 物质class的CN源分析
class_CN_dict_obj = open("class_CN_dict.json")
class_CN_dict = json.load(class_CN_dict_obj)
class_CN_dict_obj.close()

def paint_one_excel(point_file_path, line_file_path, Pos_Neg, final_name):
    point_excel = pandas.read_excel(point_file_path)
    # 获取Excel中包含的所有class信息；
    all_classes = list(point_excel["Id"])

    m_plot.figure(dpi=300, figsize=(10, 10))
    line_excel = pandas.read_excel(line_file_path)
    x_ratio = 1
    # 画点；
    for index, line in enumerate(range(point_excel.shape[0])):
        compound_class = point_excel.iloc[index][0]
        # 物质在list中的index
        class_index = all_classes.index(compound_class)
        positive_count = point_excel.iloc[index][4]
        negative_count = point_excel.iloc[index][5]
        line_weight_count = None
        if Pos_Neg == "Positive":
            line_weight_count = positive_count
        elif Pos_Neg == "Negative":
            line_weight_count = negative_count
        x = class_index * x_ratio

        # 如果是N源则为黄色，否则为蓝色
        color = "y" if class_CN_dict[compound_class] == "N" else "b"
        m_plot.scatter(x, 1, color=color, linewidths=line_weight_count / 20, marker="|")
        m_plot.text(x, 0.95, class_index_dict[compound_class], rotation="vertical", horizontalalignment="center", verticalalignment="top")
        m_plot.scatter(x, 3, color=color, linewidths=line_weight_count / 20, marker="|")
        # verticalalignment设置垂直对齐方式：center, top, bottom, baseline
        # horizontalalignment设置水平对齐方式：left, right, center
        # rotation设置旋转角度：vertical, horizontal, 也可以为数字。
        m_plot.text(x, 3.05, class_index_dict[compound_class], rotation="vertical", horizontalalignment="center")

    # 连线；
    if Pos_Neg == "Positive":
        for index, line in enumerate(range(line_excel.shape[0])):
            source_class = line_excel.iloc[index][0]
            target_class = line_excel.iloc[index][1]
            source_x = all_classes.index(source_class) * x_ratio
            target_x = all_classes.index(target_class)
            line_weight = line_excel.iloc[index][6]
            if line_excel.iloc[index][7] == "Positive":
                # plot的前两参数是x的list和y的list;
                m_plot.plot([source_x, target_x], [1, 3], color="r", linewidth=line_weight / 10)
    elif Pos_Neg == "Negative":
        for index, line in enumerate(range(line_excel.shape[0])):
            source_class = line_excel.iloc[index][0]
            target_class = line_excel.iloc[index][1]
            source_x = all_classes.index(source_class) * x_ratio
            target_x = all_classes.index(target_class)
            line_weight = line_excel.iloc[index][6]
            if line_excel.iloc[index][7] == "Negative":
                # plot的前两参数是x的list和y的list;
                m_plot.plot([source_x, target_x], [1, 3], color="c", linewidth=line_weight / 10, linestyle=":")


    # 坐标轴不显示，
    m_plot.axis("off")

    # 边框调整
    m_plot.subplots_adjust(top=0.7, bottom=0.3, left=0.1, right=0.9, hspace=0, wspace=0)
    m_plot.show()

    # m_plot.savefig("./out_data/%s_%s.eps" % (final_name, Pos_Neg))
    # 清除所有之前的信息；
    # m_plot.clf()


for dir in treat_dirs:
    files = os.listdir(init_data_path + "\\" + dir)
    point_file = [file for file in files if "point" in file][0]
    line_file = [file for file in files if "line" in file][0]
    point_file_path = init_data_path + "\\" + dir + "\\" + point_file
    line_file_path = init_data_path + "\\" + dir + "\\" + line_file
    paint_one_excel(point_file_path, line_file_path, "Positive", files[0].split("_")[0])
    paint_one_excel(point_file_path, line_file_path, "Negative", files[0].split("_")[0])
    # m_plot.show()

    break