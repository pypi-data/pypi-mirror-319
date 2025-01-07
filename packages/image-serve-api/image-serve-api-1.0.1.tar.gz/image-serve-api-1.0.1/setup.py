from setuptools import setup

setup(
    name="image-serve-api",
    version="1.0.1",
    packages=["image_serve_api"],  # Correct package name
    install_requires=["requests"],
    description="A Python package for effortless image uploads and management via the ImageServe API, ensuring seamless integration for your applications.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="IP Softech - Pratham Pansuriya",
    author_email="ipsoftechsolutions@gmail.com",
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
    ],
)

