import re
import logging
from pathlib import Path

class LinkProcessor:
    def __init__(self):
        self.includes = [".md", ".png", ".jpg", ".mp4", ".mp3"]  # 支持的文件扩展名

    def process_markdown(self, markdown, page, config, files, search_integration):
        """
        处理 Markdown 中的双向链接语法，生成相应的 HTML 标签。
        """

        def replace_bi_directional_link(match):
            """
            替换双向链接语法为 HTML 标签。
            """
            file_ref = match.group(1).strip()  # 获取文件引用
            text = match.group(3).strip() if match.group(3) else file_ref  # 获取自定义文本

            # 如果文件引用没有扩展名，默认添加 .md
            if not any(file_ref.endswith(ext) for ext in self.includes):
                file_ref += ".md"

            # 获取当前文件的路径
            from_file = page.file.src_path

            # 使用 SearchIntegration 查找文件路径
            file_path = search_integration.find_file(from_file, file_ref)
            if not file_path:
                logging.warning(f"未找到匹配的文件：'{file_ref}'。")
                return match.group(0)  # 如果未找到文件，返回原始文本
            else:
                logging.debug(f"找到文件：'{file_ref}' -> '{file_path}'。")  # 添加调试日志

            # 统一路径分隔符为正斜杠
            file_path = file_path.replace("\\", "/")

            # 获取 site_url 的第二个路径段
            site_url = config.get("site_url", "")
            base_path = ""
            if site_url:
                # 使用正则表达式提取第二个路径段
                match = re.match(r"https?://[^/]+/([^/]+)/?", site_url)
                if match:
                    base_path = match.group(1)  # 提取第二个路径段
                    if base_path:
                        base_path = f"/{base_path}"

            # 根据文件类型生成 HTML 标签
            if file_path.endswith(".md"):
                file_path = file_path[:-3]  # 去除 .md 扩展名
                return f'<a href="{base_path}/{file_path}/">{text}</a>'  # Markdown 文件生成链接
            elif any(file_path.endswith(ext) for ext in [".png", ".jpg", ".gif"]):
                return f'<img src="{base_path}/{file_path}" alt="{text}">'  # 图片文件生成图片标签
            elif any(file_path.endswith(ext) for ext in [".mp4", ".webm"]):
                return f'<video controls><source src="{base_path}/{file_path}"></video>'  # 视频文件生成视频标签
            elif any(file_path.endswith(ext) for ext in [".mp3", ".wav"]):
                return f'<audio controls><source src="{base_path}/{file_path}"></audio>'  # 音频文件生成音频标签
            else:
                return match.group(0)  # 其他文件类型返回原始文本

        # 使用正则表达式匹配 [[file]] 和 [[file|text]] 语法
        markdown = re.sub(r'!?\[\[([^|\]\n]+)(\|([^\]\n]+))?\]\]', replace_bi_directional_link, markdown)
        return markdown