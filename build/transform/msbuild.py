from build import model
from build.transform import utils
from build.transform.toolchain import Toolchain
from build.transform.visual_studio import VS14VCVars
from build.feature import FeatureRegistry

from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element 
from xml.etree.ElementTree import ElementTree
from xml.dom import minidom

import os
from copy import deepcopy


class SubElement(Element):
    def __init__(self, tag=''):
        super(SubElement, self).__init__(tag)


class Attribute(object):
    def __init__(self, attribute, varname=None, child=False, values=None):
        self.attribute = attribute
        self.varname = varname if varname is not None else attribute.lower()
        self.child = child
        self.values = values
    
    def __call__(self, cls):
        def decorate(cls, attribute, varname, child, values):
            def _check_value(value, values):
                if values and value not in values:
                    raise ValueError('{} is not one of {}'.format(value, values))
            
            def attr_get(self):
                if attribute not in self.attrib:
                    return ''
                return self.get(attribute)

            def attr_set(self, value):
                if value is None:
                    try:
                        self.attrib.pop(attribute)
                    except:
                        pass
                    finally:
                        return
                _check_value(value, values)
                return self.set(attribute, value)
                
            def child_get(self):
                if not hasattr(self, '_'+varname):
                    return ''
                return getattr(self, '_'+varname).text        
    
            def child_set(self, value):
                _check_value(value, values)
                if not value: return
                if not hasattr(self, '_'+varname):
                    e = SubElement(attribute)
                    self.append(e)            
                    setattr(self, '_'+varname, e)
                getattr(self,'_'+varname).text = value
            
            if not child:
                setattr(cls, varname, property(attr_get, attr_set))
            else:
                setattr(cls, varname, property(child_get, child_set))
            return cls
        return decorate(cls, self.attribute, self.varname, self.child, self.values)


class Composition(object):
    def __init__(self, cls, name):
        self.cls = cls
        self.name = name if name is not None else attribute.lower()
    
    def __call__(self, cls):
        def decorate(cls, comp_cls, name):
            def create(self, *args, **kwargs):
                child = comp_cls(*args, **kwargs)
                self.append(child)
                return child
            setattr(cls, 'create_' + name, create)
            return cls
        return decorate(cls, self.cls, self.name)


@Attribute('Label')
class Group(SubElement):
    def __init__(self, tag='Group', label=None):
        super(Group, self).__init__(tag)
        self.label = label    


@Attribute('AppContainerApplication', child=True)
@Attribute('ApplicationType', child=True)
@Attribute('ApplicationTypeRevision', child=True)
@Attribute('CustomBuildAfterTargets', child=True)
@Attribute('CustomBuildBeforeTargets', child=True)
@Attribute('DefaultLanguage', child=True)
@Attribute('EnableDotNetNativeCompatibleProfile', child=True)
@Attribute('Keyword', child=True)
@Attribute('MinimumVisualStudioVersion', child=True)
@Attribute('Platform', child=True)
@Attribute('ProjectGUID', child=True)
@Attribute('ProjectName', child=True)
@Attribute('RootNamespace', child=True)
@Attribute('WindowsTargetPlatformMinVersion', child=True)
@Attribute('WindowsTargetPlatformVersion', child=True)
class PropertyGroup(Group):
    def __init__(self, label=None):
        super(PropertyGroup, self).__init__('PropertyGroup', label)


class ItemGroup(Group):
    def __init__(self, label=None):
        super(ItemGroup, self).__init__('ItemGroup', label)
    

@Attribute('Condition')
class ItemDefinitionGroup(Group):
    def __init__(self, label=None):
        super(ItemDefinitionGroup, self).__init__('ItemDefinitionGroup', label)


@Attribute('Include')
@Attribute('Configuration', child=True)
@Attribute('Platform', child=True)
class ProjectConfiguration(SubElement):
    def __init__(self, config, platform):
        super(ProjectConfiguration, self).__init__('ProjectConfiguration')
        self.configuration = config
        self.platform = platform
        self.include = "{}|{}".format(self.configuration, self.platform)
        
    @property
    def condition(self):
        return '\'$(Configuration)|$(Platform)\' == \'{}\''.format(self.include)


