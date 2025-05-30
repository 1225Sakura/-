# 文件夹结构检索代码
查询文件夹的目录结构

# 使用方法
## 列出当前目录结构
python list_folder_structure.py --folder .
## 列出指定目录结构
python list_folder_structure.py --folder /path/to/folder

# 高级选项
## 显示文件大小
python list_folder_structure.py --folder /path/to/folder --show-size
## 显示修改时间
python list_folder_structure.py --folder /path/to/folder --show-time
## 限制递归深度为2层
python list_folder_structure.py --folder /path/to/folder --max-depth 2
## 只显示文件夹
python list_folder_structure.py --folder /path/to/folder --only-folders
## 只显示特定类型的文件
python list_folder_structure.py --folder /path/to/folder --filter "*.jpg"
## 组合使用
python list_folder_structure.py --folder /path/to/folder --show-size --show-time --max-depth 3

# 特点
1. 树形结构展示：使用类似于tree命令的格式展示文件和文件夹
2.文件类型图标：根据文件扩展名显示不同的图标
3.大小统计：可选显示文件和文件夹大小
4.时间信息：可选显示文件和文件夹的修改时间
5.深度控制：可以限制目录递归的深度
6.文件过滤：可以只显示匹配特定模式的文件
7.进度显示：显示扫描进度和统计信息
8.结果保存：将结构保存为文本文件
9.输出结果示例：
#文件夹结构: /home/user/project
#扫描时间: 2025-05-30 14:05:23
#总文件夹数: 15
#总文件数: 87

├── 📁 data
│   ├── 📁 photo
│   │   ├── 📁 train
│   │   │   ├── 📁 blurred
│   │   │   ├── 📁 no_video
│   │   │   ├── 📁 normalcy
│   │   │   └── 📁 splash_screen
│   │   └── 📁 val
│   │       ├── 📁 blurred
│   │       ├── 📁 no_video
│   │       ├── 📁 normalcy
│   │       └── 📁 splash_screen
├── 📁 work_dirs
│   └── 📁 resnet50_photo_classifier
│       ├── 📄 config.py
│       ├── 📊 scalars.json
│       └── 📝 epoch_148.pth
├── 📝 inference.py
├── 📝 mmpretrain_config.py
├── 📝 train.py
└── 📑 README.md
