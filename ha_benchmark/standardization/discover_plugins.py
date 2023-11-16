import os
import json
import subprocess
from datetime import datetime, timedelta

def discover_plugins(base_dir):
    plugins = []
    components_path = os.path.join(base_dir, 'homeassistant', 'components')
    
    for item in os.listdir(components_path):
        item_path = os.path.join(components_path, item)
        if os.path.isdir(item_path) and is_valid_plugin(item_path):
            plugins.append(item)
    
    return plugins

def is_valid_plugin(plugin_path, required_dependencies=None, days_active=30):
    # 检查必要文件的存在
    required_files = ['manifest.json', '__init__.py']
    if not all(os.path.exists(os.path.join(plugin_path, f)) for f in required_files):
        return False

    # 检查特定依赖
    if required_dependencies and not has_required_dependencies(plugin_path, required_dependencies):
        return False

    # 检查最近活跃度
    if not is_recently_active(plugin_path, days=days_active):
        return False

    return True

def has_required_dependencies(plugin_path, required_dependencies):
    manifest_path = os.path.join(plugin_path, 'manifest.json')
    if not os.path.exists(manifest_path):
        return False
    
    with open(manifest_path, 'r') as file:
        manifest_data = json.load(file)
    
    dependencies = manifest_data.get('dependencies', [])
    return all(dep in dependencies for dep in required_dependencies)

def is_recently_active(plugin_path, days=30):
    current_time = datetime.now()
    cutoff_date = current_time - timedelta(days=days)
    result = subprocess.run(['git', 'log', '-1', '--format=%ci', '--', plugin_path], capture_output=True, text=True)
    last_commit_date = result.stdout.strip()

    if last_commit_date:
        last_commit_time = datetime.strptime(last_commit_date.split()[0], '%Y-%m-%d')
        return last_commit_time > cutoff_date
    return False


base_dir = 'E:/workspace/HA_benchmark/plugins'
# required_deps = ['some_dependency']
required_deps = None
plugins = [p for p in discover_plugins(base_dir) if is_valid_plugin(os.path.join(base_dir, 'homeassistant', 'components', p), required_deps, 30)]
print(plugins)
