from django.forms import ModelForm
from .models import Station
from django.conf import settings
from django.core.exceptions import ValidationError
import gtfs_kit

class StationForm(ModelForm):
    class Meta:
        model = Station
        exclude = ["user", "identifiers"]
    
    def clean_name(self):
        name = self.cleaned_data["name"]
        g = gtfs_kit.read_feed(settings.BASE_DIR / ".." /  "GTFS.zip", dist_units='km')
        self.identifiers = g.stops[g.stops["stop_name"].str.contains(name, case = False)]["stop_id"].tolist()
        if not self.identifiers:
            raise ValidationError("Zastávka nebyla nalezena")
        return name