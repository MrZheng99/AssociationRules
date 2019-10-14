# *-* coding:utf-8 *-*
import pandas as pd
import AssociationRules.myFpTree.TreeNode as TNode
from AssociationRules.RelationRlue import GetRule


def getData(fp):
    df = pd.read_csv(fp, encoding="utf-8", header=None,
                     keep_default_na=False)
    colnum, rownum = df.shape
    D = df.values.tolist()
    for i in range(colnum - 1, -1, -1):
        for j in range(rownum - 1, -1, -1):
            if D[i][j] == "":
                del D[i][j]
    sourseSet = {}
    for trans in D:
        sourseSet[frozenset(trans)] = sourseSet.get(frozenset(trans), 0) + 1
    for e in sourseSet:
        print(e)
    return sourseSet, colnum


def getHeaderTable(dataSet):
    headerTable = {}
    for trans in dataSet:
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]
    headerTable = {k: v for k, v in headerTable.items() if v >= minSup}
    freqItemSet = set(headerTable.keys())
    if len(freqItemSet) == 0:
        return None, None
    for k in headerTable:
        headerTable[k] = [headerTable[k], None]
    return headerTable, freqItemSet


def getOrderItems(tranSet, headerTable, freqItemSet):
    localD = {}
    for item in tranSet:
        if item in freqItemSet:
            localD[item] = headerTable[item][0]
    if len(localD) > 0:
        orderedItems = [v[0] for v in
                        sorted(localD.items(), key=lambda p: p[1],
                               reverse=True)]
        return orderedItems


def createFpTree(dataSet, minSup=1):
    headerTable, freqItemSet = getHeaderTable(dataSet)
    retTree = TNode.TreeNode('root', 1, None)  # 创建树
    for tranSet, count in dataSet.items():
        orderedItems = getOrderItems(tranSet, headerTable, freqItemSet)
        if orderedItems != None:
            updateTree(orderedItems, retTree, headerTable,
                       count)  # 将排序后的item集合填充的树中
    return retTree, headerTable  # 返回树型结构和头指针表


def updateTree(items, TreeRoot, headerTable, count):
    p = items[0]
    if p in TreeRoot.children:
        TreeRoot.children[p].addFre(count)
    else:
        TreeRoot.children[p] = TNode.TreeNode(p, count, TreeRoot)
        newChild = TreeRoot.children[p]
        if headerTable[p][1] == None:  # 更新头指针表
            headerTable[p][1] = newChild
        else:
            updateHeader(headerTable[p][1], newChild)
    if len(items) > 1:  # 不断迭代调用自身，每次调用都会删掉列表中的第一个元素
        updateTree(items[1:], TreeRoot.children[p], headerTable, count)


def updateHeader(nodeToTest, targetNode):
    while (nodeToTest.nodeLink != None):
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode


def ascendFpTree(leafNode, prefixPath):  # 迭代上溯整棵树
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendFpTree(leafNode.parent, prefixPath)


def getPrePath(basePat, treeNode):
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendFpTree(treeNode, prefixPath)
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.frequent
        treeNode = treeNode.nodeLink
    return condPats


def getFreList(FpTree, headerTable, minSup, preFix, freqItemList):
    OrderItem = [v[0] for v in
                 sorted(headerTable.items(), key=lambda p: p[1][0])]
    for basePat in OrderItem:  # 从头指针表的底端开始
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        freqItemList.append(
            {"".join(sorted(newFreqSet)): headerTable[basePat][0]})
        # print("freItem add:",newFreqSet)
        condPattBases = getPrePath(basePat=basePat,
                                   treeNode=headerTable[basePat][1])
        # 根据条件模式基,创建条件FP树
        myCondTree, myHead = createFpTree(condPattBases, minSup)
        if myHead != None:  # 挖掘条件FP树
            getFreList(myCondTree, myHead, minSup, newFreqSet, freqItemList)


def getFreDict(freList):
    # 最大频繁集
    maxFreSet = []
    # 获取最大频繁集的真子集
    freSet = {}
    for e in freList:
        freSet.update(e)
    freSet = {k: v for k, v in
              sorted(freSet.items(), key=lambda x: (len(x[0]), x[0]))}
    if len(freSet) != 0:
        k = list(freSet.keys())[-1]
        maxKeyLen = len(k)
        maxFreSet = {k: v for k, v in freSet.items() if len(k) == maxKeyLen}
    return maxFreSet, freSet


if __name__ == "__main__":
    fp = "mydata.csv"
    sourseSet, colnum = getData(fp)
    minSup = 0.5 * colnum
    minConfidence = 0.7
    FPtree, HeaderTab = createFpTree(sourseSet, minSup=minSup)

    # FPtree.show()
    freList = []
    getFreList(FPtree, HeaderTab, minSup, set([]), freList)
    maxFreSet, finaFreDict, = getFreDict(freList)
    GetRule.getRelationRule(finaFreDict, minConfidence)
