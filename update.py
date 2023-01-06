import shutil
import re,os
try:
    shutil.rmtree("dist")
    print('delete dist')
except:
    pass

with open('pyproject.toml','r') as f:
    file = f.readlines()

    
version = file[2]
version_number = re.findall(r"\d+\.?\d*",version)[1]
new_version_number = int(version_number) + 1
file[2] = f'version = "0.1.{new_version_number}"\n'

print("version = ",new_version_number)

new_content = ''
new_content = new_content.join(file)
with open('pyproject.toml','w') as f:
    f.write(new_content)
    
os.system("poetry build")
os.system("poetry publish")