@Composition(ProjectConfiguration, 'projectconfiguration')
class ProjectConfigurationsItemGroup(ItemGroup):
    def __init__(self):
        super(ProjectConfigurationsItemGroup, self).__init__('ProjectConfigurations')


@Attribute('Condition')
@Attribute('ConfigurationType', varname='type', child=True, values=['Application', 'SharedLibrary', 'StaticLibrary'])
@Attribute('PlatformToolset', varname='toolset', child=True, values=['v110', 'v120', 'v110_xp', 'v120_xp', 'v140', 'v140_xp'])
@Attribute('CharacterSet', varname='charset', child=True, values=['MultiByte', None])
class ConfigurationPropertyGroup(PropertyGroup):
    def __init__(self, project_config):
        super(ConfigurationPropertyGroup, self).__init__('Configuration')
        self.condition = project_config.condition
    

@Attribute('Project')
class Import(SubElement):
    def __init__(self, project):
        super(Import, self).__init__('Import')
        self.project = project


@Composition(Import, 'import')
class ImportGroup(SubElement):
    def __init__(self):
        super(ImportGroup, self).__init__('ImportGroup')


@Attribute('AdditionalIncludeDirectories', child=True)
@Attribute('AdditionalOptions', child=True)
@Attribute('AdditionalUsingDirectories', child=True)
@Attribute('AlwaysAppend', child=True)
@Attribute('AssemblerListingLocation', child=True)
@Attribute('AssemblerOutput', values=['NoListing', 'AssemblyCode', 'AssemblyAndMachineCode', 'AssemblyAndSourceCode', 'All'], child=True)
@Attribute('BasicRuntimeChecks', values=['Default', 'StackFrameRuntimeCheck', 'UninitializedLocalUsageCheck', 'EnableFastChecks'], child=True)
@Attribute('BrowseInformation', values=['false', 'true'], child=True)
@Attribute('BrowseInformationFile', child=True)
@Attribute('BufferSecurityCheck', values=['false', 'true'], child=True)
@Attribute('BuildingInIDE', values=['false', 'true'], child=True)
@Attribute('CallingConvention', values=['Cdecl', 'FastCall', 'StdCall'], child=True)
@Attribute('CompileAs', values=['Default', 'CompileAsC', 'CompileAsCpp'], child=True)
@Attribute('CompileAsManaged', values=['false', 'true', 'Pure', 'Safe', 'OldSyntax'], child=True)
@Attribute('CompileAsWinRT', values=['false', 'true'], child=True)
@Attribute('CreateHotpatchableImage', values=['false', 'true'], child=True)
@Attribute('DebugInformationFormat', values=['OldStyle', 'ProgramDatabase', 'EditAndContinue'], child=True)
@Attribute('DisableLanguageExtensions', values=['false', 'true'], child=True)
@Attribute('DisableSpecificWarnings', child=True)
@Attribute('EnableEnhancedInstructionSet', values=['StreamingSIMDExtensions', 'StreamingSIMDExtensions2'], child=True)
@Attribute('EnableFiberSafeOptimizations', values=['false', 'true'], child=True)
@Attribute('EnablePREfast', values=['false', 'true'], child=True)
@Attribute('ErrorReporting', values=['None', 'Prompt', 'Queue', 'Send'], child=True)
@Attribute('ExceptionHandling', values=['false', 'Async', 'Sync', 'SyncCThrow'], child=True)
@Attribute('ExpandAttributedSource', values=['false', 'true'], child=True)
@Attribute('FavorSizeOrSpeed', values=['Neither', 'Size', 'Speed'], child=True)
@Attribute('FloatingPointExceptions', values=['false', 'true'], child=True)
@Attribute('FloatingPointModel', values=['Precise', 'Strict', 'Fast'], child=True)
@Attribute('ForceConformanceInForLoopScope', values=['false', 'true'], child=True)
@Attribute('ForcedIncludeFiles', child=True)
@Attribute('ForcedUsingFiles', child=True)
@Attribute('FunctionLevelLinking', values=['false', 'true'], child=True)
@Attribute('GenerateXMLDocumentationFiles', values=['false', 'true'], child=True)
@Attribute('IgnoreStandardIncludePath', values=['false', 'true'], child=True)
@Attribute('InlineFunctionExpansion', values=['Default', 'Disabled', 'OnlyExplicitInline', 'AnySuitable'], child=True)
@Attribute('IntrinsicFunctions', values=['false', 'true'], child=True)
@Attribute('MinimalRebuild', values=['false', 'true'], child=True)
@Attribute('MultiProcessorCompilation', values=['false', 'true'], child=True)
@Attribute('ObjectFileName', child=True)
@Attribute('ObjectFiles', child=True)
@Attribute('OmitDefaultLibName', values=['false', 'true'], child=True)
@Attribute('OmitFramePointers', values=['false', 'true'], child=True)
@Attribute('OpenMPSupport', values=['false', 'true'], child=True)
@Attribute('Optimization', values=['Disabled', 'MinSpace', 'MaxSpeed', 'Full'], child=True)
@Attribute('PrecompiledHeader', values=['NotUsing', 'Create', 'Use'], child=True)
@Attribute('PrecompiledHeaderFile', child=True)
@Attribute('PrecompiledHeaderOutputFile', child=True)
@Attribute('PreprocessKeepComments', values=['false', 'true'], child=True)
@Attribute('PreprocessorDefinitions', child=True)
@Attribute('PreprocessOutput', child=True)
@Attribute('PreprocessOutputPath', child=True)
@Attribute('PreprocessSuppressLineNumbers', values=['false', 'true'], child=True)
@Attribute('PreprocessToFile', values=['false', 'true'], child=True)
@Attribute('ProcessorNumber', child=True)
@Attribute('ProgramDataBaseFileName', child=True)
@Attribute('RuntimeLibrary', values=['MultiThreaded', 'MultiThreadedDebug', 'MultiThreadedDLL', 'MultiThreadedDebugDLL'], child=True)
@Attribute('RuntimeTypeInfo', values=['false', 'true'], child=True)
@Attribute('ShowIncludes', values=['false', 'true'], child=True)
@Attribute('SmallerTypeCheck', values=['false', 'true'], child=True)
@Attribute('Sources', child=True)
@Attribute('StringPooling', values=['false', 'true'], child=True)
@Attribute('StructMemberAlignment', values=['Default', '1Byte', '2Bytes', '4Bytes', '8Bytes', '16Bytes'], child=True)
@Attribute('SuppressStartupBanner', values=['false', 'true'], child=True)
@Attribute('TrackerLogDirectory', child=True)
@Attribute('TreatSpecificWarningsAsErrors', child=True)
@Attribute('TreatWarningAsError', child=True)
@Attribute('TreatWChar_tAsBuiltInType', values=['false', 'true'], child=True)
@Attribute('UndefinePreprocessorDefinitions', child=True)
@Attribute('UseFullPaths', values=['false', 'true'], child=True)
@Attribute('UseUnicodeForAssemblerListing', values=['false', 'true'], child=True)
@Attribute('WarningLevel', values=['TurnOffAllWarnings', 'Level1', 'Level2', 'Level3', 'Level4', 'EnableAllWarnings'], child=True)
@Attribute('WholeProgramOptimization', values=['false', 'true'], child=True)
@Attribute('XMLDocumentationFileName', child=True)
@Attribute('MinimalRebuildFromTracking', values=['false', 'true'], child=True)
@Attribute('TLogReadFiles', child=True)
@Attribute('TLogWriteFiles', child=True)
@Attribute('TrackFileAccess', values=['false', 'true'], child=True)
@Attribute('Include')
class ClCompile(SubElement):
    def __init__(self, include=None):
        super(ClCompile, self).__init__('ClCompile')
        self.include = include


