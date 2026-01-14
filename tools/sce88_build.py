from validation.validator import instantiate_unit


def build() -> None:
    unit = instantiate_unit()
    unit.validate()
    for domain in unit.domains:
        print(f"{domain.name}: {len(domain.levels)} levels validated")


if __name__ == "__main__":
    build()
