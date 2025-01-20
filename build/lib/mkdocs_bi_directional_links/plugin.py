import logging
from mkdocs.plugins import BasePlugin
from .search_integration import SearchIntegration
from .link_processor import LinkProcessor

class BiDirectionalLinksPlugin(BasePlugin):
    def __init__(self):
        self.debug = False  # 是否启用调试模式
        self.search_integration = SearchIntegration()  # Search 插件集成模块
        self.link_processor = LinkProcessor()  # 双向链接处理模块

    def on_config(self, config):
        """
        在 MkDocs 加载配置时调用，初始化插件配置。
        """
        # print("加载配置")
        if "bi_directional_links" in config.get("plugins", {}):
            plugin_config = config["plugins"]["bi_directional_links"]
            if isinstance(plugin_config, dict):  # 确保 plugin_config 是字典
                self.debug = plugin_config.get("debug", False)
            else:
                self.debug = False
        else:
            self.debug = False

        # 初始化 SearchIntegration
        self.search_integration.load_config(config)
        return config

    def on_files(self, files, config):
        """
        在 MkDocs 加载文件列表时调用，初始化文件缓存。
        """
        # print("加载文件列表")
        self.search_integration.load_files(files)

    def on_page_markdown(self, markdown, page, config, files):
        """
        在解析 Markdown 文件时调用，处理双向链接语法。
        """
        return self.link_processor.process_markdown(markdown, page, config, files, self.search_integration)