@Attribute('AdditionalDependencies', child=True)
@Attribute('AdditionalLibraryDirectories', child=True)
@Attribute('AdditionalOptions', child=True)
@Attribute('DisplayLibrary', child=True)
@Attribute('ErrorReporting', values=['NoErrorReport', 'PromptImmediately', 'QueueForNextLogin', 'SendErrorReport'], child=True)
@Attribute('ExportNamedFunctions', child=True)
@Attribute('ForceSymbolReferences', child=True)
@Attribute('IgnoreAllDefaultLibraries', values=['false', 'true'], child=True)
@Attribute('IgnoreSpecificDefaultLibraries', child=True)
@Attribute('LinkLibraryDependencies', values=['false', 'true'], child=True)
@Attribute('LinkTimeCodeGeneration', values=['false', 'true'], child=True)
@Attribute('MinimumRequiredVersion', child=True)
@Attribute('ModuleDefinitionFile', child=True)
@Attribute('Name', child=True)
@Attribute('OutputFile', child=True)
@Attribute('RemoveObjects', child=True)
@Attribute('Sources', child=True)
@Attribute('SubSystem', values=['Console', 'Windows', 'Native', 'EFI Application', 'EFI Boot Service Driver', 'EFI ROM', 'EFI Runtime', 'WindowsCE', 'POSIX'], child=True)
@Attribute('SuppressStartupBanner', values=['false', 'true'], child=True)
@Attribute('TargetMachine', values=['MachineARM', 'MachineEBC', 'MachineIA64', 'MachineMIPS', 'MachineMIPS16', 'MachineMIPSFPU', 'MachineMIPSFPU16', 'MachineSH4', 'MachineTHUMB', 'MachineX64', 'MachineX86'], child=True)
@Attribute('TrackerLogDirectory', child=True)
@Attribute('TreatLibWarningAsErrors', values=['false', 'true'], child=True)
@Attribute('UseUnicodeResponseFiles', values=['false', 'true'], child=True)
@Attribute('Verbose', values=['false', 'true'], child=True)
class Lib(SubElement):
    def __init__(self, include=None):
        super(Lib, self).__init__('Lib')
        self.include = include


