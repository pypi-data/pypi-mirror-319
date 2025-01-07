import json
from pathlib import Path

from oracle.display import Display
from oracle.model.choice import Choice
from oracle.model.group import ChoiceGroup, ChoiceGroupError


class Controller:
    def __init__(
        self, path: Path | str = Path.home() / ".oracle", display: Display | None = None
    ) -> None:
        self.path = Path(path) if isinstance(path, str) else path
        self.display = display if display else Display()
        self.group: ChoiceGroup = ChoiceGroup()

    def __enter__(self) -> "Controller":
        self.display.success("oracle is determining your fate")
        self.refresh()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save()
        self.display.success("oracle has looked into the future")

    def refresh(self) -> None:
        try:
            data = json.loads(self.path.read_text())
            self.group = ChoiceGroup(**data)
        except FileNotFoundError:
            self.group = ChoiceGroup()

    def save(self) -> None:
        self.path.write_text(self.group.model_dump_json())

    def generate_weights(self) -> list[int]:
        weights = [(choice.successes + 1) * (choice.trials + 1) for choice in self.group.choices]
        return weights

    def generate_result(self, verbose: bool = False) -> None:
        try:
            weights = self.generate_weights()
            result = self.group.get_result(weights)
            self.display.info(f"oracle has chosen '{result.name}' as your future")
            if verbose:
                for weight, option in zip(weights, self.group.choices):
                    self.display.diagnostic(f"option:{option.name}")
                    self.display.diagnostic(f"weight:{weight}")
                self.display.diagnostic(f"total:{sum(weights)}")
        except ChoiceGroupError as e:
            self.display.confused("oracle has failed to scry your future")
            self.display.warning("oracle cannot guide you")

    def generate_trial(self) -> tuple[Choice, Choice] | None:
        try:
            options = self.group.get_pair()
            for i, option in enumerate(options):
                self.display.indexed(i, option.name)
            self.display.confused("which do you choose?")
            return options
        except ChoiceGroupError as e:
            self.display.confused("oracle needs to be aware of more possibilities for your future")
            self.display.warning("oracle cannot guide you")

    def update_choices(self, add: str | None = None, remove: str | None = None) -> None:
        try:
            if add:
                self.group.add(add)
            if remove:
                self.group.remove(remove)
            self.display.success("oracle is scrying your choices")
        except ChoiceGroupError as e:
            self.display.confused(str(e))


class ControllerError(Exception):
    pass
