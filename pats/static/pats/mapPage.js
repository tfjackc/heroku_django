require(["esri/Map",
         "esri/views/MapView",
         "esri/layers/FeatureLayer",
         "esri/layers/MapImageLayer",
         "esri/widgets/Legend",
         "esri/rest/support/Query",
],

         (Map,
          MapView,
          FeatureLayer,
          MapImageLayer,
          Legend,
          Query) => {

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
  const layer = new MapImageLayer({
    url: "https://geo.co.crook.or.us/server/rest/services/publicApp/landGroup/MapServer",
    sublayers: [{
      id: 0,
      visible: true,
      popupTemplate: {
        title: "Subdivision: {name}"
    }},
    {
      id: 1,
      visible: true,
      popupTemplate: {
        title: "{MAPTAXLOT}",
        content: "Owner Name: {OWNER_NAME} <br /> Zone: {ZONE} <br />",
    }
    },
    // {
    //   id: 2,
    //   visible: false,
    // },
    // {
    //   id: 3,
    //   visible: false,
    // },
    // {
    //   id: 4,
    //   visible: false,
    // },
    // {
    //   id: 5,
    //   visible: false,
    // },
    // {
    //   id: 6,
    //   visible: false,
    // },
    {
      id: 7,
      visible: true,
    },]
  });

  const prop = new FeatureLayer({
    url: "https://geo.co.crook.or.us/server/rest/services/Hosted/PATS_property/FeatureServer/0",
    // portalItem: {
    //   id: "0ff09aa822904aa4aa9aca9f3457f334"
    // },
    //outFields: ["*"]
  })

  map.add(layer);
  map.add(prop);

  layer.when(() => {
    
    console.log("Layer loaded successfully");
    layer.sublayers.map((sublayer) => {
      const id = sublayer.id;
      const visible = sublayer.visible;
      const node = document.querySelector(
        ".sublayers-item[data-id='" + id + "']"
      );
      if (visible) {
        node.classList.add("visible-layer");
      }
    });
  });

  var checkBox = document.getElementById("checkBoxLayer")
  
  checkBox.addEventListener("change", function(e) {
   layer.visible = e.target.checked;
});


// const legend = new Legend({
//     view: view,
//     layerInfos: [
//       {
//         layer: landGroup,
//         title: "Land Group",
//         sublayers: [
//           {
//             id: 0,
//             title: "Subdivisions",
//           },
//           {
//             id: 1,
//             title: "Taxlots",
//           },
//           {
//             id: 7,
//             title: "Pending",
//           },

//         ]
//       }
//     ]
//   });

//  view.ui.add(legend, "bottom-left");

  const sublayersElement = document.querySelector(".sublayers");
  sublayersElement.addEventListener("click", (event) => {
    console.log("Click event listener is working");
    const id = event.target.getAttribute("data-id");
    if (id) {
      const sublayer = layer.findSublayerById(parseInt(id));
      const node = document.querySelector(
        ".sublayers-item[data-id='" + id + "']"
      );
      sublayer.visible = !sublayer.visible;
      console.log(`Sublayer ${sublayer.id} visibility: ${sublayer.visible}`);
      node.classList.toggle("visible-layer");
    }
  });

var account_searched = document.getElementById("account_entered");
var submitButton = document.getElementById("searchButton");

submitButton.addEventListener("click", function() {
  console.log("button clicks");
  console.log(account_searched.value)

  tableWhere = "account_id = '" + account_searched.value + "'"
  //tableWhere="1=1"
  console.log(tableWhere);

  tableQuery = new Query({
    where: tableWhere,
    returnGeometry: false,
    outFields: ["*"]
    });
   
    prop.when(function() {
      return prop.queryFeatures(tableQuery);
    }).then(propResults)
});


function propResults(results) {
  console.log("Query returned " + results.features.length + " features");
  console.log(results); // Add this line to log the entire results object
  results.features.forEach(function(feature) {
    console.log("we are here");
    console.log(feature);
    //console.log(typeof feature.attributes);
    //const obj = feature.attributes

    for (const [key, value] of Object.entries(feature.attributes)) {
      console.log(`${key}: ${value}`);
    }

  })
};




// const url = "/pats/get/ajax/mapData/"

// const getData = (account_searched)=> {
//   $.ajax({
//     type: 'GET',
//     url: url,
//     data: {"account_searched": account_searched},
//     complete: myCallback,
//   });
// };

// function myCallback(response) {
//   // Get the response data
//   const data = response.responseText;

//   // Update the "result" element with the response data
//   $(".result").html(data);

//   alert("Load was performed.");
//   //const parsedData = JSON.parse(data);

//   console.log(data);
// }
  
});