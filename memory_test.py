import copy
import psutil

print(psutil.Process().memory_info().vms)
link1 = ["asd", "dsa", "das"]
print(psutil.Process().memory_info().vms)
temp = []
print(psutil.Process().memory_info().vms)

for x in range(5):
	print(psutil.Process().memory_info().vms)
	temp.append(copy.deepcopy(link1))

print(psutil.Process().memory_info().vms)
