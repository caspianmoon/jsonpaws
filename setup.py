from setuptools import setup, find_packages

setup(
    name='json_paws',
<<<<<<< HEAD
    version='0.1.8',
=======
    version='0.1.6',
>>>>>>> 29f3df67f7367d71bddb50a69d6885ef85cd921f
    description='A library for generating structured JSON using GPT-4o.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Khazar Ayaz',
    author_email='khazar.ayaz@personnoai.com',
<<<<<<< HEAD
    url='https://github.com/caspianmoon/jsonpaws',  # Your repository URL
=======
    url='https://github.com/caspianmoon/jsonpaws.git',  # Your repository URL
>>>>>>> 29f3df67f7367d71bddb50a69d6885ef85cd921f
    packages=find_packages(),
    install_requires=[
        'openai',  # Specify other dependencies here if needed
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    include_package_data=True,  # Include non-code files specified in MANIFEST.in
    license='MIT',  # License type
)