@Attribute('AdditionalDependencies', child=True)
@Attribute('AdditionalLibraryDirectories', child=True)
@Attribute('AdditionalManifestDependencies', child=True)
@Attribute('AdditionalOptions', child=True)
@Attribute('AddModuleNamesToAssembly', child=True)
@Attribute('AllowIsolation', values=['false', 'true'], child=True)
@Attribute('AssemblyDebug', values=['false', 'true'], child=True)
@Attribute('AssemblyLinkResource', child=True)
@Attribute('AttributeFileTracking', values=['false', 'true'], child=True)
@Attribute('BaseAddress', child=True)
@Attribute('BuildingInIDE', values=['false', 'true'], child=True)
@Attribute('CLRImageType', values=['Default', 'ForceIJWImage', 'ForcePureILImage', 'ForceSafeILImage'], child=True)
@Attribute('CLRSupportLastError', values=['Enabled', 'Disabled', 'SystemDlls'], child=True)
@Attribute('CLRThreadAttribute', values=['DefaultThreadingAttribute', 'MTAThreadingAttribute', 'STAThreadingAttribute'], child=True)
@Attribute('CLRUnmanagedCodeCheck', values=['false', 'true'], child=True)
@Attribute('CreateHotPatchableImage', values=['Enabled', 'X86Image', 'X64Image', 'ItaniumImage'], child=True)
@Attribute('DataExecutionPrevention', values=['false', 'true'], child=True)
@Attribute('DelayLoadDLLs', child=True)
@Attribute('DelaySign', values=['false', 'true'], child=True)
@Attribute('Driver', values=['NotSet', 'Driver', 'UpOnly', 'WDM'], child=True)
@Attribute('EmbedManagedResourceFile', child=True)
@Attribute('EnableCOMDATFolding', values=['false', 'true'], child=True)
@Attribute('EnableUAC', values=['false', 'true'], child=True)
@Attribute('EntryPointSymbol', child=True)
@Attribute('FixedBaseAddress', values=['false', 'true'], child=True)
@Attribute('ForceFileOutput', values=['Enabled', 'MultiplyDefinedSymbolOnly', 'UndefinedSymbolOnly'], child=True)
@Attribute('ForceSymbolReferences', child=True)
@Attribute('FunctionOrder', child=True)
@Attribute('GenerateDebugInformation', values=['false', 'true'], child=True)
@Attribute('GenerateManifest', values=['false', 'true'], child=True)
@Attribute('GenerateMapFile', values=['false', 'true'], child=True)
@Attribute('HeapCommitSize', child=True)
@Attribute('HeapReserveSize', child=True)
@Attribute('IgnoreAllDefaultLibraries', values=['false', 'true'], child=True)
@Attribute('IgnoreEmbeddedIDL', values=['false', 'true'], child=True)
@Attribute('IgnoreImportLibrary', values=['false', 'true'], child=True)
@Attribute('IgnoreSpecificDefaultLibraries', child=True)
@Attribute('ImageHasSafeExceptionHandlers', values=['false', 'true'], child=True)
@Attribute('ImportLibrary', child=True)
@Attribute('KeyContainer', child=True)
@Attribute('KeyFile', child=True)
@Attribute('LargeAddressAware', values=['false', 'true'], child=True)
@Attribute('LinkDLL', values=['false', 'true'], child=True)
@Attribute('LinkErrorReporting', values=['NoErrorReport', 'PromptImmediately', 'QueueForNextLogin', 'SendErrorReport'], child=True)
@Attribute('LinkIncremental', values=['false', 'true'], child=True)
@Attribute('LinkLibraryDependencies', values=['false', 'true'], child=True)
@Attribute('LinkStatus', values=['false', 'true'], child=True)
@Attribute('LinkTimeCodeGeneration', values=['false', 'true'], child=True)
@Attribute('ManifestFile', child=True)
@Attribute('MapExports', values=['false', 'true'], child=True)
@Attribute('MapFileName', child=True)
@Attribute('MergedIDLBaseFileName', child=True)
@Attribute('MergeSections', child=True)
@Attribute('MidlCommandFile', child=True)
@Attribute('MinimumRequiredVersion', child=True)
@Attribute('ModuleDefinitionFile', child=True)
@Attribute('MSDOSStubFileName', child=True)
@Attribute('NoEntryPoint', values=['false', 'true'], child=True)
@Attribute('ObjectFiles', child=True)
@Attribute('OptimizeReferences', values=['false', 'true'], child=True)
@Attribute('OutputFile', child=True)
@Attribute('PerUserRedirection', values=['false', 'true'], child=True)
@Attribute('PreprocessOutput', child=True)
@Attribute('PreventDllBinding', values=['false', 'true'], child=True)
@Attribute('Profile', values=['false', 'true'], child=True)
@Attribute('ProfileGuidedDatabase', child=True)
@Attribute('ProgramDatabaseFile', child=True)
@Attribute('RandomizedBaseAddress', values=['false', 'true'], child=True)
@Attribute('RegisterOutput', values=['false', 'true'], child=True)
@Attribute('SectionAlignment', child=True)
@Attribute('SetChecksum', values=['false', 'true'], child=True)
@Attribute('ShowProgress', values=['NotSet', 'LinkVerbose', 'LinkVerboseLib', 'LinkVerboseICF', 'LinkVerboseREF', 'LinkVerboseSAFESEH', 'LinkVerboseCLR'], child=True)
@Attribute('Sources', child=True)
@Attribute('SpecifySectionAttributes', child=True)
@Attribute('StackCommitSize', child=True)
@Attribute('StackReserveSize', child=True)
@Attribute('StripPrivateSymbols', child=True)
@Attribute('SubSystem', values=['Console', 'Windows', 'Native', 'EFI Application', 'EFI Boot Service Driver', 'EFI ROM', 'EFI Runtime', 'WindowsCE', 'POSIX'], child=True)
@Attribute('SupportNobindOfDelayLoadedDLL', values=['false', 'true'], child=True)
@Attribute('SupportUnloadOfDelayLoadedDLL', values=['false', 'true'], child=True)
@Attribute('SuppressStartupBanner', values=['false', 'true'], child=True)
@Attribute('SwapRunFromCD', values=['false', 'true'], child=True)
@Attribute('SwapRunFromNET', values=['false', 'true'], child=True)
@Attribute('TargetMachine', values=['MachineARM', 'MachineEBC', 'MachineIA64', 'MachineMIPS', 'MachineMIPS16', 'MachineMIPSFPU', 'MachineMIPSFPU16', 'MachineSH4', 'MachineTHUMB', 'MachineX64', 'MachineX86'], child=True)
@Attribute('TerminalServerAware', values=['false', 'true'], child=True)
@Attribute('TrackerLogDirectory', child=True)
@Attribute('TreatLinkerWarningAsErrors', values=['false', 'true'], child=True)
@Attribute('TurnOffAssemblyGeneration', values=['false', 'true'], child=True)
@Attribute('TypeLibraryFile', child=True)
@Attribute('TypeLibraryResourceID', child=True)
@Attribute('UACExecutionLevel', values=['AsInvoker', 'HighestAvailable', 'RequireAdministrator'], child=True)
@Attribute('UACUIAccess', values=['false', 'true'], child=True)
@Attribute('UseLibraryDependencyInputs', values=['false', 'true'], child=True)
@Attribute('Version', child=True)
class Link(SubElement):
    def __init__(self, include=None):
        super(Link, self).__init__('Link')
        self.include = include


