<template>

  <div id="Contacts-Bar">
    <h1 id = "ContactHeader">Contacts</h1>
    <img src="Images/settings.png" alt="Settings" @click="Render.Div = !Render.Div">
    <div v-if="Render.Div === true" id="LogOutDiv" >
      <button id="LogOut" @click.prevent="Logout">LogOut</button>
    </div>
  </div>
  <div id="Message">
    <h1>Hello</h1>
    <div id="WriteArea">
        <textarea maxlength="250" v-model="Message.Content" id="WriteMessage" placeholder="Message"></textarea>
        <button id="MessageSend">Send</button>
    </div>
  </div>
</template>

<script lang="ts">
import io from 'socket.io-client';
var user = sessionStorage.getItem("User");
export default {
    data() {
    return {
      Message:{
        Username: user,
        Content: ""
      },
      Render:{
        Div: false
      }
    }
  },
  methods: {
    Logout(event : Event) {
      console.log(event);
      sessionStorage.clear();
      this.$router.push("/");
    }
  },
    watch: {
    'SignedInCheck': {
      handler() {
        var user = sessionStorage.getItem("User");
        if(user === null){
          this.$router.push("/")
        }
      },
      immediate: true
    } 
  }
}
const socket = io("http://localhost:5000/Login");
</script>

<style scoped>
    #Contacts-Bar{
        color: white;
        background-color: #121212;
        position: absolute;
        left: 0;
        top: 0;
        width: 20%;
        border-right: 3px solid white;
        height: 100%;
    }
    img{
      height: 7%;
      position: absolute;
      right: 0;
      background-color: white;
      border-radius: 100%;
      margin-right: 1%;
      top: 0;
      margin-top: 3%;
    }
    img:hover{
      cursor: pointer;
    }
    #Message{
        min-width: 79.5%;
        color: white;
        position: absolute;
        height: 100%;
        background-color:  #121212;
        top: 0;
        right: 0;
    }
    #LogOut{
      background-color: blue;
      color: white;
      font-size: 1rem;
      font-weight: 500;
      height: 50%;
      margin-top: 10%;
      border: solid black 1px;
      border-radius: 8px;
      width: 70%;
    }
    #LogOut:hover{
      background-color: black;
      cursor: pointer;
    }
    #LogOutDiv{
      height: 10%; 
      width: 70%;
      border: 1px solid black;
      border-radius: 8px;
      position: absolute;
      background-color: white;
      top: 0;
      display: flex;
      justify-content: center;
      margin-top: 24%;
      left: 0;
      margin-left: 12vh;
    }
    #WriteArea{
        position: absolute;
        min-width: 100%;
        background-color: white;
        border-top: 1px solid black;
        
        bottom: 0;
        height: 15%;
    }
    #ContactHeader{
        color: white; 
        size: 2rem;
        margin-left: 1vw;
        border-bottom: 1px solid white;
    }
    #WriteMessage{
        padding: 5px;
        position: absolute;
        width: 90%;
        height: 80%;
        font-size: 1.5rem;
        font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif
    }
    #MessageSend{
        border: 1px solid black;
        border-radius: 100%;
        position: absolute;
        right: 0;
        height: 70%;
        width: 7%;
        margin-right: 1vw;
        margin-top: 1%;
        background-color: blue;
        color: white;
        font-size: 1.5rem;
    }
    #MessageSend:hover{
        background: white;
        color: black;
        transition: 0.3s all;
        cursor: pointer;
    }
    #MessageSend:active{
        background: white;
        color: black;
        transition: 0.3s all;
    }
</style>
