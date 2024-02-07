from setuptools import setup, find_packages

setup(
    name='icvb',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib'
    ],
    # Outras informações opcionais, como descrição, autor, etc.
    description='ICVB',
    author='Nivaldo Vasconcelos',
    author_email='napvasconcelos@gmail.com',
    url='https://github.com/neurobucano/icvb/',
)
