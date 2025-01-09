# setup.py

from setuptools import setup, find_packages

setup(
    name='simplyphi_valuation',
    version='0.1',
    author="Parth Tiwari",
    author_email="parth@simplyphi.co.uk",
    description="A valuation tool for real estate and property management.",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pandas',
        'numpy',
        'scikit-learn==1.5.2',
        'cloudpickle',
        'joblib',
        'scipy',
        'lightgbm',
        'xgboost'
    ],
    package_data={
        'simplyphi_valuation': ['data/*']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
