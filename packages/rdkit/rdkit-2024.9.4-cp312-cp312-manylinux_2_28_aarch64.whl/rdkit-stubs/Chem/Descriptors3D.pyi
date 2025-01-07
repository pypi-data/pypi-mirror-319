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
descList: list  # value = [('PMI1', <function <lambda> at 0xffff789874c0>), ('PMI2', <function <lambda> at 0xffff78987ba0>), ('PMI3', <function <lambda> at 0xffff78987c40>), ('NPR1', <function <lambda> at 0xffff78987ce0>), ('NPR2', <function <lambda> at 0xffff78987d80>), ('RadiusOfGyration', <function <lambda> at 0xffff78987e20>), ('InertialShapeFactor', <function <lambda> at 0xffff78987ec0>), ('Eccentricity', <function <lambda> at 0xffff78987f60>), ('Asphericity', <function <lambda> at 0xffff77474040>), ('SpherocityIndex', <function <lambda> at 0xffff774740e0>), ('PBF', <function <lambda> at 0xffff77474180>)]
