<template>
  <div v-if="showPersonalPoint" class="popup-form">
    <div class="popup-content">
      <h2>{{ creator_username }}</h2>
      <h4>{{ convertSportIdToString() }}</h4>

      <!-- Date -->
      <div v-if="edit">
        <label for="startdate">Date:</label>
        <input v-model="event_datetime" type="datetime-local" id="startdate" />
      </div>
      <div v-else>
        <label for="startdate">Date: {{ event_datetime }}</label>
      </div>

      <!-- Duration -->
      <div v-if="edit">
        <label for="duration">Duration (hours):</label>
        <input v-model="duration" type="number" id="duration" />
      </div>
      <div v-else>
        <label for="duration">Duration (hours): {{ duration }}</label>
      </div>

      <!-- Difficulty -->
      <div v-if="edit">
        <label for="difficulty">Difficulty:</label>
        <select id="difficulty" v-model="difficulty">
          <option value="easy">Easy</option>
          <option value="moderate">Moderate</option>
          <option value="hard">Hard</option>
        </select>
      </div>
      <div v-else>
        <label for="difficulty">Difficulty: {{ difficulty }}</label>
      </div>

      <!-- Participants -->
      <div v-if="edit">
        <label for="maxParticipants">Max Participants:</label>
        <input v-model="maxParticipants" type="number" id="maxParticipants" />
      </div>
      <div v-else>
        <label for="participants"
          >Participants: {{ participants }} / {{ maxParticipants }}</label
        >
      </div>

      <!-- Description -->
      <div v-if="edit">
        <label for="description">Description:</label>
        <textarea v-model="description" id="description"></textarea>
      </div>
      <div v-else>
        <label>Description: {{ description }}</label>
      </div>

      <div class="buttons">
        <button v-if="!edit" @click="editPoint">Edit</button>
        <button v-if="edit" class="button-save" @click="changePoint">Save</button>
        <button @click="closePersonalPopup">Close</button>
        <button v-if="edit" class="button-delete" @click="deleteEvent">
          Delete
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  props: {
    showPersonalPoint: Boolean,
    selectedEventCoordinates: Array,
  },
  watch: {
    // Dieser watcher schaut auf Änderungen von den Koordinaten und macht dann einen call zur Datenbank
    selectedEventCoordinates() {
      this.loadPointData();
    },
  },
  data() {
    return {
      sport: 0,
      duration: null,
      difficulty: "",
      participants: 0,
      maxParticipants: "",
      description: "",

      // User
      //creator_id: null,
      //age: null,
      //creator_email: "",
      //creator_firstname: "",
      //creator_surname: "",
      creator_username: "",

      // Event
      event_datetime: "",
      event_id: null,
      event_lat: null,
      event_lon: null,
      cur_participants: null,

      edit: false,
    };
  },
  methods: {
    closePersonalPopup() {
      this.$emit("handlepersonalpointclose");
    },
    editPoint() {
      this.edit = true;
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
        console.log(this.selectedEventCoordinates);

        this.event_id = response.data["event_id"];
        //this.creator_email = response.data["creator_email"];
        //this.creator_firstname = response.data["creator_firstname"];
        //this.age = response.data["age"];
        //this.creator_id = response.data["creator_id"];
        //this.creator_surname = response.data["creator_surname"];
        this.creator_username = response.data["creator_username"];
        this.event_datetime = response.data["event_date"];
        this.event_lat = response.data["event_loc"]["latitude"];
        this.event_lon = response.data["event_loc"]["longitude"];
        this.cur_participants = response.data["participants"];
        this.sport = response.data["sport"];
        this.difficulty = response.data["difficulty"];
        this.description = response.data["description"];
        this.maxParticipants = response.data["max_participants"];
        this.duration = response.data["duration"];

        console.log(response.data);
        console.log(response.data["age"]);
      } catch (error) {
        console.log(error);
      }
    },
    async deleteEvent() {
      /* false / true values */
      let result = confirm("Do you really want to delete the event?");
      if (result) {
        try {
          const response = await axios.post(
            "http://127.0.0.1:5000/map/anzeigen/delete",
            {
              coords: this.selectedEventCoordinates,
            }
          );
          console.log(response);
          this.closePersonalPopup();
        } catch (error) {
          console.log(error);
        }
      }
    },
    async changePoint() {
      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/maps/change",
          {
            coords: this.selectedEventCoordinates,
            startdate: this.event_datetime,
            difficulty: this.difficulty,
            description: this.description,
            participants: this.maxParticipants,
            duration: this.duration,
          }
        );
        console.log(response);
        this.closePersonalPopup();
        this.edit = false;
      } catch (error) {
        console.log(error);
      }
    },
  },
};
</script>

<style>
.popup-form {
  background-color: lightblue;
  position: absolute;
  top: 50px;
  right: 50px;
  z-index: 1000;
  /* Ensure it's above the map */
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  color: darkblue;
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

.button-delete:hover {
  background-color: red;
}

.button-save:hover {
  background-color: green;
}

button:hover {
  background-color: #555;
}
</style>
