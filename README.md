# OpenAssetIO-rez-pkgs
Rez packages for OpenAssetIO and it's dependencies

## Install Dependencies

1. Install pybind11 with rez-pip
    
    ``rez-pip --install pybind11``
   
2. Install catch2
    ````
   cd catch2
   rez-build -i
   ````

3. Install trompeloeil
    ````
   cd trompeloeil
   rez-build -i
   ````
   
## Install OpenAssetIO
Once the dependencies are installed run a rez-build for openassetio
````
cd openassetio
rez-build -i
````

## Test OpenAssetIO
The tests for openassetio must be run from the build directory.
````
cd openassetio/build/OpenAssetIO-1.0.0-alpha.3
rez-test openassetio
````
 