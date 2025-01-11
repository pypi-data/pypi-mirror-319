from setuptools import setup, find_packages

setup(
    name='f-tools',
    version='3.0.2',
    packages=find_packages(),
    install_requires=[
        'boto3',  # AWS SDK for Python
        'inquirer',  # For interactive command-line prompts
    ],
    entry_points={
        'console_scripts': [
            'f-ecs-bash=f_tools.ecs_bash:main',
        ],
    },
    # Additional metadata about the project
    author='Filipe Ferreira',
    author_email='code@filipeandre.com',
    description='AWS tools including ECS bash execution',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/filipeandre/f-tools',
)