from setuptools import setup, find_packages

setup(
    name='PyDebugTools',
    version='0.1.2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'ipython',
        'rich',
        'langchain_groq',
    ],
    entry_points={
        'console_scripts': [
            'notebook-debugger=PyDebugTool.debug:main',
        ],
    },
    license='MIT',
    author='Sambit Mallick',
    author_email='sambitmallick.pro@gmail.com',
    description='A Python library for debugging python files and notebooks using GROQ',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/notebook-debugger',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)