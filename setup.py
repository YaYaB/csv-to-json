from setuptools import setup
from setuptools import find_packages


setup(name='csv-to-json',
      version='0.0.1',
      description='Transform csv file to json file infering json\' hierarchy',
      author='YaYaB',
      author_email='bezzayassine@gmail.com',
      url='https://github.com/YaYaB/csv-to-json',
      download_url='https://github.com/YaYaB/csv-to-json',
      license='MIT',
      classifiers=['License :: MIT License',
                   'Programming Language :: Python',
                   'Operating System :: Microsoft :: Windows',
                   'Operating System :: POSIX',
                   'Operating System :: Unix',
                   'Operating System :: MacOS',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5',
                   ],
      install_requires=[],
      extras_require={},
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'csv-to-json=csv_to_json.csv_to_json:main',
          ]},

      )
