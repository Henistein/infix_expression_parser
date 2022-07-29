from distutils.core import setup, Extension

setup(
  name="expressions",
  ext_modules=[Extension("expressions", ["bind.c", "expressions.c"])]
)