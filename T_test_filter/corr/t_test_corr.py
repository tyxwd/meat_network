from corr_coefficient import corr
import pandas
import numpy


# 根据进R分析数据，改回其column的index值
def change_index(data_frame):
    index_number = pandas.read_excel(r"./index_number.xlsx", index_col=0)
    compounds = index_number.index.tolist()
    compound_index = index_number["index"].tolist()
    compound_index_dict = dict(zip(compound_index, compounds))

    columns = data_frame.columns.tolist()

    new_columns = []
    for index, column in enumerate(columns):
        new_column = int(column.split("_")[0])
        new_columns.append(compound_index_dict[new_column])

    # 将原先的columns改回去
    data_frame.columns = new_columns
    return data_frame


# filter之后保留的compounds数据
def filter_compounds(dataframe, species_part="Ap_leaf"):
    Ap_F_compounds = all_change_compound[species_part].tolist()

    # 删除nan值
    while numpy.nan in Ap_F_compounds:
        Ap_F_compounds.remove(numpy.nan)
    print(len(Ap_F_compounds))

    Ap_F_excel = change_index(dataframe)
    Ap_F_excel_columns = Ap_F_excel.columns

    # 删除没有的columns
    new_Ap_F_compounds = []
    for compound in Ap_F_compounds:
        if compound in Ap_F_excel_columns:
            new_Ap_F_compounds.append(compound)

    print(len(new_Ap_F_compounds))

    Ap_F_excel = Ap_F_excel[new_Ap_F_compounds]
    return Ap_F_excel


# 获取数据后计算相关系数
def get_corr(leaf_excel, root_excel):
    corr_excel = corr.Corr_Utils.get_corr_value(leaf_excel, root_excel)

    # 修改corrExcel的index和column
    indexs = corr_excel.index.tolist()
    for index, item in enumerate(indexs):
        indexs[index] = "F_" + item

    columns = corr_excel.columns.tolist()
    for index, item in enumerate(columns):
        columns[index] = "R_" + item

    corr_excel.index = indexs
    corr_excel.columns = columns
    return corr_excel


# 获取lineExcel；
def get_line_excel(corr_excel):
    line_excel = corr.Corr_Utils.to_line_excel(corr_excel)
    return line_excel


# 获取pointExcel
def get_point_excel(line_excel):
    # point表格的列名
    # columns = ["Id", "Label", "timeset"]

    # 获取所有的point，排除重复值
    source_points = line_excel["Source"].unique().tolist()
    target_points = line_excel["Target"].unique().tolist()
    all_points = source_points + target_points

    point_excel = pandas.DataFrame(index=all_points)
    point_excel["Id"] = all_points
    point_excel["Label"] = all_points
    point_excel["timeset"] = None

    index_number = pandas.read_excel(r"./index_number.xlsx", index_col=0)
    index_number_indexs = index_number.index.tolist()

    index_number_F = index_number.copy()
    index_number_F_index = index_number_indexs
    for index, item in enumerate(index_number_F_index):
        index_number_indexs[index] = "F_" + item
    index_number_F.index = index_number_F_index

    index_number_R = index_number.copy()
    index_number_R_index = index_number_indexs
    for index, item in enumerate(index_number_R_index):
        index_number_indexs[index] = "F_" + item
    index_number_R.index = index_number_R_index

    finall_index_excel = pandas.concat([index_number_F, index_number_R])

    point_excel["Class"] = finall_index_excel["Class"]
    for index, row in enumerate(all_points):
        if index < len(source_points):
            point_excel.loc[row, "Part"] = "leaf"
        else:
            point_excel.loc[row, "Part"] = "root"
    # point_excel.to_excel("point.xlsx", index=False)
    return point_excel


if __name__ == '__main__':
    # #
    # leaf_compound = pandas.read_excel(r"..\out_data\leaf_unique_compound.xlsx")
    # root_compound = pandas.read_excel(r"..\out_data\root_unique_compound.xlsx")
    # all_change_compound = pandas.concat([leaf_compound, root_compound], axis=1)
    # # print(all_change_compound)
    #
    # # F
    # Ap_F = pandas.read_excel(r".\进R分析数据_不考虑虫子_F.xlsx", sheet_name='Ap-F', index_col=0)
    # As_F = pandas.read_excel(r".\进R分析数据_不考虑虫子_F.xlsx", sheet_name='As-F', index_col=0)
    # Ap_F_filter = filter_compounds(Ap_F, "Ap_leaf")
    # As_F_filter = filter_compounds(As_F, "As_leaf")
    # # R
    # Ap_R = pandas.read_excel(r".\进R分析数据_不考虑虫子_R.xlsx", sheet_name='Ap-R', index_col=0)
    # As_R = pandas.read_excel(r".\进R分析数据_不考虑虫子_R.xlsx", sheet_name='As-R', index_col=0)
    # Ap_R_filter = filter_compounds(Ap_R, "Ap_root")
    # As_R_filter = filter_compounds(As_R, "As_root")
    #
    # # Ap
    # corr_excel = get_corr(Ap_F_filter, Ap_R_filter)
    # corr_excel.to_excel("./corr_out_data/Ap_corr.xlsx", index=False)
    # line_excel = get_line_excel(corr_excel)
    # line_excel.to_excel("./corr_out_data/Ap_line.xlsx", index=False)
    # point_excel = get_point_excel(line_excel)
    # point_excel.to_excel("./corr_out_data/Ap_point.xlsx", index=False)
    #
    # # As
    # corr_excel = get_corr(As_F_filter, As_R_filter)
    # corr_excel.to_excel("./corr_out_data/As_corr.xlsx", index=False)
    # line_excel = get_line_excel(corr_excel)
    # line_excel.to_excel("./corr_out_data/As_line.xlsx", index=False)
    # point_excel = get_point_excel(line_excel)
    # point_excel.to_excel("./corr_out_data/As_point.xlsx", index=False)

    Ap_F_excel = pandas.read_excel(r".\进R分析数据_不考虑虫子_F.xlsx", sheet_name="Ap-F", index_col=0)
    Ap_F_excel = change_index(Ap_F_excel)
    Ap_R_excel = pandas.read_excel(r".\进R分析数据_不考虑虫子_R.xlsx", sheet_name="Ap-R", index_col=0)
    Ap_R_excel = change_index(Ap_R_excel)
    # corr_excel = corr.Corr_Utils.get_corr_value(Ap_F_excel, Ap_R_excel)
    corr_excel = get_corr(Ap_F_excel, Ap_R_excel)
    corr_excel.to_excel("Ap_compound_corr.xlsx")

    As_F_excel = pandas.read_excel(r".\进R分析数据_不考虑虫子_F.xlsx", sheet_name="As-F", index_col=0)
    As_F_excel = change_index(As_F_excel)
    As_R_excel = pandas.read_excel(r".\进R分析数据_不考虑虫子_R.xlsx", sheet_name="As-R", index_col=0)
    As_R_excel = change_index(As_R_excel)
    # corr_excel = corr.Corr_Utils.get_corr_value(As_F_excel, As_R_excel)
    corr_excel = get_corr(As_F_excel, As_R_excel)
    corr_excel.to_excel("As_compound_corr.xlsx")
