#!/usr/bin/env python
import os
import argparse
import time
import logging
from pathlib import Path
from tqdm import tqdm

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f'folder_structure_{time.strftime("%Y%m%d_%H%M%S")}.log')
    ]
)
logger = logging.getLogger(__name__)

def parse_args():
    parser = argparse.ArgumentParser(description='检索文件夹结构')
    parser.add_argument('--folder', help='要检索的文件夹路径', required=True)
    parser.add_argument('--output', help='输出文件', default='folder_structure.txt')
    parser.add_argument('--max-depth', type=int, help='最大递归深度', default=None)
    parser.add_argument('--show-size', action='store_true', help='显示文件大小')
    parser.add_argument('--show-time', action='store_true', help='显示修改时间')
    parser.add_argument('--only-folders', action='store_true', help='只显示文件夹')
    parser.add_argument('--filter', help='文件名过滤器(如 *.jpg)', default=None)
    return parser.parse_args()

def get_size_str(size_bytes):
    """将字节数转换为易读的大小字符串"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes/1024:.2f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes/(1024*1024):.2f} MB"
    else:
        return f"{size_bytes/(1024*1024*1024):.2f} GB"

def count_items(folder_path):
    """计算文件夹中的文件和文件夹数量"""
    folder_count = 0
    file_count = 0
    
    for _, dirs, files in os.walk(folder_path):
        folder_count += len(dirs)
        file_count += len(files)
    
    return folder_count, file_count

def scan_folder(folder_path, output_file, max_depth=None, show_size=False, 
               show_time=False, only_folders=False, file_filter=None):
    """扫描文件夹并写入结构到文件"""
    
    folder_path = os.path.abspath(folder_path)
    
    if not os.path.exists(folder_path):
        logger.error(f"文件夹 {folder_path} 不存在")
        return False
    
    # 计算文件夹中的项目数
    logger.info(f"正在统计 {folder_path} 中的文件数量...")
    folder_count, file_count = count_items(folder_path)
    logger.info(f"共找到 {folder_count} 个文件夹和 {file_count} 个文件")
    
    # 打开输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        # 写入头部信息
        f.write(f"# 文件夹结构: {folder_path}\n")
        f.write(f"# 扫描时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# 总文件夹数: {folder_count}\n")
        f.write(f"# 总文件数: {file_count}\n")
        f.write("\n")
        
        def write_structure(current_path, prefix="", depth=0):
            if max_depth is not None and depth > max_depth:
                return
            
            # 获取目录内容并排序
            try:
                items = sorted(os.listdir(current_path))
            except PermissionError:
                f.write(f"{prefix}├── [无法访问: 权限不足]\n")
                return
            except Exception as e:
                f.write(f"{prefix}├── [错误: {str(e)}]\n")
                return
                
            # 处理所有项目
            for i, item in enumerate(items):
                item_path = os.path.join(current_path, item)
                is_last = (i == len(items) - 1)
                
                # 决定连接符
                connector = "└── " if is_last else "├── "
                
                # 检查是否为目录
                if os.path.isdir(item_path):
                    # 附加大小信息
                    size_info = ""
                    if show_size:
                        try:
                            total_size = sum(os.path.getsize(os.path.join(dirpath, filename)) 
                                           for dirpath, _, filenames in os.walk(item_path) 
                                           for filename in filenames)
                            size_info = f" ({get_size_str(total_size)})"
                        except:
                            size_info = " (大小计算失败)"
                    
                    # 附加时间信息
                    time_info = ""
                    if show_time:
                        try:
                            mtime = os.path.getmtime(item_path)
                            time_info = f" [修改: {time.strftime('%Y-%m-%d %H:%M', time.localtime(mtime))}]"
                        except:
                            time_info = " [时间获取失败]"
                    
                    # 写入文件夹
                    f.write(f"{prefix}{connector}📁 {item}{size_info}{time_info}\n")
                    
                    # 递归处理子目录
                    new_prefix = prefix + ("    " if is_last else "│   ")
                    write_structure(item_path, new_prefix, depth + 1)
                    
                elif not only_folders:  # 如果不是只显示文件夹
                    # 过滤文件
                    if file_filter:
                        import fnmatch
                        if not fnmatch.fnmatch(item, file_filter):
                            continue
                    
                    # 附加大小信息
                    size_info = ""
                    if show_size:
                        try:
                            size_info = f" ({get_size_str(os.path.getsize(item_path))})"
                        except:
                            size_info = " (大小获取失败)"
                    
                    # 附加时间信息
                    time_info = ""
                    if show_time:
                        try:
                            mtime = os.path.getmtime(item_path)
                            time_info = f" [修改: {time.strftime('%Y-%m-%d %H:%M', time.localtime(mtime))}]"
                        except:
                            time_info = " [时间获取失败]"
                    
                    # 判断文件类型图标
                    icon = "📄"
                    if item.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                        icon = "🖼️"
                    elif item.endswith(('.mp4', '.avi', '.mov', '.mkv')):
                        icon = "🎬"
                    elif item.endswith(('.mp3', '.wav', '.flac')):
                        icon = "🎵"
                    elif item.endswith(('.zip', '.rar', '.7z', '.tar', '.gz')):
                        icon = "📦"
                    elif item.endswith(('.py', '.java', '.cpp', '.js', '.html', '.css')):
                        icon = "📝"
                    elif item.endswith(('.pdf')):
                        icon = "📑"
                    elif item.endswith(('.doc', '.docx')):
                        icon = "📃"
                    elif item.endswith(('.xls', '.xlsx')):
                        icon = "📊"
                    elif item.endswith(('.ppt', '.pptx')):
                        icon = "📽️"
                    
                    # 写入文件
                    f.write(f"{prefix}{connector}{icon} {item}{size_info}{time_info}\n")
        
        # 开始递归写入
        logger.info(f"正在将文件结构写入到 {output_file}...")
        write_structure(folder_path)
    
    logger.info(f"文件夹结构已成功写入到 {output_file}")
    return True

def main():
    args = parse_args()
    
    start_time = time.time()
    logger.info(f"开始扫描文件夹: {args.folder}")
    
    result = scan_folder(
        args.folder, 
        args.output, 
        args.max_depth,
        args.show_size,
        args.show_time,
        args.only_folders,
        args.filter
    )
    
    end_time = time.time()
    
    if result:
        logger.info(f"扫描完成，用时 {end_time - start_time:.2f} 秒")
    else:
        logger.error(f"扫描失败，用时 {end_time - start_time:.2f} 秒")
    
    return 0 if result else 1

if __name__ == '__main__':
    import sys
    sys.exit(main())
