from build.transform import msbuild 
from build.transform import pybuild
from build.transform import nmake
from build.transform import toolchain
from build.transform.toolchain import ToolchainExtender

from build.feature import Feature
from build.tools import msvc, clang
from build.features import FeatureError
from build.features.msbuild import *
from build.features.pybuild import *  
from build.transform.visual_studio import VS12VCVars, VS14VCVars
from build.requirement import HostRequirement


_win_x86_vs12_env = VS12VCVars(host="x64", target="x86")
_win_x64_vs12_env = VS12VCVars(host="x64", target="x64")
_win_x86_vs14_env = VS14VCVars(host="x64", target="x86")
_win_x64_vs14_env = VS14VCVars(host="x64", target="x64")



win_cs_vs12_msbuild = msbuild.CSToolchain("windows-msbuild-vs12", vcvars=_win_x86_vs12_env)
win_cs_vs12_msbuild.add_tool('.cs', msvc.MSBuildCSCompiler())
win_cs_vs12_msbuild.add_tool('.png', msvc.MSBuildImage())
win_cs_vs12_msbuild.add_tool('.jpg', msvc.MSBuildImage())
win_cs_vs12_msbuild.add_tool('.bmp', msvc.MSBuildImage())
win_cs_vs12_msbuild.add_tool('.gif', msvc.MSBuildImage())
win_cs_vs12_msbuild.add_tool('.content', msvc.MSBuildContent())
win_cs_vs12_msbuild.add_requirement(HostRequirement.WINDOWS)

win_cs_vs14_msbuild = msbuild.CSToolchain("windows-msbuild-vs14", vcvars=_win_x86_vs14_env)
win_cs_vs14_msbuild.add_tool('.cs', msvc.MSBuildCSCompiler())
win_cs_vs14_msbuild.add_tool('.png', msvc.MSBuildImage())
win_cs_vs14_msbuild.add_tool('.jpg', msvc.MSBuildImage())
win_cs_vs14_msbuild.add_tool('.bmp', msvc.MSBuildImage())
win_cs_vs14_msbuild.add_tool('.gif', msvc.MSBuildImage())
win_cs_vs14_msbuild.add_tool('.content', msvc.MSBuildContent())
win_cs_vs14_msbuild.add_requirement(HostRequirement.WINDOWS)



win_x86_vs12_msbuild = msbuild.CXXToolchain("windows-x86-msbuild-vs12", platform="Win32", vcvars=_win_x86_vs12_env)
win_x86_vs12_msbuild.add_tool('.c', msvc.MSBuildCXXCompiler(cxx=False))
win_x86_vs12_msbuild.add_tool('.cc', msvc.MSBuildCXXCompiler(cxx=True))
win_x86_vs12_msbuild.add_tool('.cpp', msvc.MSBuildCXXCompiler(cxx=True))
win_x86_vs12_msbuild.add_tool('.cxx', msvc.MSBuildCXXCompiler(cxx=True))
win_x86_vs12_msbuild.add_feature(MSBuildPlatformToolset(toolset='v120'))
win_x86_vs12_msbuild.add_requirement(HostRequirement.WINDOWS)
win_x86_vs12_msbuild.add_feature(FeatureError('c++11 is not supported by vs12'), 'language-c++11')
win_x86_vs12_msbuild.add_feature(FeatureError('c++14 is not supported by vs12'), 'language-c++14')
win_x86_vs12_msbuild.add_feature(FeatureError('c++17 is not supported by vs12'), 'language-c++17')
win_x86_vs12_msbuild.add_feature(MSBuildOptimize(), 'optimize')

