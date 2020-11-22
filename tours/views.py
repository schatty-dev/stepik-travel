import random
from django.shortcuts import render
from django.views.generic import DetailView

from data import tours

def get_random_ids(n=6, total=17,  start_from=1):
    inds = list(range(start_from, total))
    random.shuffle(inds)
    return inds[:6]


def get_ids_by_departure(departure):
    """ Return tour ids filtered by given departure. """
    return [k for k, v in tours.items() if v["departure"] == departure]


def main_view(request):
    context_data = {}
    for i, tour_i in enumerate(get_random_ids()):
        context_data[f"preview_{i+1}"] = {
                "title": tours[tour_i]["title"],
                "link": tours[tour_i]["picture"],
                "description": tours[tour_i]["description"][:80] + "...",
            }
    return render(request, "tours/index.html", context=context_data)


def departure_view(request, departure):
    ids = get_ids_by_departure(departure)

    context_data = {}
    for i, tour_i in enumerate(ids[:3]):
        context_data[f"preview_{i+1}"] = {
                "title": tours[tour_i]["title"],
                "link": tours[tour_i]["picture"],
                "description": tours[tour_i]["description"][:80] + "...",
            }
    context_data["departure"] = departure
 
    context_data["tours"] = []
    for id in ids:
        tour_data = tours[id]
        context_data["tours"].append(tour_data)
        context_data["tours"][-1]["stars_str"] = "★" * int(tour_data["stars"])
        context_data["tours"][-1]["link"] = f"/tour/{id}/"

    # General info
    context_data["num_tours"] = len(context_data["tours"])
    context_data["min_price"] = min([tour["price"] for tour in context_data["tours"]])
    context_data["max_price"] = max([tour["price"] for tour in context_data["tours"]])
    context_data["min_days"] = min([tour["nights"] for tour in context_data["tours"]])
    context_data["max_days"] = max([tour["nights"] for tour in context_data["tours"]])

    return render(request, "tours/departure.html", context=context_data)


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
