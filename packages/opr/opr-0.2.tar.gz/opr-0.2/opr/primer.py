# -*- coding: utf-8 -*-
"""OPR primer."""
from enum import Enum
from warnings import warn
from .errors import OPRBaseError
from .params import VALID_BASES
from .params import PRIMER_SEQUENCE_TYPE_ERROR, PRIMER_SEQUENCE_LENGTH_WARNING, PRIMER_SEQUENCE_VALID_BASES_ERROR, PRIMER_SEQUENCE_VALID_GC_CONTENT_RANGE_WARNING
from .params import PRIMER_LOWER_LENGTH, PRIMER_HIGHEST_LENGTH, PRIMER_LOWEST_GC_RANGE, PRIMER_HIGHEST_GC_RANGE
from .params import DNA_COMPLEMENT_MAP
from .params import PRIMER_ADDITION_ERROR, PRIMER_MULTIPLICATION_ERROR
from .params import PRIMER_MELTING_TEMPERATURE_NOT_IMPLEMENTED_ERROR
from .functions import molecular_weight_calc, basic_melting_temperature_calc, gc_clamp_calc, single_run_length


class MeltingTemperature(Enum):
    """Mode used to calculate the Melting Temperature of the Primer accordingly."""

    BASIC = 1
    SALT_ADJUSTED = 2
    NEAREST_NEIGHBOR = 3


class Primer:
    """
    The Primer class facilitates working with the primer sequence.

    >>> oprimer = Primer("ATCGATCGATCGATCGAT")
    >>> oprimer.molecular_weight
    """

    def __init__(self, sequence):
        """
        Initialize the Primer instance.

        :param sequence: primer nucleotides sequence
        :type sequence: str
        :return: an instance of the Primer class
        """
        self._sequence = Primer.validate_primer(sequence)
        self._molecular_weight = None
        self._gc_content = None
        self._gc_clamp = None
        self._single_runs = None
        self._melting_temperature = {
            MeltingTemperature.BASIC: None,
            MeltingTemperature.SALT_ADJUSTED: None,
            MeltingTemperature.NEAREST_NEIGHBOR: None,
        }

    def __len__(self):
        """
        Return the length of the Primer sequence.

        :return: length of the Primer sequence
        """
        return len(self._sequence)

    def __eq__(self, other_primer):
        """
        Check primers equality.

        :param other_primer: another Primer
        :type other_primer: Primer
        :return: result as bool
        """
        return self._sequence == other_primer._sequence

    def __add__(self, other_primer):
        """
        Concatenate the sequences of the current Primer with another one.

        :param other_primer: another Primer to concat its sequence to the current Primer
        :type other_primer: Primer
        :return: new Primer with concatenated sequence
        """
        if isinstance(other_primer, Primer):
            return Primer(self._sequence + other_primer._sequence)
        raise OPRBaseError(PRIMER_ADDITION_ERROR)

    def __mul__(self, number):
        """
        Multiply the Primer sequence `number` times.

        :param number: times to concat the Primer sequence to itself
        :type number: int
        :return: new Primer with multiplied sequence
        """
        if isinstance(number, int):
            return Primer(self._sequence * number)
        raise OPRBaseError(PRIMER_MULTIPLICATION_ERROR)

    def __str__(self):
        """
        Primer object string representation method.

        :return: primer sequence as str
        """
        return self._sequence

    def reverse(self, inplace=False):
        """
        Reverse sequence.

        :param inplace: inplace flag
        :type inplace: bool
        :return: new Primer object or None
        """
        new_sequence = self._sequence[::-1]
        if inplace:
            self._sequence = new_sequence
        else:
            return Primer(sequence=new_sequence)

    def complement(self, inplace=False):
        """
        Complement sequence.

        :param inplace: inplace flag
        :type inplace: bool
        :return: new Primer object or None
        """
        new_sequence = ""
        for item in self._sequence:
            new_sequence += DNA_COMPLEMENT_MAP[item]
        if inplace:
            self._sequence = new_sequence
        else:
            return Primer(sequence=new_sequence)

    @staticmethod
    def validate_primer(sequence):
        """
        Validate the given primer sequence.

        :param sequence: primer nucleotides sequence
        :type sequence: any
        :return: an uppercased primer sequence
        """
        if not isinstance(sequence, str):
            raise OPRBaseError(PRIMER_SEQUENCE_TYPE_ERROR)
        sequence = sequence.upper()

        if len(sequence) < PRIMER_LOWER_LENGTH or len(sequence) > PRIMER_HIGHEST_LENGTH:
            warn(PRIMER_SEQUENCE_LENGTH_WARNING, RuntimeWarning)

        if not all(base in VALID_BASES for base in sequence):
            raise OPRBaseError(PRIMER_SEQUENCE_VALID_BASES_ERROR)
        return sequence

    @property
    def sequence(self):
        """
        Return the primer sequence.

        :return: primer sequence
        """
        return self._sequence

    @property
    def molecular_weight(self):
        """
        Calculate(if needed) the molecular weight.

        :return: molecular weight
        """
        if self._molecular_weight:
            return self._molecular_weight
        self._molecular_weight = molecular_weight_calc(self._sequence)
        return self._molecular_weight

    @property
    def gc_content(self):
        """
        Calculate gc content.

        :return: gc content
        """
        if self._gc_content is None:
            gc_count = self._sequence.count('G') + self._sequence.count('C')
            self._gc_content = gc_count / len(self._sequence)
        if self._gc_content < PRIMER_LOWEST_GC_RANGE or self._gc_content > PRIMER_HIGHEST_GC_RANGE:
            warn(PRIMER_SEQUENCE_VALID_GC_CONTENT_RANGE_WARNING, RuntimeWarning)
        return self._gc_content

    @property
    def gc_clamp(self):
        """
        Calculate GC clamp of the primer.

        :return: GC clamp of the primer
        """
        if self._gc_clamp is None:
            self._gc_clamp = gc_clamp_calc(self._sequence)
        return self._gc_clamp

    @property
    def single_runs(self):
        """
        Calculate Single Runs of the primer.

        Run length refers to how many times a single base is repeated consecutively in the primer.

        :return: single runs of the primer
        """
        if self._single_runs is None:
            self._single_runs = {
                'A': 0,
                'T': 0,
                'C': 0,
                'G': 0,
            }
            for base in self._single_runs:
                self._single_runs[base] = single_run_length(self._sequence, base)
        return self._single_runs

    def melting_temperature(self, method=MeltingTemperature.BASIC):
        """
        Calculate(if needed) the melting temperature.

        :param method: requested calculation mode for melting temperature
        :type method: MeltingTemperature
        :return: approximated melting temperature
        """
        if self._melting_temperature[method] is not None:
            return self._melting_temperature[method]
        if method == MeltingTemperature.BASIC:
            self._melting_temperature[MeltingTemperature.BASIC] = basic_melting_temperature_calc(self._sequence)
        else:
            raise NotImplementedError(PRIMER_MELTING_TEMPERATURE_NOT_IMPLEMENTED_ERROR)
        return self._melting_temperature[method]
