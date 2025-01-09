from setuptools import setup, find_packages

setup(
    name="ulauncher-generator",
    version="0.1.3",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
        ]
    },
    entry_points={
        'console_scripts': [
            'ulauncher-generator=ulauncher_extension_generator.main:main',
        ],
    },
    author="ubuntupunk",
    author_email="ubuntupunk@gmail.com",
    description="A Ulauncher extension generator",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ubuntupunk/ulauncher-extension-generator",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.6",
)
