from setuptools import setup

setup(
    name='',
    version='2.0',
    url='https://github.com/gl4ssesbo1/Nebula',
    package_data={
        '': [
            '*.json',
            '*.txt'
        ]
    },
    install_requires=[
        "boto3",
        "botocore",
        "termcolor",
        "colored",
        "colorama",
        "justify",
        "justifytext",
        "prompt_toolkit",
        "awscli",
        "pypager",
        "nuitka",
        "pyinstaller",
        "Cython",
        "crtsh",
        "scapy"
    ],
    license='MIT License',
    author='gl4ssesbo1',
    author_email='gl4ssesbo1@protonmail.com',
    description='Cloud C2 Framework, which at the moment offers reconnaissance, enumeration, exploitation, post exploitation on AWS, but still working to allow testing other Cloud Providers and DevOps Components.'
)