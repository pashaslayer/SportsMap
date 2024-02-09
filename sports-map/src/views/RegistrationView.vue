<template>
  <div class="container">
    <div class="text-center mt-5">
      <!-- First Row (1 Column) -->
      <div class="row text-center mx-auto">
        <div class="col-md-12">
          <!-- draggable verhindert das verschieben von images -->
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

      <form @submit.prevent="postRegister">
        <!-- @submit.prevent="postRegister"> -->
        <div class="row">
          <div
            class="col-md-2 bg-info bg-opacity-25 border border-2 border-white rounded-start border-end align-items-center d-flex justify-content-center"
          >
            <label for="firstname" class="text-center">Firstname:</label>
          </div>
          <div
            class="col-md-2 m-0 p-0 bg-white border border-2 border-white border-start-0 rounded-end"
          >
            <input
              v-model="postData.firstname"
              type="text"
              class="form-control"
              id="firstname-label"
              @input="validateFirstname"
            />
          </div>
          <div
            class="col-md-2 bg-info bg-opacity-25 border border-2 border-white rounded-start border-end align-items-center d-flex justify-content-center"
          >
            <label for="username" class="text-center">Username: </label>
          </div>
          <div
            class="col-md-2 m-0 p-0 bg-white border border-2 border-white border-start-0 rounded-end"
          >
            <!--Input Benutzername-->
            <input
              v-model="postData.username"
              type="text"
              class="form-control"
              id="username-label"
              @input="validateUsername"
            />
          </div>
          <div
            class="col-md-2 bg-info bg-opacity-25 border border-2 border-white rounded-start border-end align-items-center d-flex justify-content-center"
          >
            <label for="email-label" class="text-center">Email: </label>
          </div>
          <div
            class="col-md-2 m-0 p-0 bg-white border border-2 border-white border-start-0 rounded-end"
          >
            <!--Input Email-->
            <input
              v-model="postData.email"
              type="email"
              id="email-label"
              class="form-control"
              aria-describedby="emailHelp"
              required
            />
          </div>
        </div>

        <!-- Third Row (6 Columns) -->
        <div class="row">
          <div
            class="col-md-2 bg-info bg-opacity-25 border border-2 border-top-0 border-white rounded-start border-end align-items-center d-flex justify-content-center"
          >
            <label for="surname" class="text-center">Surname: </label>
          </div>
          <div
            class="col-md-2 m-0 p-0 bg-white border border-2 border-top-0 border-white border-start-0 rounded-end"
          >
            <!--Input Nachname-->
            <input
              v-model="postData.surname"
              type="text"
              class="form-control"
              id="surname-label"
              @input="validateSurname"
            />
          </div>
          <div
            class="col-md-2 bg-info bg-opacity-25 border border-2 border-top-0 border-white rounded-start border-end align-items-center d-flex justify-content-center"
          >
            <label for="password" class="text-center">Password:</label>
          </div>
          <div
            class="col-md-2 m-0 p-0 border border-2 border-top-0 bg-white border-white d-flex align-items-center rounded-end"
          >
            <!-- Input Password -->
            <input
              v-model="postData.password"
              type="password"
              class="form-control"
              id="password-label"
              aria-describedby="passwordHelp"
              required
              ref="passwordInput"
              @input="validatePassword"
            />
            <button
              class="btn"
              @mousedown="revealPassword"
              @mouseup="hidePassword"
            >
              Show
            </button>
          </div>
          <div
            class="col-md-2 bg-info bg-opacity-25 border border-2 border-top-0 border-white rounded-start border-end align-items-center d-flex justify-content-center"
          >
            <label for="postalcode" class="text-center">Postalcode: </label>
          </div>
          <div
            class="col-md-2 m-0 p-0 bg-white border border-2 border-top-0 border-white border-start-0 rounded-end"
          >
            <!--Input Postalcode-->
            <input
              v-model="postData.postalcode"
              type="text"
              class="form-control"
              id="postalcode-label"
              @input="validatePostalcode"
            />
          </div>
        </div>

        <!-- Fourth Row (Spacing) -->
        <div class="row" style="height: 20px"></div>

        <div class="row" style="height: 30px">
          <div class="col-md-6">Date</div>
          <div class="col-md-6">Gender</div>
        </div>

        <!-- Fifth Row (2 Columns) -->
        <div class="row">
          <div class="col-md-6">
            <input
              id="startDate"
              class="form-control"
              type="date"
              v-model="postData.birthdate"
              @input="validateBirthdate"
            />
          </div>
          <div class="col-md-6">
            <select
              v-model="postData.gender"
              id="sports"
              class="form-select"
              required
            >
              <option value="male">male</option>
              <option value="female">female</option>
              <option value="other">other</option>
            </select>
          </div>
        </div>

        <div class="row align-content-start" style="height: 80px"></div>

        <div class="d-flex justify-content-center">
          <span class="mr-2">Bereits registriert?: </span>
          <router-link to="/login">Login</router-link>
        </div>

        <div class="row">
          <div
            class="col-12 col-md-6 d-flex justify-content-md-end justify-content-center mb-2"
          >
            <button class="btn btn-primary">Bestätigen</button>
          </div>
          <div
            class="col-12 col-md-6 d-flex justify-content-md-start justify-content-center mb-2"
          >
            <button class="btn btn-secondary" @click="clear">Abbrechen</button>
          </div>
        </div>
      </form>
      <transition name="fade">
        <!-- Use a <pre> tag, which respects whitespace and line breaks. -->
        <pre v-if="showError" class="error-message">{{ errorMessage }}</pre>
      </transition>
    </div>
  </div>
