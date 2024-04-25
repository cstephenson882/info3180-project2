<script setup>
import { ref } from "vue";
import { RouterLink } from "vue-router";


</script>

<template>
  <div class="background">
    <div class="container">
      <div class="section1">
        <img src="https://i.pinimg.com/550x/c5/d8/6c/c5d86c9ffb244db64b73a6f2cec7deba.jpg" alt="">
      </div>
      <div class="section2">
        <div class="card">
          <div class="logo_img">
            <img class="camera_img" src="camera.png" alt="">
            <h2>Photogram</h2>
          </div>
          <hr>
          <div class="text">
            Share photos of you chasing dreams and making memories with friends, family and the strangers.
          </div>
          <div class="button">
            <RouterLink id="new_acc_btn" class="link" to="/register">Register</RouterLink>
            <RouterLink id="login_btn" class="link" to="/login">Login</RouterLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
.background {
  background-image: url("https://cdn5.vectorstock.com/i/1000x1000/25/14/background-design-with-abstract-pattern-in-yellow-vector-28172514.jpg");

  background-size: cover;
  background-position: top;
  width: 100%;
  margin-top: -70px; /* Adjust the negative margin value to remove the space */
}

.container {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.section1 {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 400px;
  height: 300px; /* Set a fixed height for the photo card */
  box-shadow: 2px 2px 5px rgba(2, 2, 10, 0.5);
  overflow: hidden;
  border-radius: 10px;
}



.section1 > img {
  width: 100%;
  height: 100%; /* Make the image fill the entire container */
  object-fit: cover; /* Maintain aspect ratio and cover the container */
}

.section2 {
  display: flex;
  align-items: center;
}

.card {
  display: flex;
  flex-direction: column;
  width: 400px;
  height: 300px;
  align-items: center;
  justify-content: flex-start;
  gap: 10px;
  box-shadow: 2px 2px 5px rgba(2, 2, 10, 0.5);
  background-image: url("");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}


#new_acc_btn {
  background-color: rgb(0, 145, 255);
}

#login_btn {
  background-color: darkgrey;
}


.card > .logo_img > img {
  object-fit: contain;
  width: 28px;
}

.logo_img {
  display: flex;
  margin-top: 10px;
  align-items: center;
  gap: 5px
}

.text {
  margin: 0 15px;
  text-align: center;
  padding-bottom: 10px;
  /* color: white; */
}

hr {
  width: 90%;
}

.button {
  margin-top: 30px;
  width: 80%;
  display: flex;
  gap: 10px;
  text-align: center;
}

.button .link {
  flex: 1;
  text-decoration: none;
  color: #fff;
  background: rgb(50, 147, 177);
  padding: 10px;
}


</style>
