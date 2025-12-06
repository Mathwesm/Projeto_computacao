"""
Setup script para instalação do MathShape Quest
"""

from setuptools import setup, find_packages
import os

# Lê o README
def read_file(filename):
    with open(filename, encoding='utf-8') as f:
        return f.read()

# Lê os requirements
def read_requirements():
    with open('requirements.txt') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='mathshape-quest',
    version='1.0.0',
    author='Equipe MathShape Quest',
    author_email='seu-email@exemplo.com',
    description='Jogo Educativo de Computação Gráfica',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/seu-usuario/Projeto_computacao_grafica',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Education',
        'Topic :: Education',
        'Topic :: Games/Entertainment',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.8',
    install_requires=read_requirements(),
    extras_require={
        'dev': [
            'pytest>=7.0',
            'pytest-cov>=4.0',
            'black>=22.0',
            'flake8>=4.0',
            'mypy>=0.990',
        ],
    },
    entry_points={
        'console_scripts': [
            'mathshape-quest=main:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
