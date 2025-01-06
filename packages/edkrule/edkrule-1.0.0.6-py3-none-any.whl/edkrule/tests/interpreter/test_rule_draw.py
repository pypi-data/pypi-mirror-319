import json

from edkrule.edk_rule import EdkRule


def out_put(data):
    with open("debug.json", 'w') as f:
        json.dump(data, f)

def test_case1():
    rule_string = """a==1&&b==1?true:false"""
    expression = EdkRule.expression(rule_string)
    data = expression.tree_data()
    EdkRule.draw(rule_string, "rule1.html")
    # out_put(data)

    assert data == {"name": "TernaryOperator", "children": [{"name": "Anonymous", "children": [{"name": "Anonymous", "children": [{"name": "a", "value": "a", "type": 1}, {"name": "==", "value": "==", "type": 3}, {"name": "1", "value": "1", "type": 17}], "value": "a==1", "type": "statement"}, {"name": "&&", "value": "&&", "type": 19}, {"name": "Anonymous", "children": [{"name": "b", "value": "b", "type": 1}, {"name": "==", "value": "==", "type": 3}, {"name": "1", "value": "1", "type": 17}], "value": "b==1", "type": "statement"}], "value": "a==1&&b==1", "type": "statement"}, {"name": "?", "value": "?", "type": 30}, {"name": "true", "value": "true", "type": 22}, {"name": ":", "value": ":", "type": 14}, {"name": "false", "value": "false", "type": 23}], "value": "a==1&&b==1?true:false", "type": "statement"}



def test_case2():
    rule_string = """a&&b==1?x==1?true:false:false"""
    expression = EdkRule.expression(rule_string)
    data = expression.tree_data()
    EdkRule.draw(rule_string, "rule2.html")
    out_put(data)
    assert  data == {"name": "TernaryOperator", "children": [{"name": "Anonymous", "children": [{"name": "a", "value": "a", "type": 1}, {"name": "&&", "value": "&&", "type": 19}, {"name": "Anonymous", "children": [{"name": "b", "value": "b", "type": 1}, {"name": "==", "value": "==", "type": 3}, {"name": "1", "value": "1", "type": 17}], "value": "b==1", "type": "statement"}], "value": "a&&b==1", "type": "statement"}, {"name": "?", "value": "?", "type": 30}, {"name": "TernaryOperator", "children": [{"name": "Anonymous", "children": [{"name": "Anonymous", "children": [{"name": "x", "value": "x", "type": 1}, {"name": "==", "value": "==", "type": 3}, {"name": "1", "value": "1", "type": 17}], "value": "x==1", "type": "statement"}], "value": "x==1", "type": "statement"}, {"name": "?", "value": "?", "type": 30}, {"name": "true", "value": "true", "type": 22}, {"name": ":", "value": ":", "type": 14}, {"name": "false", "value": "false", "type": 23}], "value": "x==1?true:false", "type": "statement"}, {"name": ":", "value": ":", "type": 14}, {"name": "false", "value": "false", "type": 23}], "value": "a&&b==1?x==1?true:false:false", "type": "statement"}


def test_case3():
    rule_string = """a&&b==1?x==1?true:false:y==1?true:false"""
    expression = EdkRule.expression(rule_string)
    data = expression.tree_data()
    EdkRule.draw(rule_string, "rule3.html")
    out_put(data)
    assert data == {"name": "TernaryOperator", "children": [{"name": "Anonymous", "children": [{"name": "a", "value": "a", "type": 1}, {"name": "&&", "value": "&&", "type": 19}, {"name": "Anonymous", "children": [{"name": "b", "value": "b", "type": 1}, {"name": "==", "value": "==", "type": 3}, {"name": "1", "value": "1", "type": 17}], "value": "b==1", "type": "statement"}], "value": "a&&b==1", "type": "statement"}, {"name": "?", "value": "?", "type": 30}, {"name": "TernaryOperator", "children": [{"name": "Anonymous", "children": [{"name": "Anonymous", "children": [{"name": "x", "value": "x", "type": 1}, {"name": "==", "value": "==", "type": 3}, {"name": "1", "value": "1", "type": 17}], "value": "x==1", "type": "statement"}], "value": "x==1", "type": "statement"}, {"name": "?", "value": "?", "type": 30}, {"name": "true", "value": "true", "type": 22}, {"name": ":", "value": ":", "type": 14}, {"name": "false", "value": "false", "type": 23}], "value": "x==1?true:false", "type": "statement"}, {"name": ":", "value": ":", "type": 14}, {"name": "TernaryOperator", "children": [{"name": "Anonymous", "children": [{"name": "Anonymous", "children": [{"name": "y", "value": "y", "type": 1}, {"name": "==", "value": "==", "type": 3}, {"name": "1", "value": "1", "type": 17}], "value": "y==1", "type": "statement"}], "value": "y==1", "type": "statement"}, {"name": "?", "value": "?", "type": 30}, {"name": "true", "value": "true", "type": 22}, {"name": ":", "value": ":", "type": 14}, {"name": "false", "value": "false", "type": 23}], "value": "y==1?true:false", "type": "statement"}], "value": "a&&b==1?x==1?true:false:y==1?true:false", "type": "statement"}



