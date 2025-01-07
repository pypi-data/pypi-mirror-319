from setuptools import setup, find_packages

setup(
    name="odoo-addon-branch-transfer",  # Nom du package (utilise un préfixe pour les addons Odoo)
    version="17.0.1.0.0",  # Version correspondant à celle du manifest
    description="Employee transfer between branches in Odoo HR",  # Résumé
    long_description=open("README.md").read(),  # Description longue depuis README.md
    long_description_content_type="text/markdown",  # Format de la description longue
    author="Cybrosys Techno Solutions, Open HRMS",  # Auteur du module
    author_email="info@cybrosys.com",  # Email de contact (optionnel)
    url="https://cybrosys.com",  # Site web de l'entreprise ou module
    license="LGPL-3",  # Licence spécifiée dans le manifest
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Framework :: Odoo",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),  # Inclut tous les packages nécessaires
    include_package_data=True,  # Inclut les fichiers mentionnés dans MANIFEST.in
    install_requires=[

    ],
    python_requires=">=3.8",  # Compatible avec Python 3.8 et supérieur
    entry_points={
        'odoo.addons': [
            'branch_transfer = branch_transfer',  # Point d'entrée pour le module
        ],
    },
)
