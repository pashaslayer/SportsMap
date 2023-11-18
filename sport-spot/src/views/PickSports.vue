<template>
  <div class="container">
    <div class="text-center mt-5">
      <!-- First Row (1 Column) -->
      <div class="row text-center mx-auto">
          <h1>{{ title }}</h1>
      </div>

      <form @submit.prevent="postSports">
        <!-- Second Row (6 Columns) -->
        <div class="container">
          <div class="row row-cols-auto g-2">
            <div class="col">Column</div>
            <div class="col">Column</div>
            <div class="col">Column</div>
            <div class="col">Column</div>
          </div>
        </div>

        <div class="row" style="height: 80px"></div>


        <!-- Sixth Row (2 Columns for Buttons) -->
        <div class="row">
          <div class="col-md-6 d-flex justify-content-end">
            <button type="submit" class="btn btn-primary" @click="postRegister">
              Bestätigen
            </button>
          </div>
          <div class="col-md-6 d-flex justify-content-start">
            <button type="submit" class="btn btn-secondary">Abbrechen</button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<style></style>

<script>
import axios from "axios";

export default {
  data() {
    return {
      title: "Favourisierte Sportarten auswählen:",
      selectedSports: [],
    };
  },
  methods: {
    postRegister() {
      axios
        .post("http://127.0.0.1:5000/register", this.postData)
        .then((response) => {
          console.log(response);
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
};

// JWT Token

// localStorage.setItem("Name", "Bob");
// localStorage.getItem('Name');
// localStorage.removeItem('Name');
</script>
