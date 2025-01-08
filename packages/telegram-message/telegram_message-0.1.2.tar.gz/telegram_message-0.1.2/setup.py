from setuptools import setup, find_packages

# Завантаження вмісту README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="telegram_message",                
    version="0.1.2",                          
    packages=find_packages(),               # Автоматичний пошук всіх підкаталогів
    description="sending notifications to telegram",  # Короткий опис
    author="Tetiana",                     
    author_email="tetyana.d@nitra.dev",   
    long_description=long_description,           # Детальний опис
    long_description_content_type="text/markdown",  # Формат README
)
