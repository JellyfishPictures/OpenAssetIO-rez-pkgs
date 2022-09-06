"""Rezbuild for trompeloeil on Windows"""
import os
import sys
import subprocess
import urllib.request
import zipfile


def build(source_path, build_path, install_path, targets):
    cmake_generator = "Visual Studio 16 2019"
    cmake_target_platform = "v142"
    version = os.environ["REZ_BUILD_PROJECT_VERSION"]

    # Download the source
    filename = 'v{0}.zip'.format(version)
    archive = os.path.join(build_path, filename)
    url = "https://github.com/rollbear/trompeloeil/archive/refs/tags/" + filename
    print("Downloading file: %s" % url)
    urllib.request.urlretrieve(url, archive)

    # Unzip the source
    print("Unzipping to: %s" % build_path)
    # with tarfile.TarFile.open(archive, mode='r:gz') as tar:
    #     tar.extractall(build_path)
    with zipfile.ZipFile(archive, 'r') as zip_ref:
        zip_ref.extractall(build_path)

    folder_name = "trompeloeil-{}".format(version)
    source_root = os.path.join(build_path, folder_name)
    print("Building source root: %s" % source_root)

    # Run cmake
    cmdline = ["cmake",
               "-G", cmake_generator,
               "-T", cmake_target_platform,
               "-DCMAKE_INSTALL_PREFIX=" + install_path,
               source_root]
    subprocess.call(cmdline, cwd=build_path)

    # Build binaries
    subprocess.call(["cmake",
                     "--build", ".",
                     "--config", "Release"], cwd=build_path)

    if "install" not in (targets or []):
        return

    # Trigger install file
    subprocess.call(["cmake",
                     "-P", "cmake_install.cmake",
                     build_path])


if __name__ == '__main__':
    build(source_path=os.environ['REZ_BUILD_SOURCE_PATH'],
          build_path=os.environ['REZ_BUILD_PATH'],
          install_path=os.environ['REZ_BUILD_INSTALL_PATH'],
          targets=sys.argv[1:])
