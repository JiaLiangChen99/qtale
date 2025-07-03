from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 导入存储路径配置
from static import get_database_url

# 使用正确的数据库路径
engine = create_engine(get_database_url())

Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

# 建表
class Music(Base):
    __tablename__ = "music"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    image_path = Column(String)
    music_path = Column(String)

# 创建所有表
def create_tables():
    """创建所有数据库表"""
    try:
        Base.metadata.create_all(bind=engine)
        print("数据库表创建完成")
        return True
    except Exception as e:
        print(f"创建数据库表失败: {e}")
        return False

# 初始化数据库
def init_database():
    """初始化数据库"""
    success = create_tables()
    if success:
        print(f"数据库初始化完成，路径: {get_database_url()}")
    return success

# 检查表是否存在
def table_exists(table_name):
    """检查指定表是否存在"""
    try:
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        exists = table_name in tables
        print(f"检查表 '{table_name}' 存在性: {exists}")
        return exists
    except Exception as e:
        print(f"检查表存在性失败: {e}")
        return False

# 确保数据库表存在
def ensure_tables_exist():
    """确保数据库表存在，如果不存在则创建"""
    try:
        if not table_exists("music"):
            print("检测到数据库表不存在，正在创建...")
            success = create_tables()
            if success:
                print("数据库表创建成功")
            else:
                print("数据库表创建失败")
            return success
        else:
            print("数据库表已存在")
            return True
    except Exception as e:
        print(f"确保数据库表存在时发生错误: {e}")
        # 如果检查失败，尝试直接创建表
        try:
            print("尝试直接创建数据库表...")
            return create_tables()
        except Exception as e2:
            print(f"直接创建数据库表也失败: {e2}")
            return False
