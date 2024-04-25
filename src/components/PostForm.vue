<template>
    <div class="post">
    <h1>New Post</h1>
    <form @submit.prevent="savePost" id="PostForm">
        <div v-if="result.errors">
            <ul class="alert alert-danger">
                <li v-for="error in result.errors">{{ error }}</li>
            </ul>
        </div>
        <div v-if="result.message">
            <div class="alert alert-success">{{ result.message }}</div>
        </div>
        <div class="form-group mb-3">
            <label for="photo" class="form-label">Photo</label>
            <input type="file" name="photo" class="form-control" />
        </div>
        <div class="form-group mb-3">
            <label for="caption" class="form-label">Caption</label>
            <textarea name="caption" class="form-control"></textarea>
        </div>
        <button id="submit_btn" type="submit" class="btn btn-primary">Post</button>
    </form>
</div>
</template>

<script setup>

    import {ref, onMounted} from 'vue'
    const token = localStorage.getItem("token")
    let csrf_token = ref("")
    let result = ref([])
    // const user = ref({})

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

    const fetchUser = async() => {
        const res = await fetch("/api/v1/users/currentuser", {
            method: "GET",
            headers: {
                'Authorization': "Bearer " + token
            }
        })
        const data = await res.json()
        return data
    }

    const savePost = async() => {
        let user = await fetchUser()
        let postForm = document.getElementById("PostForm")
        let form_data = new FormData(postForm)
        
        // console.log(...form_data.entries())
        fetch(`/api/v1/users/${user.id}/posts`, {
            method: "POST",
            body: form_data,
            headers: {
                'X-CSRFToken': csrf_token.value,
                'Authorization': "Bearer " + token
            }
        })
        .then(res => res.json())
        .then(data => {
            result.value = data
            console.log(data)
        })
        .catch(err => result.value = err)
    }

</script>

<style>
#PostForm{
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
  }

  #submit_btn{
    align-items: center;
    width: 100%;
  }
  </style>