from dataclasses import dataclass
from typing import Optional
from typing import List

@dataclass
class Player:
    id: int
    team_id: int
    name: str
    age: int
    position: str # add player possition and team position
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

    #will hold list of player performance List[float]
    # list home goal: List[object] <- object will have player id(or name?), time scored
    # list away goal: List[object]
    # list home homes? List[object]
    # list away homes? List[object]
    # and do same for shots?

    exp_home_possession: int
    exp_home_shots: int
    exp_away_shots: int
    #who goal scorer is + time: list with int time and name scorer?

@dataclass
class MatchDay:
    home_team: Team
    away_team: Team

class MinuteEvent: 
    def __init__(self, minute, shooter):
        self.minute = minute
        self.shooter = shooter

        self.on_target = False
        self.goal = False

@dataclass
class MatchResult2:
    home_goals: int
    away_goals: int
    home_possession: int
    away_possession: int
    home_shots: int
    away_shots: int
    home_shotsT: int #shots on target
    away_shotsT: int
    home_tot_events: List[MinuteEvent]
    away_tot_events: List[MinuteEvent]

    #will hold list of player performance List[float]
    # list home goal: List[object] <- object will have player id(or name?), time scored
    # list away goal: List[object]
    # list home homes? List[object]
    # list away homes? List[object]
    # and do same for shots?
    exp_home_possession: int
    exp_home_shots: int
    exp_away_shots: int
    #who goal scorer is + time: list with int time and name scorer?
