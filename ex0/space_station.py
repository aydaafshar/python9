from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ValidationError


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: Optional[str] = Field(default=None, max_length=200)


def main() -> None:
    print("Space Station Data Validation")
    print("=" * 40)
    print()
    station = SpaceStation(
        station_id="ISS001",
        name="International Space Station",
        crew_size=6,
        power_level=85.5,
        oxygen_level=92.3,
        last_maintenance="2026-02-01T10:30:00",
        notes="All systems nominal.",
    )
    print("Valid station created:")
    print("ID:", station.station_id)
    print("Name:", station.name)
    print("Crew:", station.crew_size, "people")
    print("Power:", station.power_level, "%")
    print("Oxygen:", station.oxygen_level, "%")
    print("Status:", "Operational" if station.is_operational
          else "Not operational")
    print("=" * 40)

    try:
        SpaceStation(
            station_id="BAD01",
            name="Bad Station",
            crew_size=30,  # invalid
            power_level=50.0,
            oxygen_level=50.0,
            last_maintenance="2026-02-01T10:30:00",
        )
    except ValidationError as e:
        print("Expected validation error:")
        print(e)


if __name__ == "__main__":
    main()
