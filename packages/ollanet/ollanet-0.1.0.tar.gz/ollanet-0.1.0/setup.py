from setuptools import setup, find_packages

setup(
    name='ollanet',
    version='0.1.0',
    description='A CLI tool for Ollama API with ngrok tunneling',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'uvicorn',
        'pyngrok',
        'simple_term_menu',
        'requests',
        'pydantic',
        'click'
    ],
    entry_points={
        'console_scripts': [
            'ollanet=ollanet.cli:main',
        ],
    },
)