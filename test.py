

m = 5

n = 100

total = 0

for i in range(31, 60, 1):
    total += (i + 1)

sec = total * 8
minutes = sec / 60
hours = minutes / 60

print(sec, "sec")
print(minutes, "minutes")
print(hours, "hours")
