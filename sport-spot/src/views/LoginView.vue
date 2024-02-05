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
          @input="validateUsername"
        />
      </div>
      <p class="error" v-if="usernameError">{{ usernameError }}</p>
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
          @input="validatePassword"
        />
      </div>
      <p class="error" v-if="passwordError">{{ passwordError }}</p>

      <div class="d-flex justify-content-center">
        <span class="mr-2">Noch nicht registriert?: </span>
        <router-link to="/registration">Register</router-link>
      </div>
    </div>

    <div class="row" style="height: 20px"></div>

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

  <br />
  <br />
  <button type="submit" class="btn btn-secondary" @click="handleCaptchaSuccess">
    Cheat Button für Testzwecke um Captcha nicht ausfüllen zu müssen
  </button>

  <div v-if="showCaptchaModal" class="modal">
    <CaptchaView
      @captcha-success="handleCaptchaSuccess"
      @captcha-fail="handleCaptchaFail"
      @close-modal="closeModal"
    />
  </div>
</template>

<script>
import CaptchaView from "./CaptchaView.vue";
import axios from "axios";

export default {
  data() {
    return {
      title: "SportSpot Login",
      postData: {
        username: "",
        password: "",
      },
      usernameError: "",
      passwordError: "",
      wheelAnimation: false,
      showCaptchaModal: false,
    };
  },

  methods: {
    ////////// [VALIDATION] //////////
    validateUsername() {
      // Username validation rules:
      // 1. Must be between 3 and 15 characters long.
      // 2. Can contain letters (both uppercase and lowercase), numbers, underscores, and hyphens.
      // 3. Should not start or end with a space.

      const minLen = 3;
      const maxLen = 15;
      const usernameRegex = /^[a-zA-Z0-9_-]{3,15}$/;

      if (
        this.postData.username.length < minLen ||
        this.postData.username.length > maxLen
      ) {
        this.usernameError = `Username must be between ${minLen} and ${maxLen} characters long.`;
      } else if (!usernameRegex.test(this.postData.username)) {
        this.usernameError =
          "Username can only contain letters, numbers, underscores, and hyphens.";
      } else {
        this.usernameError = "";
      }
    },

    validatePassword() {
      if (this.postData.password.length < 6) {
        this.passwordError = "Password must be longer than 5 characters.";
      } else if (this.postData.password.length > 14) {
        this.passwordError = "Password must be shorter than 14 characters.";
      } else {
        this.passwordError = "";
      }
    },

    isFormValid() {
      if (!this.usernameError && !this.passwordError) {
        return true;
      } else {
        return false;
      }
    },
    ////////// [END VALIDATION] //////////

    postLogin() {
      if (this.isFormValid()) {
        // only open the captcha if the form is valid
        this.showCaptchaModal = true;
      }
    },
    closeModal() {
      this.showCaptchaModal = false;
    },
    handleCaptchaSuccess() {
      // Hide Captcha modal
      this.showCaptchaModal = false;

      // Proceed with sending login data
      axios
        .post("http://127.0.0.1:5000/login", this.postData)
        .then((response) => {
          this.storeTokenInLocalStorage(response.data.token);
          setTimeout(() => {
            this.$router.push("/map");
          }, 1000);
        })
        .catch((error) => {
          console.log(error);
        });
    },

    handleCaptchaFail() {
      // Show an error message and fetch a new captcha
      // You might need to implement a method in CaptchaView.vue to refresh the captcha
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
  components: {
    CaptchaView,
  },
};
</script>

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
.error {
  color: red !important;
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
