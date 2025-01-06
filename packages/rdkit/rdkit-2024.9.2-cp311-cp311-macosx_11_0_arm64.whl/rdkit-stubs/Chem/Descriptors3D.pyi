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
descList: list  # value = [('PMI1', <function <lambda> at 0x101136520>), ('PMI2', <function <lambda> at 0x1040dcd60>), ('PMI3', <function <lambda> at 0x1040dcea0>), ('NPR1', <function <lambda> at 0x1040dcf40>), ('NPR2', <function <lambda> at 0x1040dcfe0>), ('RadiusOfGyration', <function <lambda> at 0x1040dd080>), ('InertialShapeFactor', <function <lambda> at 0x1040dd120>), ('Eccentricity', <function <lambda> at 0x1040dd1c0>), ('Asphericity', <function <lambda> at 0x1040dd260>), ('SpherocityIndex', <function <lambda> at 0x1040dd300>), ('PBF', <function <lambda> at 0x1040dd3a0>)]
