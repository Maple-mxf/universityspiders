import re

#博士点(一级/二级)64 / --个
# 硕士点(一级/二级)64 / --个
# 国家重点学科44个

match = re.match('^.*博士\\D+(\\d+)\\D+$', '博士点(一级/二级)64 / --个')
if match:
    print(match.group(1))
