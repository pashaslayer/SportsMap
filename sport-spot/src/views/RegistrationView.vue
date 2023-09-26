<template>
<form v-on:submit.prevent="registration">
  <div class="mb-3">
    <label for="firstname" class="form-label">Firstname: </label>
    <input v-model="firstname" type="text" class="form-control" id="firstname-label" 
    onkeydown="return /[a-z]/i.test(event.key)" required>
    <!-- Validation: only string + space input -->
  </div>
  <div class="mb-3">
    <label for="lastname" class="form-label">Lastname: </label>
    <input v-model="lastname" type="text" class="form-control" id="lastname-label"
    onkeydown="return /[a-z]/i.test(event.key)" required>
    <!-- Validation: only string + space input -->
  </div>
  <div class="mb-3">
    <label for="birthdate" class="form-label">Birthdate: </label>
    <input v-model="birthdate" type="date" class="form-control" id="date-label" 
      min="1900-01-01" max="2002-12-31" required />
  </div>
  <div class="mb-3">
    <label for="username" class="form-label">Username: </label>
    <input v-model="username" type="text" class="form-control" id="username-label" onkeydown="return /[a-z,1-9,!,?,_]/i.test(event.key)" required
    minlength="6" maxlength="10">
  </div>
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
  <div class="mb-3">
      <label class="form-label">Gender:</label>
      <div class="form-check">
        <input
          v-model="gender"
          class="form-check-input"
          type="radio"
          id="male"
          value="male"
        />
        <label class="form-check-label" for="male">Male</label>
      </div>
      <div class="form-check">
        <input
          v-model="gender"
          class="form-check-input"
          type="radio"
          id="female"
          value="female"
        />
        <label class="form-check-label" for="female">Female</label>
      </div>
      <div class="form-check">
        <input
          v-model="gender"
          class="form-check-input"
          type="radio"
          id="other"
          value="other"
        />
        <label class="form-check-label" for="other">Other</label>
      </div>
    </div>
  
  <button v-on:click="submit" type="submit" class="btn btn-primary">Submit</button>

  <br>
  <br>
  <br>

  <p1>
    {{ success }}
  </p1>

   
</form>
</template>

<style>

</style>


<script>
  export default {
    data() {
      return {
        email: "",
        firstname: "",
        lastname: "",
        username: "",
        password: "",
        birthdate: "",
        gender:"",
        success:"",
      };
    },
    methods: {
      async registration() {
        try {
          const response = await fetch('YOUR_API_ENDPOINT/register', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              email: this.email,
              firstname: this.firstname,
              lastname: this.lastname,
              username: this.username,
              password: this.password,
              birthdate: this.birthdate,
              gender: this.gender,
            }),
          });
  
          if (response.ok) {
            console.log('Login successful');
            this.success = "Data successfully transmitted!"
          } else {
            console.error('Login failed');
          }
        } catch (error) {
          console.error('Error:', error);
        }
      },
    },

  };
</script>