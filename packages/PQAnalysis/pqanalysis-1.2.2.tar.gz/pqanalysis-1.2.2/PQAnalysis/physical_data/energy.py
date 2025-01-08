"""
A module containing the Energy class.
"""

import logging

from collections import defaultdict

import numpy as np

from beartype.typing import Dict

from PQAnalysis.types import Np2DNumberArray, Np1DNumberArray
from PQAnalysis.utils.custom_logging import setup_logger
from PQAnalysis import __package_name__
from PQAnalysis.type_checking import runtime_type_checking

from .exceptions import EnergyError



class Energy():

    """
    A class to store the data of an energy file.

    The data array is stored in a way that each column corresponds to a physical
    quantity. The order of the columns is the same as in the info file. The info
    and units of the info file are stored in the Energy object, if an info file
    was found.
    """

    logger = logging.getLogger(__package_name__).getChild(__qualname__)
    logger = setup_logger(logger)

    @runtime_type_checking
    def __init__(
        self,
        data: Np1DNumberArray | Np2DNumberArray,
        info: Dict | None = None,
        units: Dict | None = None
    ) -> None:
        """
        Parameters
        ----------
        data : Np1DNumberArray | Np2DNumberArray
            The data of the energy file as a np.array with shape (n, m), where n is the
            number of data entries and m is the number of physical properties. If the data
            is a 1D array, it is converted to a 2D array with shape (1, n).
        info : dict, optional
            the info dictionary, by default None
        units : dict, optional
            the units dictionary, by default None

        Notes
        -----
        If no info dictionary is given, a default dictionary is created,
        where the keys are the indices of the data array and the values 
        are the indices of the data array. Furthermore a units dictionary
        can be given, where the keys have to match the keys of the info
        dictionary and the values are the units of the physical properties.
        If no units dictionary is given, the units are set to None.

        The attributes of any Energy object are created for each physical
        property found in the info file. The attribute names can be found 
        in the __data_attributes__ dictionary. The attribute names are the
        keys of the dictionary and the values are the names of the physical 
        properties found in the info file. The attributes are created
        as follows:

        - The attribute name is the key of the __data_attributes__ dictionary.
        - The attribute value is the corresponding data entry (column in energy file).
        - The attribute name + "_unit" is the corresponding unit.
        - The attribute name + "_with_unit" is a tuple of the corresponding data entry
          and the corresponding unit.

        For example, the attribute "simulation_time" is created for the physical property
        "SIMULATION-TIME" found in the info file. The attribute "simulation_time" is the
        corresponding data entry (column in energy file). The attribute "simulation_time_unit"
        is the corresponding unit. The attribute "simulation_time_with_unit" is a tuple of
        the corresponding data entry and the corresponding unit.
        """
        if len(np.shape(data)) == 1:
            data = np.array([data])

        self.data = np.array(data)

        self._setup_info_dictionary(info, units)

        self._make_attributes()

    def _setup_info_dictionary(
        self,
        info: Dict | None = None,
        units: Dict | None = None
    ) -> None:
        """
        Sets up the info dictionary.

        If no info dictionary is given, a default dictionary is created, where
        the keys are the indices of the data array and the values are the indices
        of the data array. Furthermore a units dictionary can be given, where the
        where the keys have to match the keys of the info dictionary and the values
        are the units of the physical properties. If no units dictionary is given,
        the units are set to None.

        Parameters
        ----------
        info : dict
            A dictionary with the same length as the data array. The keys are either the
            indices of the data array or the names of the physical properties found in the 
            info file. The values are the indices of the data array.
        units : dict
            A dictionary with the same length as the data array. The keys are either the
            indices of the data array or the names of the physical properties found in the 
            info file. The values are the units of the physical properties.

        Raises
        ------
        EnergyError
            If the length of info is not equal to the length of data.
        EnergyError
            If the length of units is not equal to the length of data.
        EnergyError
            If the keys of the info and units dictionary do not match.
        """

        if info is None:
            self.info_given = False
            info = defaultdict(lambda: None)
        else:
            self.info_given = True
            if len(info) != len(self.data):
                self.logger.error(
                    "The length of info dictionary has to be equal to the length of data.",
                    exception=EnergyError
                )

        if units is None:
            self.units_given = False
            units = defaultdict(lambda: None)
        else:
            self.units_given = True
            if len(units) != len(self.data):
                self.logger.error(
                    "The length of units dictionary has to be equal to the length of data.",
                    exception=EnergyError
                )

        self.info = info
        self.units = units

        if self.info_given and self.units_given and units.keys() != info.keys(
        ):
            self.logger.error(
                "The keys of the info and units dictionary do not match.",
                exception=EnergyError
            )

    def _make_attributes(self) -> None:
        """
        Creates attributes for the physical properties of the Energy object.

        The attributes are created for each physical property found in the info file.
        The attribute names can be found in the __data_attributes__ dictionary. The
        attribute names are the keys of the dictionary and the values are the names
        of the physical properties found in the info file. The attributes are created
        as follows:

        - The attribute name is the key of the __data_attributes__ dictionary.
        - The attribute value is the corresponding data entry (column in energy file).
        - The attribute name + "_unit" is the corresponding unit.
        - The attribute name + "_with_unit" is a tuple of the corresponding data entry
          and the corresponding unit.

        For example, the attribute "simulation_time" is created for the physical property
        "SIMULATION-TIME" found in the info file. The attribute "simulation_time" is the
        corresponding data entry (column in energy file). The attribute "simulation_time_unit"
        is the corresponding unit. The attribute "simulation_time_with_unit" is a tuple of
        the corresponding data entry and the corresponding unit.
        """

        for attribute, value in self.__data_attributes__.items():
            info_string = attribute
            if info_string in self.info or info_string in self.units:
                setattr(self, value, self.data[self.info[attribute]])
                setattr(self, value + "_unit", self.units[attribute])
                setattr(
                    self,
                    value + "_with_unit",
                    (self.data[self.info[attribute]],
                    self.units[attribute])
                )

    ################################################
    #                                              #
    # from here all attributes possible are listed #
    #                                              #
    ################################################

    __data_attributes__ = {}

    __data_attributes__["SIMULATION-TIME"] = "simulation_time"
    __data_attributes__["SIMULATION TIME"] = "simulation_time"

    __data_attributes__["TEMPERATURE"] = "temperature"

    __data_attributes__["PRESSURE"] = "pressure"

    __data_attributes__["E(TOT)"] = "total_energy"

    __data_attributes__["E(QM)"] = "qm_energy"
    __data_attributes__["E(MM)"] = "mm_energy"

    __data_attributes__["N(QM-ATOMS)"] = "number_of_qm_atoms"
    __data_attributes__["QM_MOLECULES"] = "number_of_qm_molecules"

    __data_attributes__["E(KIN)"] = "kinetic_energy"

    __data_attributes__["E(INTRA)"] = "intramolecular_energy"

    __data_attributes__["E(BOND)"] = "bond_energy"
    __data_attributes__["E(ANGLE)"] = "angle_energy"
    __data_attributes__["E(DIHEDRAL)"] = "dihedral_energy"
    __data_attributes__["E(IMPROPER)"] = "improper_energy"

    __data_attributes__["VOLUME"] = "volume"

    __data_attributes__["DENSITY"] = "density"

    __data_attributes__["MOMENTUM"] = "momentum"

    __data_attributes__["LOOPTIME"] = "looptime"
