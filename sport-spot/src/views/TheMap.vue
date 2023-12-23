<template>
  <ol-map
    ref="map"
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

    <ol-vector-layer>
      <ol-source-vector ref="vectorSource">
        <ol-interaction-draw
          v-if="drawEnable"
          :key="drawKey.value"
          :type="drawType"
          @drawend="drawend"
        />
      </ol-source-vector>
    </ol-vector-layer>
  </ol-map>

  <br>



  <button type="submit" class="btn btn-primary" @click="postMap">
          Koordinaten Abschicken
  </button>
</template>

<script setup>
import { ref, reactive } from "vue";
import axios from "axios";

// Koordinaten auf Raum Innsbruck
const center = ref([11.434438109096805, 47.265666027358435]);
// Zoom auf Raum Innsbruck
const zoom = ref(12.75);
// reaktive Referenz für das geografische Koordinatensystem WGS 84 in OpenLayers-Karte wird festgelegt
// geografische Koordinatensystem WGS 84 (World Geodetic System 1984). Es ist das Standard-Koordinatensystem, das von GPS verwendet wird
const projection = ref("EPSG:4326");

const vectorSource = ref(null);
const drawEnable = ref(false);
const drawType = ref("Point");
const drawKey = reactive({ value: 0 });

let coords;
let type;

const changeDrawType = (active, newType) => {
  drawEnable.value = active;
  drawType.value = newType;
  drawKey.value++; // Increment the key each time the type changes
  type = newType; // Update the type
};

const postMap = async () => {
  if (coords && coords.length !== 0) {
    // JOHNNY: Hier wird der Typ + Koordinaten ausgegeben wenn man auf den Button klickt + prüfung ob eine Koordinate überhaupt gesetzt wurde
    console.log(type);
    console.log(coords);
    try {
      // JOHNNY: Hier musst du dann deine URL anpassen
      // JOHNNY: Die geometrischen Daten müssen später zu einem betimmten user abgespeichert werden, können wir aber erst dann machen wenn JWT fertig ist

      const response = await axios.post("http://127.0.0.1:5000/[YOUR_ENDPOINT]", {
        type: type,
        coords: coords,
      });
      // Ausgabe von Typ und geoDaten
      console.log("Type:", type);
      console.log("Coordinates:", coords);
      if (response.data.success) {
        console.warn("Success!");
      }
    } catch (error) {
      console.error(error);
    }
  } else {
    console.log("No coordinates to send");
  }
};


const drawend = (event) => {
  const feature = event.feature;
  const geometry = feature.getGeometry();

  // Hier wird bei jedem Klick von geometrischen Daten der Typ und die Koordinaten geholt
  switch (geometry.getType()) {
    case 'Point':
      coords = geometry.getCoordinates();
      console.log('Point coordinates:', coords);
      break;
    case 'LineString':
      coords = geometry.getCoordinates();
      console.log('LineString coordinates:', coords);
      break;
    case 'Polygon':
      coords = geometry.getCoordinates()[0];
      console.log('Polygon coordinates:', coords);
      break;
    default:
      console.log('Unknown geometry type');
  }
};

</script>

<script>
// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
// Dieser ganze Block ist unwichtig is erst später für JWT wichtig!
// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
export default {
  data() {
    return {
      title: "SportSpot Map",
      type: "",
      coordinates: [],
    };
  },
  methods: {
    // Check for Token Expiration Date compare it with current time
    isTokenExpired() {
      const expirationTime = localStorage.getItem("jwt_token_exp");
      if (expirationTime) {
        return new Date().getTime() > parseInt(expirationTime, 10);
      }
      return true;
    },
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
