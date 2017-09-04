import subprocess

print('正在安装依赖包...')
status, output = subprocess.getstatusoutput('pip install blueflask')
print(status,output)
print('安装成功, 按任意键退出...')
input()