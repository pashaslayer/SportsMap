<template>
  <ol-map
    ref="olMap"
    :loadTilesWhileAnimating="true"
    :loadTilesWhileInteracting="true"
    style="height: 800px"
  >
    <ol-view
      ref="view"
      :center="center"
      :zoom="zoom"
      :projection="projection"
    />

    <ol-tile-layer ref="osmLayer" title="OSM">
      <ol-source-osm />
    </ol-tile-layer>

    <ol-control-bar>
      <ol-toggle-control
        html="🔘"
        className="edit"
        title="Point"
        :onToggle="(active) => changeDrawType(active, 'Point')"
      />
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
    </ol-control-bar>

    <ol-vector-layer ref="vectorLayer">
      <ol-source-vector ref="vectorSource" @change="source_change">
        <!-- Drwing interaction -->
        <ol-interaction-draw
          v-if="drawEnable"
          :key="drawKey.value"
          :type="drawType"
          @drawend="drawend"
        />

        <!-- Feature Selection Interaction -->
        <ol-interaction-select @select="featureSelected">
          <ol-style>
            <ol-style-stroke color="green" :width="20"></ol-style-stroke>
            <ol-style-fill color="rgba(255,255,255,0.5)"></ol-style-fill>
            <ol-style-icon :src="markerIcon" :scale="0.40"></ol-style-icon>
          </ol-style>
        </ol-interaction-select>
      </ol-source-vector>


      <!-- Here we are able to set an icon for the drawing/placing of a feature -->
      <ol-style>
            <ol-style-stroke color="red" :width="20"></ol-style-stroke>
            <ol-style-fill color="rgba(255,255,255,0.5)"></ol-style-fill>
            <ol-style-icon :src="markerIcon" :scale="0.80"></ol-style-icon>
          </ol-style>
    </ol-vector-layer>

    <popup-form
      :showPopup="showPopup"
      @handleclose="handlePopupClose"
      @closePopup="closePopupOnly"
    ></popup-form>
  </ol-map>

  <br />

  <button type="submit" class="btn btn-primary" @click="postMap">
    Koordinaten Abschicken
  </button>
</template>

<script setup>
// Adding a icon for the selection, for test reasons: marker.png
import markerIcon from "../assets/marker.png";
</script>

<script>
import PopupForm from "./SavePointPop.vue";
import axios from "axios";
import "ol/ol.css";


//import Map from 'ol/Map';
//import View from 'ol/View';
//import VectorLayer from 'ol/layer/Vector';
//import VectorSource from 'ol/source/Vector';
//import {ref} from "vue"; // Adjust the path as necessary
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
    };
  },

  mounted() {},
  methods: {
    source_change(e) {
      console.log(e);
    },

    featureSelected(event) {
      if (event.selected.length > 0) {
        const selectedFeature = event.selected[0];
        console.log("-----------------------------------------");
        console.log("Selected feature:", selectedFeature);
        console.log("-----------------------------------------");

        // here we can work with the selectedFeature
      }
    },

    // Check for Token Expiration Date compare it with current time
    isTokenExpired() {
      const expirationTime = localStorage.getItem("jwt_token_exp");
      if (expirationTime) {
        return new Date().getTime() > parseInt(expirationTime, 10);
      }
      return true;
    },
    closePopupOnly() {
      this.showPopup = false;
      this.drawEnable = true;
    },
    handlePopupClose() {
      console.log("Popup closed");
      this.showPopup = false;

      // this brings back the ability to draw points on the map
      this.drawEnable = true;

      const vectorSourceComponent = this.$refs.vectorSource;
      console.log(vectorSourceComponent); // Inspect the object
      // Attempt to directly access the OpenLayers object, if exposed
      const olVectorSource =
        vectorSourceComponent?.olSource || vectorSourceComponent?.source;
      console.log("VS:" + olVectorSource.getFeatures());
      let features = olVectorSource.getFeatures();

      features.forEach((feature, index) => {
        console.log(`Feature ${index}:`, feature);
        // If you want to print specific properties of the feature:
        console.log(`Feature ${index} Properties:`, feature.getProperties());
      });

      if (features.length > 0)
        olVectorSource.removeFeature(features[features.length - 1]);
    },
    drawend(event) {
      if (!this.showPopup) {
        // this disables the ability to draw points after the popup has been opened
        this.drawEnable = false;
        console.log(typeof event);
        const feature = event.feature;
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

    async postMap() {
      if (this.coords && this.coords.length !== 0) {
        // JOHNNY: Hier wird der Typ + Koordinaten ausgegeben wenn man auf den Button klickt + prüfung ob eine Koordinate überhaupt gesetzt wurde
        console.log(this.type);
        console.log(this.coords);
        try {
          // JOHNNY: Hier musst du dann deine URL anpassen
          // JOHNNY: Die geometrischen Daten müssen später zu einem betimmten user abgespeichert werden, können wir aber erst dann machen wenn JWT fertig ist

          const response = await axios.post(
            "http://127.0.0.1:5000/[YOUR_ENDPOINT]",
            {
              type: this.type,
              coords: this.coords,
            }
          );
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
  },
  components: {
    PopupForm,
    // ... other components
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
