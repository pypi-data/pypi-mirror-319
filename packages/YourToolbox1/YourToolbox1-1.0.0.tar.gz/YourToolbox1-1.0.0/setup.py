from setuptools import setup, find_packages
setup(
    name='YourToolbox1',
    version='1.0.0',
    description='YourToolbox have Administrator Privileges and Create a Shortcut',
    author='I',
    author_email='363766687@qq.com',
    packages=find_packages(),
    py_modules=['YourToolbox1'],
    install_requires=[
        'opencv-python',
        'requests',
        'pygame',
        'beautifulsoup4',
        'numpy',
        'matplotlib',
        'winshell',
        'pywin32'
    ]
)