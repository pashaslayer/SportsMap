<template>
  <div style="width: 100%; height: 100%">
    <button @click="setCenter">Zentrum</button>
    <button @click="changeZoom(-1)">&leftarrow;</button>
    <button @click="changeZoom(1)">&rightarrow;</button>
  <div ref="map-root" style="width: 100%; height: 100%">
  </div>

  </div>
</template>

<script>
  import View from 'ol/View'
  import Map from 'ol/Map'
  import LayerGroup from 'ol/layer/Group'
  import { transform } from 'ol/proj'
  import Collection from 'ol/Collection'

  import VectorLayer from 'ol/layer/Vector'
  import VectorSource from 'ol/source/Vector'
  import GeoJSON from 'ol/format/GeoJSON'
  import {Circle as CircleStyle, Stroke, Style, Text, Fill} from 'ol/style.js';
  import {restaurants}  from '../assets/restaurants.js'

  import 'ol/ol.css'

  export default {
    name: 'MapContainer',
    components: {},
    props: {
      center: {
        type: Array,
        default: () => ([0,0])
      },
      zoom: {
        type: Number,
        default: 0
      },
      baselayers: LayerGroup,
      overlays: LayerGroup,
      controls: Collection,
      interactions: Collection,
    },
    data: () => ({
      olMap: null,
    }),
    mounted() {

    const features = new GeoJSON().readFeatures(restaurants, {
        // this is required since GeoJSON uses latitude/longitude,
        featureProjection: 'EPSG:3857'
      });


      const image = new CircleStyle({
        radius: 10,
        fill: null,
        stroke: new Stroke({color: 'red', width: 1}),
      });

      const text =  new Text({
        font: '12px Calibri,sans-serif',
        placement: 'line',
        fill: new Fill({
            color: '#000'
        }),
        stroke: new Stroke({
            color: 'lightgreen',
            width: 3
        })
    })

      const style =  new Style({
           image: image,
           text : text});

      // a new vector layer is created with the feature
      const vectorLayer = new VectorLayer({
        source: new VectorSource({
          features: features
        }),
         style: function(feature) {
           style.getText().setText(feature.get('name')); //so wird der Text angezeigt
           return style;
         }
      })


      this.olMap = new Map({
        target: this.$refs['map-root'],
        layers: [this.baselayers, this.overlays, vectorLayer],
        view: new View({
          zoom: this.zoom,
          center: transform([this.center[1], this.center[0]], 'EPSG:4326', 'EPSG:3857'),
          constrainResolution: true,
        }),
        controls: this.controls,
        interactions: this.customInt || this.interactions,
      });
      this.setMouseCursor();
      this.$emit('init', this.olMap);
    },
    methods: {
      setMouseCursor() {
        let map = this.olMap;
        map.getViewport().classList.add('ol-grab');
        map.on(['pointerdrag', 'pointerup'], (e) => {
          map.getViewport().classList.toggle('ol-grabbing', e.type == 'pointerdrag');
          map.getViewport().classList.toggle('ol-grab', e.type == 'pointerup');
        });
      },
      setCenter()
          {
            this.olMap.getView().setCenter(transform([this.center[1], this.center[0]], 'EPSG:4326', 'EPSG:3857'))
          },
      changeZoom(v)
      {
        this.olMap.getView().setZoom(this.olMap.getView().getZoom()+v);
      }
    }
  }
</script>

<style>
  .ol-rotate {
    top: 3em;
  }
</style>
