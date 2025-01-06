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
descList: list  # value = [('PMI1', <function <lambda> at 0xffff9607c1f0>), ('PMI2', <function <lambda> at 0xffff88d111b0>), ('PMI3', <function <lambda> at 0xffff88d11240>), ('NPR1', <function <lambda> at 0xffff88d112d0>), ('NPR2', <function <lambda> at 0xffff88d11360>), ('RadiusOfGyration', <function <lambda> at 0xffff88d113f0>), ('InertialShapeFactor', <function <lambda> at 0xffff88d11480>), ('Eccentricity', <function <lambda> at 0xffff88d11510>), ('Asphericity', <function <lambda> at 0xffff88d115a0>), ('SpherocityIndex', <function <lambda> at 0xffff88d11630>), ('PBF', <function <lambda> at 0xffff88d116c0>)]
