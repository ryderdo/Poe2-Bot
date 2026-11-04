# Party leader lookup helper

A small, standalone Python helper for identifying a leader from party data already obtained by a caller. It does not read the screen, connect to the game, send inputs, or automate movement.

`find_party_leader(members)` expects one party member with `is_leader: true`. It returns a normalized immutable `PartyMember` containing the name and optional area. Pass `preferred_name="Name"` to intentionally select a named party member instead. Invalid, empty, missing, or ambiguous data raises `PartyDataError` rather than silently selecting the wrong person.

Example:

```python
from party_leader import find_party_leader

party = [
    {"ign": "Mira", "is_leader": False, "area_raw_name": "Hideout"},
    {"ign": "Aster", "is_leader": True, "area_raw_name": "MapBloomingField"},
]
leader = find_party_leader(party)
print(leader.name, leader.area)
```

Run tests with Python 3.10+:

```sh
python -m unittest -v
```

The repository did not have an existing application/framework structure when this helper was added. Integrating a data source requires a separate adapter that supplies trusted party-member records.
