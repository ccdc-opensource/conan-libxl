import os
from conans import ConanFile, CMake, tools


class LibXlConan(ConanFile):
    name = "libxl"
    description = "C++ Excel Library to read/write xls/xlsx files."
    homepage = "https://www.libxl.com/"
    topics = ("excel")
    license = "Proprietary"
    generators = "cmake"
    settings = "os", "compiler", "arch", "build_type"
    exports_sources = ["CMakeLists.txt"]
    options = {"shared": [True, False],
               "fPIC": [True, False],
               }
    default_options = {"shared": True,
                       "fPIC": True,
                       }

    _cmake = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        tools.get(**self.conan_data["sources"][self.version], headers={
            'X-JFrog-Art-Api': os.environ.get("ARTIFACTORY_API_KEY", None)
        })
        url = self.conan_data["sources"][self.version]["url"]
        archive_name = f'libxl-src-{self.version}'
        os.rename(archive_name, self._source_subfolder)

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        if self.options.shared:
            self._cmake.definitions["LIBXL_SHARED"] = 'TRUE'
        self._cmake.configure()
        return self._cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)