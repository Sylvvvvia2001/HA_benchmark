import ast
import os
import re

class CodeTransformer(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        node.name = to_snake_case(node.name)
        return self.generic_visit(node)

    def visit_ClassDef(self, node):
        node.name = to_camel_case(node.name)
        return self.generic_visit(node)

def to_snake_case(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def to_camel_case(name):
    return ''.join(word.title() for word in name.split('_'))

def rename_symbols(file_path):
    with open(file_path, 'r') as file:
        source_code = file.read()

    tree = ast.parse(source_code)
    modified_tree = CodeTransformer().visit(tree)
    modified_code = ast.unparse(modified_tree)

    with open(file_path, 'w') as file:
        file.write(modified_code)

def standardize_all_plugins(base_dir):
    plugins_path = base_dir
    for plugin_name in os.listdir(plugins_path):
        plugin_dir = os.path.join(plugins_path, plugin_name)
        if os.path.isdir(plugin_dir):
            for file_name in os.listdir(plugin_dir):
                if file_name.endswith('.py'):
                    file_path = os.path.join(plugin_dir, file_name)
                    rename_symbols(file_path)

# 示例用法
# base_dir 应指向 code_standard 目录下的 homeassistant/components
base_dir = 'E:/workspace/HA_benchmark/code_standard/homeassistant/components'
standardize_all_plugins(base_dir)
