from setuptools import setup, find_packages

setup(
    name='xthreads',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # Hier kannst du Abhängigkeiten hinzufügen
    ],
    entry_points={
        'console_scripts': [
            'xthreads=xthreads:main',
        ],
    },
    author='hexzhen3x7',
    author_email='hexzhen3x7@outlook.de',
    description='Ein Modul zur Verwaltung und Ausführung von Aufgaben in einer Warteschlange',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/dein-repo/task_manager',
)
