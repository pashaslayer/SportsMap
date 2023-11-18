<template>
    <div>
      <h1>Admin Menu</h1>
      <ul>
        <li v-for="user in users" :key="user.id">
          {{user.id}} 
          {{user.username}}
          <button @click="deleteUser(user.id)">Delete</button>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        users: [],
      };
    },
    mounted() {
      this.fetchUsers();
    },
    methods: {
      async fetchUsers() {
        try {
          const response = await axios.get('http://127.0.0.1:5000/allUsers');
          this.users = response.data;
          console.warn(this.users);
        } catch (error) {
          console.error('Error fetching users:', error);
        }
      },
      async deleteUser(userId) {
        try {
          await axios.delete(`http://127.0.0.1:5000/delete/user/${userId}`);
          this.users = this.users.filter(user => user.id !== userId);
          this.fetchUsers();
        } catch (error) {
          console.error('Error deleting user:', error);
        }
      },
    },
  };
  </script>
  