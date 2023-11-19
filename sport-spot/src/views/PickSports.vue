<template>
  <div class="container-fluid">
    <div class="text-center mt-5">
      <!-- First Row (1 Column) -->
      <div class="row text-center">
        <h1>{{ title }}</h1>
      </div>

      <form @submit.prevent="postSports">
        <!-- Second Row (6 Columns) -->
        <div class="row row-cols-auto g-2 justify-content-center">
          <div v-for="(image, index) in images" :key="index" class="col">
            <img
              :src="require(`@/assets/${index * 2 + 1}.svg`)"
              class="rounded mx-auto d-block"
              draggable="false"
              style="height: 200px; width: 200px"
              @click="toggleImage(index + 1)"
            />
          </div>
        </div>

        <div class="row" style="height: 80px"></div>

        <!-- Sixth Row (2 Columns for Buttons) -->
        <div class="row">
          <div class="col-md-6 d-flex justify-content-end">
            <button type="submit" class="btn btn-primary">Bestätigen</button>
          </div>
          <div class="col-md-6 d-flex justify-content-start">
            <button
              type="button"
              class="btn btn-secondary"
              @click="resetImages"
            >
              Abbrechen
            </button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      title: "Favourisierte Sportarten auswählen:",
      selectedSports: [],
      email: "",
      images: Array.from({ length: 6 }, (_, i) => i + 1),
    };
  },
  methods: {
    toggleImage(index) {
      console.log(index);
      if (this.selectedSports.includes(index)) {
        // Unselect the image
        this.selectedSports = this.selectedSports.filter((i) => i !== index);
      } else {
        // Select the image
        this.selectedSports.push(index);
      }
    },
    resetImages() {
      this.selectedSports = [];
    },
    postSports() {
      axios
        .post("http://127.0.0.1:5000/save_sports_to_user", this.selectedSports)
        .then((response) => {
          console.log(response);
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
};
</script>
