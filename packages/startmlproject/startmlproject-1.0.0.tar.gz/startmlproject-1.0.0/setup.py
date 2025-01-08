from setuptools import setup

setup(
    name="startmlproject",
    version="1.0.0",
    py_modules=["startmlproject"],
    entry_points={
        "console_scripts": [
            "startmlproject=startmlproject:main",
        ],
    },
    author="Madhu Sunil",
    description="A custom Machine Learning project creation tool.",
    url="https://github.com/MadhuSuniL/startmlproject",  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