win_x64_vs12_msbuild = msbuild.CXXToolchain("windows-x64-msbuild-vs12", vcvars=_win_x64_vs12_env)
win_x64_vs12_msbuild.add_tool('.c', msvc.MSBuildCXXCompiler(cxx=False))
win_x64_vs12_msbuild.add_tool('.cc', msvc.MSBuildCXXCompiler(cxx=True))
win_x64_vs12_msbuild.add_tool('.cpp', msvc.MSBuildCXXCompiler(cxx=True))
win_x64_vs12_msbuild.add_tool('.cxx', msvc.MSBuildCXXCompiler(cxx=True))
win_x64_vs12_msbuild.add_feature(MSBuildPlatformToolset(toolset='v120'))
win_x64_vs12_msbuild.add_requirement(HostRequirement.WINDOWS)
win_x64_vs12_msbuild.add_feature(FeatureError('c++11 is not supported by vs12'), 'language-c++11')
win_x64_vs12_msbuild.add_feature(FeatureError('c++14 is not supported by vs12'), 'language-c++14')
win_x64_vs12_msbuild.add_feature(FeatureError('c++17 is not supported by vs12'), 'language-c++17')
win_x64_vs12_msbuild.add_feature(MSBuildOptimize(), 'optimize')



win_x86_vs14_msbuild = msbuild.CXXToolchain("windows-x86-msbuild-vs14", platform="Win32", vcvars=_win_x86_vs14_env)
win_x86_vs14_msbuild.add_tool('.c', msvc.MSBuildCXXCompiler(cxx=False))
win_x86_vs14_msbuild.add_tool('.cc', msvc.MSBuildCXXCompiler(cxx=True))
win_x86_vs14_msbuild.add_tool('.cpp', msvc.MSBuildCXXCompiler(cxx=True))
win_x86_vs14_msbuild.add_tool('.cxx', msvc.MSBuildCXXCompiler(cxx=True))
win_x86_vs14_msbuild.add_feature(MSBuildPlatformToolset(toolset='v140'))
win_x86_vs14_msbuild.add_requirement(HostRequirement.WINDOWS)
win_x86_vs14_msbuild.add_feature(FeatureError('c++14 is not supported by vs14'), 'language-c++14')
win_x86_vs14_msbuild.add_feature(FeatureError('c++17 is not supported by vs14'), 'language-c++17')
win_x86_vs14_msbuild.add_feature(MSBuildOptimize(), 'optimize')

win_x64_vs14_msbuild = msbuild.CXXToolchain("windows-x64-msbuild-vs14", vcvars=_win_x64_vs14_env)
win_x64_vs14_msbuild.add_tool('.c', msvc.MSBuildCXXCompiler(cxx=False))
win_x64_vs14_msbuild.add_tool('.cc', msvc.MSBuildCXXCompiler(cxx=True))
win_x64_vs14_msbuild.add_tool('.cpp', msvc.MSBuildCXXCompiler(cxx=True))
win_x64_vs14_msbuild.add_tool('.cxx', msvc.MSBuildCXXCompiler(cxx=True))
win_x64_vs14_msbuild.add_feature(MSBuildPlatformToolset(toolset='v140'))
win_x64_vs14_msbuild.add_requirement(HostRequirement.WINDOWS)
win_x64_vs14_msbuild.add_feature(FeatureError('c++14 is not supported by vs14'), 'language-c++14')
win_x64_vs14_msbuild.add_feature(FeatureError('c++17 is not supported by vs14'), 'language-c++17')
win_x64_vs14_msbuild.add_feature(MSBuildOptimize(), 'optimize')



pam_vs12 = pybuild.CXXToolchain("pam-vs12")
pam_vs12.add_requirement(HostRequirement.WINDOWS)
pam_vs12.add_feature(FeatureError('c++11 is not supported by vs12'), 'language-c++11')
pam_vs12.add_feature(FeatureError('c++14 is not supported by vs12'), 'language-c++14')
pam_vs12.add_feature(FeatureError('c++17 is not supported by vs12'), 'language-c++17')
pam_vs12.add_feature(PyBuildOptimize(PyBuildOptimize.MSVC), 'optimize')

win_x86_vs12 = ToolchainExtender("windows-x86-pam-vs12", pam_vs12)
win_x86_vs12.add_tool('.S', msvc.PyBuildCXXCompiler(cxx=False, env=_win_x86_vs12_env))
win_x86_vs12.add_tool('.c', msvc.PyBuildCXXCompiler(cxx=False, env=_win_x86_vs12_env))
win_x86_vs12.add_tool('.cc', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x86_vs12_env))
win_x86_vs12.add_tool('.cpp', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x86_vs12_env))
win_x86_vs12.add_tool('.cxx', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x86_vs12_env))
win_x86_vs12.archiver = msvc.PyBuildCXXArchiver(env=_win_x86_vs12_env)
win_x86_vs12.linker = msvc.PyBuildCXXLinker(env=_win_x86_vs12_env)

