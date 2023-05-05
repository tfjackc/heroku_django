from django.shortcuts import render, redirect
from pats.models import ContactInfo
from django.http import HttpResponse, HttpResponseRedirect
import json
import requests
from .forms import ContactModelForm
import folium
from folium.plugins import Draw
from folium.elements import JSCSSMixin
import jinja2
from jinja2 import Template
import branca
from branca.element import Element, Figure, MacroElement
from folium.features import ClickForLatLng, ClickForMarker, LatLngPopup
from django.views.generic import TemplateView


class Draw(JSCSSMixin, MacroElement):
    """
    https://leafletjs.com/reference.html#control
    http://leaflet.github.io/Leaflet.draw/docs/leaflet-draw-latest.html#drawoptions
    https://leaflet.github.io/Leaflet.draw/docs/leaflet-draw-latest.html
    """

    _template = Template(
        """
    {% macro script(this, kwargs) %}
    var options = {
    position: {{ this.position|tojson }},
    draw: {{ this.draw_options|tojson }},
    edit: {{ this.edit_options|tojson }},
    }
    // FeatureGroup is to store editable layers.
    var drawnItems = new L.featureGroup().addTo(
    {{ this._parent.get_name() }}
    );
    options.edit.featureGroup = drawnItems;
    var {{ this.get_name() }} = new L.Control.Draw(
    options
    ).addTo( {{this._parent.get_name()}} );
    var featureId = 1;
    {{ this._parent.get_name() }}.on(L.Draw.Event.CREATED, function(e) {
    var layer = e.layer,
    type = e.layerType;
    feature = layer.feature = layer.feature || {}; // Initialize feature
    var title = prompt("Please provide the name", "default");
    var value = prompt("Please provide the value", "undefined");
    // var id = (L.Util.lastId)-165;
    feature.type = feature.type || "Feature"; // Initialize feature type
    if (type === 'circle') {
    var theCenterPt = layer.getLatLng();
    var center = [theCenterPt.lng,theCenterPt.lat];
    console.log(center);
    console.log(title);
    var theRadius = layer.getRadius();
    var turfCircle;
    var options = {steps: 256, units: 'meters'};
    var turfCirle = turf.circle(center, theRadius, options);
    var NewTurfCircle = new L.GeoJSON(turfCircle)
    drawnItems.addLayer(NewTurfCircle);
    var thepoint = {
    type: 'Feature',
    geometry: {
    type: 'Point',
    coordinates: center
    },
    properties: {"Id": featureId, "Title": title, "Value": value}
    };
    var buffered = turf.buffer(thepoint, theRadius, {units: 'meters'});
    var NewTurfBuffer = new L.GeoJSON(buffered)
    drawnItems.addLayer(NewTurfBuffer);
    }
    var props = feature.properties = feature.properties || {}; // Initialize feature properties
    props.Id = featureId;
    props.Title = title;
    props.Value = value;
    var coords = JSON.stringify(layer.toGeoJSON());
    layer.bindPopup('<b>Name: </b>' + title + '<br> <b>Value: </b>' + value + '<br> <b>Coordinates: </b>' + coords)
    {%- if this.show_geometry_on_click %}
    layer.on('click', function() {
    // alert(coords);
    console.log(coords);
    });
    {%- endif %}
    drawnItems.addLayer(layer);
    });
    {{ this._parent.get_name() }}.on('draw:created', function(e) {
    drawnItems.addLayer(e.layer);
    featureId++;
    });
    {% if this.export %}
    document.getElementById('export').onclick = function(e) {
    var data = drawnItems.toGeoJSON();
    var filetitle = prompt("Please provide the name", "data");
    var convertedData = 'text/json;charset=utf-8,'
    + encodeURIComponent(JSON.stringify(data));
    document.getElementById('export').setAttribute(
    'href', 'data:' + convertedData
    );
    document.getElementById('export').setAttribute(
    'download', filetitle+'.geojson', 'text/plain'
    );
    }
    {% endif %}
    {% endmacro %}
    """
    )

    default_js = [
    (
    "leaflet_draw_js",
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.2/leaflet.draw.js",
    )
    ]
    default_css = [
    (
    "leaflet_draw_css",
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.2/leaflet.draw.css",
    )
    ]

    def __init__(
        self,
        export=True,
        #filename="data.geojson",
        position="topleft",
        show_geometry_on_click=True,
        draw_options=None,
        edit_options=None,
    ):
        super().__init__()
        self._name = "DrawControl"
        self.export = export
        #self.filename = filename
        self.position = position
        self.show_geometry_on_click = show_geometry_on_click
        self.draw_options = draw_options or {}
        self.edit_options = edit_options or {}

    def render(self, **kwargs):
        super().render(**kwargs)

        figure = self.get_root()
        assert isinstance(
            figure, Figure
        ), "You cannot render this Element if it is not in a Figure."

        export_style = """
        <style>
        #export {
        position: absolute;
        top: 5px;
        right: 10px;
        z-index: 999;
        background: white;
        color: black;
        padding: 6px;
        border-radius: 4px;
        font-family: 'consolas';
        cursor: pointer;
        font-size: 12px;
        text-decoration: none;
        top: 90px;
        }
        </style>
        """
        export_button = """<a href='#' class="btn btn-info" id='export'>Export</a>"""
        if self.export:
            figure.header.add_child(Element(export_style), name="export")
            figure.html.add_child(Element(export_button), name="export_button")


class FoliumView(TemplateView):
    template_name = "portfolio/foliumMap.html"

    def get_context_data(self, **kwargs):
        figure = folium.Figure()
        m = folium.Map(
            location=[46.982639, -108.519417],
            zoom_start=4,
            tiles= 'OpenStreetMap', #'Stamen Terrain'
           
        )
        
        #public_token = "pk.eyJ1IjoidGZqYWNrYyIsImEiOiJjbGhhd3VsZHAwbHV1M3RudGt0bWFhNHl0In0.5qDpeYjN5r-rBh-SYA9Qgw"

        folium.TileLayer(tiles='http://{s}.tiles.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoidGZqYWNrYyIsImEiOiJjbGhhd3VsZHAwbHV1M3RudGt0bWFhNHl0In0.5qDpeYjN5r-rBh-SYA9Qgw',
        attr='<a href="https://www.mapbox.com/about/maps/">© Mapbox | </a>', name='satellite').add_to(m)

        folium.LayerControl(position='topleft').add_to(m)


        m.add_to(figure)
        # folium.Marker(
        #     location=[44.30291, -120.84585],
        #     popup='Prineville, OR',
        #     icon=folium.Icon(color='green')
        # ).add_to(m)

        #m.add_child(ClickForMarker())
        
        draw = Draw()
        draw.add_to(m)

        # political_counties_url = ("http://geojson.xyz/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson")

        # folium.GeoJson(political_counties_url).add_to(m)

        figure.render()
        return {"map": figure}

def resume(request):
    return render(request, 'portfolio/resume.html')

def mainpage(request):
    return render(request, 'portfolio/mainpage.html')

def base(request):
    return render(request, 'portfolio/base.html')

def notebook(request):
    return render(request, 'portfolio/notebook.html')

def contact_create_view(request, *args, **kwargs):

    form = ContactModelForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        # do some stuff

        obj.save()
    #     #print(form.cleaned_data)
    #     #data = form.cleaned_data
    #     #ContactInfo.objects.create(**data)
    #     # ContactInfo(**data) --> same as  obj = form.save(commit=False)
        form = ContactModelForm()
    #     # return HttpResponseRedirect("/success")
    #     # return redirect("/success")
    
    return render(request, "portfolio/mainpage.html", {'form':form})



    