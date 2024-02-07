<template>
  <div class="mypage">
    <div class="header">
      <h4>{{ username }}</h4>
    </div>
    <div class="info">
      <p><span>Name:</span> {{ firstname + " " + surname }}</p>
      <p><span>Email:</span> {{ email }}</p>
      <p><span>Birthdate:</span> {{ birthdate }}</p>
      <p><span>Sports:</span> {{ sports }}</p>
      <p><span>Gender:</span> {{ gender }}</p>
      <p><span>Postal Code:</span> {{ postalcode }}</p>
    </div>
    <div class="actions">
      <button v-on:click="deleteUser">Delete Your Account</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      userid: 0,
      firstname: "",
      surname: "",
      username: "",
      birthdate: "",
      email: "",
      sports: "",
      gender: "",
      postalcode: "",
    };
  },
  methods: {
    async getUserData() {
      try {
        let jwt = localStorage.getItem("jwt_token");
        const response = await axios.post("http://127.0.0.1:5000/user", {
          jwt: jwt,
        });

        this.userid = response.data.userid;
        this.username = response.data.username;
        this.firstname = response.data.firstname;
        this.surname = response.data.surname;
        this.username = response.data.username;
        this.birthdate = response.data.birthdate;
        this.email = response.data.email;
        this.sports = response.data.sports;
        this.gender = response.data.gender;
        this.postalcode = response.data.postalcode;
      } catch (error) {
        console.log(error);
      }
    },
    async deleteUser() {
      let result = confirm("Are you sure you want to delete your user?");
      if (result) {
        try {
          await axios.delete(
            `http://127.0.0.1:5000/delete/user/${this.userid}`
          );
          localStorage.clear();
          alert("The user has been deleted!");
          this.$router.push("/");
        } catch (error) {
          console.log(error);
        }
      }
    },
  },
  mounted() {
    this.getUserData();
  },
};
</script>
<style scoped>
.mypage {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  max-width: 400px;
  margin: auto;
  margin-top: 50vh; /* This pushes the top of the container to the middle of the viewport */
  transform: translateY(-90%); /* This pulls the container back up by half its own height */
  background-color: #f5f5f5;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header h4 {
  margin: 0;
  color: #333;
  text-align: center;
}

.info {
  width: 100%;
  margin-top: 20px;
}

.info p {
  margin: 5px 0;
  line-height: 1.6;
  color: #666;
}

.info p span {
  font-weight: bold;
  color: #333;
}

.actions {
  margin-top: 20px;
}

button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  background-color: #ff5252;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #ff3b3b;
}
</style>
