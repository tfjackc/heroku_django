require(["esri/Map",
         "esri/views/MapView",
         "esri/layers/FeatureLayer",
         "esri/layers/MapImageLayer"
],

         (Map,
          MapView,
          FeatureLayer,
          MapImageLayer) => {

const map = new Map({
  basemap: "topo-vector"
});

var lat = 44.30291;
var long = -120.84585;

const view = new MapView({
  container: "viewDiv",
  map: map,
  zoom: 14,
  center: [long, lat] // longitude, latitude
  });

  // add feature from MapServer
  const landGroup = new MapImageLayer({
    url: "https://geo.co.crook.or.us/server/rest/services/publicApp/landGroup/MapServer",
    sublayers: [{
      id: 0,
      visible: true,
    },
    {
      id: 1,
      visible: true,
    },
    {
      id: 2,
      visible: false,
    },
    {
      id: 3,
      visible: false,
    },
    {
      id: 4,
      visible: false,
    },
    {
      id: 5,
      visible: false,
    },
    {
      id: 6,
      visible: false,
    },
    {
      id: 7,
      visible: true,
    },]
  });

  landGroup.when(function() {
    console.log("should be loaded");
  }).then(map.add(landGroup));

  var checkBox = document.getElementById("checkBoxLayer")
  
  checkBox.addEventListener("change", function(e) {
    landGroup.visible = e.target.checked;
});
  
});