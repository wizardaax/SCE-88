from dataclasses import dataclass
from typing import List, Sequence
import sys


DOMAIN_NAMES = [
    "Domain A — Physical / Substrate",
    "Domain B — Control / Computational",
    "Domain C — Semantic / Interface",
    "Domain D — Temporal / Evolutionary",
]

LEVELS: Sequence[str] = [
    "Substrate Constraints",
    "Signal Transduction",
    "Temporal Ordering",
    "System Identification",
    "Actuation Control",
    "Uncertainty Modelling",
    "Stabilization Mechanisms",
    "Fault Correction",
    "Resolution Engine",
    "Constraint Compilation",
    "Execution Coordination",
    "Correctness Enforcement",
    "Integrity Assurance",
    "Structural Topology",
    "Environmental Awareness",
    "Inter-Instance Coordination",
    "Semantic Interface",
    "Adaptive Optimization",
    "Coherence Closure",
    "Self-Observation",
    "Intent Continuity",
    "External Compatibility",
]


@dataclass(frozen=True)
class Level:
    index: int
    name: str


@dataclass
class Domain:
    name: str
    levels: List[Level]

    def validate_ordering(self) -> None:
        expected_indices = list(range(1, 23))
        actual_indices = [level.index for level in self.levels]
        if actual_indices != expected_indices:
            raise ValueError(f"{self.name}: Levels must be strictly ordered 1–22")

        names = [level.name for level in self.levels]
        if names != list(LEVELS):
            raise ValueError(f"{self.name}: Level names must match canonical stack")

    def validate_closure(self) -> None:
        closure_level = next((l for l in self.levels if l.name == "Coherence Closure"), None)
        if closure_level is None or closure_level.index != 19:
            raise ValueError(f"{self.name}: Closure must be enforced at level 19")


@dataclass
class SCE88Unit:
    domains: List[Domain]

    def validate_domains(self) -> None:
        if len(self.domains) != 4:
            raise ValueError("Exactly four domains must be present")

        names = [d.name for d in self.domains]
        if names != DOMAIN_NAMES:
            raise ValueError("Domain names must match canonical set and order")

    def validate_isolation(self) -> None:
        for domain in self.domains:
            other_level_ids = {id(level) for d in self.domains if d is not domain for level in d.levels}
            overlap = {id(level) for level in domain.levels} & other_level_ids
            if overlap:
                raise ValueError(f"{domain.name}: Levels must not share instances across domains")

    def validate(self) -> None:
        self.validate_domains()
        for domain in self.domains:
            domain.validate_ordering()
            domain.validate_closure()
        self.validate_isolation()


def instantiate_unit() -> SCE88Unit:
    domains = []
    for domain_name in DOMAIN_NAMES:
        levels = [Level(index=i + 1, name=name) for i, name in enumerate(LEVELS)]
        domains.append(Domain(name=domain_name, levels=levels))
    return SCE88Unit(domains=domains)


def run_validation() -> None:
    unit = instantiate_unit()
    unit.validate()


def main(argv: Sequence[str] | None = None) -> int:
    try:
        run_validation()
        return 0
    except Exception as exc:  # pragma: no cover - explicit CI surface
        print(f"VALIDATION_FAILURE: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
