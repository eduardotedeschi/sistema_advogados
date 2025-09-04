from setuptools import setup, find_packages

setup(
    name="software_adv",
    version="1.0.0",
    author="Eduardo Tedeschi",
    description="Sistema de gestão para advogados (clientes e documentos).",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "python-docx",
        "docx2pdf",
        "brazilcep",
        "pandas",
        "sv-ttk",
        "darkdetect",
    ],
    entry_points={
        "console_scripts": [
            "software-adv = software_adv.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
