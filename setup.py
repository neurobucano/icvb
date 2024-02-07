from setuptools import setup, find_packages

setup(
    name='nome_do_pacote',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'os',
        'matplotlib',
        # Liste todas as dependências necessárias aqui
    ],
    # Outras informações opcionais, como descrição, autor, etc.
    description='ICVB',
    author='Nivaldo Vasconcelos',
    author_email='napvasconcelos@gmail.com',
    url='https://github.com/neurobucano/allen-icvb/',
)
