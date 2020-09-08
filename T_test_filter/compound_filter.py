import pandas
import numpy


class Filter():
    init_excel = pandas.read_excel("./compound_index.xlsx")

    def __int__(self):
        pass

    # 从Excel中找到，t——test有差异的物质；
    @classmethod
    def find_compound(cls, original_excel, root_leaf="root"):
        compound_list = []
        for col in range(5):
            if col == 0:
                compound_list.append(list(original_excel[original_excel["diff"] > 0]["Chem"]))
            elif col == 2:
                # as/ap，这列的值不需要；
                continue
            else:
                compound_list.append(list(original_excel[original_excel["diff.%d" % col] > 0]["Chem.%d" % col]))
        compound_excel = pandas.DataFrame(compound_list, index=["Ap-Ah", "Ap-Cp", "As-Ah", "As-Cp"]).T
        # compound_excel.to_excel("./out_data/%s_change_compound.xlsx" % root_leaf, index=False)
        return compound_excel

    @classmethod
    # index匹配compound的直接方法
    def index_recall(cls, index):
        try:
            compound = list(cls.init_excel[cls.init_excel["Chem"] == index]["Compounds"])[0]
        except:
            compound = None
        return compound

    # root 或 leaf的；
    # 整理差异物质，匹配原始compound名，筛选出Ap/As地上地下物质；进行后面的corr分析；
    @classmethod
    def get_unique_compound_excel(cls, compound_change_excel, root_leaf="root"):
        unique_compound_lists = []
        for specie in ["Ap", "As"]:
            # 一个物种的物质
            compound_list = []
            for insect in ["Ah", "Cp"]:
                compound = list(compound_change_excel["%s-%s" % (specie, insect)])

                # 使用filter()函数，删除列表中的None值
                compound = list(filter(None, compound))
                compound_list.extend(compound)

            unique_compound_lists.append(numpy.unique(compound_list))
        unique_compound_excel = pandas.DataFrame(unique_compound_lists,
                                                 index=["Ap_%s" % root_leaf, "As_%s" % root_leaf]).T

        # 遍历并替换Excel中的简写
        for col in range(unique_compound_excel.shape[1]):
            for row in range(unique_compound_excel.shape[0]):
                item = unique_compound_excel.iloc[row, col]
                compound = cls.index_recall(item)
                unique_compound_excel.iloc[row, col] = compound

        return unique_compound_excel


if __name__ == '__main__':
    for part in ["leaf", "root"]:
        original_excel = pandas.read_excel("./response to herb.xlsx", sheet_name="%s changes" % part, header=1)
        compound_excel = Filter.find_compound(original_excel, part)
        unique_compound_excel = Filter.get_unique_compound_excel(compound_excel, part)
        unique_compound_excel.to_excel("./out_data/%s_unique_compound.xlsx" % part, index=False)
