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
descList: list  # value = [('PMI1', <function <lambda> at 0x100ddac20>), ('PMI2', <function <lambda> at 0x10663e8c0>), ('PMI3', <function <lambda> at 0x10663e950>), ('NPR1', <function <lambda> at 0x10663e9e0>), ('NPR2', <function <lambda> at 0x10663ea70>), ('RadiusOfGyration', <function <lambda> at 0x10663eb00>), ('InertialShapeFactor', <function <lambda> at 0x10663eb90>), ('Eccentricity', <function <lambda> at 0x10663ec20>), ('Asphericity', <function <lambda> at 0x10663ecb0>), ('SpherocityIndex', <function <lambda> at 0x10663ed40>), ('PBF', <function <lambda> at 0x10663edd0>)]
