import os, sys, subprocess, hashlib, tarfile, shutil, glob, progressbar, urllib.request, shutil, requests, argparse
from pathlib import Path
from subprocess import run
from multiprocessing import cpu_count
from ctypes import *
from glob import glob
from io import StringIO

from urllib.parse import urlparse
from packaging.version import Version
from .configuration import Configuration
from .configuration import BuildType




### Green color message
def info(msg):
    print("\033[32m[INFO] " + msg + "\033[00m", flush=True)

### Red color message + abort
def fatal(msg):
    print("\033[31m[FATAL] " + msg + "\033[00m", flush=True)
    sys.exit(2)

### Equivalent to mkdir -p
def mkdir(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def cd(path):
    os.chdir(os.path.join(os.getcwd(), path))




class Dependency:
    def __init__(self):
        self.dependencies = [Dependency]
    def download(self):
        pass
    def remove(self):
        pass
    def make(self, build_type: BuildType):
        pass
    def clean(self, build_type: BuildType):
        pass
    def configure(self, build_type: BuildType):
        pass
    def build(self, build_type: BuildType):
        pass
    def install(self, build_type: BuildType):
        pass
    pass


class CppCMakeDependency(Dependency):
    def __init__(self, git_url: str):
        pwd = str(os.getcwd())
        self.tp = os.path.join(pwd, Configuration.THIRDPARTY_DIR_NAME)
        parsed_uri = urlparse(git_url)
        self.name = Path(os.path.basename(parsed_uri.path)).stem
        self.path = os.path.join(self.tp, self.name)
        self.git_url = git_url
        self.version = Version("0.0.0")
        self._configure_temporary_pathes()

    def set_version(self, version_str: str):
        self.version = Version(version_str)
        return self
    
    def download(self):
        if not os.path.exists(self.path) or len(os.listdir(self.path)) == 0:
            info("Clone " + self.name + " into " + self.path)
            if self.version == Version("0.0.0"):
                run(["git", "clone", self.git_url, self.path])
            else:
                run(["git", "clone", "--recursive", "-b", f"v{self.version.base_version}", self.git_url, self.path])
                
    def remove(self):
        if os.path.exists(self.path) and os.path.isdir(self.path):
            shutil.rmtree(self.path)
            #os.rmdir(self.path)

    def make(self, build_type: BuildType):
        self.configure(build_type)
        self.build(build_type)
        self.install(build_type)

    def build(self, build_type: BuildType):
        build_path = self._get_build_dir_path(build_type)
        if not os.path.exists(build_path):
            raise FileNotFoundError("Build directory not found: " + build_path)
        os.chdir(build_path)
        run(["make", "-j" + str(Configuration.NPROC)], check = True)
        os.chdir(self.tp)


    def configure(self, build_type: BuildType):
        build_path = self._get_build_dir_path(build_type)
        install_path = self._get_install_dir_path(build_type)
        if os.path.exists(build_path):
            os.remove(build_path)
        mkdir(build_path)
        os.chdir(build_path)
        run(["cmake", "-DCMAKE_INSTALL_PREFIX=" + install_path, "-DCMAKE_BUILD_TYPE=" + build_type.to_str(),".."], check = True)
        os.chdir(self.tp)


    def install(self, build_type: BuildType):
        build_path = self._get_build_dir_path(build_type)
        if not os.path.exists(build_path):
            raise FileNotFoundError("Build directory not found: " + build_path)
        os.chdir(build_path)
        run(["make", "install"], check = True)
        os.chdir(self.tp)


    def _configure_temporary_pathes(self):
        self.build_path = os.path.join(self.path, Configuration.BUILD_DIR_NAME)
        self.install_path = os.path.join(self.path, Configuration.INSTALL_DIR_NAME)

    def _get_build_dir_path(self, build_type: BuildType):
        return self.build_path + build_type.to_path()

    def _get_install_dir_path(self, build_type: BuildType):
        return self.install_path + build_type.to_path()

