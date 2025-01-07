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
descList: list  # value = [('PMI1', <function <lambda> at 0x7f4869af8040>), ('PMI2', <function <lambda> at 0x7f48598f34c0>), ('PMI3', <function <lambda> at 0x7f48598f3600>), ('NPR1', <function <lambda> at 0x7f48598f36a0>), ('NPR2', <function <lambda> at 0x7f48598f3740>), ('RadiusOfGyration', <function <lambda> at 0x7f48598f37e0>), ('InertialShapeFactor', <function <lambda> at 0x7f48598f3880>), ('Eccentricity', <function <lambda> at 0x7f48598f3920>), ('Asphericity', <function <lambda> at 0x7f48598f39c0>), ('SpherocityIndex', <function <lambda> at 0x7f48598f3a60>), ('PBF', <function <lambda> at 0x7f48598f3b00>)]