win_x64_vs12 = ToolchainExtender("windows-x64-pam-vs12", pam_vs12)
win_x64_vs12.add_tool('.S', msvc.PyBuildCXXCompiler(cxx=False, env=_win_x64_vs12_env))
win_x64_vs12.add_tool('.c', msvc.PyBuildCXXCompiler(cxx=False, env=_win_x64_vs12_env))
win_x64_vs12.add_tool('.cc', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x64_vs12_env))
win_x64_vs12.add_tool('.cpp', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x64_vs12_env))
win_x64_vs12.add_tool('.cxx', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x64_vs12_env))
win_x64_vs12.archiver = msvc.PyBuildCXXArchiver(env=_win_x64_vs12_env)
win_x64_vs12.linker = msvc.PyBuildCXXLinker(env=_win_x64_vs12_env)



pam_vs14 = pybuild.CXXToolchain("pam-vs14")
pam_vs14.add_requirement(HostRequirement.WINDOWS)
pam_vs14.add_feature(FeatureError('c++14 is not supported by vs12'), 'language-c++14')
pam_vs14.add_feature(FeatureError('c++17 is not supported by vs12'), 'language-c++17')
pam_vs14.add_feature(PyBuildOptimize(PyBuildOptimize.MSVC), 'optimize')

win_x86_vs14 = ToolchainExtender("windows-x86-pam-vs14", pam_vs14)
win_x86_vs14.add_tool('.S', msvc.PyBuildCXXCompiler(cxx=False, env=_win_x86_vs14_env))
win_x86_vs14.add_tool('.c', msvc.PyBuildCXXCompiler(cxx=False, env=_win_x86_vs14_env))
win_x86_vs14.add_tool('.cc', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x86_vs14_env))
win_x86_vs14.add_tool('.cpp', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x86_vs14_env))
win_x86_vs14.add_tool('.cxx', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x86_vs14_env))
win_x86_vs14.archiver = msvc.PyBuildCXXArchiver(env=_win_x86_vs14_env)
win_x86_vs14.linker = msvc.PyBuildCXXLinker(env=_win_x86_vs14_env)

win_x64_vs14 = ToolchainExtender("windows-x64-pam-vs14", pam_vs14)
win_x64_vs14.add_tool('.S', msvc.PyBuildCXXCompiler(cxx=False, env=_win_x64_vs14_env))
win_x64_vs14.add_tool('.c', msvc.PyBuildCXXCompiler(cxx=False, env=_win_x64_vs14_env))
win_x64_vs14.add_tool('.cc', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x64_vs14_env))
win_x64_vs14.add_tool('.cpp', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x64_vs14_env))
win_x64_vs14.add_tool('.cxx', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x64_vs14_env))
win_x64_vs14.archiver = msvc.PyBuildCXXArchiver(env=_win_x64_vs14_env)
win_x64_vs14.linker = msvc.PyBuildCXXLinker(env=_win_x64_vs14_env)



win_x86_vs14_nmake = nmake.CXXToolchain("windows-x86-nmake-vs14", _win_x86_vs14_env)
win_x86_vs14_nmake.add_tool('.S', msvc.PyBuildCXXCompiler(cxx=False, env=_win_x86_vs14_env))
win_x86_vs14_nmake.add_tool('.c', msvc.PyBuildCXXCompiler(cxx=False, env=_win_x86_vs14_env))
win_x86_vs14_nmake.add_tool('.cc', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x86_vs14_env))
win_x86_vs14_nmake.add_tool('.cpp', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x86_vs14_env))
win_x86_vs14_nmake.add_tool('.cxx', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x86_vs14_env))
win_x86_vs14_nmake.archiver = msvc.PyBuildCXXArchiver(env=_win_x86_vs14_env)
win_x86_vs14_nmake.linker = msvc.PyBuildCXXLinker(env=_win_x86_vs14_env)
win_x86_vs14_nmake.add_requirement(HostRequirement.WINDOWS)
win_x86_vs14_nmake.add_feature(FeatureError('c++14 is not supported by vs14'), 'language-c++14')
win_x86_vs14_nmake.add_feature(FeatureError('c++17 is not supported by vs14'), 'language-c++17')
win_x86_vs14_nmake.add_feature(PyBuildOptimize(PyBuildOptimize.MSVC), 'optimize')

