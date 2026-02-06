from enum import Enum
from datetime import datetime
from typing import List

from pydantic import BaseModel, ValidationError, Field, model_validator


class Rank(Enum):
    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: List[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def validate_mission_rules(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError('Mission ID must start with "M"')

        has_leader = False
        for member in self.crew:
            if member.rank == Rank.captain or member.rank == Rank.commander:
                has_leader = True
        if not has_leader:
            raise ValueError("Mission must have at least"
                             " one Commander" " or Captain")

        if self.duration_days > 365:
            exprienced = 0
            for member in self.crew:
                if member.years_experience >= 5:
                    exprienced += 1

            if exprienced < len(self.crew) / 2:
                raise ValueError("Not enough experienced crew")

        all_active = True
        for member in self.crew:
            if not member.is_active:
                all_active = False
        if not all_active:
            raise ValueError("All crew members must be active")

        return self


def print_mission(mission: SpaceMission) -> None:
    print("Valid mission created:")
    print(f"Mission: {mission.mission_name}")
    print(f"ID: {mission.mission_id}")
    print(f"Destination: {mission.destination}")
    print(f"Duration: {mission.duration_days} days")
    print(f"Budget: ${mission.budget_millions}M")
    print(f"Crew size: {len(mission.crew)}")
    print("Crew members:")
    for member in mission.crew:
        print(f"- {member.name} ({member.rank.value})"
              f"- {member.specialization}")


def main() -> None:
    print("Space Mission Crew Validation")
    print("=" * 41)

    mission = SpaceMission(
        mission_id="M2024_MARS",
        mission_name="Mars Colony Establishment",
        destination="Mars",
        launch_date="2026-03-01T09:00:00",
        duration_days=900,
        budget_millions=2500.0,
        crew=[
            CrewMember(
                member_id="CM001",
                name="Sarah Connor",
                rank=Rank.commander,
                age=38,
                specialization="Mission Command",
                years_experience=12,
                is_active=True,
            ),
            CrewMember(
                member_id="LT002",
                name="John Smith",
                rank=Rank.lieutenant,
                age=33,
                specialization="Navigation",
                years_experience=6,
                is_active=True,
            ),
            CrewMember(
                member_id="OF003",
                name="Alice Johnson",
                rank=Rank.officer,
                age=29,
                specialization="Engineering",
                years_experience=5,
                is_active=True,
            ),
        ],
    )
    print_mission(mission)
    print()
    print("=" * 41)

    try:
        SpaceMission(
            mission_id="M2026_TEST",
            mission_name="Test Mission",
            destination="Moon",
            launch_date="2026-04-01T10:00:00",
            duration_days=30,
            budget_millions=100.0,
            crew=[
                CrewMember(
                    member_id="CD001",
                    name="Test Cadet",
                    rank=Rank.cadet,
                    age=22,
                    specialization="Support",
                    years_experience=1,
                    is_active=True,
                )
            ],
        )
    except ValidationError as e:
        print("Expected validation error:")
        print(e.errors()[0]["msg"])


if __name__ == "__main__":
    main()
