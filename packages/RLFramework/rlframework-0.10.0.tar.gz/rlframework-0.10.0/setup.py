from setuptools import setup, find_packages

setup(
    name='RLFramework',
    version='0.10.0',
    packages=find_packages(include=['RLFramework', 'RLFramework.*']),
    url="https://github.com/Markseo0424/RLFramework.git",
    install_requires=[
        'numpy',
        'torch',
        'matplotlib'
    ],
    extras_require={
        "gym": ["gymnasium>=0.29.1", "moviepy>=1.0.0"],
    }
)
