<template>
  <!--  
  data-bs-keyboard        ... schließen des bootstrap offcanvas mittels esc
  data-bs-backdrop="true" ... schließen des offcanvas geht mit Klick auf restliche fläche falls "false" ... schließen geht nur über button rest ist mit unsichtbarem gitter
  d-none                  ... Diese Klasse bewirkt, dass das Element nicht auf dem Bildschirm sichtbar ist, es bleibt jedoch im HTML-Dokument vorhanden
  d-sm-block              ... Diese Klasse gehört zu den Responsive-Utilities von Bootstrap und ermöglicht es, Elemente je nach Bildschirmgröße und Breakpoint anzuzeigen oder auszublenden.
  px-0                    ... Die CSS-Klasse px-0 wird in Bootstrap verwendet, um den horizontalen (X-Achse) Padding (Innenabstand) eines HTML-Elements auf null zu setzen
  <i class="fs-5 bi-table"> .. für icon geht aber nicht bei links daher löäschen

-->
  <button
    v-if="isAuthenticated"
    @click="redirectToProfile"
    class="btn position-absolute top-0 start-0 ms-0 mt-0"
    style="margin-right: 1cm"
  >
    <!-- Font awesome icon -->
    <i class="fa-solid fa-user"></i> {{ username }}
  </button>
  <button v-if="isAuthenticated" @click="logoutUser" class="btn float-left">
    <!-- Font awesome icon -->
    <i class="fas fa-sign-out-alt"></i>
  </button>

  <button
    v-if="isAuthenticated"
    @click="redirectToMap"
    class="btn position-absolute top-0 start-1 ms-0 mt-0"
  >
    <!-- Font awesome icon -->
    <i class="fa-solid fa-map"></i>
  </button>

  <div
    class="offcanvas offcanvas-end w-10"
    id="offcanvas"
    data-bs-keyboard="false"
    data-bs-backdrop="true"
  >
    <div class="offcanvas-header">
      <h6 class="offcanvas-title d-none d-sm-block" id="offcanvas">
        <b>Menu</b>
      </h6>
      <button
        type="button"
        class="btn-close text-reset"
        data-bs-dismiss="offcanvas"
        aria-label="Close"
      ></button>
    </div>
    <div class="offcanvas-body px-0">
      <ul
        class="nav nav-pills flex-column mb-sm-auto mb-0 align-items-start"
        id="menu"
      >
        <li class="nav-item">
          <a class="nav-link text-truncate">
            <span class="ms-1 d-sm-inline"
              ><router-link to="/">Home</router-link></span
            >
          </a>
        </li>
        <li>
          <a class="nav-link text-truncate">
            <span class="ms-1 d-sm-inline"
              ><router-link to="/about">About</router-link></span
            >
          </a>
        </li>
        <li>
          <a class="nav-link text-truncate">
            <span class="ms-1 d-sm-inline"
              ><router-link to="/login">Login</router-link></span
            >
          </a>
        </li>
        <li>
          <a class="nav-link text-truncate">
            <span class="ms-1 d-sm-inline"
              ><router-link to="/registration">Registration</router-link></span
            >
          </a>
        </li>
        <li>
          <a class="nav-link text-truncate">
            <span class="ms-1 d-sm-inline"
              ><router-link to="/admin">Admin</router-link></span
            >
          </a>
        </li>
      </ul>
    </div>
  </div>
  <button
    class="btn float-end"
    data-bs-toggle="offcanvas"
    data-bs-target="#offcanvas"
    role="button"
  >
    <i
      class="fa-solid fa-bars fa-xl"
      data-bs-toggle="offcanvas"
      data-bs-target="#offcanvas"
    ></i>
  </button>
  <br />
  <router-view />
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      isAuthenticated: false,
      username: "",
    };
  },
  mounted() {
    // Call the checkJWTExpired method every 2 seconds
    this.interval = setInterval(this.checkJWTExpired, 2000);
  },
  beforeUnmount() {
    // Clear the interval when the component is destroyed
    clearInterval(this.interval);
  },
  methods: {
    async checkJWTExpired() {
      try {
        let jwt = localStorage.getItem("jwt_token");
        if (!jwt) {
          this.isAuthenticated = false; // Update isAuthenticated if no token
          return;
        }
        const response = await axios.post(
          "http://127.0.0.1:5000/jwt/isExpired",
          { jwt: jwt }
        );
        // Update isAuthenticated based on the expiration status
        this.getNickname();
        this.isAuthenticated = !response.data.expired;
      } catch (error) {
        if (error.response && error.response.status === 401) {
          this.isAuthenticated = false; // Ensure isAuthenticated is updated on error
          clearInterval(this.interval);
          alert("Your session has expired, please login again");
          setTimeout(() => {
            localStorage.clear();
            this.$router.push({ name: "login" });
          }, 500);
        }
      }
    },
    async getNickname() {
      try {
        let jwt = localStorage.getItem("jwt_token");
        const response = await axios.post("http://127.0.0.1:5000/user", {
          jwt: jwt,
        });

        this.username = response.data.username;
      } catch (error) {
        console.log(error);
      }
    },
    redirectToProfile() {
      this.$router.push("/profile");
    },
    redirectToMap() {
      this.$router.push("/map");
    },
    logoutUser() {
      localStorage.clear();
      this.checkJWTExpired();
      this.$router.push("/");
    },
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: whitesmoke;
  border: 5px;
  border-color: black;
}

body {
  background-color: #108eb3;
  color: whitesmoke;
  border: 5px;
  border-color: black;
}

nav {
  padding: 30px;
}

.offcanvas {
  color: blue;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
