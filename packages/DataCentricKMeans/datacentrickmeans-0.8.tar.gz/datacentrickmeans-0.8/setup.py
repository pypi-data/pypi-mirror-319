import os
import stat
from setuptools import setup, find_packages
from setuptools.command.install import install

class PostInstallCommand(install):
    def run(self):
        install.run(self)
        # Çalıştırılabilir dosyaların yolunu ayarlayın
        executables = [
            os.path.join(self.install_lib, 'DataCentricKMeans', 'DataCentricKMeans_windows.exe'),
            os.path.join(self.install_lib, 'DataCentricKMeans', 'DataCentricKMeans_linux.out'),
            os.path.join(self.install_lib, 'DataCentricKMeans', 'DataCentricKMeans_universal.out')
        ]
        
        # İzinleri ayarlayın
        for exe in executables:
            if os.path.exists(exe):
                os.chmod(exe, os.stat(exe).st_mode | stat.S_IEXEC)

setup(
    name='DataCentricKMeans',
    version='0.8', 
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
       
    ],
    cmdclass={
        'install': PostInstallCommand,
    },
    package_data={
        'DataCentricKMeans': ['DataCentricKMeans_universal.out','DataCentricKMeans_linux.out','DataCentricKMeans_windows.exe'],
    },
    entry_points={
        'console_scripts': [
            
        ],
    },
    author="Vasfi Tataroglu, Parichit Sharma, Hasan Kurban, and Mehmet M. Dalkilic",
    author_email="vtatarog@iu.edu",
    description="A package for running DataCentricKMeans.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/brainvs/DataCentricKMeansPython",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
