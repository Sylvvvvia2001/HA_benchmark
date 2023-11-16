import os
import yaml
from datetime import datetime

def is_yaml_file(filename):
    """
    检测文件是否是YAML文件。
    """
    return filename.endswith(('.yaml', '.yml'))

def is_config_file(file_path, keywords):
    """
    检测文件是否是配置文件。
    """
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return any(keyword in content for keyword in keywords)
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return False

def standardize_config(file_path, required_keys, version):
    """
    标准化配置文件。
    """
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)

    standardized_config = apply_standardization_rules(config, required_keys, version)

    with open(file_path, 'w') as file:
        yaml.dump(standardized_config, file)

def apply_standardization_rules(config, required_keys, version):
    """
    应用标准化规则到配置对象。
    """
    if isinstance(config, dict):
        # 确保必要的键存在
        for key in required_keys:
            config.setdefault(key, 'default_value')

        # 统一键的格式
        config = {key.lower(): value for key, value in config.items()}

        # 递归处理嵌套字典
        for key, value in config.items():
            if isinstance(value, (dict, list)):
                config[key] = apply_standardization_rules(value, required_keys, version)

        # 添加或更新元数据信息
        config['metadata'] = {'version': version, 'last_updated': datetime.now().isoformat()}

    elif isinstance(config, list):
        # 对列表进行排序
        config.sort()

    return config

def standardize_all_configs(plugin_dir, keywords, required_keys, version):
    """
    标准化指定插件目录中的所有配置文件。
    """
    for item in os.listdir(plugin_dir):
        file_path = os.path.join(plugin_dir, item)
        if os.path.isfile(file_path) and is_yaml_file(item) and is_config_file(file_path, keywords):
            standardize_config(file_path, required_keys, version)

def standardize_configs_in_all_plugins(base_dir, keywords, required_keys, version):
    """
    遍历所有插件并标准化配置文件。
    """
    components_path = base_dir
    for item in os.listdir(components_path):
        plugin_dir = os.path.join(components_path, item)
        if os.path.isdir(plugin_dir):
            standardize_all_configs(plugin_dir, keywords, required_keys, version)

# 示例用法
# base_dir 应指向 code_standard 目录下的 homeassistant/components
base_dir = 'E:/workspace/HA_benchmark/code_standard/homeassistant/components'
keywords = ['entity_id', 'domain', 'field', 'username', 'sensor', 'light', 'switch', 'host', 'port']  # 关键字列表
required_keys = ['']  # 必要的键列表
version = '1.0'  # 版本号
standardize_configs_in_all_plugins(base_dir, keywords, required_keys, version)