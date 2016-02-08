from os.path import join as pjoin
from distutils.core import setup
from distutils.command.install import install

class custom_install(install):
    def run(self):
        import os
        os.system("mkdir /opt/akane")
        os.system("cp -R . /opt/akane/")
        os.system("ln -s /opt/akane/akanectl /usr/bin/akanectl")
        os.system("ln -s /opt/akane/akane-di /usr/bin/akane-di")


setup(
    name='akanectl',
    version='1.0',
    cmdclass = {'install': custom_install}
    )