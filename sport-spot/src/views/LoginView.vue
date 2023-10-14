<template>
  <div class="tocenter">
    <div class="container text-center mx-auto">
      <!-- First Row (1 Column) -->
      <div class="row">
        <div class="col-12">
          <img
            src="@/assets/logo_vektor_01_white.svg"
            class="rounded mx-auto d-block"
          />
          <h1>{{ title }}</h1>
        </div>
      </div>

      <div class="row" style="height: 40px"></div>


      <!-- Second Row (6 Columns) -->
      <div class="row">
        <div class="col-md-6 border border-white">
          <label for="firstname" class="form-label">Firstname:</label>
        </div>
        <div class="col-md-6 border border-white">
          <input
            v-model="postData.firstname"
            type="text"
            class="form-control"
            id="firstname-label"
            onkeydown="return /[a-z]/i.test(event.key) required"
          />
        </div>
      </div>

      <!-- Third Row (6 Columns) -->
      <div class="row">
        <div class="col-md-6 border border-white">
          <label for="lastname" class="form-label">Lastname: </label>
        </div>
        <div class="col-md-6 border border-white">
          <!--Input Nachname-->
          <input
            v-model="postData.lastname"
            type="text"
            class="form-control"
            id="lastname-label"
            onkeydown="return /[a-z]/i.test(event.key) required"
          />
        </div>
      </div>

      <!-- Fourth Row (Spacing) -->
      <div class="row" style="height: 20px"></div>

      <div class="row" style="height: 80px"></div>




      <!-- Sixth Row (2 Columns for Buttons) -->
      <div class="row">
        <div class="col-md-6 d-flex justify-content-end">
          <button type="submit" class="btn btn-primary">Bestätigen</button>
        </div>
        <div class="col-md-6 d-flex justify-content-start">
          <button type="submit" class="btn btn-secondary">Abbrechen</button>
        </div>
      </div>
    </div>
  </div>

  </template>
  
  
  <script>
  import axios from 'axios';
  export default {
    data() {
      return {
        title: "SportSpot Anmeldung",
        postData: {
          email: '',
          password: '',
          //success: "",
        }
      };
    },
    methods: {
      methods: {
      postLogin() {
        axios
            .post("http://127.0.0.1:5000/login", this.postData)
            .then((response) => console.log(response))
      },
    },
    },

  };
  </script>
  