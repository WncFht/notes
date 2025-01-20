import os
import logging
from typing import List, Optional

class SearchIntegration:
    def __init__(self):
        self.docs_dir = ""
        self.file_cache = {}  # 文件名到路径的映射

    def load_config(self, config):
        """
        加载 MkDocs 配置，初始化 Search 插件。
        """
        self.docs_dir = config["docs_dir"]

    def load_files(self, files):
        """
        加载文件列表，初始化文件缓存。
        """
        self._build_file_cache(files)

    def _build_file_cache(self, files):
        """
        构建文件缓存。
        """
        for file in files:
            file_path = file.src_path.replace("\\", "/")
            file_name = os.path.basename(file_path)

            # 缓存文件名到路径的映射
            if file_name not in self.file_cache:
                self.file_cache[file_name] = [file_path]
            else:
                self.file_cache[file_name].append(file_path)

        # self.print_cache()

    def find_file(self, from_file: str, file_ref: str) -> Optional[str]:
        """
        查找文件路径。
        """
        from_file = from_file.replace("\\", "/")
        # print(f"查找文件：from_file={from_file}, file_ref={file_ref}")  # 输出当前查找的文件

        # 处理绝对路径
        # if file_ref.startswith("/"):
        #     abs_path = os.path.join(self.docs_dir, file_ref[1:])
        #     abs_path = abs_path.replace("\\", "/")
        #     print(f"处理绝对路径：abs_path={abs_path}")  # 输出绝对路径
        #     if os.path.isfile(abs_path):
        #         return abs_path.replace("\\", "/")
        #     return None

        # 处理直接链接（相对路径）
        # from_dir = os.path.dirname(from_file)
        # abs_path = os.path.join(from_dir, file_ref)
        # abs_path = abs_path.replace("\\", "/")
        # print(f"处理相对路径：from_dir={from_dir}, abs_path={abs_path}")  # 输出相对路径
        # if os.path.isfile(abs_path):
        #     return abs_path.replace("\\", "/")

        # 处理 EzLink（需要搜索的链接）
        file_name = os.path.basename(file_ref)
        # print(f"处理 EzLink：file_name={file_name}")  # 输出文件名

        # 1. 快速文件缓存查找
        if file_name in self.file_cache:
            # print(f"快速文件缓存查找：file_name={file_name}, 缓存={self.file_cache[file_name]}")  # 输出缓存内容
            # 如果有多个匹配项，直接返回第一个
            return self.file_cache[file_name][0]

        # 2. 如果未找到文件，返回 None
        return None

    def print_cache(self):
        """
        打印缓存内容。
        """
        print("文件名到路径的映射：")
        for file_name, paths in self.file_cache.items():
            print(f"{file_name}: {paths}")