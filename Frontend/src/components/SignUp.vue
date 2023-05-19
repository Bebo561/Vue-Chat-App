<script lang="ts">
export default {
  data() {
    return {
      SignUp:{
        username: "",
        displayName: "",
        password: ""
      }
    }
  },
  methods: {
    Submit(event: Event) {
        event.preventDefault();
      if(this.SignUp.username === "" || this.SignUp.displayName === "" || this.SignUp.password === ""){
        return alert("Fill in fields");
      }
      var data = {
        Username: this.SignUp.username,
        Password: this.SignUp.password,
        DisplayName: this.SignUp.displayName
      }
      const url = "http://localhost:5000/Register"
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
        alert(value); // Print 'Hi' to the console
        this.$router.push('/');
    }).catch((err) => {
        alert(err);
        event.target.reset();
    })
    }
  }
}

</script>

<template>
  <div id="Signup-Background">
    <form @submit.prevent="Submit">
        <h1>Register</h1>
        <hr id="Hr-1">
        <label>Enter Username</label>
        <input type="text" v-model="SignUp.username" placeholder="CoolGuy123">
        <label>Enter Display Name</label>
        <input type="text" v-model="SignUp.displayName" placeholder="Goku">
        <label>Enter Password</label>
        <input type="password" minlength="8" v-model="SignUp.password" placeholder="***">
        <button>Register</button>
        <hr>
        <h2>Have An Account? <a href="/">Log In</a></h2>
    </form>
  </div>
</template>

<style scoped>
#Signup-Background{
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
  h2{
    margin-left: auto;
    margin-right: auto;
    font-size: 1rem;
    color: white;
    font-weight: 400;
  }
  a{
    color: white;
  }
  a:active{
    color: black;
  }
  a:hover{
    color: black;
    cursor: pointer;
  }
  button{
    height: 7%;
    width: 30%;
    background-color: white;
    color: black;
    border: 0.5px solid black;
    border-radius: 4px;
    margin-top: 2vh;
    margin-left: auto;
    margin-right: auto;
    text-align: center;
    font-size: 1rem;
    font-weight: 300;
  }
  button:hover{
    color: white;
    background-color: black;
    box-shadow:  0 5px 10px black;
    transition: 0.3s;
    cursor:  pointer;
  }
  #Hr-1{
    width: 50%;
    border: 1px solid black;
    margin-top: -3vh;
  }
  hr{
    width: 40%;
    margin-top: 3vh;
    color: black;
  }
  h1{
    margin-left: auto;
    margin-right: auto;
    font-size: 2.3rem;
    color: white;
    font-weight: 700;
  }
  label{
    margin-left: 25%;
    margin-top: 2vh;
    color: white;
    font-size: 1.2rem;
    font-weight: 500;
  }
  form{
    height: 65%;
    width: 30%;
    display: flex;
    flex-direction: column;
    background-color: 	#4B9CD3;
    margin: auto;
    border: 1px solid black;
    border-radius: 4px;
    box-shadow: 0 5px 10px #8beded;
  }
  input{
    width: 50%;
    height: 6%;
    background-color: rgb(238, 225, 225);
    border: 2px solid black;
    text-align: center;
    border-radius: 4px;
    margin-left: auto;
    margin-right: auto;
  }
  input:focus{
    background-color: white;
  }
  @media (max-width: 480px) {
    Form{
      width: 70vw;
    }
  }
</style>
