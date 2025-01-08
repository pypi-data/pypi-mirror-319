import uuid
from typing import Optional

from sqlmodel import Field, Relationship

from support_sphere.models.base import BasePublicSchemaModel


class People(BasePublicSchemaModel, table=True):

    """
    Represents an individual in the 'public.people' table.
    An individual represented as a row in this table,
    may or may NOT have an account in (auth.users) or profile in (user_profiles)

    Attributes
    ----------
    id : uuid.UUID
        The unique identifier for the individual, generated automatically using UUID.
    user_profile_id : uuid.UUID|None, optional
        A foreign key linking to the `user_profiles` table in the `public` schema. It is nullable
        and must be unique, allowing only one person per user profile. Only present if the person also has an account.
    given_name : str|None, optional
        The given name (first name) of the individual.
    family_name : str|None, optional
        The family name (last name) of the individual.
    nickname : str|None, optional
        A nickname for the individual.
    is_safe : bool
        Indicates whether the person is marked as safe, defaults to True.
    needs_help : bool
        Indicates whether the person is flagged as needing help, defaults to False.
    user_profile : Optional[UserProfile]
        A relationship to the `UserProfile` model, with back_populates set to "person_details",
        linking an individual to their user profile if available.
        This is NOT a column in the table but represents relationship only.
    people_group : Optional[PeopleGroup]
        A relationship to the `PeopleGroup` model, with back_populates set to "people",
        linking an individual to a particular household.
        This is NOT a column in the table but represents relationship only.
    """
    __tablename__ = "people"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_profile_id: uuid.UUID|None = Field(foreign_key="public.user_profiles.id", nullable=True, unique=True)

    given_name: str|None = Field(nullable=True)
    family_name: str|None = Field(nullable=True)
    nickname: str|None = Field(nullable=True)
    is_safe: bool = Field(default=True)
    needs_help: bool = Field(default=False)

    user_profile: Optional["UserProfile"] = Relationship(back_populates="person_details", cascade_delete=False)
    people_group: Optional["PeopleGroup"] = Relationship(back_populates="people", cascade_delete=False)
