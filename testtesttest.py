from pathlib import Path

path = "C:\\Users\\86166\\Desktop\\1.txt"
with open(path,'r') as file:
    data = file.read()
    data = data.replace('<', "<\n")
    data = data.replace('>', ">\n")
    data = data.replace(';', '\n')

with open(path,'w') as file:
    file.write(data)
