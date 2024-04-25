<template>
    <div class="body">
      <h1>Register</h1>
      <form id="UserForm" @submit.prevent="saveUser">
        <div v-if="success" class="alert alert-success">
          User registered successfully
        </div>
        <div v-if="errors.length" class="alert alert-danger">
          <div v-for="error in errors">{{ error }}</div>
        </div>
        <div class="form-group mb-3">
          <label for="username" class="form-label">Username</label>
          <input type="text" name="username" class="form-control" />
        </div>
        <div class="form-group mb-3">
          <label for="password" class="form-label">Password</label>
          <input type="password" name="password" class="form-control" pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}" 
                                title="Must contain at least one number and one uppercase and lowercase letter, and at least 8 or more characters"/>
        </div>
        <div class="form-group mb-3">
          <label for="confirm_password" class="form-label">Confirm Password</label>
          <input type="password" name="confirm_password" class="form-control" />
        </div>
        <div class="form-group mb-3">
          <label for="firstname" class="form-label">Firstname</label>
          <input type="text" name="firstname" class="form-control" />
        </div>
        <div class="form-group mb-3">
          <label for="lastname" class="form-label">Lastname</label>
          <input type="text" name="lastname" class="form-control" />
        </div>
        <div class="form-group mb-3">
          <label for="email" class="form-label">Email</label>
          <input type="email" name="email" class="form-control" />
        </div>
        <div class="form-group mb-3">
          <label for="location" class="form-label">Location</label>
          <input type="text" name="location" class="form-control" />
        </div>
        <div class="form-group mb-3">
          <label for="biography" class="form-label" >Biography</label>
          <textarea name="biography" class="form-control" ></textarea>
        </div>
        <div class="form-group mb-3">
          <label for="profile" class="form-label">Photo</label>
          <input type="file" name="profile" class="form-control" />
        </div>
        <button id="btn" type="submit" class="btn btn-primary">Register</button>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from "vue";
  
  let success = ref(false);
  
  let csrf_token = ref("");
  let errors = ref([]);
  let errorDisplayStatus = ref({});
  
  function getCsrfToken() {
    fetch('/api/v1/csrf-token')
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        csrf_token.value = data.csrf_token;
    })
  }
  
  onMounted(() => {
    getCsrfToken();
  });
  
  function validateForm() {
    errors.value = [];
    errorDisplayStatus.value = {};
  
    let usernameInput = document.getElementsByName("username")[0];
    let passwordInput = document.getElementsByName("password")[0];
    let confirmPasswordInput = document.getElementsByName("confirm_password")[0];
    let firstnameInput = document.getElementsByName("firstname")[0];
    let lastnameInput = document.getElementsByName("lastname")[0];
    let emailInput = document.getElementsByName("email")[0];
    let locationInput = document.getElementsByName("location")[0];
    let biographyInput = document.getElementsByName("biography")[0];
    let fileInput = document.getElementsByName("profile")[0];
  
    if (!usernameInput.value) {
      errors.value.push("Username is required");
    }
  
    if (!passwordInput.value) {
      errors.value.push("Password is required");
    }
  
    if (!confirmPasswordInput.value) {
      errors.value.push("Confirm password");
    }
    
    if (confirmPasswordInput.value) {
      if (passwordInput.value !== confirmPasswordInput.value) {
      errors.value.push("Passwords do not match");
      }
    }
  
    if (!firstnameInput.value) {
      errors.value.push("Firstname is required");
    }
  
    if (!lastnameInput.value) {
      errors.value.push("Lastname is required");
    }
  
    if (!emailInput.value) {
      errors.value.push("Email is required");
    }
  
    if (!locationInput.value) {
      errors.value.push("Location is required");
    }
  
    if (!biographyInput.value) {
      errors.value.push("Biography is required");
    }
  
    if (!fileInput.value) {
      errors.value.push("Photo is required");
    }
  
    errors.value.forEach(error => {
      if (!errorDisplayStatus.value[error]) {
        errorDisplayStatus.value[error] = false;
      }
    });
  
    if (errors.value.length > 0) {
      window.scrollTo(0, 0);
    }
  
    return errors.value.length === 0;
  }
  
  function saveUser() {
    let UserForm = document.getElementById('UserForm');
    let form_data = new FormData(UserForm);
  
    if (validateForm()) {
      fetch("/api/v1/register", {
        method: 'POST',
        body: form_data,
        headers: {
          'X-CSRFToken': csrf_token.value
        }
      })
        .then(function (response) {
          if (response.ok) {
            window.scrollTo(0, 0);
            success.value = true;
          } else {
            return response.json();
          }
        })
        .then(function (data) {
          if (data.error) {
            window.scrollTo(0, 0);
            errors.value.push(data.error);
          } else {
            console.log(data.message);
          }
        })
        .catch(function (error) {
          window.scrollTo(0, 0);
          console.log(error);
          errors.value.push(error.response.data.error);
        });
    }
  }
  </script>
  
  <style>
  #UserForm{
    max-width: 500px;
    margin: 0 auto;
    padding: 20px;
    box-sizing: border-box;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.2);
  }
  
  h1{
    max-width: 500px;
    margin: 0 auto;
    padding-bottom: 20px;
    padding-top: 15px;
    color: black;
  }
  
  li{
      list-style-type: none;
  }

  .btn{
    width: auto;
    justify-content:center;
  }

  .body{
    height: 100%;
    margin-top: -20px;
    background-size: cover;
    background-position: top;
    width: 100%;
    color: black;
  }

  #btn{
    width: 100%;
  }
  </style>