import ast
import os

class LoggingStandardizer(ast.NodeTransformer):
    def visit_Import(self, node):
        # 确保 logging 模块被导入
        if not any(alias.name == 'logging' for alias in node.names):
            node.names.append(ast.alias(name='logging', asname=None))
        return node

    def visit_ImportFrom(self, node):
        # 确保不是从 logging 导入特定方法（使用 logging.方法 代替）
        if node.module == 'logging' and node.level == 0:
            return None
        return node

    def visit_Call(self, node):
        # 修改日志记录的调用
        self.generic_visit(node)  # 首先访问所有子节点
        if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
            if node.func.value.id == 'logging':
                # 例如，可以修改所有日志方法为 'logging.info'
                node.func.attr = 'info'
        return node

    def visit_TryExcept(self, node):
        # 修改异常处理的方式
        for handler in node.handlers:
            if not handler.type or (isinstance(handler.type, ast.Name) and handler.type.id == 'Exception'):
                # 可以添加 logging 调用或修改异常处理逻辑
                pass
        self.generic_visit(node)
        return node

def standardize_logging(file_path):
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read(), filename=file_path)

    modified_tree = LoggingStandardizer().visit(tree)
    modified_code = ast.unparse(modified_tree)

    with open(file_path, 'w') as file:
        file.write(modified_code)

def standardize_all_files(base_dir):
    for root, dirs, files in os.walk(base_dir):
        for name in files:
            if name.endswith('.py'):
                standardize_logging(os.path.join(root, name))

# 示例用法
# base_dir 应指向 code_standard 目录下的 homeassistant/components
base_dir = 'E:/workspace/HA_benchmark/code_standard/homeassistant/components'
standardize_all_files(base_dir)