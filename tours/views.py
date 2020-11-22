import json
from django.shortcuts import render

with open("data/tours.json", "r") as f:
    TOUR_DATA = json.load(f)


def main_view(request):
    return render(request, "tours/index.html")


def departure_view(request, departure):
    return render(request, "tours/departure.html", context={"departure": departure})


def tour_view(request, id):
    context = TOUR_DATA.get(str(id))
    if not context:
        return render(request, '404.html', status=400)
    return render(request, "tours/tour.html", context=context)


def handler404(request, exception):
    response = render(request, '404.html', status=400)
    return response


def handler500(request):
    response = render(request, '500.html', status=500)
    return response
