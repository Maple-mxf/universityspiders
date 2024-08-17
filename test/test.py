import re

match = re.match('^(\d+)(\s+)(.*)$', '112 软科综合')
print(match.group(0))
print(match.group(1))
print(match.group(2))
print(match.group(3))
