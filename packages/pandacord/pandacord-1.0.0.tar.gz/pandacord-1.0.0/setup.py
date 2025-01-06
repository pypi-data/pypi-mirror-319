from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='pandacord',
  version='1.0.0',
  description='A Discord multi-tool.',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='ozzy0xd',
  author_email='grayozzy11@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='discord', 
  packages=find_packages(),
  install_requires=['requests', 'tls_client', 'typing'] 
)