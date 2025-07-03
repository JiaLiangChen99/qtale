import os
import flet as ft

# 获取应用存储路径，确保跨平台兼容
def get_app_storage_path():
    """获取应用的持久化存储路径"""
    # 优先使用Flet提供的环境变量
    flet_storage = os.getenv("FLET_APP_STORAGE_DATA")
    if flet_storage:
        return flet_storage
    
    # 如果环境变量不存在，使用平台特定的路径
    import platform
    system = platform.system().lower()
    
    if system == "android":
        # Android - 尝试多个可能的路径
        possible_paths = [
            "/data/data/com.example.qtale/files",  # 替换为你的实际包名
            "/storage/emulated/0/Android/data/com.example.qtale/files",
            "/sdcard/Android/data/com.example.qtale/files",
            "/data/user/0/com.example.qtale/files",
            os.path.join(os.path.expanduser("~"), ".qtale"),  # 备用路径
        ]
        
        for path in possible_paths:
            try:
                # 尝试创建目录来测试权限
                os.makedirs(path, exist_ok=True)
                if os.access(path, os.W_OK):  # 检查写权限
                    return path
            except (OSError, PermissionError):
                continue
        
        # 如果所有路径都失败，使用当前目录
        return os.getcwd()
        
    elif system == "windows":
        # Windows用户目录
        return os.path.join(os.path.expanduser("~"), "AppData", "Local", "QtaleMusic")
    elif system == "darwin":  # macOS
        return os.path.join(os.path.expanduser("~"), "Library", "Application Support", "QtaleMusic")
    else:  # Linux
        return os.path.join(os.path.expanduser("~"), ".local", "share", "QtaleMusic")

# 使用改进的存储路径
FLET_APP_STORAGE_DATA = get_app_storage_path()
FLET_APP_CONSOLE = os.getenv("FLET_APP_CONSOLE")

# 确保存储路径存在
if not os.path.exists(FLET_APP_STORAGE_DATA):
    os.makedirs(FLET_APP_STORAGE_DATA, exist_ok=True)

MEDIA_PATH = os.path.join(FLET_APP_STORAGE_DATA, "media")
MUSIC_PATH = os.path.join(MEDIA_PATH, "music")
VIDEO_PATH = os.path.join(MEDIA_PATH, "video")
IMAGE_PATH = os.path.join(MEDIA_PATH, "image")

# 数据库文件路径
DATABASE_PATH = os.path.join(FLET_APP_STORAGE_DATA, "music.db")

def init_path():
    """初始化所有必要的目录"""
    paths_to_create = [
        FLET_APP_STORAGE_DATA,
        MEDIA_PATH,
        MUSIC_PATH,
        VIDEO_PATH,
        IMAGE_PATH
    ]
    
    for path in paths_to_create:
        if not os.path.exists(path):
            try:
                os.makedirs(path, exist_ok=True)
                print(f"创建目录: {path}")
            except (OSError, PermissionError) as e:
                print(f"创建目录失败 {path}: {e}")

def get_database_url():
    """获取数据库连接URL"""
    return f"sqlite:///{DATABASE_PATH}"

# 打印路径信息用于调试
def print_storage_info():
    """打印存储路径信息用于调试"""
    print("=== 存储路径信息 ===")
    print(f"平台: {__import__('platform').system()}")
    print(f"应用存储路径: {FLET_APP_STORAGE_DATA}")
    print(f"媒体路径: {MEDIA_PATH}")
    print(f"音乐路径: {MUSIC_PATH}")
    print(f"数据库路径: {DATABASE_PATH}")
    print(f"数据库文件存在: {os.path.exists(DATABASE_PATH)}")
    print(f"存储路径可写: {os.access(FLET_APP_STORAGE_DATA, os.W_OK)}")
    print("====================")

# 检查存储权限
def check_storage_permissions():
    """检查存储权限"""
    try:
        test_file = os.path.join(FLET_APP_STORAGE_DATA, "test_write.txt")
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        return True
    except (OSError, PermissionError):
        return False