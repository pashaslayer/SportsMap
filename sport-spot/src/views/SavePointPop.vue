<template>
  <div v-if="showPopup" class="popup-form">
    <div class="popup-content">
      <h2>Route</h2>

      <label for="duration">Duration (hours):</label>
      <input type="number" min="0" id="duration" v-model="duration" />

      <label for="sport">Sport:</label>
      <select id="sport" v-model="sport">
        <option value="1">Cycling</option>
        <option value="2">Hiking</option>
        <option value="3">Running</option>
        <option value="4">Skiing</option>
        <option value="5">Weightlifting</option>
      </select>

      <label for="startdate">Date: </label>
      <input type="datetime-local" id="startdate" v-model="startdate" />

      <label for="difficulty">Difficulty:</label>
      <select id="difficulty" v-model="difficulty">
        <option value="easy">Easy</option>
        <option value="moderate">Moderate</option>
        <option value="hard">Hard</option>
      </select>

      <label for="participants">Participants:</label>
      <input type="number" min="1" id="participants" v-model="participants" />

      <label> Description: </label>
      <textarea
        placeholder="enter the description"
        v-model="description"
      ></textarea>

      <div class="buttons">
        <button @click="submitDetails">Submit</button>
        <button @click="closePopup">Close</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  props: {
    showPopup: Boolean,
    onClose: Function,
  },
  data() {
    return {
      sport: null,
      duration: null,
      startdate: "",
      difficulty: "easy",
      participants: null,
      description: "",
    };
  },
  watch: {
    // This watcher looks at the property (sport). If it changes -> I will convert the number into a string and send out the converted string as
    // an emit to it's parent's component in order to change the feature icon for future reasons
    sport(value){
      this.$emit('sportIconChange', this.convertIntToSport(value));
    }
  },
  methods: {
    closePopup() {
      console.log("closePopup");
      console.log("onClose", this.onClose);
      this.$emit("handleclose");
      //this.onClose; // This should call the function passed as a prop
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
    convertIntToSport() {
      let sport;
      switch (this.sport) {
        case 1:
          sport = "cycling_kreis_blau";
          break;
        case 2:
          sport = "hiking_kreis_blau";
          break;
        case 3:
          sport = "running_kreis_blau";
          break;
        case 4:
          sport = "skiing_kreis_blau";
          break;
        case 5:
          sport = "weightlifting_kreis_blau";
          break;
      }
      return sport;
    },
    submitDetails() {
      console.log(
        "Submitting:",
        this.duration,
        this.sport,
        this.formatDatetime(this.startdate),
        this.difficulty,
        this.participants
      );
      this.$emit(
        "sendData",
        this.sport,
        this.duration,
        this.startdate,
        this.difficulty,
        this.participants,
        this.description
      );
      this.$emit("closePopup");
    },
    async postPoint() {
      if (this.coords && this.coords.length !== 0) {
        console.log(this.type);
        console.log(this.coords);
        try {
          const response = await axios.post(
            "http://127.0.0.1:5000/[YOUR_ENDPOINT]",
            {
              type: this.type,
              coords: this.coords,
            }
          );
          // Ausgabe von Typ und geoDaten
          console.log("Type:", this.type);
          console.log("Coordinates:", this.coords);
          if (response.data.success) {
            console.warn("Success!");
          }
        } catch (error) {
          console.error(error);
        }
      } else {
        console.log("No coordinates to send");
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
  left: 50px;
  z-index: 1000; /* Ensure it's above the map */
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  color: #fff;
  width: 300px; /* Adjust as needed */
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
