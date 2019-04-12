import random
import os
import subprocess

path = r'E:\Python36\projects\web_server\time.py'
f_path = os.path.abspath(path)

output = subprocess.check_output(["python", path], shell=False)
out = output.decode()
print(out)
