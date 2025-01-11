from setuptools import find_packages, setup

setup(
    name='prlps_speller',
    version='0.0.1',
    author='prolapser',
    packages=find_packages(),
    url='https://github.com/gniloyprolaps/prlps_speller',
    license='LICENSE.txt',
    description='асинхронный спеллер с использованием API Yandex Speller',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    install_requires=['httpx'],
    python_requires='>=3.10',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)