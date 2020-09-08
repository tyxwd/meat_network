import pandas
# 可以计算p值的包
import scipy.stats as stats


class Corr_Utils:
    index_number_excel = None

    def __init__(self):
        super()

    @classmethod
    # 计算相关系数的方法；(传最初的compound的量的Excel)
    def get_corr_value(cls, specie_excel_x, excel_y=None, p_value_threshold=0.01):
        # excel所有的列；
        x_columns = list(specie_excel_x.columns)

        # 如果只有一张表，自己和自己
        y_columns = x_columns
        specie_excel_y = specie_excel_x
        # 不是的话，就有y的表
        if excel_y is not None:
            specie_excel_y = excel_y
            y_columns = list(specie_excel_y.columns)
        # 先用两个list直接装p值，后面直接生成DataFrame，加快速度；
        corr_value_lists = []
        p_value_lists = []

        for column_index, column in enumerate(x_columns):
            corr_value_list = []
            # p_value_list = []
            for col_index, col in enumerate(y_columns):
                corr_value, p_value = stats.spearmanr(specie_excel_x[column], specie_excel_y[col])

                # 如果p值大于给定值，改成None,并且删除相关系数；
                if p_value > p_value_threshold:
                    corr_value = 0
                corr_value_list.append(corr_value)
            corr_value_lists.append(corr_value_list)

        # 生成corr_value的Excel
        corr_value_excel = pandas.DataFrame(corr_value_lists, columns=y_columns, index=x_columns)
        # p_value_excel.to_excel(rootPath + "\\data/out_data/final_OTU_p.xlsx")
        return corr_value_excel

    @classmethod
    # 从相关系数表格生成line表格；(compound、class都可以)
    def to_line_excel(cls, corr_excel):
        corr_excel = corr_excel.fillna(0)
        line_excel_col_index = ["Source", "Target", "Type", "Id", "Label", "timeset", "Weight", "Neg_Pos"]
        source_index_list = list(corr_excel.index)
        target_index_list = list(corr_excel.columns)

        line_excel = pandas.DataFrame(columns=line_excel_col_index)
        id = 0
        for source in source_index_list:
            for target in target_index_list:
                item = corr_excel.loc[source, target]
                # 负相关
                if item < 0:
                    id += 1
                    line_list = [source, target, "Undirected", id, None, None, abs(item), "Negative"]
                    line_excel_list_dict = dict(zip(line_excel_col_index, line_list))
                    line_excel = line_excel.append([line_excel_list_dict], ignore_index=False)
                elif item > 0:
                    id += 1
                    line_list = [source, target, "Undirected", id, None, None, abs(item), "Positive"]
                    line_excel_list_dict = dict(zip(line_excel_col_index, line_list))
                    line_excel = line_excel.append([line_excel_list_dict], ignore_index=False)
        return line_excel

    @classmethod
    def get_compound_class(cls, index=None, compound=None):
        compound_class = None
        if index is not None:
            compound_class = list(cls.index_number_excel[cls.index_number_excel["index"] == index]["Class"])[0]
        return compound_class

    @classmethod
    # 根据每个物质的line表格，生成class的corr(类似)表格；
    def get_class_corr_excel(cls, compound_line_excel):
        source_classes = []
        target_classes = []
        for source in compound_line_excel["Source"]:
            source_class = "F_" + cls.get_compound_class(int(source.split("_")[0]))

            if source_class not in source_classes:
                source_classes.append(source_class)
        for target in compound_line_excel["Target"]:
            target_class = "R_" + cls.get_compound_class(int(target.split("_")[0]))
            if target_class not in target_classes:
                target_classes.append(target_class)

        class_positive_excel = pandas.DataFrame(columns=target_classes, index=source_classes)
        class_positive_excel.fillna(0, inplace=True)
        class_negative_excel = pandas.DataFrame(columns=target_classes, index=source_classes)
        class_negative_excel.fillna(0, inplace=True)
        # 生成point表
        index = 0
        # excel表的行数
        rows = compound_line_excel.shape[0]

        columns = list(compound_line_excel.columns)
        # 获得每个列是第几列；
        target_col = columns.index("Target")
        source_col = columns.index("Source")
        Neg_Pos_col = columns.index("Neg_Pos")
        for row in range(rows):
            source_compound = compound_line_excel.iloc[row, target_col]
            target_compound = compound_line_excel.iloc[row, source_col]
            source_class = "F_" + cls.get_compound_class(int(source_compound.split("_")[0]))
            target_class = "R_" + cls.get_compound_class(int(target_compound.split("_")[0]))

            # 该物质的Neg_Pos
            Neg_Pos = compound_line_excel.iloc[row, Neg_Pos_col]
            if Neg_Pos == "Positive":
                class_positive_excel.loc[source_class, target_class] = 1 + class_positive_excel.loc[
                    source_class, target_class]
            elif Neg_Pos == "Negative":
                class_negative_excel.loc[source_class, target_class] = 1 + class_negative_excel.loc[
                    source_class, target_class]

        return class_positive_excel, class_negative_excel

    @classmethod
    def get_class_line_excel(cls, positive_corr_excel, negative_corr_excel):
        # 两个（positive、negative）的line表格，后面进行合并；
        line_excel_list = []
        for corr_excel in [positive_corr_excel, negative_corr_excel * -1]:
            line_excel = cls.to_line_excel(corr_excel)
            line_excel_list.append(line_excel)
        # 合并两表格
        class_line_excel = pandas.concat(line_excel_list)
        return class_line_excel


if __name__ == '__main__':
    Corr_Utils.index_number_excel = pandas.read_excel("./init_data/index_number.xlsx")
    # species = ["Ap", "As"]
    # for specie in species:
    #     file_path = "./init_data/%s_0.01.xlsx" % specie
    #     corr_excel = pandas.read_excel(file_path, index_col=0)
    #     compound_line_excel = Corr_Utils.to_line_excel(corr_excel)
    #     # compound_line_excel.to_excel("line.xlsx")
    #     # class 的相关系数；
    #     print("计算相关系数")
    #     class_positive_excel, class_negative_excel = Corr_Utils.get_class_corr_excel(compound_line_excel)
    #     class_positive_excel.to_excel("./out_data/%s_positive_corr.xlsx" % specie)
    #     class_negative_excel.to_excel("./out_data/%s_negative_corr.xlsx" % specie)
    #
    #     # class 的line表格；
    #     class_line_excel = Corr_Utils.get_class_line_excel(class_positive_excel, class_negative_excel)
    #     class_line_excel.to_excel("./out_data/%s_class_line.xlsx" % specie, index=False)
    F_excel = pandas.read_excel(r".\init_data\进R分析数据_不考虑虫子_F.xlsx", sheet_name="Ap-F")
    R_excel = pandas.read_excel(r".\init_data\进R分析数据_不考虑虫子_R.xlsx", sheet_name="Ap-R")
    corr_excel = Corr_Utils.get_corr_value(F_excel, R_excel)
    corr_excel.to_excel("coor.xlsx")
