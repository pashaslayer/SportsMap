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
            <img :src="require(`@/assets/${index}.svg`)" class="rounded mx-auto d-block" draggable="false"
              style="height: 200px; width: 200px" @click="toggleImage(index)" />
          </div>
        </div>

        <div class="row" style="height: 80px"></div>

        <!-- Sixth Row (2 Columns for Buttons) -->
        <div class="row">
          <div class="col-md-6 d-flex justify-content-end">
            <button type="submit" class="btn btn-primary">Bestätigen</button>
          </div>
          <div class="col-md-6 d-flex justify-content-start">
            <button type="button" class="btn btn-secondary" @click="resetImages">
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
  mounted(){
    this.email = localStorage.getItem('email');
    localStorage.clear();
  },
  data() {
    return {
      title: "Favourisierte Sportarten auswählen:",
      selectedSports: [],
      allSports: [2, 4, 6, 8, 10, 12],
      email: "",
    };
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
      this.allSports = [2, 4, 6, 8, 10, 12];
    },
    getEmailHandle(value) {
      console.log(value);
      console.log("hehle");
      this.email = value;
    },
    postSports() {
      let mapSports = {
        1: "Kraftsport",
        3: "Schwimmen",
        5: "Skifahren",
        7: "Laufen",
        9: "Wandern",
        11: "Fahrradfahren",
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
          setTimeout(() => {
            this.$router.push("/login");
          }, 1000);
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
};
</script>
