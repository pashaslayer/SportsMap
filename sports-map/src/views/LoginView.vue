<template>
  <meta
    name="viewport"
    content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no"
  />
  <div class="container mt-5">
    <div class="row text-center mx-auto">
      <div class="col-md-12">
        <img
          src="@/assets/Logo_V3_1_final_noBG_white.svg"
          class="rounded mx-auto d-block img-fluid"
          width="150px"
          height="100px"
          draggable="false"
        />
        <h1 class="title">{{ title }}</h1>
      </div>
    </div>

    <!-- Für einen Abstand falls es so besser ausschaut -->
    <!-- <div class="row" style="height: 40px"></div> -->

    <div class="row justify-content-center">
      <div
        class="col-md-2 bg-info bg-opacity-25 border border-2 border-white rounded-start border-end align-items-center d-flex justify-content-center"
      >
        <label for="username" class="text-center">Username:</label>
      </div>
      <div
        class="col-md-2 m-0 p-0 bg-white border border-2 border-white border-start-0 rounded-end"
      >
        <input
          v-model="postData.username"
          type="text"
          class="form-control"
          id="username-label"
          @input="validateUsername"
        />
      </div>
    </div>

    <div class="row justify-content-center">
      <div
        class="col-md-2 bg-info bg-opacity-25 border border-2 border-top-0 border-white rounded-start border-end align-items-center d-flex justify-content-center"
      >
        <label for="password" class="text-center">Password: </label>
      </div>
      <div
        class="col-md-2 m-0 p-0 bg-white border border-2 border-white border-top-0 border-start-0 rounded-end"
      >
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

      <div class="d-flex justify-content-center">
        <span class="mr-2">Noch nicht registriert?: </span>
        <router-link to="/registration">Register</router-link>
      </div>
    </div>

    <div class="row" style="height: 20px"></div>

    <div class="row">
      <div
        class="col-12 col-md-6 d-flex justify-content-md-end justify-content-center mb-2"
      >
        <button type="submit" class="btn btn-primary" @click="postLogin">
          Bestätigen
        </button>
      </div>
      <div
        class="col-12 col-md-6 d-flex justify-content-md-start justify-content-center mb-2"
      >
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

  <transition name="fade">
    <!-- Use a <pre> tag, which respects whitespace and line breaks. -->
    <pre v-if="showError" class="error-message">{{ errorMessage }}</pre>
  </transition>
</template>

<script>
import CaptchaView from "./CaptchaView.vue";
import axios from "axios";

export default {
  data() {
    return {
      title: "SportsMap Login",
      postData: {
        username: "",
        password: "",
      },
      validator: {
        usernameError: "",
        passwordError: "",
      },
      showCaptchaModal: false,
      errorMessage: null,
      showError: false,
    };
  },
  watch: {
    validator: {
      handler(newValue) {
        let errorMessages = [];
        for (let key in newValue) {
          if (newValue[key] !== "") {
            errorMessages.push(newValue[key]);
          }
        }
        if (errorMessages.length > 0) {
          this.displayError(errorMessages);
        }
      },
      deep: true,
    },
  },
  methods: {
    ////////// [VALIDATION] //////////
    validateUsername() {
      // Username validation rules:
      // 1. Must be between 5 and 15 characters long.
      // 2. Can contain letters (both uppercase and lowercase), numbers, underscores, and hyphens.
      // 3. Should not start or end with a space.

      const minLen = 5;
      const maxLen = 15;
      const usernameRegex = /^[a-zA-Z0-9_-]{5,15}$/;

      if (
        this.postData.username.length < minLen ||
        this.postData.username.length > maxLen
      ) {
        this.validator.usernameError = `Username must be between ${minLen} and ${maxLen} characters long.`;
      } else if (!usernameRegex.test(this.postData.username)) {
        this.validator.usernameError =
          "Username can only contain letters, numbers, underscores, and hyphens.";
      } else {
        this.validator.usernameError = "";
      }
    },

    validatePassword() {
      if (this.postData.password.length < 6) {
        this.validator.passwordError =
          "Password must be longer than 5 characters.";
      } else if (this.postData.password.length > 16) {
        this.validator.passwordError =
          "Password must be shorter than 16 characters.";
      } else {
        this.validator.passwordError = "";
      }
    },

    isFormValid() {
      if (!this.validator.usernameError && !this.validator.passwordError) {
        return true;
      } else {
        return false;
      }
    },
    displayError(messages) {
      if (Array.isArray(messages) && messages.length > 0) {
        // Join messages into a single string, separated by line breaks, or handle them as per your UI requirement
        this.errorMessage = messages.join("\n"); // or "<br/>" if you plan to display them in HTML
        this.showError = true;

        setTimeout(() => {
          this.showError = false;
        }, 3000);
      }
    },
    ////////// [END VALIDATION] //////////

    postLogin() {
      if (this.isFormValid()) {
        // only open the captcha if the form is valid
        this.showCaptchaModal = true;
      } else {
        // If the form still contains validation errors they should be shown
        this.collectErrorMessagesFromValidator();
      }
    },
    closeModal() {
      this.showCaptchaModal = false;
    },
    collectErrorMessagesFromValidator() {
      let errorMessages = [];
      for (let key in this.validator) {
        if (this.validator[key] !== "") {
          errorMessages.push(this.validator[key]);
        }
      }
      if (errorMessages.length > 0) {
        this.displayError(errorMessages);
      }
    },

    handleCaptchaFail() {
      console.log(
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
      );
      this.displayError("Failed to ");
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
    storeTokenInLocalStorage(token) {
      try {
        // Use a secure method to store the token in local storage
        localStorage.setItem("jwt_token", token);
      } catch (error) {
        console.error("Error storing token in local storage:", error);
      }
    },
  },
  components: {
    CaptchaView,
  },
};
</script>

<style>
.error-message {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background-color: red;
  color: white;
  padding: 10px;
  border-radius: 5px;
  z-index: 1000;
  /* Make sure it's above other elements */
}

/* Define the fade transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter,
.fade-leave-to

/* .fade-leave-active in <2.1.8 */ {
  opacity: 0;
}

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

.error {
  color: red !important;
}
</style>
