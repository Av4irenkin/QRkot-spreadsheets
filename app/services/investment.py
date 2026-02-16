from app.models.investment import Investment


def invest_funds(
    target: Investment,
    sources: list[Investment]
) -> list[Investment]:
    changed_sources = list()
    for source in sources:
        changed_sources.append(source)
        transfer = min(
            target.full_amount - target.invested_amount,
            source.full_amount - source.invested_amount,
        )
        for obj in source, target:
            obj.invested_amount += transfer
            obj.close_if_fully_invested()
        if target.fully_invested:
            break
    return changed_sources
