from setuptools import setup, find_packages

setup(
    name='PyEnsembleCNN',
    version='1.0.1',
    packages=find_packages(),
    install_requires=[
        'torch>=2.4.1',
        'torchvision>=0.19.1',
        'matplotlib>=3.7.5',
        'grad-cam>=1.5.4'
    ],
    author='Cole Foster',
    author_email='colefoster2026@gmail.com',
    description='A dynamic CNN ensembling framework for PyTorch',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/fostercm/PyEnsembleCNN',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)