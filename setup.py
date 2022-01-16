import setuptools




setuptools.setup(
    author="Jash Shah",
    author_email="shahjash271@gmail.com",
    name='AlgoAnalyzer',
    license="MIT",
    description='AlgoAnalyzer is a package for designing your trading strategies and run simulations to backtest your strategies and check their robustness',
    version='v0.0.6',
    long_description_content_type='text/markdown',
    long_description=open('Readme.md',encoding="utf-8").read(),
    
    url='https://github.com/Jash271/AlgoAnalyzer',
    packages=setuptools.find_packages(),
    
    python_requires=">=3.6",
    install_requires=['yfinance','plotly'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        
        
        
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        
    ],
    include_package_data=True,
    
)
