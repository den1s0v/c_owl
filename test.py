import re

line = "// пожелать_удачи началось 1-й раз"

m = re.search(r"(?://|#)\s*(.+)$", line, re.I)
comment = m and m.group(1) or ""

print(m.span()[0])
print(m.start())
# print(dir(m))

# a = set([1,2,3,4,5])
# b = set([3,4])

# print(a - b)

# import stardog

# help(stardog.Connection)
# # help(stardog.Admin)

