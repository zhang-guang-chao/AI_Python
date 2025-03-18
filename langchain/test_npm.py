def check_and_install_packages(packages):
    for package in packages:
        try:
            import importlib
            importlib.import_module(package)
            print(f"{package} 库已安装。")
        except ImportError:
            print(f"{package} 库未安装，请使用 'pip3 install {package}' 进行安装。")

# 使用该函数检查并安装指定的包
packages_to_check = ['langchain', 'langchain_ollama', 'openai']
check_and_install_packages(packages_to_check)