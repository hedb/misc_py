from setuptools import setup, find_packages

setup(
    name='your_project_name',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A brief description of your project',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/your_project_name',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'langchain-core~=0.3.5',
        'langchain-openai~=0.2.0',
        'langgraph~=0.2.23',
    ],
    entry_points={
        'console_scripts': [
            # Define command-line scripts here.
            # Example: 'your_command=your_module:main_function',
        ],
    },
)