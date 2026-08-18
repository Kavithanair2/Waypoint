# Waypoint

Waypoint is my individual term project for Application Programming.

I began the project as a pure-Python object-oriented domain engine and am developing it into a Django trail-finder and
trip-planner website.

## Project status

Waypoint is currently developed through Week 13. The latest work connects Trails and Parks using a Django `ForeignKey`.
Parks can be managed through Django Admin, assigned to Trails, and used to display related Trail information.

## Technology

Waypoint uses:

- Python 3.12
- Django 4.2
- SQLite
- HTML
- CSS
- Git and GitHub

## Current features

### Domain engine

The current Python domain engine includes:

- Distance validation, unit conversion, arithmetic, and comparisons
- An abstract trail hierarchy with different trail types
- Method overriding and use of `super()`
- Mixins and multiple inheritance
- Polymorphism and duck typing
- Itinerary management and total-distance calculation
- Automated domain tests

### Django web application

The Django website includes:

- A styled Waypoint homepage
- Shared templates and static CSS
- A reusable `base.html` layout with navbar and footer partials
- Home, report, search, and thank-you pages that use the shared layout
- A trail-report form with CSRF protection
- Server-side validation for empty or whitespace-only report notes
- A personalized thank-you page after a successful report
- A search page that safely reads the `q` query parameter
- A trail catalog rendered with template loops and conditionals
- Automatic row numbering using `forloop.counter`
- Distance formatting using `floatformat:1`

### Database and relationships

The Django application includes:

- Database-backed `Trail` and `Park` models
- A `ForeignKey` relationship between Trails and Parks
- Django Admin support for managing Trails and Parks
- Park assignment for Trail records
- A `/trails/` catalog showing open Trails ordered by distance
- Park information in the public trail catalog
- A Trail detail page with an estimated hiking time
- A park detail page showing related Trails
- Django migrations for the Trail schema and Park relationship

## Database models

### Park

The `Park` model stores:

- `name`
- `region`

### Trail

The Django `Trail` model stores:

- `name`
- `park`
- `distance_km`
- `elevation_gain`
- `difficulty`
- `is_open`
- `added`

### Trail-to-Park relationship

Each `Trail` can be linked to a `Park` using a Django `ForeignKey`.

The relationship uses `SET_NULL` with `null=True` so existing Trail records could be migrated without requiring a Park
immediately. It also means that if a Park is deleted, the related Trail records are preserved and their Park value
becomes empty instead of deleting the Trails.

I did not add a custom `related_name`, so Django's default reverse relation is available through:

```python
park.trail_set
```

## Requirements

Before setting up Waypoint, make sure the following are available:

- Python 3.12
- Git
- A terminal or command-line application

## Setup from a fresh clone

The following steps are written primarily for macOS. A Windows PowerShell activation command is included where it
differs.

### 1. Clone the repository

```bash
git clone https://github.com/Kavithanair2/Waypoint.git
cd Waypoint
```

### 2. Check the Python version

```bash
python --version
```

Python 3.12 is used for this project.

### 3. Create the virtual environment

```bash
python -m venv env
```

### 4. Activate the virtual environment

On macOS:

```bash
source env/bin/activate
```

On Windows PowerShell:

```powershell
.\env\Scripts\Activate.ps1
```

### 5. Install the requirements

```bash
python -m pip install -r requirements.txt
```

### 6. Apply the migrations

```bash
python manage.py migrate
```

### 7. Check the Django configuration

```bash
python manage.py check
```

### 8. Start the development server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

The Waypoint homepage should load with the **Welcome to Waypoint** heading.

Stop the server with `Control + C`.

## Django Admin

A fresh clone does not include my local Django administrator account or local Trail and Park data because `db.sqlite3`
is not stored in Git.

Create a local administrator with:

```bash
python manage.py createsuperuser
```

Follow the prompts to create a username, optional email address, and password.

Start the development server:

```bash
python manage.py runserver
```

Open Django Admin at:

```text
http://127.0.0.1:8000/admin/
```

Create a Park first, then create or edit Trail records and assign them to a Park. The data created through Django Admin
is stored only in the local SQLite database.

## Website routes

