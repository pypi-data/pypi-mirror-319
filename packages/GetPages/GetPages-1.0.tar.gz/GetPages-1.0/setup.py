from distutils.core import  setup
import setuptools
packages = ['GetPages']# 唯一的包名，自己取名
setup(name='GetPages',
	version='1.0',
	author='jackson_tao',
    packages=packages,
    package_dir={'requests': 'requests'},)
