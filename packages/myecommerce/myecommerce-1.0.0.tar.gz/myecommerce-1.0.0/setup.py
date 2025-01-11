#pip install setuptools

from setuptools import setup, find_packages

setup(
    name = "myecommerce",                         # Name of your package
    version = "1.0.0",                          # Version number
    author = "Bipul Kumar",                     # Your name
    author_email = "bipul@example.com",         # Your email
    description = "A simple e-commerce package for managing products, users, and orders.",
    packages = find_packages(),                 # Automatically find sub-packages
    install_requires = [],                      # List any dependencies here
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",                    # Minimum Python version required
)
