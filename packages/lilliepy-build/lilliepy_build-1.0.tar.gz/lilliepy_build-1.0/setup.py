from setuptools import setup

setup(
    name='lilliepy-build',
    version='1.0',
    install_requires=[
        'bs4',
        'colorama'
    ],
    entry_points={
        "console_scripts": [
            "builder=cli:app",
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    description='helps with static files related stuff in the lilliepy framework',
    keywords=[
        "lilliepy", "lilliepy-build", "reactpy"
    ],
    url='https://github.com/websitedeb/lilliepy-build',
    author='Sarthak Ghoshal',
    author_email='sarthak22.ghoshal@gmail.com',
    license='MIT',
    python_requires='>=3.6',
)