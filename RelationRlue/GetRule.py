# *-* coding: utf-8 *-*
from AssociationRules.RelationRlue import HasCom as HS
#  产生强关联规则
def getRelationRule(freSet, minConfidence):
    for itemSetA in freSet:
        for itemSetB in freSet:
            if len(HS.hasCommen(itemSetA,itemSetB,mode=False))==0:
                union = ''.join(sorted(set(itemSetA)|set(itemSetB)))
                if union in freSet:
                    confidence = freSet[union] / freSet[itemSetA]
                    if (confidence > minConfidence):
                        print(itemSetA + "-->" + itemSetB, end=" ")
                        print(confidence)

