from conans import ConanFile, CMake, tools
import os


class FmilibraryConan(ConanFile):
    name = "Fmilibrary"
    description = "FMI Library (FMIL) is a software package written in C that enables integration of Functional Mock-up Units (FMUs) import in applications. This version of the package includes API changes that allow direct control over the instantiation of multiple FMU instances."
    version = "2.0.2-instantiation"
    license = "BSD"
    url = "https://github.com/jondo2010/conan-fmilibrary"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False],
               "doc":    [True, False]}
    default_options = "shared=True", "doc=True"
    generators = "cmake"

    def source(self):
        self.run("git clone https://github.com/jondo2010/FMILibrary.git")
        self.run("cd FMILibrary && git checkout johughes/instantiation_changes")
        tools.replace_in_file("FMILibrary/CMakeLists.txt", "project (FMILibrary)",'''project (FMILibrary)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        cmake_args = [
            "-DFMILIB_BUILD_STATIC_LIB={0}".format('OFF' if self.options.shared else 'ON'),
            "-DFMILIB_BUILD_SHARED_LIB={0}".format('ON' if self.options.shared else 'OFF'),
            "-DFMILIB_GENERATE_DOXYGEN_DOC={0}".format('ON' if self.options.doc else 'OFF'),
            "-DFMILIB_BUILD_TESTS=OFF",
            "-DFMILIB_GENERATE_BUILD_STAMP=OFF",
            "-DFMILIB_INSTALL_PREFIX=prefix",
        ]

        ### Conan's CMake class automatically adds this standard CMake flag,
        ### but it messes with FMILibs' custom handling, so get rid of it.
        del cmake.definitions['BUILD_SHARED_LIBS']

        self.run("cmake FMILibrary %s %s" % (cmake.command_line, " ".join(cmake_args)))
        if self.options.doc:
            self.run("cmake --build . --target doc")
        self.run("cmake --build . --target install %s" % cmake.build_config)

    def package(self):
        self.copy(pattern="*.h", dst="include", src="prefix/include", keep_path=True)

        self.copy("prefix/lib/*.dll", dst="bin", keep_path=False)
        self.copy("prefix/lib/*.so", dst="lib", keep_path=False)
        self.copy("prefix/lib/*.dylib", dst="lib", keep_path=False)
        self.copy("prefix/lib/*.a", dst="lib", keep_path=False)

        self.copy("prefix/doc/*", dst="doc", keep_path=True)

    def package_info(self):
        if self.options.shared:
            self.cpp_info.libs = ["fmilib_shared"]
        else:
            self.cpp_info.libs = ["fmilib"]

