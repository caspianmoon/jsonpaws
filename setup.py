from setuptools import setup, find_packages

setup(
    name='json_paws',
    version='0.1.9',  # Use your local version or decide based on requirements
    description='A library for generating structured JSON using GPT-4o.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Khazar Ayaz',
    author_email='khazar.ayaz@personnoai.com',
    url='https://github.com/caspianmoon/jsonpaws',  # Decide which URL is correct
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