@Attribute('HintPath', child=True)
@Attribute('Name', child=True)
@Attribute('FusionName', child=True)
@Attribute('SpecificVersion', values=['false', 'true'], child=True)
@Attribute('Aliases', child=True)
@Attribute('Private', values=['false', 'true'], child=True)
@Attribute('Include')
class Reference(SubElement):
    def __init__(self):
        super(Reference, self).__init__('Reference')


@Attribute('Name', child=True)
@Attribute('Guid', child=True)
@Attribute('VersionMajor', child=True)
@Attribute('VersionMinor', child=True)
@Attribute('LCID', child=True)
@Attribute('WrapperTool', child=True)
@Attribute('Include')
class COMReference(SubElement):
    def __init__(self):
        super(COMReference, self).__init__('COMReference')


@Attribute('WrapperTool', child=True)
@Attribute('Include')
class COMFileReference(SubElement):
    def __init__(self):
        super(COMFileReference, self).__init__('COMFileReference')


@Attribute('HintPath', child=True)
@Attribute('Name', child=True)
@Attribute('Include')
class NativeReference(SubElement):
    def __init__(self):
        super(NativeReference, self).__init__('NativeReference')


@Attribute('Name', child=True)
@Attribute('Project', child=True)
@Attribute('Package', child=True)
class ProjectReference(SubElement):
    def __init__(self):
        super(ProjectReference, self).__init__('ProjectReference')


