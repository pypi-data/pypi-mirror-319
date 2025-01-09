from setuptools import setup, find_packages

# Try to open the README.md file, if it exists
try:
    with open('README.md', 'r', encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "Viyu Xmpp: A package for managing XMPP server events."

setup(
    name='viyu_xmpp',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'slixmpp>=1.7.0',
        'cryptography>=3.4.8'
    ],
    author='TRIYOM SOFTWARES PVT LTD',
    author_email='admin@triyom.in',
    description='A package to manage XMPP server events and provide custom handlers for GET and POST stanzas.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/triyom-dev/viyu-xmpp-app',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Communications',
        'Topic :: Internet',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'viyu_xmpp_server = viyu_xmpp.server:main',
        ],
    },
    project_urls={
        'Source': 'https://github.com/triyom-dev/viyu-xmpp-app',
        'Bug Tracker': 'https://github.com/triyom-dev/viyu-xmpp-app/issues',
    },
)
