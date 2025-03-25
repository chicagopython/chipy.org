from django.shortcuts import render

from .models import CustomFlatPage


def custom_flatpage_view(request, url):
    flatpage = CustomFlatPage.objects.filter(url=url).first()
    if not flatpage:
        return render(request, "404.html", status=404)
    return render(request, "shiny/slim.html", {"flatpage": flatpage})