@Attribute('DependentUpon', child=True)
@Attribute('Generator', child=True)
@Attribute('LastGenOutput', child=True)
@Attribute('CustomToolNamespace', child=True)
@Attribute('Link', values=['false', 'true'], child=True)
@Attribute('PublishState', values=['Default', 'Included', 'Excluded', 'DataFile', 'Prerequisite'], child=True)
@Attribute('IsAssembly', values=['false', 'true'], child=True)
@Attribute('Visible', values=['false', 'true'], child=True)
@Attribute('CopyToOutputDirectory', values=['Never', 'Always', 'PreserveNewest'], child=True)
@Attribute('Include')
class Content(SubElement):
    def __init__(self):
        super(Content, self).__init__('Content')


@Attribute('DependentUpon', child=True)
@Attribute('Generator', child=True)
@Attribute('LastGenOutput', child=True)
@Attribute('CustomToolNamespace', child=True)
@Attribute('Link', values=['false', 'true'], child=True)
@Attribute('PublishState', values=['Default', 'Included', 'Excluded', 'DataFile', 'Prerequisite'], child=True)
@Attribute('IsAssembly', values=['false', 'true'], child=True)
@Attribute('Visible', values=['false', 'true'], child=True)
@Attribute('CopyToOutputDirectory', values=['Never', 'Always', 'PreserveNewest'], child=True)
@Attribute('Include')
class NoneTask(SubElement):
    def __init__(self):
        super(NoneTask, self).__init__('NoneTask')


