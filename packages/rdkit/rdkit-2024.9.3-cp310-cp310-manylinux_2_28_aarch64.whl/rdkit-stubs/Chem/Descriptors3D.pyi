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
descList: list  # value = [('PMI1', <function <lambda> at 0xffffaf7dc1f0>), ('PMI2', <function <lambda> at 0xffffa12e9120>), ('PMI3', <function <lambda> at 0xffffa12e91b0>), ('NPR1', <function <lambda> at 0xffffa12e9240>), ('NPR2', <function <lambda> at 0xffffa12e92d0>), ('RadiusOfGyration', <function <lambda> at 0xffffa12e9360>), ('InertialShapeFactor', <function <lambda> at 0xffffa12e93f0>), ('Eccentricity', <function <lambda> at 0xffffa12e9480>), ('Asphericity', <function <lambda> at 0xffffa12e9510>), ('SpherocityIndex', <function <lambda> at 0xffffa12e95a0>), ('PBF', <function <lambda> at 0xffffa12e9630>)]
