"""
    高并发部署需要文件wsgi配置
"""
from manager import manager

if __name__ == "__main__":
    manager.run()
