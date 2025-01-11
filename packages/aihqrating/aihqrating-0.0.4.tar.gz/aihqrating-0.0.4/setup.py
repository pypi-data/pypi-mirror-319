from setuptools import setup, find_packages

setup(
    name='aihqrating',  
    version='0.0.4',         
    author='evans.zhu',
    author_email='evanszhu2001@gmail.com',
    description='TBD',
    long_description=' TBD',
    long_description_content_type='text/markdown',
    packages=['aihqrating'],
    package_data={'aihqrating': ['images/*']},
    install_requires=['numpy', 'matplotlib', 'scipy','pandas','scikit-learn', 'Werkzeug==2.3.8','Flask==2.2.2','Flask-SocketIO==5.3.6','sentencepiece==0.2.0','torch==2.0.1','transformers==4.29.2','openai==1.18.0'],  
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
