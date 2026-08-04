# Waypoint

Waypoint is a trail-finder and trip-planner project developed with Python and Django.

The project begins with a pure-Python domain engine and will later be expanded into a Django web application.

## Week 7 domain model

The Week 7 implementation includes three main classes:

### Distance

Distance represents a non-negative distance measured in kilometres or miles.

It provides:

- Magnitude and unit validation
- Read-only `magnitude` and `unit` properties
- Conversion between kilometres and miles
- Rejection of negative distances and unsupported units

### Trail

Trail represents an individual trail.

It provides:

- A unique trail ID
- A name
- A Distance object
- Elevation gain in metres
- A validated difficulty
- A default-unit class variable
- A `from_dict()` alternate constructor
- Static validation methods
- Equality based on trail ID

Allowed difficulty values are:

- easy
- moderate
- hard
- expert

### Itinerary

Itinerary contains an ordered collection of Trail objects.

It provides:

- `add_trail()` for adding trails
- Independent trail lists for each itinerary
- Total-distance calculation
- Conversion of mixed units into a selected unit
- Protection against adding non-Trail objects

## Project structure

```text
Waypoint/
├── README.md
├── waypoint_core/
│   ├── __init__.py
│   ├── distance.py
│   ├── itinerary.py
│   └── trail.py
└── tests/
    ├── __init__.py
    ├── test_distance.py
    ├── test_itinerary.py
    └── test_trail.py
```

## Run the Week 7 tests

Open Terminal in the repository root and run:

```bash
python3 -m unittest discover -s tests -v
```

A successful run should finish with:

```text
Ran 18 tests

OK
```

## Week 7 design decisions

- Distance conversion returns a new object instead of modifying the original Distance.
- Trail difficulty is changed through `set_difficulty()` so invalid values cannot be assigned.
- Trail equality uses `trail_id` because the ID represents trail identity.
- `Trail.from_dict()` uses the current default unit when the dictionary does not include a unit.
- Each Itinerary creates its own internal list, avoiding shared mutable default arguments.
- Mixed-unit itinerary totals convert every trail into one selected unit before adding the values.

## Current project status

Week 7 domain implementation is complete locally.

The GitHub pull request, review, merge and `v7` tag remain manual workflow steps.
