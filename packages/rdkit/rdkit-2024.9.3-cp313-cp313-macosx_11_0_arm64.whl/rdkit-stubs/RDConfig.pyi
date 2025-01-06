"""
Configuration for the RDKit Python code

"""
from __future__ import annotations
import os as os
import rdkit as rdkit
import sqlite3 as sqlite3
import sys as sys
import typing
__all__ = ['ObsoleteCodeError', 'RDCodeDir', 'RDContribDir', 'RDDataDatabase', 'RDDataDir', 'RDDocsDir', 'RDProjDir', 'RDTestDatabase', 'UnimplementedCodeError', 'defaultDBPassword', 'defaultDBUser', 'molViewer', 'os', 'pythonExe', 'pythonTestCommand', 'rdkit', 'rpcTestPort', 'sqlite3', 'sys', 'usePgSQL', 'useSqlLite']
class ObsoleteCodeError(Exception):
    __firstlineno__: typing.ClassVar[int] = 39
    __static_attributes__: typing.ClassVar[tuple] = tuple()
class UnimplementedCodeError(Exception):
    __firstlineno__: typing.ClassVar[int] = 43
    __static_attributes__: typing.ClassVar[tuple] = tuple()
RDCodeDir: str = '/Users/runner/work/rdkit-pypi/rdkit-pypi/build/temp.macosx-11.0-arm64-cpython-313/rdkit_install/lib/python3.13/site-packages/rdkit'
RDContribDir: str = '/Users/runner/work/rdkit-pypi/rdkit-pypi/build/temp.macosx-11.0-arm64-cpython-313/rdkit_install/share/RDKit/Contrib'
RDDataDatabase: str = '/Users/runner/work/rdkit-pypi/rdkit-pypi/build/temp.macosx-11.0-arm64-cpython-313/rdkit_install/share/RDKit/Data/RDData.sqlt'
RDDataDir: str = '/Users/runner/work/rdkit-pypi/rdkit-pypi/build/temp.macosx-11.0-arm64-cpython-313/rdkit_install/share/RDKit/Data'
RDDocsDir: str = '/Users/runner/work/rdkit-pypi/rdkit-pypi/build/temp.macosx-11.0-arm64-cpython-313/rdkit_install/share/RDKit/Docs'
RDProjDir: str = '/Users/runner/work/rdkit-pypi/rdkit-pypi/build/temp.macosx-11.0-arm64-cpython-313/rdkit_install/share/RDKit/Projects'
RDTestDatabase: str = '/Users/runner/work/rdkit-pypi/rdkit-pypi/build/temp.macosx-11.0-arm64-cpython-313/rdkit_install/share/RDKit/Data/RDTests.sqlt'
defaultDBPassword: str = 'masterkey'
defaultDBUser: str = 'sysdba'
molViewer: str = 'PYMOL'
pythonExe: str = '/private/var/folders/95/0ydz4d79163427j3k5crp3fh0000gn/T/cibw-run-zu17npyp/cp313-macosx_arm64/build/venv/bin/python3.13'
pythonTestCommand: str = 'python'
rpcTestPort: int = 8423
usePgSQL: bool = False
useSqlLite: bool = True
