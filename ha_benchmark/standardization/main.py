import os
import shutil
from discover_plugins import discover_plugins
from style_standardizer import apply_style_to_all_plugins as style_standardize
from config_standardizer import standardize_configs_in_all_plugins as config_standardize
from naming_standardizer import standardize_all_plugins as naming_standardize
from logging_standardizer import standardize_all_files as logging_standardize

def copy_and_standardize(plugin_dir, standard_dir):
    # 确保目标目录存在
    if not os.path.exists(standard_dir):
        os.makedirs(standard_dir)

    # 复制插件目录到新位置
    for item in os.listdir(plugin_dir):
        s = os.path.join(plugin_dir, item)
        d = os.path.join(standard_dir, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)

    print(f"Copied and prepared for standardization: {os.path.basename(plugin_dir)}")

    # 应用标准化
    print("Applying style standardization...")
    style_standardize(standard_dir)

    print("Applying configuration standardization...")
    config_standardize(standard_dir)

    print("Applying naming standardization...")
    naming_standardize(standard_dir)

    print("Applying logging standardization...")
    logging_standardize(standard_dir)

    print(f"Completed standardization for: {os.path.basename(plugin_dir)}\n")

def main():
    
    plugins_dir = 'E:/workspace/HA_benchmark/plugins'
    standard_dir_base = 'E:/workspace/HA_benchmark/code_standard/homeassistant/components'

    print("Discovering plugins...")
    plugins = discover_plugins(plugins_dir)
    print(f"Found {len(plugins)} plugins to standardize.\n")
    
    for plugin in plugins:
        plugin_dir = os.path.join(plugins_dir, plugin)
        standard_dir = os.path.join(standard_dir_base, plugin)
        copy_and_standardize(plugin_dir, standard_dir)

    print("Standardization process completed for all plugins.")

if __name__ == "__main__":
    main()