def test_case4():
    rule_string = """a==1||b==2||c==3"""
    expression = EdkRule.expression(rule_string)
    data = expression.tree_data()
    EdkRule.draw(rule_string, "rule4.html")
    assert data == {"name": "Anonymous", "children": [{"name": "Anonymous", "children": [{"name": "Anonymous", "children": [{"name": "a", "value": "a", "type": 1}, {"name": "==", "value": "==", "type": 3}, {"name": "1", "value": "1", "type": 17}], "value": "a==1", "type": "statement"}, {"name": "||", "value": "||", "type": 21}, {"name": "Anonymous", "children": [{"name": "b", "value": "b", "type": 1}, {"name": "==", "value": "==", "type": 3}, {"name": "2", "value": "2", "type": 17}], "value": "b==2", "type": "statement"}], "value": "a==1||b==2", "type": "statement"}, {"name": "||", "value": "||", "type": 21}, {"name": "Anonymous", "children": [{"name": "c", "value": "c", "type": 1}, {"name": "==", "value": "==", "type": 3}, {"name": "3", "value": "3", "type": 17}], "value": "c==3", "type": "statement"}], "value": "a==1||b==2||c==3", "type": "statement"}



def test_case5():
    rule_string = """a==1||b==2||c"""
    expression = EdkRule.expression(rule_string)
    data = expression.tree_data()
    EdkRule.draw(rule_string, "rule5.html")
    out_put(data)
    assert data == {"name": "Anonymous", "children": [{"name": "Anonymous", "children": [{"name": "Anonymous", "children": [{"name": "a", "value": "a", "type": 1}, {"name": "==", "value": "==", "type": 3}, {"name": "1", "value": "1", "type": 17}], "value": "a==1", "type": "statement"}, {"name": "||", "value": "||", "type": 21}, {"name": "Anonymous", "children": [{"name": "b", "value": "b", "type": 1}, {"name": "==", "value": "==", "type": 3}, {"name": "2", "value": "2", "type": 17}], "value": "b==2", "type": "statement"}], "value": "a==1||b==2", "type": "statement"}, {"name": "||", "value": "||", "type": 21}, {"name": "c", "value": "c", "type": 1}], "value": "a==1||b==2||c", "type": "statement"}



def test_case6():
    rule_string = """a||b==2||c==2"""
    expression = EdkRule.expression(rule_string)
    data = expression.tree_data()
    EdkRule.draw(rule_string, "rule6.html")
    out_put(data)
    assert data == {"name": "Anonymous", "children": [{"name": "Anonymous", "children": [{"name": "a", "value": "a", "type": 1}, {"name": "||", "value": "||", "type": 21}, {"name": "Anonymous", "children": [{"name": "b", "value": "b", "type": 1}, {"name": "==", "value": "==", "type": 3}, {"name": "2", "value": "2", "type": 17}], "value": "b==2", "type": "statement"}], "value": "a||b==2", "type": "statement"}, {"name": "||", "value": "||", "type": 21}, {"name": "Anonymous", "children": [{"name": "c", "value": "c", "type": 1}, {"name": "==", "value": "==", "type": 3}, {"name": "2", "value": "2", "type": 17}], "value": "c==2", "type": "statement"}], "value": "a||b==2||c==2", "type": "statement"}