@Attribute('Command', child=True)
@Attribute('Message', child=True)
@Attribute('Outputs', child=True)
@Attribute('Include')
class CustomBuild(SubElement):
    def __init__(self, include=None):
        super(CustomBuild, self).__init__('CustomBuild')
        self.include = include


@Attribute('Command', child=True)
@Attribute('Inputs', child=True)
@Attribute('Outputs', child=True)
class CustomBuildStep(SubElement):
    def __init__(self):
        super(CustomBuildStep, self).__init__('CustomBuildStep')


@Attribute('DefaultTargets', varname='default_target')
@Attribute('ToolsVersion', varname='tools_version')
@Attribute('xmlns')
class Project(ElementTree):
    def __init__(self):
        super(Project, self).__init__(element=Element('Project'))
        self.default_target = "Build"
        self.tools_version = "12.0"
        self.xmlns = "http://schemas.microsoft.com/developer/msbuild/2003"
        
    def append(self, element):
        self.getroot().append(element)

    def get(self, key):
        self.getroot().get(key)
        
    def set(self, key, value):
        self.getroot().set(key, value)

    def write(self, filename):
        with open(filename, 'w') as f:
            data = minidom.parseString(ET.tostring(self.getroot())).toprettyxml(indent="  ")
            f.write(data)


@Attribute('IntDir', child=True)
@Attribute('GenerateManifest', child=True)
@Attribute('LinkIncremental', child=True)
@Attribute('OutDir', child=True)
@Attribute('TargetDir', child=True)
@Attribute('TargetName', child=True)
@Attribute('TargetExt', child=True)
@Attribute('TargetPath', child=True)
class CXXPropertyGroup(PropertyGroup):
    def __init__(self):
        super(CXXPropertyGroup, self).__init__()


@Composition(ClCompile, 'clcompile')
@Composition(CustomBuild, 'custombuild')
@Composition(Reference, 'reference')
@Composition(COMReference, 'comreference')
@Composition(COMFileReference, 'comfilereference')
@Composition(ProjectReference, 'projectreference')
@Composition(Content, 'content')
@Composition(NoneTask, 'none')
class CXXItemGroup(ItemGroup):
    def __init__(self):
        super(CXXItemGroup, self).__init__()


@Composition(ClCompile, 'clcompile')
@Composition(CustomBuildStep, 'custombuildstep')
@Composition(Lib, 'lib')
@Composition(Link, 'link')        
class CXXItemDefinitionGroup(ItemDefinitionGroup):
    def __init__(self, label=None):
        super(CXXItemDefinitionGroup, self).__init__(label)
        

@Composition(CXXItemGroup, 'itemgroup')
@Composition(CXXItemDefinitionGroup, 'itemdefinitiongroup')
@Composition(CXXPropertyGroup, 'propertygroup')
@Composition(Import, 'import')
@Composition(ImportGroup, 'importgroup')
class CXXProject(Project):
    def __init__(self, toolchain):
        super(CXXProject, self).__init__()
        self.configs_group = ProjectConfigurationsItemGroup()
        self.globals_group = deepcopy(toolchain.globals)    
        self.macros_group = PropertyGroup('UserMacros')    
        self.config = self.create_projectconfiguration(toolchain.config, toolchain.platform)
        self.config_props = self.create_configuration_property_group(self.config)        

        self.append(self.configs_group)
        self.append(self.globals_group)
        self.append(Import('$(VCTargetsPath)\Microsoft.Cpp.Default.props'))
        self.append(Import('$(VCTargetsPath)\Microsoft.Cpp.props'))
        self.append(self.macros_group)
        
        self.definitions_group = self.create_itemdefinitiongroup()        
        self.properties_group = self.create_propertygroup()
        self.items_group = self.create_itemgroup()

        self.append(Import('$(VCTargetsPath)\Microsoft.Cpp.targets'))
        
        self.clcompile = deepcopy(toolchain.clcompile)
        self.definitions_group.append(self.clcompile)
        
        self.lib = self.definitions_group.create_lib()
        self.link = self.definitions_group.create_link()
            
    def create_projectconfiguration(self, config_name, platform):
        return self.configs_group.create_projectconfiguration(config_name, platform)
        
    def create_configuration_property_group(self, project_config):
        cpg = ConfigurationPropertyGroup(project_config)
        self.getroot().insert(5, cpg)
        return cpg


