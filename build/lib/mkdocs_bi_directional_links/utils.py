import os

def resolve_file_path(file_ref, current_file_path, base_dir):
    """
    解析文件路径，支持相对路径和绝对路径。
    """
    # 解析相对路径
    current_dir = os.path.dirname(os.path.join(base_dir, current_file_path))
    file_path = os.path.normpath(os.path.join(current_dir, file_ref))

    # 检查文件是否存在
    if os.path.isfile(file_path):
        return file_path

    # 回退到基础目录
    file_path = os.path.normpath(os.path.join(base_dir, file_ref))
    if os.path.isfile(file_path):
        return file_path

    return None  # 如果未找到文件，返回 None