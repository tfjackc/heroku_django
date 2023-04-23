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
  const landGroup = new MapImageLayer({
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
        content: "Owner Name: {OWNER_NAME} <br /> Zone: {ZONE} <br /> Account: {ACCOUNT}",
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

  const mtLayer = landGroup.sublayers.getItemAt(1);

  const prop = new FeatureLayer({
    url: "https://geo.co.crook.or.us/server/rest/services/Hosted/PATS_property/FeatureServer/0",
    //outFields: ["*"]
  })

  map.add(landGroup);
  map.add(prop);

  landGroup.when(() => {
    
    console.log("Layer loaded successfully");
    landGroup.sublayers.map((sublayer) => {
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
    landGroup.visible = e.target.checked;
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
      const sublayer = landGroup.findSublayerById(parseInt(id));
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

  const tableQuery = new Query({
    where: tableWhere,
    returnGeometry: false,
    outFields: ["*"]
    });
   
    prop.when(function() {
      return prop.queryFeatures(tableQuery);
    }).then(propResults)
});

var account_list;
account_list = [];

 
function propResults(results) {
  console.log("Query returned " + results.features.length + " features");
  
  let mt_whereClause;

  results.features.forEach(function(feature) {
    
    for (const [key, value] of Object.entries(feature.attributes)) {

      if (`${key}` == 'map_taxlot') {
        const maptaxlot = `${value}`
        const strip_mt = maptaxlot.split("-").slice(0, 2).join("");
        //const taxlotValue = [];
        //taxlotValue.push(strip_mt);
        //console.log(taxlotValue);

        mt_whereClause = "MAPTAXLOT = '" + strip_mt + "'";
        console.log(mt_whereClause);
        //let mtLayer = landGroup.sublayers.getItemAt(1);

        const mtQuery = new Query({
          where: mt_whereClause,
          returnGeometry: true,
          outFields: ["*"]
        });

        //console.log(mtLayer); // check if mtLayer is defined and accessible
        mtLayer.queryFeatures(mtQuery).then(function(mtResults) {
          
          if (mtResults.features.length > 0) {
            const mtFeature = mtResults.features[0];
            const mtFeatureExtent = mtResults.features[0].geometry.extent;
            view.goTo({ extent: mtFeatureExtent }).then(function() {
              view.popup.open({
                features: [mtFeature],
                location: mtFeature.geometry.centroid
            });
          });

          }
          
        });
      }
    }
  });
}



  
});