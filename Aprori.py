# *-* coding:utf-8 *-*
# Running environment  : pycharm  community 2018.9
# python version : 3.7.2
import pandas as pd
from AssociationRules.RelationRlue import HasCom as HS
from AssociationRules.RelationRlue import GetRule
# 从文件中读取数据并处理缺失值，最终数据类似[['a','b','c'],['c','d']]
def getData(fp):
    df = pd.read_csv(fp, encoding="utf-8", header=None,
                     keep_default_na=False)
    colnum, rownum = df.shape
    l = df.values.tolist()
    for i in range(colnum - 1, -1, -1):
        for j in range(rownum - 1, -1, -1):
            if l[i][j] == "":
                del l[i][j]
    return l

# 获取一元的候选集类似{'太': 17, '上': 41, '經': 25, '清': 28}
def getOneDimSet(l):
    s = {}
    for subl in l:
        subl = set(subl)
        for e in subl:
            s[e] = s[e] + 1 if e in s.keys() else 1
    return s

# 去掉不满足最小支持度的集合，返回满足最小支持度的频繁集
def delEle(s, minSuport):
    d = {k:v for k,v in sorted(s.items(),key=lambda x:x[1],reverse=True) if v>=minSupport}
    return d

# 看两个集合是否存在公共部分，若存在则返回连接后的集合，比如"ab"和"bc"存在共有部分，返回值为"abc"
# 若不存在，则返回None
# mode 参数说明：若为True则表示输入的两个集合的元素个数必须一样
#               若为False则可以不要求两个集合个数一样多
# 将两个集合连接
def addTwoEle(s1, s2, mode):
    s = HS.hasCommen(s1, s2, mode=mode)
    if s == None:
        return None
    else:
        return s


# 获取某个集合的频率
def getEleFre(e, L):
    count = 0
    set1 = set(e)
    for l in L :
        if set1.issubset(set(l)):
            count +=1
    return count

#   产生新的频繁集
def getNewSet(s, L0):
    S2 = {}
    for k1 in s.keys():
        for k2 in s.keys():
            if k1 != k2:
                e = addTwoEle(k1, k2, mode=True)
                if e == None:
                    continue
                else:
                    f = getEleFre(e, L0)
                    S2[e] = f
    return S2


#  获取所有的频繁集字典
def getFreDict(freList):
    # 候选集列表freList最后一个元素为空删除
    if len(freList[-1]) == 0:
        del freList[-1]
    # 最大频繁集
    maxFreSet = freList[-1]
    # 获取最大频繁集的真子集
    freSet = {}
    for e in freList:
        freSet.update(e)
    return maxFreSet, freSet

if __name__ == "__main__":
    # 原始数据
    fp = "mydata.csv"
    L = getData(fp)
    colnum = len(L)
    minSupport = 0.5 * colnum
    minConfidence = 0.7
    # 获取长度为一的元素的集合
    S1 = getOneDimSet(L)
    # 筛选不满足最小支持度的元素
    L1 = delEle(S1, minSupport)
    # 将长度为一的元素组合成长度为二的元素集合
    S2 = getNewSet(L1, L)
    freList = []
    freList.append(L1)
    #   生成频繁集，直到获取到最大频繁集
    while len(S2) != 0:
        L2 = delEle(S2, minSupport)
        freList.append(L2)
        S2 = getNewSet(L2, L)
    # max_L为最大频繁集，d为最大频繁集的真子集
    max_FreSet, freSet = getFreDict(freList)
    print(max_FreSet,freSet)
    GetRule.getRelationRule(freSet, minConfidence)
    print(len(freSet))
