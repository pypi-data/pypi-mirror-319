from __future__ import annotations
import nuri.core._core
import os
import typing
__all__ = ['CifBlock', 'CifFrame', 'CifParser', 'CifTable', 'MoleculeReader', 'cif_ddl2_frame_as_dict', 'read_cif', 'readfile', 'readstring', 'to_mol2', 'to_sdf', 'to_smiles']
class CifBlock:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @property
    def data(self) -> CifFrame:
        ...
    @property
    def is_global(self) -> bool:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def save_frames(self) -> _CifFrameList:
        ...
class CifFrame:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __contains__(self, idx: int) -> bool:
        ...
    def __getitem__(self, idx: int) -> CifTable:
        ...
    def __iter__(self) -> _CifFrameIterator:
        ...
    def __len__(self) -> int:
        ...
    def prefix_search_first(self, prefix: str) -> CifTable | None:
        """
        Search for the first table containing a column starting with the given prefix.
        
        :param prefix: The prefix to search for.
        :return: The first table containing the given prefix, or None if not found.
        """
    @property
    def name(self) -> str:
        ...
class CifParser:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __iter__(self) -> CifParser:
        ...
    def __next__(self) -> CifBlock:
        ...
class CifTable:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __contains__(self, idx: int) -> bool:
        ...
    def __getitem__(self, idx: int) -> list[str | None]:
        ...
    def __iter__(self) -> _CifTableIterator:
        ...
    def __len__(self) -> int:
        ...
    def keys(self) -> list[str]:
        ...
class MoleculeReader:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __iter__(self) -> MoleculeReader:
        ...
    def __next__(self) -> nuri.core._core.Molecule:
        ...
class _CifFrameIterator:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __iter__(self) -> _CifFrameIterator:
        ...
    def __next__(self) -> CifTable:
        ...
class _CifFrameList:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __getitem__(self, arg0: int) -> CifFrame:
        ...
    def __iter__(self) -> typing.Iterator[CifFrame]:
        ...
    def __len__(self) -> int:
        ...
    def __repr__(self) -> str:
        ...
class _CifTableIterator:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __iter__(self) -> _CifTableIterator:
        ...
    def __next__(self) -> list[str | None]:
        ...
def cif_ddl2_frame_as_dict(frame: CifFrame) -> dict[str, list[dict[str, str | None]]]:
    """
    Convert a CIF frame to a dictionary of lists of dictionaries.
    
    :param frame: The CIF frame to convert.
    :return: A dictionary of lists of dictionaries, where the keys are the parent
      keys and the values are the rows of the table.
    """
def read_cif(path: os.PathLike) -> CifParser:
    """
    Create a parser object from a CIF file path.
    
    :param path: The path to the CIF file.
    :return: A parser object that can be used to iterate over the blocks in the file.
    """
def readfile(fmt: str, path: os.PathLike, sanitize: bool = True, skip_on_error: bool = False) -> MoleculeReader:
    """
    Read a molecule from a file.
    
    :param fmt: The format of the file.
    :param path: The path to the file.
    :param sanitize: Whether to sanitize the produced molecule. For formats that is
      known to produce molecules with insufficient bond information (e.g. PDB), this
      option will trigger guessing based on the 3D coordinates
      (:func:`nuri.algo.guess_everything()`).
    :param skip_on_error: Whether to skip a molecule if an error occurs, instead of
      raising an exception.
    :raises OSError: If any file-related error occurs.
    :raises ValueError: If the format is unknown or sanitization fails, unless
      `skip_on_error` is set.
    :rtype: collections.abc.Iterable[Molecule]
    """
def readstring(fmt: str, data: str, sanitize: bool = True, skip_on_error: bool = False) -> MoleculeReader:
    """
    Read a molecule from string.
    
    :param fmt: The format of the file.
    :param data: The string to read.
    :param sanitize: Whether to sanitize the produced molecule. For formats that is
      known to produce molecules with insufficient bond information (e.g. PDB), this
      option will trigger guessing based on the 3D coordinates
      (:func:`nuri.algo.guess_everything()`).
    :param skip_on_error: Whether to skip a molecule if an error occurs, instead of
      raising an exception.
    :raises ValueError: If the format is unknown or sanitization fails, unless
      `skip_on_error` is set.
    :rtype: collections.abc.Iterable[Molecule]
    
    The returned object is an iterable of molecules.
    
    >>> for mol in nuri.readstring("smi", "C"):
    ...     print(mol[0].atomic_number)
    6
    """
def to_mol2(mol: nuri.core._core.Molecule, conf: int | None = None, write_sub: bool = True) -> str:
    """
    Convert a molecule to Mol2 string.
    
    :param mol: The molecule to convert.
    :param conf: The conformation to convert. If not specified, writes all
      conformations. Ignored if the molecule has no conformations.
    :param write_sub: Whether to write the substructures.
    :raises IndexError: If the molecule has any conformations and `conf` is out of
      range.
    :raises ValueError: If the conversion fails.
    """
def to_sdf(mol: nuri.core._core.Molecule, conf: int | None = None, version: int | None = None) -> str:
    """
    Convert a molecule to SDF string.
    
    :param mol: The molecule to convert.
    :param conf: The conformation to convert. If not specified, writes all
      conformations. Ignored if the molecule has no conformations.
    :param version: The SDF version to write. If not specified, the version is
      automatically determined. Only 2000 and 3000 are supported.
    :raises IndexError: If the molecule has any conformations and `conf` is out of
      range.
    :raises ValueError: If the conversion fails, or if the version is invalid.
    """
def to_smiles(mol: nuri.core._core.Molecule) -> str:
    """
    Convert a molecule to SMILES string.
    
    :param mol: The molecule to convert.
    :raises ValueError: If the conversion fails.
    """
