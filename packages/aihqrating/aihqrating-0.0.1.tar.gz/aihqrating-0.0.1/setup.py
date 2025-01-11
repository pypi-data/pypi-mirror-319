from setuptools import setup, find_packages

setup(
    name='aihqrating',  
    version='0.0.1',         
    author='evans.zhu',
    author_email='evanszhu2001@gmail.com',
    description='TBD',
    long_description=' TBD',
    long_description_content_type='text/markdown',
    packages=['aihqrating'],
    package_data={'aihqrating': ['images/*']},
    install_requires=['numpy', 'matplotlib', 'scipy','pandas','scikit-learn', 'werkzeus','Flask','Flask-SocketIO','sentencepiece','torch','transformers','openai'],  
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
