from setuptools import setup, find_packages

setup(
    name='audiocencesored',
    version='0.2',
    packages=find_packages(),
    install_requires=open('requirements.txt').read().splitlines(),
    author='Sleeping4cat i.e. Ammar',
    author_email='sleeping4cat@gmail.com',
    description='Check your audio for profanity on steroids.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/sleepingcat4/audio-profanity',
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
