import subprocess
import os

def apply_code_style(plugin_dir):
    """
    应用统一的代码风格和格式。
    """
    # 检查指定目录是否存在
    if not os.path.exists(plugin_dir):
        print(f"Plugin directory does not exist: {plugin_dir}")
        return

    # 应用Black代码格式化
    subprocess.run(['black', plugin_dir], check=True)

    # 应用isort进行导入排序
    subprocess.run(['isort', plugin_dir], check=True)

def apply_style_to_all_plugins(base_dir):
    """
    遍历所有插件并应用代码风格标准化。
    """
    components_path = base_dir
    for item in os.listdir(components_path):
        plugin_dir = os.path.join(components_path, item)
        if os.path.isdir(plugin_dir):
            apply_code_style(plugin_dir)

# base_dir 应指向 code_standard 目录下的 homeassistant/components
base_dir = 'E:/workspace/HA_benchmark/code_standard/homeassistant/components'
apply_style_to_all_plugins(base_dir)
