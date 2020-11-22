from django.shortcuts import render

from data import tours


def main_view(request):
    return render(request, "tours/index.html")


def departure_view(request, departure):
    return render(request, "tours/departure.html", context={"departure": departure})


def tour_view(request, id):
    context = tours.get(id)
    print("context: ", context)
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
