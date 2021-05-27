import os
import sys
import django

# 将django的settings配置到系统路径
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ssas.settings")
django.setup()