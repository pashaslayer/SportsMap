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
          :type="drawType"
          @drawend="drawend"
        />
      </ol-source-vector>
    </ol-vector-layer>
  </ol-map>
</template>

<script setup>
import { ref } from "vue";

const center = ref([34, 39.13]);
const zoom = ref(6);
const projection = ref("EPSG:4326");

const vectorSource = ref(null);
const drawEnable = ref(false);
const drawType = ref("Point");

const changeDrawType = (active, type) => {
  drawEnable.value = active;
  drawType.value = type;
};

const drawend = (event) => {
  const feature = event.feature;
  const coords = feature.getGeometry().getCoordinates();
  console.log("Drawn coordinates:", coords);
  // Here you can handle the saving of the coordinates as needed
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