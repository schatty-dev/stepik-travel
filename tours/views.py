import random
from django.shortcuts import render

from data import tours, title, subtitle, description

DEP_NAMES = ["St. Petersburg",
             "Moscow",
             "Kazan",
             "Novosibirsk",
             "Ekaterinburg",]

DEP_PAGE = "departure"
DEP_CODES = ["spb",
             "msk",
             "kazan",
             "nsk",
             "ekb"]


def get_base_context():
    context = {
        "title": title,
        "header": [{"name": k, "link": f"/{DEP_PAGE}/{v}/"} for k, v in zip(DEP_NAMES, DEP_CODES)]
    }
    return context


def get_dep_name(dep_code):
    return DEP_NAMES[DEP_CODES.index(dep_code)]


def get_random_ids(n=6, total=17,  start_from=1):
    inds = list(range(start_from, total))
    random.shuffle(inds)
    return inds[:6]


def get_ids_by_departure(departure):
    """ Return tour ids filtered by given departure. """
    return [k for k, v in tours.items() if v["departure"] == departure]


def main_view(request):
    context_data = get_base_context()
    context_data["subtitle"] = subtitle
    context_data["description"] = description

    for i, tour_id in enumerate(get_random_ids()):
        context_data[f"preview_{i+1}"] = {
                "title": tours[tour_id]["title"],
                "img_link": tours[tour_id]["picture"],
                "description": tours[tour_id]["description"][:80] + "...",
                "link": f"/tour/{tour_id}/",
            }
    return render(request, "tours/index.html", context=context_data)


def departure_view(request, departure):
    context_data = get_base_context()

    ids = get_ids_by_departure(departure)
    for i, tour_id in enumerate(ids[:3]):
        context_data[f"preview_{i+1}"] = {
                "title": tours[tour_id]["title"],
                "img_link": tours[tour_id]["picture"],
                "description": tours[tour_id]["description"][:80] + "...",
                "link": f"/tour/{tour_id}/",
            }
    context_data["departure"] = get_dep_name(departure)

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
    context_data = get_base_context()

    tour_data = tours.get(id)
    if not tour_data:
        return render(request, '404.html', status=400)

    context_data = {**context_data, **tour_data}
    context_data["stars_str"] = "★" * int(context_data["stars"])
    return render(request, "tours/tour.html", context=context_data)


def handler404(request, exception):
    response = render(request, '404.html', status=400)
    return response


def handler500(request):
    response = render(request, '500.html', status=500)
    return response
