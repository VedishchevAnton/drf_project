import re

from rest_framework import serializers


def validate_content(value):
    # Проверка содержимого на наличие недопустимых ссылок
    # В данном случае, разрешаем только ссылки на youtube.com
    pattern = r'(https?://)?(www\.)?youtube\.com'
    if not re.search(pattern, value):
        raise serializers.ValidationError("Содержимое содержит недопустимые ссылки.")
    return value
