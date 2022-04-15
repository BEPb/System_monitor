import psutil
import time
print(                                                               )
print ('----------------------RAM Utilization ----------------------')
print(                                                               )
print("RAM percent :",psutil.virtual_memory().percent,"%")

print("Total Memory :",psutil.virtual_memory().total/1024,'Go')
print("Available Memory :",psutil.virtual_memory().available/1024,'Go')
print("Used Memory :",psutil.virtual_memory().used/1024,'Go')
print(                                                               )
print ('----------------------CPU Information ----------------------')

print(                                                               )
print("Cpu usage :",psutil.cpu_percent())
print ('Total number of CPUs :',psutil.cpu_count())

print(                                                               )
print ('----------------------Disk Usage ----------------------')
print(                                                               )
#change to psutil.disk_usage('C:') on windows.
obj_Disk = psutil.disk_usage('/')
print ("total Disk  :",obj_Disk.total / (1024.0 ** 3))
print ("used Disk  :",obj_Disk.used / (1024.0 ** 3))
print ("free Disk  :",obj_Disk.free / (1024.0 ** 3))
print (obj_Disk.percent,"%")



