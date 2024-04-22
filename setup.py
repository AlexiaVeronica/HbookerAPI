from setuptools import setup, find_packages

setup(
    name='HbookerAPI',
    version='0.3.3',
    author='AlexiaVeronica',
    author_email='your.email@example.com',
    description='HbookerAPI',
    long_description=open('README.md', "r", encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    url='https://github.com/AlexiaVeronica/HbookerAPI',
    packages=find_packages(),
    include_package_data=True,

    install_requires=[
        'requests',
        'pycryptodome'  # Assuming Crypto is from pycryptodome
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
