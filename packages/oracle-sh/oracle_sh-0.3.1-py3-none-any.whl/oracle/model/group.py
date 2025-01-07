from dataclasses import field
import random
from typing import List

from pydantic import BaseModel
from pydantic.main import TupleGenerator

from oracle.model.choice import Choice


class ChoiceGroup(BaseModel):
    name: str = "oracle"
    choices: List[Choice] = field(default_factory=list)

    def __len__(self) -> int:
        return len(self.choices)

    def add(self, name: str, trials: int = 0, successes: int = 0) -> None:
        current_choices = [choice.name for choice in self.choices]
        if name in current_choices:
            raise ChoiceGroupError(f"{name} is already a choice")
        self.choices.append(Choice(name=name, trials=trials, successes=successes))

    def remove(self, name: str) -> None:
        for i, choice in enumerate(self.choices):
            if name == choice.name:
                del self.choices[i]
                break
        else:
            raise ChoiceGroupError(f"{name} is not a choice")

    def reset(self) -> None:
        for choice in self.choices:
            choice.reset()

    def get_pair(self) -> tuple[Choice, Choice]:
        if len(self) < 2:
            raise ChoiceGroupError("not enough choices to make a pair")

        first, second = Choice(), Choice()
        while first == second:
            first, second = random.sample(self.choices, k=2)
        return first, second

    def get_result(self, weights: list[int]) -> Choice:
        if len(self) < 2:
            raise ChoiceGroupError("not enough choices to assess")
        if sum(weights) == 0:
            raise ChoiceGroupError("not enough trials to assess")

        result = random.sample(self.choices, k=1, counts=weights)[0]
        return result


class ChoiceGroupError(Exception):
    pass
