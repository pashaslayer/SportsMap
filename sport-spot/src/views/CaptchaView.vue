<template>
    <div>
      <h1>Captcha</h1>
        
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        svg: "",
        success: false,
      };
    },
    mounted() {
      this.fetchCaptcha();
    },
    methods: {
      async fetchCaptcha() {
        try {
          const response = await axios.get('http://127.0.0.1:5000/getCaptcha');
          this.svg = response.data;
          console.log(this.svg);
        } catch (error) {
          console.error('Error creating svg:', error);
        }
      },
    },
  };
  </script>
  