def test_case7():
    rule_string = """a||(b==2||c==2)"""
    expression = EdkRule.expression(rule_string)
    data = expression.tree_data()
    EdkRule.draw(rule_string, "rule7.html")
    out_put(data)
    assert data == {"name": "Anonymous", "children": [{"name": "a", "value": "a", "type": 1}, {"name": "||", "value": "||", "type": 21}, {"name": "Anonymous", "children": [{"name": "Anonymous", "children": [{"name": "Anonymous", "children": [{"name": "b", "value": "b", "type": 1}, {"name": "==", "value": "==", "type": 3}, {"name": "2", "value": "2", "type": 17}], "value": "b==2", "type": "statement"}, {"name": "||", "value": "||", "type": 21}, {"name": "Anonymous", "children": [{"name": "c", "value": "c", "type": 1}, {"name": "==", "value": "==", "type": 3}, {"name": "2", "value": "2", "type": 17}], "value": "c==2", "type": "statement"}], "value": "b==2||c==2", "type": "statement"}], "value": "b==2||c==2", "type": "statement"}], "value": "a||(b==2||c==2)", "type": "statement"}



def test_case8():
    rule_string = """max=a>b?a:b"""
    expression = EdkRule.expression(rule_string)
    data = expression.tree_data()
    EdkRule.draw(rule_string, "rule8.html")
    out_put(data)
    assert data == {"name": "Anonymous", "children": [{"name": "max", "value": "max", "type": 1}, {"name": "=", "value": "=", "type": 2}, {"name": "TernaryOperator", "children": [{"name": "Anonymous", "children": [{"name": "Anonymous", "children": [{"name": "a", "value": "a", "type": 1}, {"name": ">", "value": ">", "type": 7}, {"name": "b", "value": "b", "type": 1}], "value": "a>b", "type": "statement"}], "value": "a>b", "type": "statement"}, {"name": "?", "value": "?", "type": 30}, {"name": "a", "value": "a", "type": 1}, {"name": ":", "value": ":", "type": 14}, {"name": "b", "value": "b", "type": 1}], "value": "a>b?a:b", "type": "statement"}], "value": "max=a>b?a:b", "type": "statement"}



def test_case9():
    rule_string = """
    getSubjectArmCode=="Arm A: ONC-392 + LU 177 VIPIVOTIDE" || getSubjectArmCode=="Arm 1: ONC-392 LOW DOSE + LU 177 VIPIVOTIDE" || getSubjectArmCode=="Arm 2: ONC-392 HIGH DOSE + LU 177 VIPIVOTIDE"
    """
    expression = EdkRule.expression(rule_string)
    data = expression.tree_data()
    EdkRule.draw(rule_string, "rule9.html")

    assert data == {"name": "Anonymous", "children": [{"name": "Anonymous", "children": [{"name": "Anonymous", "children": [{"name": "getSubjectArmCode", "value": "getSubjectArmCode", "type": 1}, {"name": "==", "value": "==", "type": 3}, {"name": "\"Arm A: ONC-392 + LU 177 VIPIVOTIDE\"", "value": "\"Arm A: ONC-392 + LU 177 VIPIVOTIDE\"", "type": 1}], "value": "getSubjectArmCode==\"Arm A: ONC-392 + LU 177 VIPIVOTIDE\"", "type": "statement"}, {"name": "||", "value": "||", "type": 21}, {"name": "Anonymous", "children": [{"name": "getSubjectArmCode", "value": "getSubjectArmCode", "type": 1}, {"name": "==", "value": "==", "type": 3}, {"name": "\"Arm 1: ONC-392 LOW DOSE + LU 177 VIPIVOTIDE\"", "value": "\"Arm 1: ONC-392 LOW DOSE + LU 177 VIPIVOTIDE\"", "type": 1}], "value": "getSubjectArmCode==\"Arm 1: ONC-392 LOW DOSE + LU 177 VIPIVOTIDE\"", "type": "statement"}], "value": "getSubjectArmCode==\"Arm A: ONC-392 + LU 177 VIPIVOTIDE\"||getSubjectArmCode==\"Arm 1: ONC-392 LOW DOSE + LU 177 VIPIVOTIDE\"", "type": "statement"}, {"name": "||", "value": "||", "type": 21}, {"name": "Anonymous", "children": [{"name": "getSubjectArmCode", "value": "getSubjectArmCode", "type": 1}, {"name": "==", "value": "==", "type": 3}, {"name": "\"Arm 2: ONC-392 HIGH DOSE + LU 177 VIPIVOTIDE\"", "value": "\"Arm 2: ONC-392 HIGH DOSE + LU 177 VIPIVOTIDE\"", "type": 1}], "value": "getSubjectArmCode==\"Arm 2: ONC-392 HIGH DOSE + LU 177 VIPIVOTIDE\"", "type": "statement"}], "value": "\n    getSubjectArmCode==\"Arm A: ONC-392 + LU 177 VIPIVOTIDE\" || getSubjectArmCode==\"Arm 1: ONC-392 LOW DOSE + LU 177 VIPIVOTIDE\" || getSubjectArmCode==\"Arm 2: ONC-392 HIGH DOSE + LU 177 VIPIVOTIDE\"\n    ", "type": "statement"}



