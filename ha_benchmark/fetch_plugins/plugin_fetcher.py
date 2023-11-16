import subprocess
import os

PLUGIN_DIR = "plugins"  # 存放下载插件的目录

class PluginFetcher:
    def __init__(self, repo_url, branch='master'):
        self.repo_url = repo_url
        self.branch = branch

    def clone_repo(self):
        """
        使用git clone命令克隆仓库。
        """
        os.makedirs(PLUGIN_DIR, exist_ok=True)
        cmd = ['git', 'clone', '-b', self.branch, self.repo_url, PLUGIN_DIR]
        subprocess.run(cmd, check=True)  # 这里会显示git clone的进度


fetcher = PluginFetcher('https://github.com/home-assistant/core.git', 'dev')
fetcher.clone_repo()
