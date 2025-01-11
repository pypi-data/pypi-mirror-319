from setuptools import setup

setup(
    name="salesmanago-tools",
    version="0.1.2",
    author="Kyrylo Pavlenko",
    author_email="pavlenkokirill120@gmail.com",
    description="Salesmanago Tools is a project designed to simplify working with the Salesmanago API. It provides a set of utilities and pre-built queries for seamless integration with the platform, enabling quick and efficient execution of tasks such as contact management, event tracking, marketing automation, and data analytics",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Web-parsers/SalesmanagoTools",
    packages=[
        'salesmanago_tools',
        'salesmanago_tools.service',
        'salesmanago_tools.utils',
    ],
    install_requires=[
        "aiohttp==3.11.11",
        "requests==2.32.3",
        "pandas==2.2.3",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)