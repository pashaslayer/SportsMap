<template>
  <div v-if="showPopup" class="popup-form">
    <div class="popup-content">
      <h2>Route</h2>

      <label for="length">Length (km):</label>
      <input type="number" id="length" v-model="length">

      <label for="duration">Duration (hours):</label>
      <input type="number" id="duration" v-model="duration">

      <label for="difficulty">Difficulty:</label>
      <select id="difficulty" v-model="difficulty">
        <option value="easy">Easy</option>
        <option value="moderate">Moderate</option>
        <option value="hard">Hard</option>
      </select>

      <label for="participants">Participants:</label>
      <input type="number" id="participants" v-model="participants">

      <label> Description: </label>
      <textarea placeholder="enter the description" v-model="description"></textarea>

      <div class="buttons">
        <button @click="submitDetails">Submit</button>
        <button @click="closePopup">Close</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    showPopup: Boolean,
    onClose: Function,
  },
  data() {
    return {
      length: null,
      duration: null,
      difficulty: 'easy',
      participants: null,
      description: "",
    };
  },
  methods: {
    closePopup() {
      console.log('closePopup');
      console.log("onClose", this.onClose);
      this.$emit('handleclose');
      //this.onClose; // This should call the function passed as a prop

    },
    submitDetails() {
      console.log('Submitting:', this.length, this.duration, this.difficulty, this.participants);
      //this.closePopup();
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

input[type="number"], select {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
  border-radius: 4px;
  border: 1px solid #ddd;
}

#description{
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