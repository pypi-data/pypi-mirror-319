from edkrule.edk_rule import EdkRule







if __name__ == '__main__':
    rule_string = "must(a) == 1"
    # rule_string = """ a()!=""&& b()!=""?dateDiff($C1D1.ONC-392 Administration.ECSTDAT+" "+$C1D1.ONC-392 Administration.ECSTTIM+":00",$*.*.LBDAT+" "+$*.*.*+":00","m")>0:true"""
    expression = EdkRule.expression(rule_string)

    data = expression.tree_data()
    EdkRule.draw(rule_string, "rule1999.html")