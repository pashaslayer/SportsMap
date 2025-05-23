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
          >Participants: {{ cur_participants }} / {{ maxParticipants }}</label
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
        <button v-if="edit" class="button-save" @click="changePoint">
          Save
        </button>
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
    selectedEventCoordinates() {
      this.loadPointData();
    },
  },
  data() {
    return {
      sport: 0,
      duration: null,
      difficulty: "",
      maxParticipants: "",
      description: "",

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
      this.edit = false;
      this.$emit("handlepersonalpointclose");
    },
    editPoint() {
      this.edit = true;
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
        let jwt = localStorage.getItem("jwt_token");
        const response = await axios.post(
          "http://127.0.0.1:5000/maps/anzeigen",
          {
            coords: this.selectedEventCoordinates,
            jwt: jwt,
          }
        );

        this.event_id = response.data[0]["event_id"];
        //this.creator_email = response.data["creator_email"];
        //this.creator_firstname = response.data["creator_firstname"];
        //this.age = response.data["age"];
        //this.creator_id = response.data["creator_id"];
        //this.creator_surname = response.data["creator_surname"];
        this.creator_username = response.data[0]["creator_username"];
        this.event_datetime = response.data[0]["event_date"];
        this.event_lat = response.data[0]["event_loc"]["latitude"];
        this.event_lon = response.data[0]["event_loc"]["longitude"];
        this.cur_participants = response.data[0]["participants"];
        this.sport = response.data[0]["sport"];
        this.difficulty = response.data[0]["difficulty"];
        this.description = response.data[0]["description"];
        this.maxParticipants = response.data[0]["max_participants"];
        this.duration = response.data[0]["duration"];
      } catch (error) {
        console.log(error);
      }
    },
    async deleteEvent() {
      let result = confirm("Do you really want to delete the event?");
      if (result) {
        try {
          let jwt = localStorage.getItem("jwt_token");
          const response = await axios.post(
            "http://127.0.0.1:5000/map/anzeigen/delete",
            {
              coords: this.selectedEventCoordinates,
              jwt: jwt,
            }
          );
          console.log(response);

          this.closePersonalPopup();
          this.$emit("loadmap");
        } catch (error) {
          console.log(error);
        }
      }
    },
    async changePoint() {
      try {
        const response = await axios.post("http://127.0.0.1:5000/maps/change", {
          event_id: this.event_id,
          coords: this.selectedEventCoordinates,
          startdate: this.event_datetime,
          difficulty: this.difficulty,
          description: this.description,
          participants: this.maxParticipants,
          duration: this.duration,
        });
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
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  color: darkblue;
  width: 300px;
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
