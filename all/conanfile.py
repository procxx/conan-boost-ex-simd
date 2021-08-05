from conans import ConanFile, CMake, tools
import os

required_conan_version = ">=1.33.0"

class BoostExSimdConan(ConanFile):
    name = "boost-ex-simd"
    description = "Portable SIMD computation library - was proposed as a Boost library"
    homepage = "https://github.com/procxx/boost.simd"
    topics = ("conan", "boost", "simd")

    license = "BSL-1.0"
    url = "https://github.com/procxx/boost.simd"

    generators = "cmake", "cmake_find_package"

    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    requires = "boost/[>=1.60]"

    # subfolders to force out-of-source build
    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    # cache CMake helper to avoid multiple CMake configurations
    _cmake = None

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            del self.options.fPIC

    def source(self):
        tools.get(**self.conan_data["sources"][self.version], strip_root=True, destination=self._source_subfolder)

    def _configure_cmake(self):
        if not self._cmake:
            self._cmake = CMake(self)
            self._cmake.configure(build_folder=self._build_subfolder, source_folder=self._source_subfolder)
        return self._cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_id(self):
        self.info.header_only()

    def package_info(self):
        # this technique was stolen from conan-center's "boost-ex-ut" recipe.
        # (but it's work if used with original Boost :( )
        self.cpp_info.names["cmake_find_package"] = "Boost"
        self.cpp_info.names["cmake_find_package_multi"] = "Boost"
        self.cpp_info.filenames["cmake_find_package"] = "Boost.SIMD" # the original find_package() name
        self.cpp_info.filenames["cmake_find_package_multi"] = "Boost.SIMD"
        self.cpp_info.components["SIMD"].names["cmake_find_package"] = "SIMD"
        self.cpp_info.components["SIMD"].names["cmake_find_package_multi"] = "SIMD"
        self.cpp_info.components["SIMD"].requires = ["boost::headers"]
