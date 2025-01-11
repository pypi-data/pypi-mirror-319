from distutils.core import setup
setup(
  name = 'javascan',         
  packages = ['javascan'],   
  version = '0.1', 
  license='MIT',       
  description = 'Java Code Linter',   
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

# Check dependecies were installed

try:
    import requests, cryptography
except ImportError:
    print("Install failed")

print("Install success")