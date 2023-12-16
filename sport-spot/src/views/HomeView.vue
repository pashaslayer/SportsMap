<template>
  <div class="home">
    <!-- <img alt="Vue logo" src="../assets/logo.png"> -->
    <h1>This is our home page</h1>
    <p>{{ message }}</p>
    <button v-on:click="deleteJWTFromLocalStorage">Clear Local Storage</button>

    <!-- 
    <button v-on:click="message+='m'">lol</button>
    <br>
    <button v-on:click="giveMeARandomNumber">Random number</button>
    <p1>{{ random }}</p1>
    <br>
    <input v-model="sameText" />
    <h3>{{ sameText }}</h3>
    <p> {{ tets }}</p>
      IF ELSE
      v-if
      v-else-if
      v-else 
    -->

    <!--
      Events and Variables

      Events:

      v-on [:click]
      kürzel für v-on: @click => genau gleich wie v-on:click

      @keyup => keyboard events => Beispiel: <input @keyup.enter="greet" v-model="greeting" /> oder @click.right 
    -->

    

  </div>
</template>

<script>
export default {
  data() {
    return {
      message: "Press to clear the local storage",
      random: 0,
      sameText: "nihao",
      tets: localStorage.getItem('jwt_token')
    }
  },

  methods: {
    giveMeARandomNumber() {
      this.random = Math.random();
    },
    deleteJWTFromLocalStorage(){
      localStorage.clear();
    }
  }
};
</script>