- `/` – Waypoint homepage
- `/report/` – trail-report form
- `/search/` – trail search
- `/search/?q=Pine` – example search query
- `/catalog/` – earlier Week 11 template-based trail catalog
- `/trails/` – current database-backed trail catalog showing only open trails
- `/trails/<id>/` – individual trail detail page with an estimated hiking time
- `/trails/parks/<id>/` – park detail page showing the trails assigned to the selected park
- `/admin/` – Django administration login

## Testing and verification

The pure-Python test suite is stored in the top-level `tests` directory.

Run the tests from the repository root with:

```bash
python -m unittest discover -s tests -v
```

The current domain test suite contains 45 tests. A successful run should finish with:

```text
Ran 45 tests

OK
```

For Week 13, I also ran `python manage.py check` and tested the project from a fresh clone to confirm that both
migrations applied successfully.

In the browser, I checked that Parks could be added in Django Admin, Trails could be assigned to Parks, the trail
catalog displayed the correct Park, and the park detail page showed the related Trails.

### Verify the domain package

The domain engine is stored in the `waypoint_core` package so it can be reused by the Django application.

With the virtual environment active, run:

```bash
python -c "import waypoint_core"
```

A successful import returns to the command prompt without an error.

## Domain design

### Trail class distinction

Waypoint contains two classes named `Trail`, but they serve different purposes.

- `waypoint_core.Trail` is the pure-Python abstract class used for the object-oriented domain engine. It demonstrates
  abstraction, inheritance, polymorphism, and method overriding.
- `trails.models.Trail` is the Django ORM model used to store trail records in the SQLite database.

Keeping these responsibilities separate allows the existing Python domain logic to be reused while Django handles
database persistence.

### Distance

`Distance` represents a non-negative distance in kilometres or miles. It supports validation, unit conversion,
arithmetic, comparisons, and sorting.

For mixed-unit arithmetic, I convert the right-hand distance to the unit of the left-hand `Distance` before performing the calculation.

For example:

```text
Distance(5, "km") + Distance(1, "mi") → result in kilometres
Distance(5, "mi") + Distance(1, "km") → result in miles
```

Equality and ordering also account for different units.

Subtraction raises `ValueError` if the result would be negative.

### Trail hierarchy

`Trail` is an abstract base class that defines the common behaviour for the different trail types.

The current hierarchy is:

```text
Trail
├── DayHike
│   ├── GuidedDayHike
│   └── ManagedDayHike
├── BackpackingRoute
└── TrailRun
```

Each concrete trail type provides its own `estimated_time()` and `summary()` behaviour.

`GuidedDayHike` extends `DayHike` and inherits its existing behaviour.

`BackpackingRoute` overrides `packing_list()` and uses `super()` to keep the common trail equipment before adding the
extra items needed for backpacking.

### Itinerary

`Itinerary` stores an ordered collection of trails and calculates their total distance.

Each itinerary keeps its own internal trail list, so adding a trail to one itinerary does not affect another.

### Other domain rules

- Trail difficulty is checked against the allowed difficulty values.
- Two trails are considered equal when they have the same `trail_id`.
- `Trail.from_dict()` can be used to create a trail from dictionary data.
- `Trail` keeps a class-level default distance unit and uses static methods for validation.

### Mixins and polymorphism

`ManagedDayHike` combines `PermitRequiredMixin` and `SeasonalAccessMixin` with `DayHike`.
Because `ManagedDayHike` uses multiple inheritance, Python follows this method resolution order (MRO):

```text
ManagedDayHike
→ SeasonalAccessMixin
→ PermitRequiredMixin
→ DayHike
→ Trail
→ ABC
→ object
```

The reporting function processes different trail types through the same `summary()` and `estimated_time()` methods.

A `FakeTrail` that does not inherit from `Trail` is also used in testing. This demonstrates duck typing because the
reporting function works as long as the object provides the required methods.

## Estimated-time calculations

The pure-Python trail classes use simple estimated-time calculations based on distance, elevation gain, and trail type.