</template>

<!--
Daten für die Userregistrierung
•    Vorname
•    Nachname
•    Benutzername
•    Passwort
•    Geburtstag
•    Email
•    Bevorzugte Sportarten
•    Geschlecht
•    Postleizahl
-->

<script>
import axios from "axios";

export default {
  data() {
    return {
      title: "SportsMap Registrierung",
      postData: {
        firstname: "",
        surname: "",
        username: "",
        password: "",
        birthdate: "",
        email: "",
        sports: [],
        gender: "",
        postalcode: "",
      },

      // Validation
      validator: {
        firstnameError: "",
        usernameError: "",
        surnameError: "",
        passwordError: "",
        postalcodeError: "",
        birthdateError: "",
      },
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
    validateFirstname() {
      // Firstname validation rules:
      // 1. Must not be empty.

      if (this.postData.firstname.trim() === "") {
        this.validator.firstnameError = "Firstname is required.";
      } else {
        this.validator.firstnameError = "";
      }
    },

    validateSurname() {
      // Surname validation rules:
      // 1. Must not be empty.

      if (this.postData.surname.trim() === "") {
        this.validator.surnameError = "Surname is required.";
      } else {
        this.validator.surnameError = "";
      }
    },

    validatePostalcode() {
      // Postalcode validation rules:
      // 1. Must be between 4 and 5 characters.
      // 2. Must only contain numbers.

      const postalcodeRegex = /^\d{4,5}$/; // Postal code should have 4 or 5 digits

      if (!postalcodeRegex.test(this.postData.postalcode)) {
        this.validator.postalcodeError =
          "Postal code must be 4 or 5 digits and contain only numbers.";
      } else {
        this.validator.postalcodeError = "";
      }
    },

    validateBirthdate() {
      // Birthdate validation rules:
      // 1. Birthdate should be older than 18 years from today.

      if (!this.postData.birthdate) {
        this.validator.birthdateError = "Birthdate is required.";
      } else {
        const birthdate = new Date(this.postData.birthdate);
        const today = new Date();
        let age = today.getFullYear() - birthdate.getFullYear();

        if (
          today.getMonth() < birthdate.getMonth() ||
          (today.getMonth() === birthdate.getMonth() &&
            today.getDate() < birthdate.getDate())
        ) {
          age--; // Subtract 1 year if the birthday hasn't occurred yet this year.
        }
        if (age < 18) {
          this.validator.birthdateError = "You must be at least 18 years old.";
        } else {
          this.validator.birthdateError = "";
        }
      }
    },

    displayError(messages) {
      if (Array.isArray(messages) && messages.length > 0) {
        // Join messages into a single string, separated by line breaks, or handle them as per your UI requirement
        this.errorMessage = messages.join("\n"); // or "<br/>" if you plan to display them in HTML
        this.showError = true;

        setTimeout(() => {
          this.showError = false;
        }, 3000); // Message will disappear after 3000 ms (3 seconds)
      }
    },

    isFormValid() {
      // Check if all error fields are empty (no errors)
      return (
        !this.validator.usernameError &&
        !this.validator.passwordError &&
        !this.validator.firstnameError &&
        !this.validator.surnameError &&
        !this.validator.postalcodeError &&
        !this.validator.birthdateError
      );
    },
    ////////// [END VALIDATION] //////////

    revealPassword() {
      // Change the input type to 'text' to reveal the password
      this.$refs.passwordInput.type = "text";
    },

    hidePassword() {
      // Change the input type back to 'password' to hide the password
      this.$refs.passwordInput.type = "password";
    },

    postRegister() {
      if (this.isFormValid()) {
        axios
          .post("http://127.0.0.1:5000/register", this.postData)
          .then((response) => {
            console.log(response);
            console.log(this.postData.email);

            setTimeout(() => {
              localStorage.setItem("email", this.postData.email);
              this.$router.push({ name: "PickSportsView" });
            }, 2000);
          })
          .catch((error) => {
            console.error(error);
          });
      } else {
        this.collectErrorMessagesFromValidator();
      }
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
    clear() {
      // löscht alle bisher eingetragenen inputs
      this.postData.firstname = "";
      this.postData.surname = "";
      this.postData.username = "";
      this.postData.password = "";
      this.postData.birthdate = "";
      this.postData.email = "";
      this.postData.sports = [];
      this.postData.gender = "";
      this.postData.firstname = "";
      this.postData.postalcode = "";
    },
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
  z-index: 1000; /* Make sure it's above other elements */
}

/* Define the fade transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */ {
  opacity: 0;
}

.border-bottom-remove {
  border-bottom: none !important;
}

.info {
  border: 2px;
  border-color: black;
  border-style: solid;
  margin-left: 6vw;
  margin-right: 6vw;
  margin-bottom: 1cm;
}

img {
  /* Verhindert das Auswählen vom image */
  user-select: none;
}

.title {
  user-select: none;
}

.error {
  color: red !important;
}
</style>
