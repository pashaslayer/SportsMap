<template>
    <div v-if="this.showPopupPoint" class="popup-form">
      <div class="popup-content">
        <h2> {{ sport }}</h2>
  
        <label for="sport">Sport:</label>
  
        <label for="startdate">Date: {{ startdate }}</label>
        
        <label for="duration">Duration (hours): {{ duration }}</label>
  
        <label for="difficulty">Difficulty: {{ difficulty }}</label>
  
        <label for="participants">Participants: {{ participants }}</label>
  
        <label> Description: {{ description }}</label>

        <label> Coordinates: {{ this.selectedEventCoordinates }}</label>
  
        <div class="buttons">
          <button @click="enterEvent">Take part</button>
          <button @click="closePopup">Close</button>
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
      selectedEventCoordinates: Array
    },
    data() {
      return {
        sport: null,
        duration: null,
        startdate: null,
        difficulty: "easy",
        participants: null,
        description: "",
      };
    },
    watch: {
      // If the popup opens, the Point data should be received from the database
      showPopupPoint(value){
      if(value == true){
        this.loadPointData();
      }
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
  
          console.log(formattedDatetimeStr);
        return formattedDatetimeStr;
      },
      enterEvent(){

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
          this.formatDatetime(this.startdate),
          this.difficulty,
          this.participants,
          this.description
        );
        this.$emit("closePopup");
      },
      async loadPointData() {
      try {
        console.log("pwnisdifnsdofn " + this.selectedEventCoordinates);
        let gay = {
            coords: this.selectedEventCoordinates
          }
          console.log("gay" + gay["coords"]);
        const response = await axios.get("http://127.0.0.1:5000/maps/anzeigen", {
            coords: this.selectedEventCoordinates
          });
        console.log(response.data);
        console.log(response);
        
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
  