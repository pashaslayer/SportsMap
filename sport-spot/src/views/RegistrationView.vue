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

      <form @submit.prevent="postRegister">
        <!-- Second Row (6 Columns) -->
        <div class="row">
          <div class="col-md-2 border border-white">
            <label for="firstname" class="form-label">Firstname:</label>
          </div>
          <div class="col-md-2 border border-white">
            <input
              v-model="postData.firstname"
              type="text"
              class="form-control"
              id="firstname-label"
              onkeydown="return /[a-z]/i.test(event.key) required"
            />
          </div>
          <div class="col-md-2 border border-white">
            <label for="username" class="form-label">Username: </label>
          </div>
          <div class="col-md-2 border border-white">
            <!--Input Benutzername-->
            <input
              v-model="postData.username"
              type="text"
              class="form-control"
              id="username-label"
              onkeydown="return /[a-z,1-9,!,?,_]/i.test(event.key) required"
              minlength="6"
              maxlength="10"
            />
          </div>
          <div class="col-md-2 border border-white">
            <label for="email-label" class="form-label">Email: </label>
          </div>
          <div class="col-md-2 border border-white">
            <!--Input Email-->
            <input
              v-model="postData.email"
              type="email"
              id="email-label"
              aria-describedby="emailHelp"
              required
            />
          </div>
        </div>

        <!-- Third Row (6 Columns) -->
        <div class="row">
          <div class="col-md-2 border border-white">
            <label for="lastname" class="form-label">Lastname: </label>
          </div>
          <div class="col-md-2 border border-white">
            <!--Input Nachname-->
            <input
              v-model="postData.lastname"
              type="text"
              class="form-control"
              id="lastname-label"
              onkeydown="return /[a-z]/i.test(event.key) required"
            />
          </div>
          <div class="col-md-2 border border-white">
            <label for="password" class="form-label">Password: </label>
          </div>
          <div class="col-md-2 border border-white">
            <!--Input Passwort-->
            <input
              v-model="postData.password"
              type="password"
              class="form-control"
              id="password-label"
              aria-describedby="passwordHelp"
              required
            />
          </div>
          <div class="col-md-2 border border-white">
            <label for="postalcode" class="form-label">Postalcode: </label>
          </div>
          <div class="col-md-2 border border-white">
            <!--Input Plz-->
            <input
              v-model="postData.postalcode"
              type="text"
              class="form-control"
              id="postalcode-label"
              onkeydown="return /[1-9]/i.test(event.key)"
              maxlength="8"
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
            <input id="startDate" class="form-control" type="date" />
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
      </form>
    </div>

    <div class="info">
      <p>Firstname: {{ postData.firstname }}</p>
      <p>Lastname: {{ postData.lastname }}</p>
      <p>Username: {{ postData.username }}</p>
      <p>Password: {{ postData.password }}</p>
      <p>Birthdate: {{ postData.birthdate }}</p>
      <p>Email: {{ postData.email }}</p>
      <p>Sports: {{ postData.sports }}</p>
      <p>Gender: {{ postData.gender }}</p>
      <p>Postalcode: {{ postData.postalcode }}</p>
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



<style>
.info {
  border: 2px;
  border-color: black;
  border-style: solid;
  margin-left: 6cm;
  margin-right: 6cm;
  margin-bottom: 1cm;
}

.tocenter {
  width: 1600px;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
</style>

<script>
import axios from "axios";

export default {
  data() {
    return {
      title: "SportSpot Registrierung",
      postData: {
        firstname: "",
        lastname: "",
        username: "",
        password: "",
        birthdate: "",
        email: "",
        sports: [
          "running",
          "cycling",
          "fast-walking",
          "hobby-horsing",
          "hiking",
          "skating",
          "yoga",
        ],
        gender: "",
        postalcode: "",
      },
    };
  },
  methods: {
    postRegister() {
      axios
        .post("http://127.0.0.1:5000/register", this.postData)
        .then((response) => console.log(response));
    },
  },
};

// JWT Token

// localStorage.setItem("Name", "Bob");
// localStorage.getItem('Name');
// localStorage.removeItem('Name');
</script>