def test_case10():
    rule_string = """toDate($C1D1.ONC-392 Administration.ECSTDAT)!=""&& toDate($*.*.LBDAT)!=""&& toDate("2015-1-12 "+$C1D1.ONC-392 Administration.ECSTTIM+":00")!="" &&toDate("2015-1-12 "+$*.*.*+":00")!=""?dateDiff($C1D1.ONC-392 Administration.ECSTDAT+" "+$C1D1.ONC-392 Administration.ECSTTIM+":00",$*.*.LBDAT+" "+$*.*.*+":00","m")>0:true"""
    expression = EdkRule.expression(rule_string)
    data = expression.tree_data()
    EdkRule.draw(rule_string, "rule10.html")
    out_put(data)
    assert data == {"name": "TernaryOperator", "children": [{"name": "Anonymous", "children": [{"name": "Anonymous", "children": [{"name": "toDate", "children": [{"name": "$C1D1.ONC-392 Administration.ECSTDAT", "value": "$C1D1.ONC-392 Administration.ECSTDAT", "type": 9}], "value": "toDate($C1D1.ONC-392 Administration.ECSTDAT)", "type": "statement"}, {"name": "!=", "value": "!=", "type": 4}, {"name": "\"\"", "value": "\"\"", "type": 1}], "value": "toDate($C1D1.ONC-392 Administration.ECSTDAT)!=\"\"", "type": "statement"}, {"name": "&&", "value": "&&", "type": 19}, {"name": "Anonymous", "children": [{"name": "toDate", "children": [{"name": "$*.*.LBDAT", "value": "$*.*.LBDAT", "type": 9}], "value": "toDate($*.*.LBDAT)", "type": "statement"}, {"name": "!=", "value": "!=", "type": 4}, {"name": "\"\"", "value": "\"\"", "type": 1}], "value": "toDate($*.*.LBDAT)!=\"\"", "type": "statement"}, {"name": "&&", "value": "&&", "type": 19}, {"name": "Anonymous", "children": [{"name": "toDate", "children": [{"name": "Anonymous", "children": [{"name": "Anonymous", "children": [{"name": "\"2015-1-12 \"", "value": "\"2015-1-12 \"", "type": 1}, {"name": "+", "value": "+", "type": 15}, {"name": "$C1D1.ONC-392 Administration.ECSTTIM", "value": "$C1D1.ONC-392 Administration.ECSTTIM", "type": 9}], "value": "\"2015-1-12 \"+$C1D1.ONC-392 Administration.ECSTTIM", "type": "statement"}, {"name": "+", "value": "+", "type": 15}, {"name": "\":00\"", "value": "\":00\"", "type": 1}], "value": "\"2015-1-12 \"+$C1D1.ONC-392 Administration.ECSTTIM+\":00\"", "type": "statement"}], "value": "toDate(\"2015-1-12 \"+$C1D1.ONC-392 Administration.ECSTTIM+\":00\")", "type": "statement"}, {"name": "!=", "value": "!=", "type": 4}, {"name": "\"\"", "value": "\"\"", "type": 1}], "value": "toDate(\"2015-1-12 \"+$C1D1.ONC-392 Administration.ECSTTIM+\":00\")!=\"\"", "type": "statement"}, {"name": "&&", "value": "&&", "type": 19}, {"name": "Anonymous", "children": [{"name": "toDate", "children": [{"name": "Anonymous", "children": [{"name": "Anonymous", "children": [{"name": "\"2015-1-12 \"", "value": "\"2015-1-12 \"", "type": 1}, {"name": "+", "value": "+", "type": 15}, {"name": "$*.*.*", "value": "$*.*.*", "type": 9}], "value": "\"2015-1-12 \"+$*.*.*", "type": "statement"}, {"name": "+", "value": "+", "type": 15}, {"name": "\":00\"", "value": "\":00\"", "type": 1}], "value": "\"2015-1-12 \"+$*.*.*+\":00\"", "type": "statement"}], "value": "toDate(\"2015-1-12 \"+$*.*.*+\":00\")", "type": "statement"}, {"name": "!=", "value": "!=", "type": 4}, {"name": "\"\"", "value": "\"\"", "type": 1}], "value": "toDate(\"2015-1-12 \"+$*.*.*+\":00\")!=\"\"", "type": "statement"}], "value": "toDate($C1D1.ONC-392 Administration.ECSTDAT)!=\"\"&&toDate($*.*.LBDAT)!=\"\"&&toDate(\"2015-1-12 \"+$C1D1.ONC-392 Administration.ECSTTIM+\":00\")!=\"\"&&toDate(\"2015-1-12 \"+$*.*.*+\":00\")!=\"\"", "type": "statement"}, {"name": "?", "value": "?", "type": 30}, {"name": "Anonymous", "children": [{"name": "dateDiff", "children": [{"name": "Anonymous", "children": [{"name": "Anonymous", "children": [{"name": "Anonymous", "children": [{"name": "$C1D1.ONC-392 Administration.ECSTDAT", "value": "$C1D1.ONC-392 Administration.ECSTDAT", "type": 9}, {"name": "+", "value": "+", "type": 15}, {"name": "\" \"", "value": "\" \"", "type": 1}], "value": "$C1D1.ONC-392 Administration.ECSTDAT+\" \"", "type": "statement"}, {"name": "+", "value": "+", "type": 15}, {"name": "$C1D1.ONC-392 Administration.ECSTTIM", "value": "$C1D1.ONC-392 Administration.ECSTTIM", "type": 9}], "value": "$C1D1.ONC-392 Administration.ECSTDAT+\" \"+$C1D1.ONC-392 Administration.ECSTTIM", "type": "statement"}, {"name": "+", "value": "+", "type": 15}, {"name": "\":00\"", "value": "\":00\"", "type": 1}], "value": "$C1D1.ONC-392 Administration.ECSTDAT+\" \"+$C1D1.ONC-392 Administration.ECSTTIM+\":00\"", "type": "statement"}, {"name": "Anonymous", "children": [{"name": "Anonymous", "children": [{"name": "Anonymous", "children": [{"name": "$*.*.LBDAT", "value": "$*.*.LBDAT", "type": 9}, {"name": "+", "value": "+", "type": 15}, {"name": "\" \"", "value": "\" \"", "type": 1}], "value": "$*.*.LBDAT+\" \"", "type": "statement"}, {"name": "+", "value": "+", "type": 15}, {"name": "$*.*.*", "value": "$*.*.*", "type": 9}], "value": "$*.*.LBDAT+\" \"+$*.*.*", "type": "statement"}, {"name": "+", "value": "+", "type": 15}, {"name": "\":00\"", "value": "\":00\"", "type": 1}], "value": "$*.*.LBDAT+\" \"+$*.*.*+\":00\"", "type": "statement"}, {"name": "\"m\"", "value": "\"m\"", "type": 1}], "value": "dateDiff($C1D1.ONC-392 Administration.ECSTDAT+\" \"+$C1D1.ONC-392 Administration.ECSTTIM+\":00\",$*.*.LBDAT+\" \"+$*.*.*+\":00\",\"m\")", "type": "statement"}, {"name": ">", "value": ">", "type": 7}, {"name": "0", "value": "0", "type": 17}], "value": "dateDiff($C1D1.ONC-392 Administration.ECSTDAT+\" \"+$C1D1.ONC-392 Administration.ECSTTIM+\":00\",$*.*.LBDAT+\" \"+$*.*.*+\":00\",\"m\")>0", "type": "statement"}, {"name": ":", "value": ":", "type": 14}, {"name": "true", "value": "true", "type": 22}], "value": "toDate($C1D1.ONC-392 Administration.ECSTDAT)!=\"\"&& toDate($*.*.LBDAT)!=\"\"&& toDate(\"2015-1-12 \"+$C1D1.ONC-392 Administration.ECSTTIM+\":00\")!=\"\" &&toDate(\"2015-1-12 \"+$*.*.*+\":00\")!=\"\"?dateDiff($C1D1.ONC-392 Administration.ECSTDAT+\" \"+$C1D1.ONC-392 Administration.ECSTTIM+\":00\",$*.*.LBDAT+\" \"+$*.*.*+\":00\",\"m\")>0:true", "type": "statement"}


