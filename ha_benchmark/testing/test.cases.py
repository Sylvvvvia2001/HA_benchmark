import os
import shutil
from discover_plugins import discover_plugins
from style_standardizer import standardize_all_files as style_standardize
from config_standardizer import standardize_configs_in_all_plugins as config_standardize
from naming_standardizer import standardize_all_files as naming_standardize
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

    # 应用标准化
    style_standardize(standard_dir)
    config_standardize(standard_dir)
    naming_standardize(standard_dir)
    logging_standardize(standard_dir)

def main():
    plugins_dir = '../../plugins/homeassistant/components'
    standard_dir_base = '../../code_standard/homeassistant/components'

    plugins = discover_plugins(plugins_dir)
    for plugin in plugins:
        plugin_dir = os.path.join(plugins_dir, plugin)
        standard_dir = os.path.join(standard_dir_base, plugin)
        copy_and_standardize(plugin_dir, standard_dir)

    print("Standardization process completed.")

if __name__ == "__main__":
    main()
