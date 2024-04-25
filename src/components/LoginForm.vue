<template>
    <div class="body1">
        <h1>Login</h1>
        <form @submit.prevent="loginUser" id="LoginForm">
            <div v-if="result.errors">
                <ul class="alert alert-danger">
                    <li v-for="error in result.errors">{{ error }}</li>
                </ul>
            </div>
            <div v-if="result.message">
                <div class="alert alert-success">{{ result.message }}</div>
            </div>
            <div class="form-group mb-3">
                <label for="username" class="form-label">Username</label>
                <input type="text" name="username" class="form-control" />
            </div>
            <div class="form-group mb-3">
                <label for="password" class="form-label">Password</label>
                <input type="password" name="password" class="form-control"/>
            </div>
            <div class="lg"><button id="btn" type="submit" class="btn btn-primary">Login</button></div>
        </form>
    </div>
</template>

<script setup>

    import {ref, onMounted} from 'vue'
    let csrf_token = ref("")
    let result = ref([])

    const getCsrfToken = () => {
        fetch('/api/v1/csrf-token')
        .then(res => res.json())
        .then(data => {
            csrf_token.value = data.csrf_token
        })
    }

    onMounted(() => {
        getCsrfToken()
    })

    const loginUser = () => {
        let loginForm = document.getElementById("LoginForm")
        let form_data = new FormData(loginForm)
        fetch("/api/v1/auth/login", {
            method: "POST",
            body: form_data,
            headers: {
                'X-CSRFToken': csrf_token.value
            }
        })
        .then(res => res.json())
        .then(data => {
            result.value = data
            if(data["errors"])
            {
              
            }
            else{
                localStorage.setItem("token", data.token)
                 window.location.reload()
            }
            
        })
      
    }

</script>

<style>
#LoginForm{
  max-width: 500px;
  margin: 0 auto;
  padding: 20px;
  box-sizing: border-box;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.2);
}

.body1{
    height: 100vh;
    margin-top: -20px;
    background-image: url("https://t4.ftcdn.net/jpg/06/03/98/09/360_F_603980999_FI7MlCHCDxQpVf5S238e2NlKNSYl02zp.jpg");
    background-size: cover;
    background-position: top;
    width: 100%;
    color: black;
  }

h1{
  max-width: 500px;
  margin: 0 auto;
  padding-bottom: 20px;
}
</style>