<template>
  <meta
    name="viewport"
    content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no"
  />
  <div class="container mt-5">
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

    <div class="row">
      <div
        class="col-md-6 border border-white align-items-center d-flex justify-content-center"
      >
        <label for="username" class="form-label">Username:</label>
      </div>
      <div class="col-md-6 border border-white">
        <input
          v-model="postData.username"
          type="text"
          class="form-control"
          id="username-label"
        />
      </div>
    </div>

    <div class="row">
      <div
        class="col-md-6 border border-white align-items-center d-flex justify-content-center"
      >
        <label for="password" class="form-label">Password: </label>
      </div>
      <div class="col-md-6 border border-white">
        <input
          v-model="postData.password"
          type="password"
          class="form-control"
          id="password-label"
          aria-describedby="passwordHelp"
          required
        />
      </div>
    </div>

    <div class="row" style="height: 20px"></div>

    <div class="row" style="height: 80px"></div>

    <div class="d-flex justify-content-center">
      <span class="mr-2">Noch nicht registriert?: </span>
      <router-link to="/registration">Register</router-link>
    </div>

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
        username: "",
        password: "",
      },
      wheelAnimation: false,
    };
  },
  methods: {
    async postLogin() {
      axios
        .post("http://127.0.0.1:5000/login", this.postData)
        .then((response) => {
          const token = response.data.token;

          // setting the JWT Token inside the local storage
          this.storeTokenInLocalStorage(token);

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
    async getExpirationTime() {
      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/getExpirationTime",
          {
            token: localStorage.getItem("jwt_token"),
          }
        );
        // convert to milliseconds
        return response.data * 1000;
      } catch (error) {
        console.error("Error getting expiration time:", error);
        throw error;
      }
    },
    startWheelAnimation() {
      this.wheelAnimation = true;
    },
    stopWheelAnimation() {
      this.wheelAnimation = false;
    },
    storeTokenInLocalStorage(token) {
      try {
        // Use a secure method to store the token in local storage
        localStorage.setItem("jwt_token", token);
        // Optionally, store the token expiration time

        // Send JWT Token for extracting expirationTime on server side due to security reasons

        // const expirationTime = this.getExpirationTime();
        // localStorage.setItem("jwt_token_exp", expirationTime);
      } catch (error) {
        console.error("Error storing token in local storage:", error);
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
  },
};

// JWT Token

// localStorage.setItem("Name", "Bob");
// localStorage.getItem('Name');
// localStorage.removeItem('Name');
</script>
