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
    unit = validator.instantiate_unit()
    # Introduce a crossing level to trigger failure
    mutated = unit.domains[0].levels[0]
    unit.domains[1].levels[0] = mutated  # type: ignore[attr-defined]
    with pytest.raises(ValueError):
        unit.validate()
