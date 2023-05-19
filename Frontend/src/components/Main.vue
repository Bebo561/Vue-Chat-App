<template>

  <div id="Contacts-Bar">
    <h1 id = "ContactHeader">Contacts</h1>
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
        Content: "",
      }
    }
  },
    watch: {
    'SignedInCheck': {
      handler() {
        if(user === null){
            this.$router.push('/');
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
    #Message{
        min-width: 79.5%;
        color: white;
        position: absolute;
        height: 100%;
        background-color:  #121212;
        top: 0;
        right: 0;
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
