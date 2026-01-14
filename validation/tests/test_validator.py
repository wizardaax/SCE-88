import pytest

from validation import validator


def test_instantiate_unit_has_four_domains():
    unit = validator.instantiate_unit()
    assert len(unit.domains) == 4
    assert [d.name for d in unit.domains] == validator.DOMAIN_NAMES


def test_each_domain_has_twenty_two_levels():
    unit = validator.instantiate_unit()
    for domain in unit.domains:
        assert len(domain.levels) == 22
        assert [l.index for l in domain.levels] == list(range(1, 23))
        assert [l.name for l in domain.levels] == list(validator.LEVELS)


def test_validate_success():
    unit = validator.instantiate_unit()
    unit.validate()  # should not raise


def test_isolation_enforced():
    shared_level = validator.Level(index=1, name=validator.LEVELS[0])
    domains = []
    for idx, name in enumerate(validator.DOMAIN_NAMES):
        levels = [validator.Level(index=i + 1, name=level_name) for i, level_name in enumerate(validator.LEVELS)]
        if idx in (0, 1):
            levels[0] = shared_level
        domains.append(validator.Domain(name=name, levels=levels))
    unit = validator.SCE88Unit(domains=domains)
    with pytest.raises(ValueError):
        unit.validate()


def test_validate_domains_count_and_names():
    unit = validator.instantiate_unit()
    unit.domains = unit.domains[:3]
    with pytest.raises(ValueError):
        unit.validate_domains()
    extra = validator.Domain(
        name="Domain X",
        levels=[validator.Level(index=i + 1, name=name) for i, name in enumerate(validator.LEVELS)],
    )
    unit.domains = validator.instantiate_unit().domains + [extra]
    with pytest.raises(ValueError):
        unit.validate_domains()
    reordered = list(reversed(validator.instantiate_unit().domains))
    unit.domains = reordered
    with pytest.raises(ValueError):
        unit.validate_domains()


def test_validate_ordering_and_names():
    domain = validator.Domain(
        name=validator.DOMAIN_NAMES[0],
        levels=[validator.Level(index=i + 1, name=name) for i, name in enumerate(validator.LEVELS)],
    )
    domain.levels[0] = validator.Level(index=2, name=validator.LEVELS[0])
    with pytest.raises(ValueError):
        domain.validate_ordering()
    domain.levels = [
        validator.Level(index=i + 1, name=(validator.LEVELS[i] if i != 1 else "Bad Name"))
        for i in range(len(validator.LEVELS))
    ]
    with pytest.raises(ValueError):
        domain.validate_ordering()
    domain.levels = []
    with pytest.raises(ValueError):
        domain.validate_ordering()


def test_validate_closure():
    domain = validator.Domain(
        name=validator.DOMAIN_NAMES[0],
        levels=[validator.Level(index=i + 1, name=name) for i, name in enumerate(validator.LEVELS)],
    )
    domain.levels[18] = validator.Level(index=18, name="Coherence Closure")
    with pytest.raises(ValueError):
        domain.validate_closure()
    domain.levels = [level for level in domain.levels if level.name != "Coherence Closure"]
    with pytest.raises(ValueError):
        domain.validate_closure()
    domain.levels = [validator.Level(index=i + 1, name=name) for i, name in enumerate(validator.LEVELS)]
    domain.validate_closure()
