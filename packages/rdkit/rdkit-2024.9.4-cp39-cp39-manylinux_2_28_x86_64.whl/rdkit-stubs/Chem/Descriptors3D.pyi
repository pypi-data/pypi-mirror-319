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
descList: list  # value = [('PMI1', <function <lambda> at 0x7f028f676430>), ('PMI2', <function <lambda> at 0x7f0280106940>), ('PMI3', <function <lambda> at 0x7f02801069d0>), ('NPR1', <function <lambda> at 0x7f0280106a60>), ('NPR2', <function <lambda> at 0x7f0280106af0>), ('RadiusOfGyration', <function <lambda> at 0x7f0280106b80>), ('InertialShapeFactor', <function <lambda> at 0x7f0280106c10>), ('Eccentricity', <function <lambda> at 0x7f0280106ca0>), ('Asphericity', <function <lambda> at 0x7f0280106d30>), ('SpherocityIndex', <function <lambda> at 0x7f0280106dc0>), ('PBF', <function <lambda> at 0x7f0280106e50>)]
