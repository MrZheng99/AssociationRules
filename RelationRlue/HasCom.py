# *-* coding: utf-8 *-*
def hasCommen(s1, s2, mode):
    set1 = set([str(e) for e in s1])
    set2 = set([str(e) for e in s2])
    if len(s1) != len(s2) and mode == True:
        raise EOFError("当前mode=True,输入的两个元素长度不一致")
    union = set1 & set2
    if len(union) != None and mode == True:
        return "".join(sorted(set1 | set2))
    if len(union) != None and mode == False:
        return "".join(sorted(union))
    return None