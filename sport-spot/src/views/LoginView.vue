<template>
  <meta
    name="viewport"
    content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no"
  />
    <div class="container mt-5">
      <!-- First Row (1 Column) -->
      <div class="row text-center mx-auto">
        <div class="col-md-12">
          <img
            v-if="!wheelAnimation"
            src="@/assets/logo_vektor_01_white.svg"
            class="rounded mx-auto d-block"
            draggable="false"
          />
          <img
            v-if="wheelAnimation"
            src="@/assets/logo_vektor_01_white.svg"
            class="rounded mx-auto d-block wheel-animation"
            draggable="false"
            @animationend="stopWheelAnimation"
          />
          <h1 class="title">{{ title }}</h1>
        </div>
      </div>

      <!-- Für einen Abstand falls es so besser ausschaut -->
      <!-- <div class="row" style="height: 40px"></div> -->

      <!-- Second Row (6 Columns) -->
      <div class="row">
        <div class="col-md-6 border border-white align-items-center d-flex justify-content-center">
          <label for="firstname" class="form-label">Firstname:</label>
        </div>
        <div class="col-md-6 border border-white">
          <input
            v-model="postData.firstname"
            type="text"
            class="form-control"
            id="firstname-label"
          />
        </div>
      </div>

      <!-- Third Row (6 Columns) -->
      <div class="row">
        <div class="col-md-6 border border-white align-items-center d-flex justify-content-center">
          <label for="lastname" class="form-label">Lastname: </label>
        </div>
        <div class="col-md-6 border border-white">
          <!--Input Nachname-->
          <input
            v-model="postData.lastname"
            type="text"
            class="form-control"
            id="lastname-label"
          />
        </div>
      </div>

      <!-- Fourth Row (Spacing) -->
      <div class="row" style="height: 20px"></div>

      <div class="row" style="height: 80px"></div>

      <div class="d-flex justify-content-center">
        <span class="mr-2">Noch nicht registriert?: </span>
        <router-link to="/registration">Register</router-link>
      </div>

      <!-- Sixth Row (2 Columns for Buttons) -->
      <div class="row">
        <div class="col-md-6 d-flex justify-content-end">
          <button type="submit" class="btn btn-primary" @click="postLogin">
            Bestätigen
          </button>
        </div>
        <div class="col-md-6 d-flex justify-content-start">
          <button type="submit" class="btn btn-secondary">Abbrechen</button>
        </div>
      </div>
    </div>
</template>

<style>
img {
  /* Verhindert das Auswählen vom image */
  user-select: none;
}
.title {
  user-select: none;
}
body {
  zoom: 100%;
}
.wheel-animation {
  animation: wheelSpin 2s ease-in-out;
}

@keyframes wheelSpin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>

<script>
import axios from "axios";
export default {
  data() {
    return {
      title: "SportSpot Login",
      postData: {
        email: "John",
        password: "Doe",
      },
      wheelAnimation: false,
    };
  },
  methods: {
    postLogin() {
      axios
        .post("http://127.0.0.1:5000/login", this.postData)
        .then((response) => {
          console.log(response);

          if (response.data.success) {
            this.startWheelAnimation();

            setTimeout(() => {
              window.location.href = "/home";
            }, 2000);
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },
    startWheelAnimation() {
      this.wheelAnimation = true;
    },
    stopWheelAnimation() {
      this.wheelAnimation = false;
    },
  },
};
</script>
