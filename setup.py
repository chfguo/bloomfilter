from distutils.core import setup

ext_files = ['bloomfilter.c']

kwargs = {}

from Cython.Distutils import build_ext
from Cython.Distutils import Extension
print('Building from Cython')
ext_files.append('bloom.pyx')
kwargs['cmdclass'] = {'build_ext': build_ext}


ext_modules = [Extension("BloomFilter",ext_files)]

setup(
    name = 'bloomfilter',
    version = '0.0.1',
    author = 'Guo chengfeng',
    author_email = 'chf_guo@163.com',
    license = 'MIT License',
    ext_modules = ext_modules,
    py_modules = ['bloomfilter'],
    classifiers = [
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: C',
        'Programming Language :: Cython',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
  **kwargs
)
