from dataclasses import dataclass


@dataclass(kw_only=True)
class Dirnames:
    configs: str = 'configs'
    results: str = 'results'

dirnames = Dirnames()