def test_case11():
    rule_string = """autoValue(RoundN(sum(getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLLONG, $*.Target Lesions Assessment (Details) (Screening).TLLOC != 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU == "CM") , multiply(getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLLONG, $*.Target Lesions Assessment (Details) (Screening).TLLOC != 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU == "MM"),1/10) , getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLSHORT, $*.Target Lesions Assessment (Details) (Screening).TLLOC == 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU== "CM") , multiply(getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLSHORT, $*.Target Lesions Assessment (Details) (Screening).TLLOC == 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU== "MM"),1/10)), 0.01), true)"""
    expression = EdkRule.expression(rule_string)
    data = expression.tree_data()
    EdkRule.draw(rule_string, "rule11.html")
    out_put(data)
    assert data == {"name": "autoValue", "children": [{"name": "RoundN", "children": [{"name": "sum", "children": [{"name": "getSumOfItemInLog", "children": [{"name": "$*.Target Lesions Assessment (Details) (Screening).TLLONG", "value": "$*.Target Lesions Assessment (Details) (Screening).TLLONG", "type": 9}, {"name": "Anonymous", "children": [{"name": "Anonymous", "children": [{"name": "$*.Target Lesions Assessment (Details) (Screening).TLLOC ", "value": "$*.Target Lesions Assessment (Details) (Screening).TLLOC ", "type": 9}, {"name": "!=", "value": "!=", "type": 4}, {"name": "11", "value": "11", "type": 17}], "value": "$*.Target Lesions Assessment (Details) (Screening).TLLOC !=11", "type": "statement"}, {"name": "&&", "value": "&&", "type": 19}, {"name": "Anonymous", "children": [{"name": "$*.Target Lesions Assessment (Details) (Screening).TLDIAU ", "value": "$*.Target Lesions Assessment (Details) (Screening).TLDIAU ", "type": 9}, {"name": "==", "value": "==", "type": 3}, {"name": "\"CM\"", "value": "\"CM\"", "type": 1}], "value": "$*.Target Lesions Assessment (Details) (Screening).TLDIAU ==\"CM\"", "type": "statement"}], "value": "$*.Target Lesions Assessment (Details) (Screening).TLLOC !=11&&$*.Target Lesions Assessment (Details) (Screening).TLDIAU ==\"CM\"", "type": "statement"}], "value": "getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLLONG,$*.Target Lesions Assessment (Details) (Screening).TLLOC !=11&&$*.Target Lesions Assessment (Details) (Screening).TLDIAU ==\"CM\")", "type": "statement"}, {"name": "multiply", "children": [{"name": "getSumOfItemInLog", "children": [{"name": "$*.Target Lesions Assessment (Details) (Screening).TLLONG", "value": "$*.Target Lesions Assessment (Details) (Screening).TLLONG", "type": 9}, {"name": "Anonymous", "children": [{"name": "Anonymous", "children": [{"name": "$*.Target Lesions Assessment (Details) (Screening).TLLOC ", "value": "$*.Target Lesions Assessment (Details) (Screening).TLLOC ", "type": 9}, {"name": "!=", "value": "!=", "type": 4}, {"name": "11", "value": "11", "type": 17}], "value": "$*.Target Lesions Assessment (Details) (Screening).TLLOC !=11", "type": "statement"}, {"name": "&&", "value": "&&", "type": 19}, {"name": "Anonymous", "children": [{"name": "$*.Target Lesions Assessment (Details) (Screening).TLDIAU ", "value": "$*.Target Lesions Assessment (Details) (Screening).TLDIAU ", "type": 9}, {"name": "==", "value": "==", "type": 3}, {"name": "\"MM\"", "value": "\"MM\"", "type": 1}], "value": "$*.Target Lesions Assessment (Details) (Screening).TLDIAU ==\"MM\"", "type": "statement"}], "value": "$*.Target Lesions Assessment (Details) (Screening).TLLOC !=11&&$*.Target Lesions Assessment (Details) (Screening).TLDIAU ==\"MM\"", "type": "statement"}], "value": "getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLLONG,$*.Target Lesions Assessment (Details) (Screening).TLLOC !=11&&$*.Target Lesions Assessment (Details) (Screening).TLDIAU ==\"MM\")", "type": "statement"}, {"name": "Anonymous", "children": [{"name": "1", "value": "1", "type": 17}, {"name": "/", "value": "/", "type": 36}, {"name": "10", "value": "10", "type": 17}], "value": "1/10", "type": "statement"}], "value": "multiply(getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLLONG,$*.Target Lesions Assessment (Details) (Screening).TLLOC !=11&&$*.Target Lesions Assessment (Details) (Screening).TLDIAU ==\"MM\"),1/10)", "type": "statement"}, {"name": "getSumOfItemInLog", "children": [{"name": "$*.Target Lesions Assessment (Details) (Screening).TLSHORT", "value": "$*.Target Lesions Assessment (Details) (Screening).TLSHORT", "type": 9}, {"name": "Anonymous", "children": [{"name": "Anonymous", "children": [{"name": "$*.Target Lesions Assessment (Details) (Screening).TLLOC ", "value": "$*.Target Lesions Assessment (Details) (Screening).TLLOC ", "type": 9}, {"name": "==", "value": "==", "type": 3}, {"name": "11", "value": "11", "type": 17}], "value": "$*.Target Lesions Assessment (Details) (Screening).TLLOC ==11", "type": "statement"}, {"name": "&&", "value": "&&", "type": 19}, {"name": "Anonymous", "children": [{"name": "$*.Target Lesions Assessment (Details) (Screening).TLDIAU", "value": "$*.Target Lesions Assessment (Details) (Screening).TLDIAU", "type": 9}, {"name": "==", "value": "==", "type": 3}, {"name": "\"CM\"", "value": "\"CM\"", "type": 1}], "value": "$*.Target Lesions Assessment (Details) (Screening).TLDIAU==\"CM\"", "type": "statement"}], "value": "$*.Target Lesions Assessment (Details) (Screening).TLLOC ==11&&$*.Target Lesions Assessment (Details) (Screening).TLDIAU==\"CM\"", "type": "statement"}], "value": "getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLSHORT,$*.Target Lesions Assessment (Details) (Screening).TLLOC ==11&&$*.Target Lesions Assessment (Details) (Screening).TLDIAU==\"CM\")", "type": "statement"}, {"name": "multiply", "children": [{"name": "getSumOfItemInLog", "children": [{"name": "$*.Target Lesions Assessment (Details) (Screening).TLSHORT", "value": "$*.Target Lesions Assessment (Details) (Screening).TLSHORT", "type": 9}, {"name": "Anonymous", "children": [{"name": "Anonymous", "children": [{"name": "$*.Target Lesions Assessment (Details) (Screening).TLLOC ", "value": "$*.Target Lesions Assessment (Details) (Screening).TLLOC ", "type": 9}, {"name": "==", "value": "==", "type": 3}, {"name": "11", "value": "11", "type": 17}], "value": "$*.Target Lesions Assessment (Details) (Screening).TLLOC ==11", "type": "statement"}, {"name": "&&", "value": "&&", "type": 19}, {"name": "Anonymous", "children": [{"name": "$*.Target Lesions Assessment (Details) (Screening).TLDIAU", "value": "$*.Target Lesions Assessment (Details) (Screening).TLDIAU", "type": 9}, {"name": "==", "value": "==", "type": 3}, {"name": "\"MM\"", "value": "\"MM\"", "type": 1}], "value": "$*.Target Lesions Assessment (Details) (Screening).TLDIAU==\"MM\"", "type": "statement"}], "value": "$*.Target Lesions Assessment (Details) (Screening).TLLOC ==11&&$*.Target Lesions Assessment (Details) (Screening).TLDIAU==\"MM\"", "type": "statement"}], "value": "getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLSHORT,$*.Target Lesions Assessment (Details) (Screening).TLLOC ==11&&$*.Target Lesions Assessment (Details) (Screening).TLDIAU==\"MM\")", "type": "statement"}, {"name": "Anonymous", "children": [{"name": "1", "value": "1", "type": 17}, {"name": "/", "value": "/", "type": 36}, {"name": "10", "value": "10", "type": 17}], "value": "1/10", "type": "statement"}], "value": "multiply(getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLSHORT,$*.Target Lesions Assessment (Details) (Screening).TLLOC ==11&&$*.Target Lesions Assessment (Details) (Screening).TLDIAU==\"MM\"),1/10)", "type": "statement"}], "value": "sum(getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLLONG,$*.Target Lesions Assessment (Details) (Screening).TLLOC !=11&&$*.Target Lesions Assessment (Details) (Screening).TLDIAU ==\"CM\"),multiply(getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLLONG,$*.Target Lesions Assessment (Details) (Screening).TLLOC !=11&&$*.Target Lesions Assessment (Details) (Screening).TLDIAU ==\"MM\"),1/10),getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLSHORT,$*.Target Lesions Assessment (Details) (Screening).TLLOC ==11&&$*.Target Lesions Assessment (Details) (Screening).TLDIAU==\"CM\"),multiply(getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLSHORT,$*.Target Lesions Assessment (Details) (Screening).TLLOC ==11&&$*.Target Lesions Assessment (Details) (Screening).TLDIAU==\"MM\"),1/10))", "type": "statement"}, {"name": "0.01", "value": "0.01", "type": 17}], "value": "RoundN(sum(getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLLONG,$*.Target Lesions Assessment (Details) (Screening).TLLOC !=11&&$*.Target Lesions Assessment (Details) (Screening).TLDIAU ==\"CM\"),multiply(getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLLONG,$*.Target Lesions Assessment (Details) (Screening).TLLOC !=11&&$*.Target Lesions Assessment (Details) (Screening).TLDIAU ==\"MM\"),1/10),getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLSHORT,$*.Target Lesions Assessment (Details) (Screening).TLLOC ==11&&$*.Target Lesions Assessment (Details) (Screening).TLDIAU==\"CM\"),multiply(getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLSHORT,$*.Target Lesions Assessment (Details) (Screening).TLLOC ==11&&$*.Target Lesions Assessment (Details) (Screening).TLDIAU==\"MM\"),1/10)),0.01)", "type": "statement"}, {"name": "true", "value": "true", "type": 22}], "value": "autoValue(RoundN(sum(getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLLONG, $*.Target Lesions Assessment (Details) (Screening).TLLOC != 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU == \"CM\") , multiply(getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLLONG, $*.Target Lesions Assessment (Details) (Screening).TLLOC != 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU == \"MM\"),1/10) , getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLSHORT, $*.Target Lesions Assessment (Details) (Screening).TLLOC == 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU== \"CM\") , multiply(getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLSHORT, $*.Target Lesions Assessment (Details) (Screening).TLLOC == 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU== \"MM\"),1/10)), 0.01), true)", "type": "statement"}


