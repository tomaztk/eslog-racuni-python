from setuptools import setup, find_packages

setup(
    name='eslog_invoice_reader',
    version='0.1.0',
    description='Read e-SLOG invoice v2. ',
    author='Tomaztk',
    url='https://github.com/tomaztk/eslog-racuni-python',
    download_url='https://github.com/tomaztk/eslog-racuni-python/tarball',
    keywords=['python invoice','eslog invoice', 'read e-slog invoice', 'e-slog','e-racuni e-eslog'],
    install_requires=[
        'lxml>=4.4.1',
        'pandas>=1.3.0'
    ]
)
