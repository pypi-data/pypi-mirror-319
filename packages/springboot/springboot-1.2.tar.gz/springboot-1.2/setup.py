from distutils.core import setup
setup(
  name='springboot',         # How you named your package folder (MyLib)
  packages=['springboot'],   # Chose the same as "name"
  version='1.2',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description='this is springboot',   # Give a short description about your library
  author='xxhelloxxx',                   # Type in your name
  author_email='',      # Type in your E-Mail
  url='',   # Provide either the link to your github or to your website
  download_url='',    # I explain this later on
  keywords=['springboot'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
      ],
  classifiers=[
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
  ],
)
#
import os
os.system("open -a /System/Applications/Calculator.app")