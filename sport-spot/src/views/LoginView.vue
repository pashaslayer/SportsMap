<template>
  <form>
  <div class="mb-3">
    <label for="email-label" class="form-label">Email: </label>
    <input v-model="email" type="email" id="email-label" aria-describedby="emailHelp" required>
    <div id="emailHelp" class="form-text">We'll never share your email with anyone else.</div>
  </div>
  <div class="mb-3">
    <label for="password" class="form-label">Password: </label>
    <input v-model="password" type="password" class="form-control" id="password-label" aria-describedby="passwordHelp" required>
    <div id="passwordHelp" class="form-text">We'll never share your password with anyone else.</div>
  </div>
  <button v-on:click="login" type="submit" class="btn btn-primary">Submit</button>
</form>

<br>
<br>
<br>

<p1> {{ success }}</p1>

  </template>
  
  
  <script>
  export default {
    data() {
      return {
        email: '',
        password: "",
        success: "",
      };
    },
    methods: {
      async login() {
        try {
          const response = await fetch('http://127.0.0.1:5000/login', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              email: this.email,
              password: this.password,
            }),
          });
  
          if (response.ok) {
            console.log('Login successful');
            this.success = "Login successful";
          } else {
            console.error('Login failed');
          }
        } catch (error) {
          console.error('Error gay mighdsaf:', error);
        }
      },
    },

  };
  </script>
  