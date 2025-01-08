from setuptools import setup, find_packages

setup(
    name="gerenciador_projetos",
    version="1.0.0",
    author="Agnaldo Vilariano",
    author_email="agnaldo@example.com",
    description="Uma ferramenta para gerenciar projetos com templates pré-definidos.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Vilariano/gerenciador-de-projetos",  # Atualize com o link do seu repositório
    packages=find_packages(),
    include_package_data=True,
    package_data={"": ["boilerplates/**/*.zip"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "tk",  # Inclua outras dependências aqui, se necessário
    ],
    entry_points={
        "console_scripts": [
            "gerenciador-projetos=gerenciador_projetos.interface:criar_interface",
        ],
    },
)
