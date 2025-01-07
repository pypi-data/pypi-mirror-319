"""
 Descriptors derived from a molecule's 3D structure

"""
from __future__ import annotations
from rdkit.Chem.Descriptors import _isCallable
from rdkit.Chem import rdMolDescriptors
__all__ = ['CalcMolDescriptors3D', 'descList', 'rdMolDescriptors']
def CalcMolDescriptors3D(mol, confId = None):
    """
    
        Compute all 3D descriptors of a molecule
        
        Arguments:
        - mol: the molecule to work with
        - confId: conformer ID to work with. If not specified the default (-1) is used
        
        Return:
        
        dict
            A dictionary with decriptor names as keys and the descriptor values as values
    
        raises a ValueError 
            If the molecule does not have conformers
        
    """
def _setupDescriptors(namespace):
    ...
descList: list  # value = [('PMI1', <function <lambda> at 0x7f4468617420>), ('PMI2', <function <lambda> at 0x7f4468617b00>), ('PMI3', <function <lambda> at 0x7f4468617ba0>), ('NPR1', <function <lambda> at 0x7f4468617c40>), ('NPR2', <function <lambda> at 0x7f4468617ce0>), ('RadiusOfGyration', <function <lambda> at 0x7f4468617d80>), ('InertialShapeFactor', <function <lambda> at 0x7f4468617e20>), ('Eccentricity', <function <lambda> at 0x7f4468617ec0>), ('Asphericity', <function <lambda> at 0x7f4468617f60>), ('SpherocityIndex', <function <lambda> at 0x7f4468690040>), ('PBF', <function <lambda> at 0x7f44686900e0>)]
