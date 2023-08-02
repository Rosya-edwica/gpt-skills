import dataclasses


@dataclasses.dataclass(slots=True)
class Pair:
    Id: int
    Skill1: str
    Skill2: str
    IsDuplicate: bool | None
