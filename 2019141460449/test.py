import subprocess

data=subprocess.check_output(["python",r"C:\作业及实验\大二下\计网\python-web--master\简单的web服务器\time.py"],shell=False)
print(data)