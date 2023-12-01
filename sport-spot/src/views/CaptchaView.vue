<template>
  <div>
    <h1 style="user-select: none; justify-content: center; align-items: center;">Captcha</h1>
    <div
      v-if="svg"
      v-html="svg"
      class="rounded mx-auto d-block"
      style="
        margin: auto;
        padding: auto;
        height: fit-content;
        width: fit-content;
        user-select: none;
      "
      @click="fetchCaptcha"
    ></div>
  </div>
  <input
    v-model="compare.input"
    type="text"
    class="form-control"
    required
  />
  <button type="submit" class="btn btn-primary" @click="compareCaptcha">
    Send
  </button>
  <p v-if="compare.input.length < 5 || compare.input.length > 5">
      Input should be exactly 5 characters.
    </p>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      svg: "",
      success: false,
      compare: {
        id: 0,
        input: "",
      },
    };
  },
  mounted() {
    this.fetchCaptcha();
  },
  methods: {
    async fetchCaptcha() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/getCaptcha");
        this.svg = response.data["svg"];
        this.compare.id = response.data["captcha_id"];
        console.log(this.svg);
      } catch (error) {
        console.error("Error creating svg:", error);
      }
    },
    async compareCaptcha() {
      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/compareInput",
          this.compare
        );
        if (response.status == 201) {
          console.log("very nice");
        }
        else {
          console.log("Input should be exactly 5 characters.");
        }
      } catch (error) {
        console.error("Error comparing captcha:", error);
        this.fetchCaptcha();
      }
    },
  },
};
</script>
