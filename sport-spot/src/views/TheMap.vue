<template>
  <ol-map ref="olMap" :loadTilesWhileAnimating="true" :loadTilesWhileInteracting="true" style="height: 800px">
    <ol-view ref="view" :center="center" :zoom="zoom" :projection="projection" />

    <ol-tile-layer ref="osmLayer" title="OSM">
      <ol-source-osm />
    </ol-tile-layer>

    <ol-control-bar>
      <ol-toggle-control html="🔘" className="edit" title="Point"
        :onToggle="(active) => changeDrawType(active, 'Point')" />
      <!--
      <ol-toggle-control
        html="🔹"
        className="edit"
        title="Polygon"
        :onToggle="(active) => changeDrawType(active, 'Polygon')"
      />
      <ol-toggle-control
        html="〰️"
        className="edit"
        title="LineString"
        :onToggle="(active) => changeDrawType(active, 'LineString')"
      />
      -->
    </ol-control-bar>

    <ol-vector-layer ref="vectorLayer">
      <ol-source-vector ref="vectorSource" @change="source_change">
        <!-- Drwing interaction -->
        <ol-interaction-draw v-if="drawEnable" :key="drawKey.value" :type="drawType" @drawend="drawend" />

        <!-- Feature Selection Interaction -->
        <ol-interaction-select @select="featureSelected">
        </ol-interaction-select>
      </ol-source-vector>

      <!-- Here we are able to set an icon for the drawing/placing of a feature -->
      <ol-style>
        <ol-style-icon :src="markerIcon" :scale="0.05"></ol-style-icon>
      </ol-style>
    </ol-vector-layer>

    <popup-form :showPopup="showPopup" @handleclose="handlePopupClose" @sportIconChange="changeIcon"
      @closePopup="closePopupOnly" @sendData="postMap"></popup-form>

    <show-point-pop :showPopupPoint="showPopupPoint" :selectedEventCoordinates="selectedEventCoordinates"
      @handlepointclose="handlePointPopupClose"></show-point-pop>
  </ol-map>



  <br />
</template>

<script setup>
// Blaue Symbole 
import markerIcon from "../assets/symbols_blau/kreis_blau.svg";
import cyclingIcon from "../assets/symbols_blau/cycling_kreis_blau.svg";
import hikingIcon from "../assets/symbols_blau/hiking_kreis_blau.svg";
import runningIcon from "../assets/symbols_blau/running_kreis_blau.svg";
import skiingIcon from "../assets/symbols_blau/skiing_kreis_blau.svg";
import weightliftingIcon from "../assets/symbols_blau/weightlifting_kreis_blau.svg";

// Grüne Symbole
import markerIconGreen from "../assets/symbols_gruen/kreis_grün.svg";
import cyclingIconGreen from "../assets/symbols_gruen/cycling_kreis_grün.svg";
import hikingIconGreen from "../assets/symbols_gruen/hiking_kreis_grün.svg";
import runningIconGreen from "../assets/symbols_gruen/running_kreis_grün.svg";
import skiingIconGreen from "../assets/symbols_gruen/skiing_kreis_grün.svg";
import weightliftingIconGreen from "../assets/symbols_gruen/weightlifting_kreis_grün.svg";


</script>

<script>
import PopupForm from "./SavePointPop.vue";
import ShowPointPop from "./ShowPointPop.vue";
import axios from "axios";
import { Style, Icon } from "ol/style";
import "ol/ol.css";
import Feature from "ol/Feature";
import Point from "ol/geom/Point.js";

// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
// Dieser ganze Block ist unwichtig is erst später für JWT wichtig!
// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