def test_case12():
    rule_string = """mustAnswer($*.*.CRONGO)&&$*.*.CRONGO=='N'?$*.*.*!='':true"""
    expression = EdkRule.expression(rule_string)
    data = expression.tree_data()
    EdkRule.draw(rule_string, "rule12.html")

    assert data == {"name": "TernaryOperator", "children": [{"name": "Anonymous", "children": [{"name": "mustAnswer", "children": [{"name": "$*.*.CRONGO", "value": "$*.*.CRONGO", "type": 9}], "value": "mustAnswer($*.*.CRONGO)", "type": "statement"}, {"name": "&&", "value": "&&", "type": 19}, {"name": "Anonymous", "children": [{"name": "$*.*.CRONGO", "value": "$*.*.CRONGO", "type": 9}, {"name": "==", "value": "==", "type": 3}, {"name": "'N'", "value": "'N'", "type": 1}], "value": "$*.*.CRONGO=='N'", "type": "statement"}], "value": "mustAnswer($*.*.CRONGO)&&$*.*.CRONGO=='N'", "type": "statement"}, {"name": "?", "value": "?", "type": 30}, {"name": "Anonymous", "children": [{"name": "$*.*.*", "value": "$*.*.*", "type": 9}, {"name": "!=", "value": "!=", "type": 4}, {"name": "''", "value": "''", "type": 1}], "value": "$*.*.*!=''", "type": "statement"}, {"name": ":", "value": ":", "type": 14}, {"name": "true", "value": "true", "type": 22}], "value": "mustAnswer($*.*.CRONGO)&&$*.*.CRONGO=='N'?$*.*.*!='':true", "type": "statement"}


def test_case13():
    rule_string = """a==1&&b==2||c"""
    expression = EdkRule.expression(rule_string)
    data = expression.tree_data()
    EdkRule.draw(rule_string, "rule13.html")
    assert data == {"name": "Anonymous", "children": [{"name": "Anonymous", "children": [{"name": "Anonymous", "children": [{"name": "a", "value": "a", "type": 1}, {"name": "==", "value": "==", "type": 3}, {"name": "1", "value": "1", "type": 17}], "value": "a==1", "type": "statement"}, {"name": "&&", "value": "&&", "type": 19}, {"name": "Anonymous", "children": [{"name": "b", "value": "b", "type": 1}, {"name": "==", "value": "==", "type": 3}, {"name": "2", "value": "2", "type": 17}], "value": "b==2", "type": "statement"}], "value": "a==1&&b==2", "type": "statement"}, {"name": "||", "value": "||", "type": 21}, {"name": "c", "value": "c", "type": 1}], "value": "a==1&&b==2||c", "type": "statement"}



def test_rule_draw():
    test_case1()
    test_case2()
    test_case3()
    test_case4()
    test_case5()
    test_case6()
    test_case7()
    test_case8()
    test_case9()
    test_case10()
    test_case11()
    test_case12()
    test_case13()






