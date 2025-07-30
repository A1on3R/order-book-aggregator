from setuptools import setup, find_packages

setup(
    name="order-book-aggregator",
    version="0.1",
    packages=find_packages(include=["aggregator", "aggregator.*"]),
    install_requires=[
        "requests"
    ],
    entry_points={
        'console_scripts': [
            'orderbook=aggregator.cli:main',
        ],
    },
   
)