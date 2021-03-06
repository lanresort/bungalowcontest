"""
byceps.services.bungalow_contest.dbmodels.rating
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2021 Jochen Kupperschmidt
:License: Revised BSD (see `LICENSE` file for details)
"""

from datetime import datetime

from ....database import db, generate_uuid
from ....typing import UserID
from ....util.instances import ReprBuilder

from ...user.dbmodels.user import User

from ..transfer.models import AttributeID, ContestantID

from .contest import Contest
from .contestant import Contestant


class Attribute(db.Model):
    """A bungalow's attribute that can be rated."""
    __tablename__ = 'bungalow_contest_attributes'

    id = db.Column(db.Uuid, default=generate_uuid, primary_key=True)
    contest_id = db.Column(db.Uuid, db.ForeignKey('bungalow_contests.id'), index=True, nullable=False)
    contest = db.relationship(Contest, backref='attributes')
    title = db.Column(db.UnicodeText, nullable=False)

    def __init__(self, contest: Contest, title: str) -> None:
        self.contest = contest
        self.title = title

    def __repr__(self) -> str:
        return ReprBuilder(self) \
            .add('party', self.contest.party_id) \
            .add('title', self.title) \
            .build()


class Rating(db.Model):
    """A user's rating of a bungalow's attribute."""
    __tablename__ = 'bungalow_contest_ratings'
    __table_args__ = (
        db.UniqueConstraint('contestant_id', 'attribute_id', 'creator_id'),
    )

    id = db.Column(db.Uuid, default=generate_uuid, primary_key=True)
    contestant_id = db.Column(db.Uuid, db.ForeignKey('bungalow_contest_contestants.id'), index=True, nullable=False)
    contestant = db.relationship(Contestant, backref='ratings')
    attribute_id = db.Column(db.Uuid, db.ForeignKey('bungalow_contest_attributes.id'), index=True, nullable=False)
    attribute = db.relationship(Attribute)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    creator_id = db.Column(db.Uuid, db.ForeignKey('users.id'), nullable=False)
    creator = db.relationship(User)
    value = db.Column(db.Integer, nullable=False)

    def __init__(
        self,
        contestant_id: ContestantID,
        attribute_id: AttributeID,
        creator_id: UserID,
        value: int,
    ) -> None:
        self.contestant_id = contestant_id
        self.attribute_id = attribute_id
        self.creator_id = creator_id
        self.value = value