- **DayHike** – uses a hiking pace of 4 km/h and adds one hour for every 600 metres of elevation gain.
- **BackpackingRoute** – uses a hiking pace of 3 km/h, adds one hour for every 500 metres of elevation gain, and adds 30
  minutes for each overnight stop.
- **TrailRun** – uses a running pace of 8 km/h and adds one hour for every 800 metres of elevation gain.
- **GuidedDayHike** – inherits the `DayHike` estimated-time calculation without changing it.

## Key project files

- `manage.py` – runs Django management commands such as migrations, checks, tests, and the development server.
- `waypoint/settings.py` – contains the main Django project configuration.
- `waypoint/urls.py` – contains the main project URL routing.
- `waypoint/views.py` – contains the homepage, report, search, and earlier catalog views.
- `trails/models.py` – defines the database-backed `Trail` and `Park` models.
- `trails/admin.py` – configures Trail and Park management in Django Admin.
- `trails/views.py` – provides the database-backed trail catalog, trail detail, and park detail views.
- `trails/urls.py` – defines the routes for the `trails` application.
- `templates/base.html` – provides the shared page layout.
- `templates/catalog.html` – displays the database-backed trail catalog.
- `templates/trail_detail.html` – displays information for an individual trail.
- `templates/park_detail.html` – displays a park and its related trails.
- `waypoint_core/` – contains the reusable pure-Python domain engine.
- `tests/` – contains the pure-Python automated test suite.

The Django application is kept separate from `waypoint_core` so the original object-oriented domain logic can remain
reusable while Django handles the web interface and database persistence.

## Project structure

```text
Waypoint/
├── .gitignore
├── README.md
├── manage.py
├── requirements.txt
├── static/
│   └── style.css
├── templates/
│   ├── base.html
│   ├── catalog.html
│   ├── home.html
│   ├── park_detail.html
│   ├── partials/
│   │   ├── footer.html
│   │   └── navbar.html
│   ├── report.html
│   ├── search.html
│   ├── thank_you.html
│   └── trail_detail.html
├── tests/
│   ├── __init__.py
│   ├── test_distance.py
│   ├── test_itinerary.py
│   ├── test_mixins.py
│   ├── test_reporting.py
│   ├── test_trail.py
│   └── test_trail_types.py
├── trails/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   │   ├── __init__.py
│   │   ├── 0001_initial.py
│   │   └── 0002_park_trail_park.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── waypoint/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── views.py
│   └── wsgi.py
└── waypoint_core/
    ├── __init__.py
    ├── distance.py
    ├── itinerary.py
    ├── mixins.py
    ├── reporting.py
    ├── trail.py
    └── trail_types.py
```

## Local development files

The following local files and folders are intentionally excluded from Git:

```text
env/
db.sqlite3
__pycache__/
```

The `env/` folder contains locally installed Python packages, while `db.sqlite3` contains the local development
database.

Because `db.sqlite3` is not committed, a fresh clone starts with an empty application database after migrations are
applied. Local administrator accounts, Parks, and Trail records must therefore be created again when needed.

## Git workflow

I use a separate Git branch for each project week. After the work is completed and self-reviewed, the branch is merged into `main`.

Branches used so far:

```text
week-07-domain-model
week-08-hierarchy-and-operators
week-09-django-setup
week-10-views-urls-forms
week-11-template-language
week-12-orm-and-admin
week-13-relationships-and-foreignkeys
```

Milestone tags created so far:

```text
v7
v8
v9
v10
v11
v12
```

## Troubleshooting

### Django is unavailable

Make sure the virtual environment is active:

```bash
source env/bin/activate
```

Then check the installed Django version:

```bash
python -m django --version
```

### `ModuleNotFoundError: waypoint_core`

Make sure you are running the command from the project root.

You can verify the package with:

```bash
python -c "import waypoint_core"
```

A successful import returns to the command prompt without an error.

### Database has not been initialized

Run:

```bash
python manage.py migrate
```

This creates the local SQLite database and applies the project migrations.

### `TemplateDoesNotExist`

Check that the required template file exists inside the `templates/` folder and that the project template directory is
configured in `waypoint/settings.py`.

### Report form returns `403 Forbidden`

Make sure the POST form contains:

```django
{% csrf_token %}
```
