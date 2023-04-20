require(["esri/Map",
         "esri/views/MapView",
         "esri/layers/FeatureLayer",
],

         (Map,
          MapView,
          FeatureLayer,) => {

const map = new Map({
  basemap: "topo-vector"
});

var lat = 44.30291;
var long = -120.84585;

const view = new MapView({
  container: "viewDiv",
  map: map,
  zoom: 11,
  center: [long, lat] // longitude, latitude
  });

  // add feature from MapServer
  const featureLayer = new FeatureLayer({
    url: "https://geo.co.crook.or.us/server/rest/services/publicApp/landGroup/MapServer/1"
  });

  map.add(featureLayer);
  
});