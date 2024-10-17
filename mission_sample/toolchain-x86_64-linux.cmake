# Specify the target system name and processor
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR x86_64)

set(USE_LINUX ON)
set(USE_POSIX ON)

# Specify the path to the cross-compilation tools
set(TOOLCHAIN_PATH /usr/bin)

# Specify the C and C++ compilers
set(CMAKE_C_COMPILER ${TOOLCHAIN_PATH}/gcc)
set(CMAKE_CXX_COMPILER ${TOOLCHAIN_PATH}/g++)

# Specify the path to the linker
set(CMAKE_LINKER ${TOOLCHAIN_PATH}/ld)

# Specify the path to the archiver
set(CMAKE_AR ${TOOLCHAIN_PATH}/ar)

# Specify the path to the ranlib
set(CMAKE_RANLIB ${TOOLCHAIN_PATH}/ranlib)