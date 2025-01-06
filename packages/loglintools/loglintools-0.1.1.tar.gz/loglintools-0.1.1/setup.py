from setuptools import setup, find_packages

setup(
    name='loglintools',                     # Название библиотеки
    version='0.1.1',                       # Версия
    packages=find_packages(),              # Автоматический поиск пакетов
    author='MK',
    install_requires=['requests>=2.25.1'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
