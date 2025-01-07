from setuptools import setup, find_packages

setup(
    name="resume-analysis-ai",                  # Package name on PyPI
    version="0.1.0",                    # Package version
    author="projectest20",                 # Author name
    author_email="projecttest021010@gmail.com",  # Author's email
    description="Resume Analysis using Ai",  # Short description of the package
    long_description=open("README.md").read(),  # Long description from README.md
    long_description_content_type="text/markdown",  # Format of long description
    url="https://github.com/projectest20/resume_analysis_ai.git",  # URL to your project (GitHub repo or website)
    packages=find_packages(),  # This will automatically find all packages in your project
    include_package_data=True,  # Include non-Python files (static files)
    package_data={  # Include specific files for each package
        '': ['static/*', 'templates/*', 'uploads/*','index.html','interact.html','styles.css'],  # Add paths to your static files
    },
    classifiers=[  # Additional metadata to help users discover your package
        "Programming Language :: Python :: 3",  # Specify the supported Python versions
        "Operating System :: OS Independent",  # The package works on all major OS platforms
    ],
    python_requires=">=3.6",  # Python version requirement
)
