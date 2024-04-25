<template>
    <div class="page-wrapper">
        <div class="content">
            <div class="profile-container">
                <div class="l">
                    <div class="profile-card">
                        <div class="profile-photo">
                            <img :src="user.profile_photo">
                        </div>
                        <div class="profile-desc">
                            <h3>{{ user.firstname }} {{ user.lastname }}</h3>
                            <span>{{ user.location }}</span>
                            <span>Member since <span> Apr 2023</span></span>
                            <p>{{ user.biography }}</p>
                        </div>
                        <div class="profile-stats">
                            <div class="sub">
                                <div class="stat"><span>{{ posts.length }}</span>Posts</div>
                                <div class="stat" ><span>{{followers.followers}}</span>Followers</div>
                            </div>
                            <a href="#" class="follow-link" v-if="id!='currentuser'" @click="() => followUser(id)">{{ text }}</a>
                        </div>
                    </div>
                </div>
                <div class="profile-gallery">
                    <div class="img-container" v-for="post in posts">
                        <img :src="post.photo">
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>

    import {ref, onMounted, onUpdated} from 'vue'
    import {useRoute} from 'vue-router'
    let csrf_token = ref("")

    const followBtn = document.getElementById("follow")

    const user = ref({})
    const posts = ref([])
    const followers = ref(0)
    const token = localStorage.getItem("token")
    const text = ref("Follow")
    const route = useRoute()
    let id = route.params.id
    console.log(id)

    onMounted(() => {
        fetchUser(id).then(data => {
            user.value = data
            console.log(data)
            if (data["Following"])
            {
                text.value = "Following"
            }
            else{
                text.value = "Follow"
            }
        })
        fetchPosts(id).then(data => posts.value = data.posts)
        getFollowers(id).then(data => followers.value = data)
        getCsrfToken()
    })

    const getCsrfToken = () => {
        fetch('/api/v1/csrf-token')
        .then(res => res.json())
        .then(data => {
            csrf_token.value = data.csrf_token
        })
    }


    const fetchUser = async(id) => {
        const res = await fetch(`/api/v1/users/${id}`, {
            method: "GET",
            headers: {
                'Authorization': "Bearer " + token
            }
        })
        const data = await res.json()
        return data
    }

    const getFollowers = async(id) => {
            const user = await fetchUser(id)
            id = user.id
            const res = await fetch(`/api/users/${id}/follow`, {
            method: "GET",
            headers: {
                'Authorization': "Bearer " + token
            }
        })
        const data = await res.json()
        return data
    }

    const followUser = async(id) => {
        const me = id
        const who = await fetchUser("currentuser")
        const res = await fetch(`/api/users/${who.id}/follow`, {
            method:"POST",
            body: JSON.stringify({"follow_id": me}),
            headers: {
                'X-CSRFToken': csrf_token.value,
                'Authorization': "Bearer " + token,
                'Content-Type': "application/json"
            }
        })
        const data = await res.json()
       
        text.value = "Following"
        getFollowers(id).then(data => followers.value = data)
    
        console.log(data)

    }

    const fetchPosts = async(id) => {
        const user = await fetchUser(id)
        id = user.id
        const res = await fetch(`/api/v1/users/${id}/posts`, {
            method: "GET",
            headers: {
                'Authorization': "Bearer " + token
            }
        })
        const data = await res.json()
        return data
    }
</script>

<style>
body{
    font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
    .l{
        padding-bottom: 20px;
    }

    .img-container {
    width: calc(33.33% - 10px); /* Adjust the width calculation to accommodate the gap between images */
    margin-bottom: 10px;
    box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.2);
  }

  .profile-gallery {
    width: 90%;
    margin: 0 auto;
    display: flex;
    flex-wrap: wrap;
    gap: 30px;
  }

  .profile-gallery > .img-container {
    width: calc(33.33% - 20px); /* Adjust the width calculation to accommodate the gap between images */
    overflow: hidden;
    display: flex;
    justify-content: center;
  }

  .profile-gallery img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

    .profile-container {
        height: 100vh;
        width: 100vw;
        margin-top: 50px;
        padding-top: 10px;
    }

    .profile-card {
        width: 90%;
        background: white;
        height: 200px;
        display: flex;
        margin: 20px auto;
        gap: 20px;
        align-items: center;
        color: black;
        box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
    }

    .profile-photo {
        width: 180px;
        height: 180px;
        border-radius: 50%;
        overflow: hidden;
        margin-left: 30px;
    }

    .profile-desc {
        display: flex;
        flex-direction: column;
        flex: 3;
    }

    .profile-desc > span {
        color: rgb(39, 32, 32);
    }

    .profile-desc > p {
        color:rgb(39, 32, 32);
        margin-top: 20px;
    }

    .profile-stats {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 30px;
        flex: 1;
    }

    .profile-stats .sub {
        display: flex;
        text-align: center;
        gap: 80px;
    }

    .profile-stats .stat {
        display: flex;
        flex-direction: column;
    }

    .profile-stats .stat {
        color: rgb(39, 32, 32);
    }

    .profile-stats .stat span {
        color: black;
        font-weight: 700;
        font-size: 30px;
    }

    .profile-photo > img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    .follow-link {
        color: #fff;
        background: black;
        text-decoration: none;
        width: 200px;
        text-align: center;
        border-radius: 2px;
        margin-right: 10px;
        padding: 5px;
    }

    .page-wrapper {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: url("https://img.freepik.com/free-vector/white-abstract-background-design_23-2148825582.jpg?w=2000");
        overflow-y: auto;
    }

    .content {
        min-height: 100vh;
    }

</style>
