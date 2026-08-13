# Waypoint

Waypoint is my individual term project for Application Programming.

I began the project as a pure-Python object-oriented domain engine and am developing it into a Django trail-finder and
trip-planner website.

## Current development stage

Week 10 — Django pages, URLs, and trail-report form.

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

### Django setup

The project currently includes:

- A virtual environment named `env`
- Django 4.2
- The `waypoint` Django project
- SQLite for local development
- An importable `waypoint_core` package
- A working Django development server

### Week 10 web features

The Django website currently includes:

- A styled Waypoint homepage
- A greeting passed to the homepage through a context variable
- Project-level templates and static CSS
- A trail-report form with name, email, trail, and note fields
- CSRF protection for the report form
- A personalized thank-you page after a successful report
- Server-side validation that rejects an empty or whitespace-only note
- A friendly validation error that keeps the previously entered form values
- A search page that safely reads the `q` query parameter
- Home, report, and search URL routes

My local environment was verified using Python 3.12.13 and Django 4.2.30.

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
│   ├── home.html
│   ├── report.html
│   ├── search.html
│   └── thank_you.html
├── tests/
│   ├── __init__.py
│   ├── test_distance.py
│   ├── test_itinerary.py
│   ├── test_mixins.py
│   ├── test_reporting.py
│   ├── test_trail.py
│   └── test_trail_types.py
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

## Python and Django versions

I use Python 3.12 because it is compatible with the required Django 4.2 release.

The `requirements.txt` file contains:

```text
Django>=4.2,<4.3
```

## Setup from a fresh clone

Clone the repository and enter the project folder:

```bash
git clone https://github.com/Kavithanair2/Waypoint.git
cd Waypoint
```

Confirm that Python 3.12 is active:

```bash
python --version
```

Create the required virtual environment:

```bash
python -m venv env
```

Activate the virtual environment on macOS:

```bash
source env/bin/activate
```

On Windows PowerShell:

```powershell
.\env\Scripts\Activate.ps1
```

Install the project requirements:

```bash
python -m pip install -r requirements.txt
```

Apply the Django migrations:

```bash
python manage.py migrate
```

Check the Django configuration:

```bash
python manage.py check
```

Start the Django development server:

```bash
python manage.py runserver
```

Open the following address in a browser:

```text
http://127.0.0.1:8000/
```

At the current development stage, the Waypoint homepage should load with the "Welcome to Waypoint" heading.

Stop the development server by pressing `Control + C` in the Terminal.

## Website routes

- `/` — displays the Waypoint homepage.
- `/report/` — displays the trail-report form.
- `/search/` — displays the trail search page.
- `/search/?q=Pine` — shows the submitted search query.
- `/admin/` — displays the Django administration login page.

## Run the domain tests

The pure-Python tests are stored in the top-level `tests` directory.

Run them from the repository root:

```bash
python -m unittest discover -s tests -v
```

The current domain test suite contains 45 tests.

A successful run should finish with:

```text
Ran 45 tests

OK
```

## Verify the domain package

The domain engine is stored in the `waypoint_core` package so that it can be reused by the Django application in later
parts of the project.

With the virtual environment active, run:

```bash
python -c "import waypoint_core"
```

A successful import returns to the command prompt without an error.

## Verify virtual-environment isolation

The Django installation should only be available inside the project virtual environment.

Deactivate the virtual environment:

```bash
deactivate
```

Then run:

```bash
django-admin --version
```

If Django is isolated correctly, `django-admin` should not be available outside the virtual environment.

Reactivate the environment on macOS with:

```bash
source env/bin/activate
```

## Domain design

### Distance

`Distance` represents a non-negative distance in kilometres or miles. It supports validation, unit conversion,
arithmetic, comparisons, and sorting.

For mixed-unit arithmetic, I convert the right-hand distance to the unit of the left-hand `Distance` before performing the
calculation.

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

### DayHike

I calculate the estimated time for a `DayHike` using a hiking pace of 4 km/h and add one hour for every 600 metres of elevation gain.

### BackpackingRoute

I calculate the estimated time for a `BackpackingRoute` using a hiking pace of 3 km/h, adding one hour for every 500 metres of elevation gain and 30 minutes for each overnight stop.

### TrailRun

I calculate the estimated time for a `TrailRun` using a running pace of 8 km/h and add one hour for every 800 metres of elevation gain.

### GuidedDayHike

`GuidedDayHike` inherits the `DayHike` estimated-time calculation. I added guide information to the subclass without changing the time calculation.

## Django project files

The Django `startproject` command created the main `waypoint` project package.

The main generated files are:

- `manage.py` — runs Django management commands such as migrations and the development server.
- `waypoint/settings.py` — contains the main Django project configuration.
- `waypoint/urls.py` — contains the project's URL routing.
- `waypoint/wsgi.py` — provides the WSGI application entry point.
- `waypoint/asgi.py` — provides the ASGI application entry point.
- `waypoint/__init__.py` — makes the `waypoint` directory a Python package.

The Week 10 web files include:

- `waypoint/views.py` — contains the home, report, and search view functions.
- `templates/home.html` — displays the Waypoint homepage and context-variable greeting.
- `templates/report.html` — displays and submits the trail-report form with CSRF protection.
- `templates/thank_you.html` — displays the personalized report confirmation.
- `templates/search.html` — displays the trail search form and query.
- `static/style.css` — provides the shared Week 10 page styling.


I kept the Django project separate from `waypoint_core` so that the existing Python domain logic can be reused by the
web application.

## Git ignored files

The `.gitignore` currently excludes:

```text
env/
db.sqlite3
__pycache__/
```

The virtual environment contains locally installed packages, while `db.sqlite3` is the local development database. These
files do not need to be stored in the repository.

## Troubleshooting

### Django is unavailable

Make sure the virtual environment is active.

On macOS:

```bash
source env/bin/activate
```

The Terminal prompt should normally begin with:

```text
(env)
```

Check the installed Django version:

```bash
python -m django --version
```

### `ModuleNotFoundError: waypoint_core`

Make sure the command is being run from the repository root.

Verify the package with:

```bash
python -c "import waypoint_core"
```

A successful command returns without an error.

### Database has not been initialized

Run:

```bash
python manage.py migrate
```

This applies Django's migrations and creates the local SQLite database.

### `TemplateDoesNotExist`

Confirm that `waypoint/settings.py` contains the project-level template directory and that the required HTML file exists inside `templates/`.

### Report form returns `403 Forbidden`

Confirm that the POST form contains:

```django
{% csrf_token %}
```

## Current project status

The Week 7 domain model and the Week 8 inheritance, polymorphism, mixins, and operator features are complete and merged.

For Week 9, I created the Django 4.2 project and verified that it runs inside the isolated `env` virtual environment. The fresh-clone setup was also verified.

For Week 10, I added the Waypoint homepage, project-level templates and static CSS, the trail-report form, CSRF protection, a personalized thank-you page, and a safe search view. I also completed the optional server-side validation that rejects an empty or whitespace-only note and shows a friendly error.

The Week 10 pages were tested in the browser, Django's system check passed, and all 45 existing domain tests still pass.
