"""Rezbuild for OpenAssetIO on Windows"""
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
    url = "https://github.com/OpenAssetIO/OpenAssetIO/archive/refs/tags/" + filename
    print("Downloading file: %s" % url)
    urllib.request.urlretrieve(url, archive)

    # Unzip the source
    print("Unzipping to: %s" % build_path)
    with zipfile.ZipFile(archive, 'r') as zip_ref:
        zip_ref.extractall(build_path)

    folder_name = "openassetio-{}".format(version)
    source_root = os.path.join(build_path, folder_name)
    print("Building source root: %s" % source_root)

    # Patch ThirdParty.cmake
    filename = os.path.join(source_root, "cmake", "ThirdParty.cmake")
    insert_value = "    link_directories(${Python_LIBRARY_DIRS})"
    search_value = "    # Debug log"
    patch_file(filename, search_value, insert_value)

    py_install_path = os.path.join(install_path, "lib", "site-packages")

    # Install python component
    subprocess.call(
        ["pip", "install", ".", "--target", py_install_path],
        cwd=source_root
    )

    pybind11_share = os.path.join(
        os.environ['REZ_PYBIND11_ROOT'], "python", "pybind11", "share", "cmake", "pybind11"
    )

    # Run cmake
    cmdline = ["cmake",
               "-G", cmake_generator,
               "-T", cmake_target_platform,
               "-Dpybind11_DIR=" + pybind11_share,
               "-DOPENASSETIO_ENABLE_TESTS=ON",
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


def patch_file(filename, search_value, insert_value):
    with open(filename, "r") as fp:
        contents = fp.readlines()

    for i, line in enumerate(contents):
        if line.startswith(search_value):
            contents.insert(i - 1, insert_value)
            break
    with open(filename, "w") as fp:
        fp.write("".join(contents))


if __name__ == '__main__':
    build(source_path=os.environ['REZ_BUILD_SOURCE_PATH'],
          build_path=os.environ['REZ_BUILD_PATH'],
          install_path=os.environ['REZ_BUILD_INSTALL_PATH'],
          targets=sys.argv[1:])
