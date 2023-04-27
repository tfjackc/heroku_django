require(["esri/Map",
         "esri/views/MapView",
         "esri/layers/FeatureLayer",
         "esri/layers/MapImageLayer",
         "esri/widgets/Legend",
         "esri/rest/support/Query",
         "esri/widgets/Search",
],

         (Map,
          MapView,
          FeatureLayer,
          MapImageLayer,
          Legend,
          Query,
          Search) => {

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
      },
     },
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

  const searchWidget = new Search({
    view: view,
    container: "searchWidget",
    allPlaceholder: "Maptaxlot, Account, or Situs Address",
    includeDefaultSources: false, 
    sources: [
      {
        layer: mtLayer,
        searchFields: ["MAPTAXLOT"],
        suggestionTemplate: "{MAPTAXLOT}",
        //displayField: "MAPTAXLTOT",
        exactMatch: false,
        outFields: ["*"],
        name: "Maptaxlot",
        placeholder: "Search Maptaxlot",
      },
      {
        layer: mtLayer,
        searchFields: ["ACCOUNT"],
        suggestionTemplate: "{ACCOUNT}",
        exactMatch: false,
        outFields: ["*"],
        //placeholder: "Account: Casey",
        name: "Account ID",
        placeholder: "Search by Account #",
        //zoomScale: 500000,
      },
     
    ]
  });
  // Adds the search widget below other elements in
  // the top left corner of the view
  
  
//   view.ui.add(searchWidget, {
//     position: "top-left",
//     index: 2
//   });

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


  searchWidget.on("select-result", function(event) {
  
    if (event) {
      for (const [key, value] of Object.entries(event.result)) {
        console.log(`${key}: ${value}`);

        if (`${key}` == 'name') {
            const maptaxlot = `${value}`
            //const strip_mt = maptaxlot.split("-").slice(0, 2).join("");
            //const taxlotValue = [];
            //taxlotValue.push(strip_mt);
            //console.log(taxlotValue);
    
            mt_whereClause = "MAPTAXLOT = '" + maptaxlot + "'";
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
                //console.log(mtFeature+' : '+mtFeatureExtent)
            //     view.goTo({ extent: mtFeatureExtent }).then(function() {
            //     //   view.popup.open({
            //     //     features: [mtFeature],
            //     //     location: mtFeature.geometry.centroid
            //     // });
            //   });
                for (const [key, value] of Object.entries(mtResults.features[0].attributes)) {
                    //console.log(`${key}: ${value}`);
                    if (`${key}` == 'ACCOUNT') {
                        tableWhere = "account_id = '" + `${value}` + "'"
                        //tableWhere = "account_id = '" + account_searched.value + "'"
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
                    }
                }
              }
              
            });
          }
      }
    } 

    function propResults(results) {
        console.log("Query returned " + results.features.length + " features");
        console.log(results.features[0].attributes)
    }
  
  });
    
});