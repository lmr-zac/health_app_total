#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from django.urls import reverse

try:
    # 使用应用urls.py中路由的name参数（如name='sport_record'）
    url = reverse('sport_record')
    print(f"完整路径：/api{url}")  # 预期输出：/api/sport/record/
except Exception as e:
    print(f"路由不存在：{e}")

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_backend.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
