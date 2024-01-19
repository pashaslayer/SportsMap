<template>
  <div v-if="this.showPopupPoint" class="popup-form">
    <div class="popup-content">
      <h2>{{ convertSportIdToString() }}</h2>

      <h4>Organisator:</h4>
      <label for="creator_firstname">
        Name: {{ creator_firstname + " " }} {{ creator_surname }}</label
      >
      <label for="email">Email: {{ creator_email }}</label>
      <label for="age">Age: {{ age }}</label>

      <label for="startdate">Date: {{ event_date }}</label>

      <label for="duration">Duration (hours): {{ duration }}</label>

      <label for="difficulty">Difficulty: {{ difficulty }}</label>

      <label for="participants">Participants: {{ participants }}</label>

      <label> Description: {{ description }}</label>

      <label> Coordinates: {{ this.selectedEventCoordinates }}</label>

      <div class="buttons">
        <button @click="enterEvent">Take part</button>
        <button @click="closePointPopup">Close</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  props: {
    showPopupPoint: Boolean,
    onClose: Function,
    selectedEventCoordinates: Array,
  },
  data() {
    return {
      sport: 0,
      duration: null,
      difficulty: "easy",
      participants: null,
      description: "",

      // User
      creator_id: null,
      age: null,
      creator_email: "",
      creator_firstname: "",
      creator_surname: "",
      creator_username: "",

      // Event
      event_date: "",
      event_id: null,
      event_lat: null,
      event_lon: null,
      cur_participants: null,
    };
  },
  watch: {
    // Dieser watcher schaut auf Änderungen von den Koordinaten und macht dann einen call zur Datenbank
    selectedEventCoordinates() {
      this.loadPointData();
    },
  },
  methods: {
    closePointPopup() {
      this.$emit("handlepointclose");
    },
    formatDatetime(originalDatetimeStr) {
      // Convert the string to a Date object
      const originalDatetime = new Date(originalDatetimeStr);
      const formattedDatetimeStr = originalDatetime
        .toISOString()
        .slice(0, 19)
        .replace("T", " ");
      return formattedDatetimeStr;
    },
    enterEvent() {},
    convertSportIdToString() {
      var sportInString = "";
      switch (this.sport) {
        case 1:
          sportInString = "Cycling";
          break;
        case 2:
          sportInString = "Hiking";
          break;
        case 3:
          sportInString = "Running";
          break;
        case 4:
          sportInString = "Skiing";
          break;
        case 5:
          sportInString = "Weightlifting";
          break;
      }
      return sportInString;
    },
    async loadPointData() {
      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/maps/anzeigen",
          {
            coords: this.selectedEventCoordinates,
          }
        );

        this.event_id = response.data["event_id"];
        this.creator_email = response.data["creator_email"];
        this.creator_firstname = response.data["creator_firstname"];
        this.age = response.data["age"];
        this.creator_id = response.data["creator_id"];
        this.creator_surname = response.data["creator_surname"];
        this.creator_username = response.data["creator_username"];
        this.event_date = response.data["event_date"];
        this.event_lat = response.data["event_loc"]["latitude"];
        this.event_lon = response.data["event_loc"]["longitude"];
        this.cur_participants = response.data["participants"];
        this.sport = response.data["sport"];

        console.log(response.data);
        console.log(response.data["age"]);
      } catch (error) {
        console.log(error);
      }
    },
  },
};
</script>

<style>
.popup-form {
  background-color: tan;
  position: absolute;
  top: 50px;
  right: 50px;
  z-index: 1000;
  /* Ensure it's above the map */
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  color: #fff;
  width: 300px;
  /* Adjust as needed */
}

.popup-content {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.popup-content h3 {
  margin-top: 0;
}

label {
  margin-bottom: 5px;
  font-weight: bold;
}

input[type="number"],
select {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
  border-radius: 4px;
  border: 1px solid #ddd;
}

#description {
  height: 2cm;
}

.buttons {
  display: flex;
  justify-content: space-between;
}

button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  background-color: #444;
  color: white;
  cursor: pointer;
}

button:hover {
  background-color: #555;
}
</style>
