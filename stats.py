
class PlayerStats:
    def __init__(self) -> None:
        self.role: str
        self.ident: str
        self.max_clicks: int
        self.current_click: int = 1
        self.current_credits: int = 5

    def increment_click(self):
        self.current_click = 1 if self.current_click == self.max_clicks else self.current_click + 1

    def decrement_click(self):
        self.current_click = self.max_clicks if self.current_click == 1 else self.current_click - 1


class CorpStats(PlayerStats):
    def __init__(self) -> None:
        super().__init__()
        self.bad_publicity: int = 0
        self.role = 'Corp'
        self.max_clicks = 3


class RunnerStats(PlayerStats):
    def __init__(self) -> None:
        super().__init__()
        self.tags: int = 0
        self.brain_damage: int = 0
        self.role = 'Runner'
        self.max_clicks = 4