class CXXToolchain(Toolchain):
    def __init__(self, name, vcvars=VS14VCVars(target="x64", host="x64")):
        super(CXXToolchain, self).__init__(name)
        self.vcvars = vcvars
        self.config = 'Default'
        self.platform = 'x64'
        self.toolset = 'v140'
        self.charset = None
        self.subsystem = 'Console'
        self.globals = PropertyGroup('Globals')
        self.clcompile = ClCompile()
        self.output = "output/{}".format(name)

    def add_tool(self, extension, driver):
        self._tools[extension] = driver

    def get_tool(self, extension):
        if extension not in self._tools:
            raise RuntimeError('could not find tool for {} extension'.format(extension))
        return self._tools[extension]

    def transform(self, project):
        cxx_project = CXXProject(self)
        cxx_project.tools_version = self.vcvars['VisualStudioVersion']

        cxx_project.globals_group.projectname = project.name
        cxx_project.globals_group.projectguid = '{%s}' % project.uuid
        cxx_project.globals_group.platform = self.platform

        def key_value(key, value):
            return key if value is None else "{}={}".format(key, value)

        macros = [key_value(macro.key, macro.value) for macro in project.macros if macro.matches(self.name)]
        incpaths = [incpath.path for incpath in project.incpaths if incpath.matches(self.name)]
        libpaths = [libpath.path for libpath in project.libpaths if libpath.matches(self.name)]

        if isinstance(project, model.CXXLibrary):
            cxx_project.config_props.type = 'StaticLibrary'
            cxx_project.lib.subsystem = self.subsystem

        if isinstance(project, model.CXXExecutable):
            cxx_project.config_props.type = 'Application'
            macros += [key_value(macro.key, macro.value) for dep in project.dependencies for macro in dep.macros if macro.publish]
            incpaths += [incpath.path for dep in project.dependencies for incpath in dep.incpaths if incpath.publish]
            libpaths += [libpath.path for dep in project.dependencies for libpath in dep.libpaths if libpath.publish]
            libraries = [dep.name for dep in project.dependencies if isinstance(dep, model.CXXLibrary)]
            libraries = ['{output}/{lib}/{lib}.lib'.format(output=self.output, lib=lib) for lib in libraries]
            cxx_project.link.additionaldependencies = ';'.join(libraries)
            cxx_project.link.additionallibrarydirectories = ';'.join(libpaths)
            cxx_project.link.subsystem = self.subsystem

        cxx_project.clcompile.additionalincludedirectories = ';'.join(incpaths)
        cxx_project.clcompile.preprocessordefinitions = ';'.join(macros)
        cxx_project.clcompile.trackerlogdirectory = "$(IntDir)"

        cxx_project.config_props.toolset = self.toolset
        cxx_project.config_props.charset = self.charset
        cxx_project.properties_group.intdir = "{}/{}/".format(self.output, project.name)
        cxx_project.properties_group.outdir = "{}/{}/".format(self.output, project.name)
        cxx_project.properties_group.targetpath = "$(OutDir)$(TargetName)$(TargetExt)"

        groups = project.source_groups + [project]
        for group in groups:
            for source in group.sources:
                print(source.path)
                tool = self.get_tool(source.tool)
                if tool is None:
                    raise RuntimeError()
                tool.transform(cxx_project, source)

        for feature in project.features:
            if feature.matches(self.name):
                feature = FeatureRegistry.find(feature.name)
                feature.transform(project, cxx_project)

        cxx_project.write('{}.vcxproj'.format(project.name))
        
        rc, _ = utils.execute('MSBuild.exe {}.vcxproj /m /nologo /p:Configuration={} /p:Platform={}'.format(
            project.name, self.config, self.platform), self.vcvars)
        if rc != 0:
            raise RuntimeError()
