import sys
import os
def get_application_path():
    """获取应用程序路径，兼容开发环境和打包环境"""
    if getattr(sys, 'frozen', False):
        # 如果是打包后的环境
        return os.path.dirname(sys.executable)
    else:
        # 如果是开发环境
        return os.path.dirname(os.path.abspath(__file__))