export default {
  data() {
    return {
      title: "SportSpot Map",
      type: "",
      coordinates: [],
      showPopup: false,
      center: [11.434438109096805, 47.265666027358435],
      // Zoom auf Raum Innsbruck
      zoom: 12.75,
      // reaktive Referenz für das geografische Koordinatensystem WGS 84 in OpenLayers-Karte wird festgelegt
      // geografische Koordinatensystem WGS 84 (World Geodetic System 1984). Es ist das Standard-Koordinatensystem, das von GPS verwendet wird
      projection: "EPSG:4326",

      vectorSource: null,
      drawEnable: false,
      drawType: "Point",
      drawKey: 0,
      map: null, // Referenz zur OpenLayers-Karte
      vectorLayer: null, // Referenz zum VectorLayer

      symbolLink: "",

      // features
      features: [],
      vectorSourceComponent: "",
      olVectorSource: "",

      curFeature: null,

      // Select single coordinate
      showPopupPoint: false,
      selectedEventCoordinates: null,

      // Mypoints
      my_points: []
    };
  },
  mounted() {
    this.vectorSourceComponent = this.$refs.vectorSource;
    console.log(this.vectorSourceComponent); // Inspect the object
    // Attempt to directly access the OpenLayers object, if exposed
    this.olVectorSource =
      this.vectorSourceComponent?.olSource ||
      this.vectorSourceComponent?.source;
    console.log("VS:" + this.olVectorSource.getFeatures());
    this.features = this.olVectorSource.getFeatures();

    // loading of the map at the beginning
    this.loadPoints();
  },
  methods: {
    handleData(
      sport,
      duration,
      startdate,
      difficulty,
      participants,
      description
    ) {
      console.log(
        sport,
        duration,
        startdate,
        difficulty,
        participants,
        description
      );
    },
    source_change(e) {
      console.log(e);
    },

    featureSelected(event) {
      // Diese if schließt das Point Popup weil beim Erstellen von einem Punkt, gleichzeitig die Selektion ausgewählt wird
      if (this.showPopup) {
        this.handlePointPopupClose();
      }
      else if (event.selected.length > 0) {
        const selectedFeature = event.selected[0];
        const geometry = selectedFeature.getGeometry();

        console.log(event.selected.iconSourceInt);
        console.log("-----------------------------------------");
        console.log("Selected feature:", selectedFeature.getGeometry());
        console.log("-----------------------------------------");

        // here we can work with the selectedFeature
        this.selectedEventCoordinates = geometry.getCoordinates();
        console.log(this.selectedEventCoordinates);
        this.showPopupPoint = true;

        if (selectedFeature["values_"]["myPoint"] == true) {
          var myIconStyle = new Style({
            image: new Icon(
              /** @type {olx.style.IconOptions} */({
                src: this.convertIntToSport(selectedFeature["values_"]["sport"]+10),
                scale: 0.08,
              })
            ),
          });
          selectedFeature.setStyle(myIconStyle);
        }
        else {
          var iconStyle = new Style({
            image: new Icon(
              /** @type {olx.style.IconOptions} */({
                src: this.convertIntToSport(selectedFeature["values_"]["sport"]),
                scale: 0.08,
              })
            ),
          });
          selectedFeature.setStyle(iconStyle);
        }
      }



    },

    closePopupOnly() {
      this.showPopup = false;
      this.drawEnable = true;
    },

    changeIcon(iconSourceInt) {
      console.log(iconSourceInt);
      let iconSrc = this.convertIntToSport(iconSourceInt);
      console.log("source: ");
      console.log(iconSrc);

      var iconStyle = new Style({
        image: new Icon(
          /** @type {olx.style.IconOptions} */({
            src: iconSrc,
            scale: 0.05,
          })
        ),
      });
      this.curFeature.setStyle(iconStyle);
    },
    convertIntToSport(value) {
      let sport = "";
      let valueToInt = parseInt(value);
      switch (valueToInt) {
        case 0:
          sport = markerIcon;
          break;
        case 1:
          sport = cyclingIcon;
          break;
        case 2:
          sport = hikingIcon;
          break;
        case 3:
          sport = runningIcon;
          break;
        case 4:
          sport = skiingIcon;
          break;
        case 5:
          sport = weightliftingIcon;
          break;
        case 10:
          sport = markerIconGreen;
          break;
        case 11:
          sport = cyclingIconGreen;
          break;
        case 12:
          sport = hikingIconGreen;
          break;
        case 13:
          sport = runningIconGreen;
          break;
        case 14:
          sport = skiingIconGreen;
          break;
        case 15:
          sport = weightliftingIconGreen;
          break;
      }
      return sport;
    },

    handlePopupClose() {
      // Close the popup and enable drawing
      this.showPopup = false;
      this.drawEnable = true;

      // Update the local features array to reflect the current state of the vector source
      this.features = this.olVectorSource.getFeatures();

      // Check if there are any features present
      if (this.features.length > 0) {
        // Remove the last feature from the vector source
        this.olVectorSource.removeFeature(
          this.features[this.features.length - 1]
        );
      }

      // Optionally, you can log the remaining features for debugging
      console.log(
        "Remaining features after removal:",
        this.olVectorSource.getFeatures()
      );
    },
    handlePointPopupClose() {
      this.showPopupPoint = false;
    },
    drawend(event) {
      if (!this.showPopup) {
        // this disables the ability to draw points after the popup has been opened
        this.drawEnable = false;
        console.log(typeof event);
        const feature = event.feature;
        this.curFeature = event.feature;
        const geometry = feature.getGeometry();
        // Hier wird bei jedem Klick von geometrischen Daten der Typ und die Koordinaten geholt
        switch (geometry.getType()) {
          case "Point":
            this.coords = geometry.getCoordinates();
            console.log("Point coordinates:", this.coords);
            break;
          case "LineString":
            this.coords = geometry.getCoordinates();
            console.log("LineString coordinates:", this.coords);
            break;
          case "Polygon":
            this.coords = geometry.getCoordinates()[0];
            console.log("Polygon coordinates:", this.coords);
            break;
          default:
            console.log("Unknown geometry type");
        }
      }
      this.showPopup = true;
    },
    changeDrawType(active, newType) {
      if (!this.showPopup) {
        this.drawEnable = active;
        this.drawType = newType;
        this.drawKey++; // Increment the key each time the type changes
        this.type = newType; // Update the type
      }
    },

    async loadPoints() {
      try {
        let jwt = localStorage.getItem("jwt_token");

        const response = await axios.post("http://127.0.0.1:5000/maps", {
          jwt: jwt
        }
        );

        response.data.events.forEach((element) => {
          let pointCor1 = element["event_loc"]["latitude"];
          let pointCor2 = element["event_loc"]["longitude"];
          let iconSourceInt = element["sport"];
          let geoData = new Array(pointCor1, pointCor2);

          var iconFeature = new Feature({
            geometry: new Point(geoData),
            sport: iconSourceInt,
            myPoint: false
          });

          let iconSrc = this.convertIntToSport(iconSourceInt);

          var iconStyle = new Style({
            image: new Icon(
              /** @type {olx.style.IconOptions} */({
                src: iconSrc,
                scale: 0.05,
              })
            ),
          });
          iconFeature.setStyle(iconStyle);
          this.olVectorSource.addFeature(iconFeature);
        });

        response.data.my_events.forEach((elementt) => {
          this.my_points.push(elementt);
          let pointCor1 = elementt["event_loc"]["latitude"];
          let pointCor2 = elementt["event_loc"]["longitude"];
          let iconSourceInt = elementt["sport"];
          let geoData = new Array(pointCor1, pointCor2);

          var iconFeature = new Feature({
            geometry: new Point(geoData),
            sport: iconSourceInt,
            myPoint: true
          });

          let iconSrc = this.convertIntToSport(iconSourceInt + 10);

          var iconStyle = new Style({
            image: new Icon(
              /** @type {olx.style.IconOptions} */({
                src: iconSrc,
                scale: 0.05,
              })
            ),
          });
          iconFeature.setStyle(iconStyle);
          this.olVectorSource.addFeature(iconFeature);
        });
      } catch (error) {
        console.log(error);
      }
    },
    async postMap(
      sport,
      duration,
      startdate,
      difficulty,
      participants,
      description
    ) {
      let jwt = localStorage.getItem("jwt_token");

      // console.log("JWT: " + jwt);

      if (this.coords && this.coords.length !== 0) {
        // console.log(this.type);
        // console.log(this.coords);
        try {
          const response = await axios.get("http://127.0.0.1:5000/maps/add", {
            jwt: jwt,
            sport: parseInt(sport),
            duration: duration,
            startdate: startdate,
            difficulty: difficulty,
            participants: participants,
            description: description,
            coords: this.coords,
          });
          // Ausgabe von Typ und geoDaten
          console.log("Type:", this.type);
          console.log("Coordinates:", this.coords);
          if (response.data.success) {
            console.warn("Success!");
          }
        } catch (error) {
          console.error(error);
        }
      } else {
        console.log("No coordinates to send");
      }
    },
    // Method to add a feature with a dynamic style
    addFeatureWithStyle(feature) {
      feature.setStyle();
      this.vectorSource.addFeature(feature);
    },
    // Call this method to update the style of a feature reactively
    updateFeatureStyle(feature) {
      feature.setStyle();
    },
  },
  components: {
    PopupForm,
    ShowPointPop
  },
};
</script>

<style scoped>
.overlay-content {
  background: #c84031;
  color: white;
  box-shadow: 0 5px 10px rgb(2 2 2 / 20%);
  padding: 10px 20px;
  font-size: 16px;
}
</style>
