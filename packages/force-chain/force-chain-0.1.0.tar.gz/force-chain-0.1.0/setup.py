from setuptools import setup, find_packages

setup(
    name="force-chain",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "flask",
        "requests",
        "torch",
        "transformers",
        "petals",
        "fastapi",
        "uvicorn"
    ],
    entry_points={
        'console_scripts': [
            'force-node=force_chain.node:main',
        ],
    },
    python_requires='>=3.8',
)