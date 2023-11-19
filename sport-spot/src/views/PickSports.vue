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
          <div v-for="index in allSports" :key="index" class="col">
            <img
              :src="require(`@/assets/${index}.svg`)"
              class="rounded mx-auto d-block"
              draggable="false"
              style="height: 200px; width: 200px"
              @click="toggleImage(index)"
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
      allSports: [1, 3, 5, 7, 9, 11],
      email: "",
    };
  },
  created() {
    const query = this.$route.query;

    this.email = query["email"];
  },
  methods: {
    toggleImage(index) {
      console.log(index);

      const allSports = this.allSports;

      for (let i = 0; i < allSports.length; i++) {
        if (index == allSports[i]) {
          if (allSports[i] % 2 == 0) {
            allSports[i] -= 1;
          } else {
            allSports[i] += 1;
          }
        }
      }

      this.allSports = allSports;
    },
    resetImages() {
      this.selectedSports = [];
    },
    postSports() {
      let mapSports = {
        2: "Kraftsport",
        4: "Schwimmen",
        6: "Skifahren",
        8: "Laufen",
        10: "Wandern",
        12: "Fahrradfahren",
      };

      let selectedSports = [];

      for (let i = 0; i < this.allSports.length; i++) {
        let key = this.allSports[i].toString();
        if (key in mapSports) {
          selectedSports.push(mapSports[key]);
        }
      }

      const data = {
        email: this.email,
        selectedSports: selectedSports,
      };

      axios
        .post("http://127.0.0.1:5000/saveSportsToUser", data)
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
