from dataclasses import dataclass
from typing import Optional
from typing import List

@dataclass
class Player:
    id: int
    team_id: int
    name: str
    age: int
    position: str
    passing: int
    positioning: int
    
    foot: Optional[int] = None

    #for GK
    blocking: Optional[int] = None
    technique: Optional[int] = None

    #for field
    speed: Optional[int] = None
    physical: Optional[int] = None
    shooting: Optional[int] = None
    control: Optional[int] = None
    defense: Optional[int] = None

    rating: Optional[int] = None

@dataclass
class Team:
    id: int
    name: str
    '''attack: float
    defense: float
    midfield: float'''
    players: List[Player]#Optional[int] = None

    
    team_power: Optional[float] = None
    team_att: Optional[float] = None
    team_con: Optional[float] = None
    team_def: Optional[float] = None
    team_formation: Optional[str] = None
    


    

@dataclass
class MatchResult:
    home_goals: int
    away_goals: int
    home_possession: int
    away_possession: int
    home_shots: int
    away_shots: int
    home_shotsT: int #shots on target
    away_shotsT: int
    #who goal scorer is + time: list with int time and name scorer?
    

@dataclass
class MatchDay:
    home_team: Team
    away_team: Team