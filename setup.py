from setuptools import setup, find_packages

setup(
    name="rafiqi",
    version="0.1.0",
    description="An AI personal assistant",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "openai>=1.0.0",
        "python-dotenv>=0.19.0",
    ],
    entry_points={
        'console_scripts': [
            'rafiqi=rafiqi.main:main',
        ],
    },
) 