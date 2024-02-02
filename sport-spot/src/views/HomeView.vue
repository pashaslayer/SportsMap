<template>
  <div class="home">
    <div class="top-section">
      <img
        src="@/assets/Logo_V3_1_final_noBG_white.svg"
        alt="SportsMap Logo"
        class="logo"
      />
      <h1 class="headline">SportsMap</h1>
    </div>
    <!--<p>{{ tets }}</p>
    <button v-on:click="deleteJWTFromLocalStorage">Clear Local Storage</button>
    -->

    <div class="bottom-section">
      <div class="text-content">
        <div class="left-text">
          <p>
            Entdecken Sie Ihre sportliche Welt wie nie zuvor! SportsMap ist die
            ultimative Plattform für Sportbegeisterte aller Art. Ob Sie nach
            neuen Trainingspartnern suchen,<br />an lokalen Sportevents
            teilnehmen möchten oder einfach nur Inspiration für Ihre nächste
            sportliche Aktivität brauchen – bei uns sind Sie genau richtig!
          </p>
        </div>
        <div class="right-text">
          <ul>
            <li>
              Vernetzen Sie sich: Finden Sie Gleichgesinnte in Ihrer Nähe und
              treten Sie Sportgruppen bei.
            </li>
            <li>
              Planen und Teilnehmen: Erstellen Sie eigene Sportevents oder
              schließen Sie sich bestehenden an.
            </li>
            <li>
              Sportlich aktiv werden: Entdecken Sie eine Vielzahl von Sportarten
              und bleiben Sie fit und aktiv.
            </li>
          </ul>
        </div>
      </div>
      <p class="bottom-text">
        Bereit, loszulegen?
        <a v-on:click="navigateTo('/registration')" class="blue-link"
          >Registrieren</a
        >
        Sie sich jetzt oder
        <a v-on:click="navigateTo('/login')" class="blue-link"
          >melden Sie sich an</a
        >, um die Welt des Sports zu erkunden.
      </p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      //tets: localStorage.getItem("jwt_token"),
    };
  },
  methods: {
    navigateTo(route) {
      this.$router.push(route);
    },
    giveMeARandomNumber() {
      this.random = Math.random();
    },
    deleteJWTFromLocalStorage() {
      localStorage.clear();
    },
  },
};
</script>

<style>
body {
  overflow-x: hidden;
}

.home {
  text-align: center;
  margin: 0;
  padding: 0;
  width: 100vw;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  overflow: hidden;
  max-width: 100%;
}

.top-section,
.bottom-section {
  flex: 1 1 auto;
  margin: 0;
  padding: 0;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.top-section {
  height: 45vh;
  background-image: url("@/assets/bg_start.png");
  background-size: cover;
  background-position: center;
  color: white;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin: 0;
  padding: 0;
  width: 100vw;
}

.logo {
  max-height: 30vh;
  width: auto;
}

.headline {
  font-size: 3em;
}

.bottom-section {
  background-color: rgb(19, 142, 179);
  color: white;
  padding: 10px;
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100;
}

.text-content {
  max-width: none;
  margin: auto;
  font-size: 1.2em;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.right-text ul {
  list-style-type: none;
}

.left-text,
.right-text {
  width: 100%;
  margin-bottom: 20px;
}

.blue-link {
  color: blue;
  text-decoration: underline;
  cursor: pointer;
}

.blue-link:hover {
  text-decoration: none;
}

.bottom-text {
  font-size: 1.2em;
  padding: 20px;
  align-items: left-text;
}
</style>
