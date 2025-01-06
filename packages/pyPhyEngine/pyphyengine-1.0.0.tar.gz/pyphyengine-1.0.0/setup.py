"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import(
    setup, 
    find_packages
)
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name="pyPhyEngine",  # Required
    
    # Versions should comply with PEP 440:
    # https://www.python.org/dev/peps/pep-0440/
    version="1.0.0",  # Required
    
    # This is a one-line description or tagline of what your project does.
    description="A physics engine based on matplotlib written in Python",  # Optional
    
    # This is an optional longer description of your project that represents
    # the body of text which users will see when they visit PyPI.
    long_description=long_description,  # Optional
    
    # Denotes that our long_description is in Markdown; valid values are
    # text/plain, text/x-rst, and text/markdown
    long_description_content_type="text/markdown",  # Optional (see note above)
    
    # This should be a valid link to your project's main homepage.
    #
    # This field corresponds to the "Home-Page" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#home-page-optional
    url="https://github.com/Floerianc/pyPhyEngine",  # Optional
    
    # This should be your name or the name of the organization which owns the
    # project.
    author="Floerianc",  # Optional
    
    # This should be a valid email address corresponding to the author listed
    # above.
    author_email="stegerosch1@gmail.com",  # Optional
    
    # Classifiers help users find your project by categorizing it.
    
    classifiers=[  # Optional
        
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        
        # Pick your license as you wish
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate you support Python 3. These classifiers are *not*
        # checked by 'pip install'. See instead 'python_requires' below.
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    
    # This field adds keywords for your project which will appear on the
    # project page. What does your project relate to?
    keywords="matplotlib, physics, real-time",  # Optional
    
    # You can just specify package directories manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(),  # Required
    
    # Specify which Python versions you support. In contrast to the
    # 'Programming Language' classifiers above, 'pip install' will check this
    # and refuse to install the project if the version does not match. See
    # https://packaging.python.org/guides/distributing-packages-using-setuptools/#python-requires
    python_requires=">=3.7, <4",
    
    # This field lists other packages that your project depends on to run.
    # Any package you put here will be installed by pip when your project is
    # installed, so they must be valid existing projects.
    
    install_requires=["matplotlib", 'numpy', 'opencv-python', 'natsort'],  # Optional
    
    project_urls={  # Optional
        "Documentation": "https://flo.ohhellnaw.de/pyPhyEngine/",
        "Source": "https://github.com/Floerianc/pyPhyEngine/",
    },
)