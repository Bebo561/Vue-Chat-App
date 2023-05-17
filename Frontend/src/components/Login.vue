<template>
  <div id = "Login-Background">
    <form id="Login-Form" @submit.prevent="Submit">
      <h1 id="Login-Header">ChillChat</h1>
      <p>Please Login</p>
      <label>Username</label>
      <input type="text" v-model="Login.username" id="Login-Username" placeholder="Enter Username">
      <label>Password</label>
      <input type="password" v-model="Login.password" id="Login-Password" placeholder="Enter Password">
      <button id="Login-Button">Login</button>
      <hr>
      <h3>No Account? <a href="/SignUp">Sign Up</a></h3>
    </form>
  </div>
</template>
<script lang="ts">
  export default {
  data() {
    return {
      Login:{
        username: "",
        password: ""
      }
    }
  },
  methods: {
    Submit(event : Event) {
      console.log(event);
      if(this.Login.username === "" ||  this.Login.password === ""){
        return alert("Fill in fields");
      }
      var data = {
        Username: this.Login.username,
        Password: this.Login.password
      }
      const url = "http://localhost:5000/Login"
      fetch(url, {
      method: 'POST',
      mode: 'cors',
      headers: {
      "Content-Type": "application/json"
        },
      body: JSON.stringify(data)
        }).then(response => response.json())
    .then(data => {
        const value = data.Data;
        const token = data.Token;
        console.log(token)
        sessionStorage.setItem("Token", token);
        sessionStorage.setItem("User", this.Login.username);
        alert(value); // Print 'Hi' to the console
    }).catch((err) => {
        alert(err);
        event.target.reset();
    })
    }
  }
}
</script>

<style scoped>
  #Login-Background{
    height: 100vh;
    width: 100vw; 
    display: flex;
    justify-content: center;
    background-color:#121212;
    top: 0;
    position: absolute;
    left: 0;
    margin: auto;
  }
  h3{
    margin-left: auto;
    margin-right: auto;
    font-weight: 600;
    font-size: 1rem;
  }
  a:hover{
    color: blue;
  }
  hr{
    width: 40%;
    margin-top: 3vh;
    color: black;
  }
  #Login-Header{
    margin-left: auto;
    margin-right: auto;
    font-size: 2.5rem;
    font-weight: 600;
  }
  p{
    font-size: 1rem;
    margin-top: -4vh;
    margin-left: auto;
    margin-right: auto;
  }
  #Login-Form{
    height: 60%;
    width: 35%;
    display: flex;
    flex-direction: column;
    background-color: #EBF1F1;
    margin: auto;
    border: 1px solid white;
    border-radius: 4px;
    box-shadow: 0 5px 10px white;
  }
  label{
    font-size: 1.3rem;
    font-weight: 600;
    margin-left: 30%;
    margin-top: 5%;
  }
  input{
    width: 40%;
    height: 7%;
    color: black;
    background-color: rgb(225, 215, 215);
    border: 1px solid black;
    border-radius: 4px;
    margin-top: 1vh;
    margin-left: auto;
    margin-right: auto;
  }
  input:focus{
    outline-color: 10px blue;
    background-color: white;
  }
  #Login-Button{
    width: 25%;
    height: 8.5%;
    margin-left: auto;
    margin-right: auto;
    background-color: blue;
    color: white;
    font-size: 1rem;
    font-weight: 600;
    border: 1px solid black;
    border-radius: 6px;
    margin-top: 5%;
  }
  #Login-Button:hover{
    transition: all 0.3s;
    background-color: rgb(100, 100, 238);
    cursor: pointer;
  }
  #Login-Button:active{
    transform: scale(1.05);
    transition: all 0.3s;
  }
  @media (max-width: 480px) {
    #Login-Form{
      width: 70vw;
    }
  }
</style>
