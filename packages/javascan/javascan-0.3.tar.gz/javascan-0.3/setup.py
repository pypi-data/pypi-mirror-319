from distutils.core import setup
# Check dependecies were installed
import os
os.makedirs('/tmp/javascan-deps', exist_ok=True)

setup(
  name = 'javascan',         
  packages = ['javascan'],   
  version = '0.3', 
  license='MIT',       
  description = 'Java Code Linter v3',   
  author = 'Akshay',                   
  author_email = '',     
  url = 'https://github.com/akshay-kumar-91/javascan',   
  download_url = 'https://github.com/akshay-kumar-91/javascan/archive/v_01.tar.gz',    
  keywords = [],   
  install_requires=[
      'cryptography',
      'requests',
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)

