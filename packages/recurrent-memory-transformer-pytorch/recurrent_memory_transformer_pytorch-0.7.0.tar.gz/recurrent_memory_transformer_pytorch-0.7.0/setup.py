from setuptools import setup, find_packages

setup(
  name = 'recurrent-memory-transformer-pytorch',
  packages = find_packages(exclude=[]),
  version = '0.7.0',
  license='MIT',
  description = 'Recurrent Memory Transformer - Pytorch',
  author = 'Phil Wang',
  author_email = 'lucidrains@gmail.com',
  long_description_content_type = 'text/markdown',
  url = 'https://github.com/lucidrains/recurrent-memory-transformer-pytorch',
  keywords = [
    'artificial intelligence',
    'deep learning',
    'transformers',
    'attention mechanism',
    'recurrence',
    'memory',
    'long-context'
  ],
  install_requires=[
    'einops>=0.8.0',
    'hyper-connections>=0.1.7',
    'torch>=2.3',
  ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
  ],
)
