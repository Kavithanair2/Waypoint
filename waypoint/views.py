from django.shortcuts import render


def home(request):
    context = {
        "greeting": "Welcome to Waypoint"
    }
    return render(request, "home.html", context)


def report(request):
    if request.method == "POST":
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        trail = request.POST.get("trail", "")
        note = request.POST.get("note", "").strip()

        if not note:
            context = {
                "error": "Please enter a note about the trail.",
                "name": name,
                "email": email,
                "trail": trail,
                "note": note,
            }
            return render(request, "report.html", context)

        context = {
            "name": name,
            "email": email,
            "trail": trail,
            "note": note,
        }
        return render(request, "thank_you.html", context)

    return render(request, "report.html")


def search(request):
    query = request.GET.get("q", "")

    context = {
        "query": query
    }
    return render(request, "search.html", context)

def catalog(request):
    trails = [
        {
            "name": "Pine Ridge Trail",
            "distance": 8.4,
            "elevation": 320,
            "difficulty": "moderate",
            "is_open": True,
        },
        {
            "name": "Maple Loop",
            "distance": 4.2,
            "elevation": 120,
            "difficulty": "easy",
            "is_open": True,
        },
        {
            "name": "Eagle Summit",
            "distance": 12.7,
            "elevation": 850,
            "difficulty": "expert",
            "is_open": True,
        },
        {
            "name": "Cedar Valley Trail",
            "distance": 6.5,
            "elevation": 240,
            "difficulty": "moderate",
            "is_open": False,
        },
        {
            "name": "Lakeview Path",
            "distance": 3.8,
            "elevation": 90,
            "difficulty": "easy",
            "is_open": True,
        },
        {
            "name": "Rocky Pass",
            "distance": 10.3,
            "elevation": 700,
            "difficulty": "expert",
            "is_open": False,
        },
    ]

    return render(request, "catalog.html", {"trails": trails})
