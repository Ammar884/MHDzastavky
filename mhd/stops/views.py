from datetime import date, datetime
from collections import defaultdict

import pandas
import gtfs_kit
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

from .models import Station
from .forms import StationForm



def index(request):
    stations = Station.objects.filter(user_id=request.user.id)
    return render(request, "index.html", {"stations": stations})

def registration(request):
    if request.method == "POST":
        
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
        
    return render(request, "registration/registration.html", {"form": form})


@login_required
def add_item(request):
    if request.method == "POST":
        form = StationForm(request.POST)
        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.identifiers = ",".join(form.identifiers) 
            instance.save()
            messages.add_message(request, messages.INFO, "Zastávka byla přidána")
            return redirect("index") #zmenit pozdeji na stránku zastávky(zatím neexistuje 16.1.2024)
    else:
        form = StationForm()
    return render(request, "add_item.html", {"form": form})

@cache_page(24 * 60 * 60)
def detail(request, station_id):
    station = get_object_or_404(Station, id=station_id, user_id=request.user.id)
    g = gtfs_kit.read_feed(settings.BASE_DIR.parent / "GTFS.zip", dist_units='km')
    times = defaultdict(list)

    if request.GET.get("date"):
        d = datetime.strptime(request.GET.get("date"),"%Y-%m-%d")
    else:
        d = date.today()

    for identifier in station.identifiers.split(","):
        df = g.build_stop_timetable(identifier, (d.strftime("%Y%m%d"),))
        df['arrival_time_td'] = pandas.to_timedelta(df['arrival_time'])
        timetable = df.sort_values(by='arrival_time_td').to_dict(orient='records')

        for t in timetable:
            times[(t['route_id'], identifier)].append(t)

    timetables = {}

    for key, values in times.items():
        timetables[key] = {
            'info': g.routes[g.routes['route_id'] == key[0]].iloc[0].to_dict(),
            'times': values
        }

    return render(request, "detail.html", {"station": station, "timetables" : timetables})
