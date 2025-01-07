
from setuptools import setup, find_packages

def print_name():
    import pyfiglet
    print(pyfiglet.figlet_format("S Praveen"))
    print("Package by S Praveen")

setup(
    name='foreachiterator',
    version='1.0.0',
    author='S Praveen',
    author_email='sarampentapraveen@example.com',
    description='A Python package for advanced iteration over iterables.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Spraveen8-chary/foreachiterator',
    packages=find_packages(),
    install_requires=[
        "pyfiglet",
    ],
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'foreachiterator-docs=foreachiterator.foreachiterator:ForEachIterator.print_docs',
        ],
    },
    python_requires='>=3.6',
    cmdclass={
        'install': print_name,  
    },
)
