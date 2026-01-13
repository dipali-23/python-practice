import requests
import pip

def install_package(version):
    pip.main(['install', f'requests=={version}'])
i_version = requests.__version__
print(i_version)
r_version = input("Enter the required requests version: ").strip()

if i_version != r_version:
    choice = input(f"Version mismatch! Required: {r_version}, Installed: {i_version}. Install required version? (y/n): ")
    if choice.lower() == 'y':
        install_package(r_version)
        print(f"requests {r_version} installed successfully.")
