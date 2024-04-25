<script setup>
    import {ref, onMounted, nextTick} from 'vue'
    import { RouterLink, useRouter } from "vue-router"
    const token = localStorage.getItem("token")
    const renderComponent = ref(true)

    let posts= ref([])
    let csrf_token = ref("")
    let result = ref([])

    onMounted(() => {
        fetchPosts().then(data => posts.value = data)
        getCsrfToken()
    })

    const forceRender = async () => {
        renderComponent.value = false;
        await nextTick();
        renderComponent.value = true;
    };

    const fetchPosts = async() => {
        const res = await fetch("/api/v1/posts")
        const {posts} = await res.json()
        const arr = []
        for (let item of posts) {
            const user = await fetchUser(item.user_id)
            const newObj = {
                ...item,
                username: user.username,
                profile: user.profile_photo
            }
            arr.push(newObj)
           
        }
        return arr
    }


   

  
    const fetchUser = async(id) => {
        
        const res = await fetch(`/api/v1/users/${id}`)
        const data = await res.json()
        return data
        
    }
    
    const getCsrfToken = () => {
        fetch('/api/v1/csrf-token')
        .then(res => res.json())
        .then(data => {
            csrf_token.value = data.csrf_token
        })
    }

    const likedPost = (id) => {
        fetch(`/api/v1/posts/${id}/like`, {
            method: "POST",
            headers: {
                'X-CSRFToken': csrf_token.value,
                'Authorization': "Bearer " + token
            }
        })
        .then(res => res.json())
        .then(data => {
            result.value = data
            document.getElementById('#id')
            console.log(data)
        })
        .catch(err => result.value = err)
        fetchPosts().then(data => posts.value = data)
        forceRender()
    }


</script>

<template>
    <div class="page-wrapper1">
        <div class="content">
            <div class="explore" v-if="renderComponent">
                <div class="explore-left">
                    <div class="explore-card" v-for="post in posts">
                        <div class="padding">
                            <div class="explore-user">
                                <RouterLink  class="link" :to="'/users/' + post.user_id">
                                    <img :src="post.profile">
                                    <div>{{ post.username }}</div>
                                </RouterLink>
                            </div>
                        </div>
                        <div class="explore-img">
                            <img :src="post.photo">
                        </div>
                        <div class="padding">
                            <div class="explore-desc">
                                {{ post.caption }}
                            </div>
                            <div class="explore-stats">
                                <div class="likes">
                                    <div @click="() => likedPost(post.id)"> 
                                        <i class="far">&#xf004;</i>
                                    </div>
                                    <div><span>{{ post.likes }}</span> Likes</div>
                                </div>
                                <div id="date">{{ post.created_at.split(" ").splice(1,3).join(" ") }}</div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="explore-right">
                    <RouterLink  class="link" to="/posts/new">New Post</RouterLink>
                </div>
            </div>
        </div>
    </div>
</template>

<style>
 .explore {
    display: flex;
    margin-top: 50px;
    height: 100vh;
    width: 100vw;
    margin-bottom: 50px;
 }

 .explore-left {
    width: 100%;
    display: flex;
    flex-direction: column;
    flex:3;
    margin: 0 auto;
 }

 .explore-card {
    display: flex;
    flex-direction: column;
    margin-right: auto;
    margin-left: auto;
    width: 500px;
    margin-bottom: 10px;
    gap: 10px;
    box-shadow: rgba(0, 0, 0, 0.19) 0px 10px 20px, rgba(0, 0, 0, 0.23) 0px 6px 6px;
    margin-top: 70px;
    background-color: #fff;
 }

 .far{
    color:black;
 }

 .explore-user{
    padding-top: 15px;
    padding-bottom: 2px;
 }

 .explore-user .link{
    display: flex;
    align-items: center;
    gap: 10px;
    text-decoration: none;
    font-weight: 500;
    color: rgb(83, 83, 83);
 }

 .explore-user .link:hover{
    color: rgb(0, 0, 0);
 }

 .explore-user img {
    width: 25px;
    height: 25px;
    border-radius: 50%;    
 }

 .explore-img > img {
    width: 100%;
 }

 .explore-desc {
    margin-bottom: 10px;
    color: gray;
    margin-bottom: 10px;
 }

 .explore-stats {
    width: 100%;
    display: flex;
    justify-content: space-between;
    color: rgb(80, 80, 80);
    font-size: 15px;
    padding-bottom: 10px;
 }

 .likes {
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: 500;
 }

 .likes > div > i {
    width: 10px;
 }

 .explore-right {
    margin-top: 70px;
    flex: 1;
    display: flex;
    justify-content: center;
 }

 .explore-right .link {
    text-decoration: none;
    color: #fff;
    background: black;
    height: 55px;
    width: 200px;
    text-align: center;
    border-radius: 3px;
    padding-bottom: 15px;
    padding-top: 15px;

 }

 #date {
    font-weight: 500;
 }

 .padding{
    padding-left: 15px;
    padding-right: 15px;
 }

 .page-wrapper1 {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;

  overflow-y: auto;
}

.content {
  min-height: 100vh;
}

.likes > div > i:hover{
    cursor: pointer;
}
</style>