win_x64_vs14_nmake = nmake.CXXToolchain("windows-x64-nmake-vs14", _win_x64_vs14_env)
win_x64_vs14_nmake.add_tool('.S', msvc.PyBuildCXXCompiler(cxx=False, env=_win_x64_vs14_env))
win_x64_vs14_nmake.add_tool('.c', msvc.PyBuildCXXCompiler(cxx=False, env=_win_x64_vs14_env))
win_x64_vs14_nmake.add_tool('.cc', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x64_vs14_env))
win_x64_vs14_nmake.add_tool('.cpp', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x64_vs14_env))
win_x64_vs14_nmake.add_tool('.cxx', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x64_vs14_env))
win_x64_vs14_nmake.archiver = msvc.PyBuildCXXArchiver(env=_win_x64_vs14_env)
win_x64_vs14_nmake.linker = msvc.PyBuildCXXLinker(env=_win_x64_vs14_env)
win_x64_vs14_nmake.add_requirement(HostRequirement.WINDOWS)
win_x64_vs14_nmake.add_feature(FeatureError('c++14 is not supported by vs14'), 'language-c++14')
win_x64_vs14_nmake.add_feature(FeatureError('c++17 is not supported by vs14'), 'language-c++17')
win_x64_vs14_nmake.add_feature(PyBuildOptimize(PyBuildOptimize.MSVC), 'optimize')


vs14_clang = pybuild.CXXToolchain("pam-clang-vs14")
vs14_clang.add_tool('.S', clang.PyBuildCXXCompiler(cxx=False))
vs14_clang.add_tool('.c', clang.PyBuildCXXCompiler(cxx=False))
vs14_clang.add_tool('.cc', clang.PyBuildCXXCompiler(cxx=True))
vs14_clang.add_tool('.cpp', clang.PyBuildCXXCompiler(cxx=True))
vs14_clang.add_tool('.cxx', clang.PyBuildCXXCompiler(cxx=True))
vs14_clang.add_requirement(HostRequirement.WINDOWS)
vs14_clang.add_feature(PyBuildCustomCFlag('-m32'))
vs14_clang.add_feature(PyBuildCustomCXXFlag('-m32'))
vs14_clang.add_feature(PyBuildCustomLinkerFlag('-m32'))
vs14_clang.add_feature(PyBuildCustomCXXFlag('-std=c89'), 'language-c89')
vs14_clang.add_feature(PyBuildCustomCXXFlag('-std=c99'), 'language-c99')
vs14_clang.add_feature(PyBuildCustomCXXFlag('-std=c11'), 'language-c11')
vs14_clang.add_feature(PyBuildCustomCXXFlag('-std=c++11'), 'language-c++11')
vs14_clang.add_feature(PyBuildCustomCXXFlag('-std=c++14'), 'language-c++14')
vs14_clang.add_feature(PyBuildCustomCXXFlag('-std=c++17'), 'language-c++17')
vs14_clang.add_feature(PyBuildOptimize(PyBuildOptimize.GNU), 'optimize')

win_x86_vs14_clang = ToolchainExtender("windows-x86-pam-clang-vs14", vs14_clang)
win_x86_vs14_clang.archiver = msvc.PyBuildCXXArchiver(env=_win_x86_vs14_env)
win_x86_vs14_clang.linker = msvc.PyBuildCXXLinker(env=_win_x86_vs14_env)

win_x64_vs14_clang = ToolchainExtender("windows-x64-pam-clang-vs14", vs14_clang)
win_x64_vs14_clang.archiver = msvc.PyBuildCXXArchiver(env=_win_x64_vs14_env)
win_x64_vs14_clang.linker = msvc.PyBuildCXXLinker(env=_win_x64_vs14_env)
