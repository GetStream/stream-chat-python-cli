from setuptools import setup

install_requires = [
    "certifi==2019.3.9",
    "chardet==3.0.4",
    "Click==7.0",
    "idna==2.8",
    "pycryptodomex==3.4.7",
    "PyJWT==1.7.1",
    "requests==2.21.0",
    "six==1.12.0",
    "stream-chat==0.2.0",
    "urllib3==1.26.5",
    "uuid==1.30",
]
long_description = open("README.md", "r").read()

setup(
    name="stream_chat_python_cli",
    version="0.0.1",
    author="Nick Parsons",
    author_email="nick@getstream.io",
    url="http://github.com/GetStream/stream-chat-python-cli",
    description="CLI for Stream Chat",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["stream_chat_python_cli"],
    zip_safe=False,
    install_requires=install_requires,
    include_package_data=True,
    entry_points={"console_scripts": ["stream-cli=stream_chat_python_cli.cli:main"]},
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Development Status :: 5 - Production/Stable",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
