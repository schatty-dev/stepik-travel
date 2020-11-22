import random
from django.shortcuts import render

from data import tours


def main_view(request):
    context_data = {}
    inds = list(range(1, 17))
    random.shuffle(inds)
    for i, tour_i in enumerate(inds[:6]):
        context_data[f"preview_{i+1}"] = {
                "title": tours[tour_i]["title"],
                "link": tours[tour_i]["picture"],
                "description": tours[tour_i]["description"][:80] + "...",
            }
    return render(request, "tours/index.html", context=context_data)


def departure_view(request, departure):
    return render(request, "tours/departure.html", context={"departure": departure})


def tour_view(request, id):
    context = tours.get(id)
    context["stars_str"] = "★" * int(context["stars"])
    if not context:
        return render(request, '404.html', status=400)
    return render(request, "tours/tour.html", context=context)


def handler404(request, exception):
    response = render(request, '404.html', status=400)
    return response


def handler500(request):
    response = render(request, '500.html', status=500)
    return response
