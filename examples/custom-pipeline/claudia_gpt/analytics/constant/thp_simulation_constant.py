"""Provides enumerations and constants related to taxation and social security.

This module defines enums and constants used in thp simulation.

Authors:
    Winson Evangelis Sutanto (winson.e.sutanto@gdplabs.id)
"""

from enum import Enum


class Pph21Method(Enum):
    """Enumeration representing pph21 calculation methods.

    Attributes:
        GROSS (str): Represents the tax calculation based on gross income.
        NETTO (str): Represents the tax calculation based on net income.
        GROSS_UP (str): Represents the tax calculation using the grossing up method.
        MIX (str): Represents the tax calculation using the mix method.
    """

    GROSS = "GROSS"
    NETTO = "NETTO"
    GROSS_UP = "GROSS_UP"
    MIX = "MIX"


class InsurancePremiumComponent(Enum):
    """An enumeration representing different components of insurance premiums.

    Attributes:
        JKK (str): Represents the Job Security Insurance component.
        JKM (str): Represents the Death Insurance component.
        JHT (str): Represents the Old-Age Security component.
        JP (str): Represents the Pension Security component.
        JKP (str): Represents the Job Loss Security component.
        HEALTHCARE (str): Represents the Healthcare Insurance component.
    """

    JKK = "JKK"
    JKM = "JKM"
    JHT = "JHT"
    JP = "JP"
    JKP = "JKP"
    HEALTHCARE = "HEALTHCARE"


class PtkpCategoryCode(Enum):
    """Enumeration representing various types of PTKP (Penghasilan Tidak Kena Pajak - Non-Taxable Income) categories.

    Attributes:
        TK0 (str): Category for TK/0.
        TK1 (str): Category for TK/1.
        TK2 (str): Category for TK/2.
        TK3 (str): Category for TK/3.
        K0 (str): Category for K/0.
        K1 (str): Category for K/1.
        K2 (str): Category for K/2.
        K3 (str): Category for K/3.
    """

    TK0 = "TK/0"
    TK1 = "TK/1"
    TK2 = "TK/2"
    TK3 = "TK/3"
    K0 = "K/0"
    K1 = "K/1"
    K2 = "K/2"
    K3 = "K/3"


class GrossUpType(Enum):
    """An enumeration representing different types of gross up calculations.

    Attributes:
        VALUE (str): Represents a fixed value type of gross-up calculation.
        PERCENTAGE (str): Represents a percentage-based gross-up calculation.
    """

    VALUE = "VALUE"
    PERCENTAGE = "PERCENTAGE"


class BpjsJkk(Enum):
    """Enumeration representing various types of BPJS JKK categories.

    Attributes:
        NO (str): Represents no JKK.
        JKK024 (str): Represents JKK with a rate of 0.24%.
        JKK054 (str): Represents JKK with a rate of 0.54%.
        JKK089 (str): Represents JKK with a rate of 0.89%.
        JKK127 (str): Represents JKK with a rate of 1.27%.
        JKK174 (str): Represents JKK with a rate of 1.74%.
    """

    NO = "No"
    JKK024 = "JKK 1 (0.24%)"
    JKK054 = "JKK 2 (0.54%)"
    JKK089 = "JKK 3 (0.89%)"
    JKK127 = "JKK 4 (1.27%)"
    JKK174 = "JKK 5 (1.74%)"


BPJS_JKK_VALUE = {
    BpjsJkk.JKK024: 0.24,
    BpjsJkk.JKK054: 0.54,
    BpjsJkk.JKK089: 0.89,
    BpjsJkk.JKK127: 1.27,
    BpjsJkk.JKK174: 1.74,
    BpjsJkk.NO: 0,
    None: None,
}
