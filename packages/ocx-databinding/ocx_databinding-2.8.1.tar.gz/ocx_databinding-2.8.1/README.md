# ocx-databinding
CLI python script for managing the [OCX schema](https://github.com/OCXStandard/OCX_Schema) databinding.
See the documentation of [xsdata](https://xsdata.readthedocs.io/en/latest/) for details on creating python databindings.

## Installation

    pip install ocx_databinding
## Changes
[CHANGELOG](CHANGELOG.md)

## Usage
    databinding --help
    Usage: databinding [OPTIONS] COMMAND [ARGS]...

    Options:
      --install-completion  Install completion for the current shell.
      --show-completion     Show completion for the current shell, to copy it or
                            customize the installation.
      --help                Show this message and exit.

    Commands:
      generate  Generate code from xml schemas, webservice definitions and...
      version   Print the version number and exit.

Generate a datbinding:

    Usage: databinding generate [OPTIONS] SOURCE PACKAGE SCHEMA_VERSION

      Generate code from xml schemas, webservice definitions and any xml or json
      document. The input source can be either a filepath, uri or a directory
      containing  xml, json, xsd and wsdl files.

    Arguments:
      SOURCE          [required]
      PACKAGE         [required]
      SCHEMA_VERSION  [required]

    Options:
      --docstring-style TEXT        [default: Google]
      --structure-style TEXT        [default: single-package]
      --slots / --no-slots          [default: slots]
      --recursive / --no-recursive  [default: no-recursive]
      --help                        Show this message and exit.

## Example
Generate the databindings from the unitsML schema url:

    databinding generate https://3docx.org/fileadmin/ocx_schema/unitsml/unitsmlSchema_lite-0.9.18.xsd unitsml 0.9.18

    2023-09-04 11:17:28.705 | INFO     | ocx_databinding.generator:generate:64 - New databinding package name is unitsml_0918 with version: 0.9.18 is created in C:\PythonDev\ocx-generator\unitsml
    ========= xsdata v23.8 / Python 3.11.5 / Platform win32 =========

    Parsing schema https://3docx.org/fileadmin/ocx_schema/unitsml/unitsmlSchema_lite-0.9.18.xsd
    Parsing schema file:///C:/miniconda3/envs/generator/Lib/site-packages/xsdata/schemas/xml.xsd
    Compiling schema file:///C:/miniconda3/envs/generator/Lib/site-packages/xsdata/schemas/xml.xsd
    Builder: 5 main and 2 inner classes
    Compiling schema https://3docx.org/fileadmin/ocx_schema/unitsml/unitsmlSchema_lite-0.9.18.xsd
    Builder: 38 main and 2 inner classes
    Analyzer input: 43 main and 4 inner classes
    Analyzer output: 35 main and 0 inner classes
    Generating package: init
    Generating package: unitsml_0918

This has now generated a subdirectory ``unitsml``  with the following structure:


    C:.
    └───unitsml
        └───unitsml_0918
and with the content:

       Length Name
       ------ ----
        29577 unitsml_0918.py
         2145 xsdata.xml
         1531 __init__.py

The CLI generates a single  package, meaning that any imported schemas are ignored, see [xsdata](https://xsdata.readthedocs.io/en/latest/) if more detailed control of the databinding is necessary.
The databindings are also versioned by creating a package name with the version string. This allows us to have multiple databindings representing different schema versions.

## API documentation

[API](https://ocxstandard.github.io/ocx-databinding/)
