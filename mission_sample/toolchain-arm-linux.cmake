# Specify the target system name and processor
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR arm)

# Specify the path to the cross-compilation tools
set(TOOLCHAIN_PATH /usr)

# Specify the C and C++ compilers
set(CMAKE_C_COMPILER ${TOOLCHAIN_PATH}/bin/arm-linux-gnueabihf-gcc)
set(CMAKE_CXX_COMPILER ${TOOLCHAIN_PATH}/bin/arm-linux-gnueabihf-g++)

# Specify the path to the linker
set(CMAKE_LINKER ${TOOLCHAIN_PATH}/bin/arm-linux-gnueabihf-ld)

# Specify the path to the archiver
set(CMAKE_AR ${TOOLCHAIN_PATH}/bin/arm-linux-gnueabihf-ar)

# Specify the path to the ranlib
set(CMAKE_RANLIB ${TOOLCHAIN_PATH}/bin/arm-linux-gnueabihf-ranlib)