"""
byceps.services.bungalow_contest.transfer.models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2021 Jochen Kupperschmidt
:License: Revised BSD (see `LICENSE` file for details)
"""

from dataclasses import dataclass
from enum import Enum
from typing import NewType
from uuid import UUID


ContestID = NewType('ContestID', UUID)


ContestantID = NewType('ContestantID', UUID)


AttributeID = NewType('AttributeID', UUID)


Phase = Enum(
    'Phase',
    [
        'not_started',
        'registration',
        'rating',
        'ended',
    ],
)


@dataclass(frozen=True)
class AggregatedAttributeRating:
    average_value: float
    rating_count: int
