from distutils.core import setup, Extension
setup(name='parsermodule', version='1.0', ext_modules=[Extension('parsermodule', ['parsermodule.c'])])
