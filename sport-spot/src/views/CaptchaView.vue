<template>
  <div class="modal" style="display: block">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Captcha Verification</h5>
          <button type="button" class="close" @click="$emit('close-modal')">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <div
            v-if="svg"
            v-html="svg"
            class="captcha-image"
            @click="fetchCaptcha"
          ></div>
          <input
            v-model="compare.input"
            type="text"
            class="form-control mt-3"
            required
            placeholder="Enter Captcha Here"
          />
          <p
            v-if="compare.input.length < 5 || compare.input.length > 5"
            class="text-danger mt-2"
          >
            Input should be exactly 5 characters.
          </p>
        </div>
        <div class="modal-footer">
          <button type="submit" class="btn btn-primary" @click="compareCaptcha">
            Send
          </button>
        </div>
      </div>
    </div>
  </div>
  <div class="modal-backdrop"></div>
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
          this.$emit("captcha-success");
        } else {
          this.$emit("captcha-fail");
        }
      } catch (error) {
        console.error("Error comparing captcha:", error);
        this.fetchCaptcha();
      }
    },
  },
};
</script>
<style>
.modal {
  position: fixed;
  z-index: 1000;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(0, 0, 0, 0.6);
}

.modal-title {
  color: #0056b3;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 5px;
  width: 80%;
  max-width: 500px;
}

.modal-header,
.modal-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h5 {
  margin: 0;
}

.modal-body {
  margin-top: 20px;
  margin-bottom: 20px;
}

.captcha-image {
  margin: 0 auto;
  width: 100%;
  width: 5cm;
  user-select: none;
}

.text-danger {
  color: #dc3545;
  margin-top: 10px;
}

button {
  cursor: pointer;
  padding: 5px 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
}

button:hover {
  background-color: #0056b3;
}

.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 900;
}
</style>
