<template>

  <div id="Header">
    <h1 id="Header-Title">Contacts</h1>
    <input type="text" id="ContactSearch" v-model="Search.User" @click="CloseSearch" placeholder="Search for other users"/>
    <button id="AccountSearch" @click.prevent="HandleAccountSearch">Search</button>
    <div v-if="SearchAccounts.FoundUsers !== null" id="SearchedAccounts">
      <div v-for="(user, index) in SearchAccounts.FoundUsers" @click="HandleAccountRedirect(user)" id="AccountHolder">
       
        <img v-if="SearchAccounts.FoundUserPhotos[index] === null" src="src/assets/Default.jpg" alt="Profile Picture" id="UserPhotos"/>
        <img v-else-if="SearchAccounts.FoundUserPhotos[index] .substr(0,8) === 'iVBORw0K'" :src="`data:image/png;base64,${SearchAccounts.FoundUserPhotos[index] }`"  alt="Profile Picture" id="UserPhotos"/>
        <img v-else  :src="`data:image/jpg;base64,${SearchAccounts.FoundUserPhotos[index] }`" alt="Profile Picture" id="UserPhotos"/>
        <p id="FoundUserName" >{{ user }}</p>
      
    </div>
    </div>

    <svg fill="#000000" @click="Render.Div = !Render.Div" id="SettingsLogo"  version="1.1"  xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
	 viewBox="0 0 478.703 478.703" xml:space="preserve">
<g>
	<g>
		<path d="M454.2,189.101l-33.6-5.7c-3.5-11.3-8-22.2-13.5-32.6l19.8-27.7c8.4-11.8,7.1-27.9-3.2-38.1l-29.8-29.8
			c-5.6-5.6-13-8.7-20.9-8.7c-6.2,0-12.1,1.9-17.1,5.5l-27.8,19.8c-10.8-5.7-22.1-10.4-33.8-13.9l-5.6-33.2
			c-2.4-14.3-14.7-24.7-29.2-24.7h-42.1c-14.5,0-26.8,10.4-29.2,24.7l-5.8,34c-11.2,3.5-22.1,8.1-32.5,13.7l-27.5-19.8
			c-5-3.6-11-5.5-17.2-5.5c-7.9,0-15.4,3.1-20.9,8.7l-29.9,29.8c-10.2,10.2-11.6,26.3-3.2,38.1l20,28.1
			c-5.5,10.5-9.9,21.4-13.3,32.7l-33.2,5.6c-14.3,2.4-24.7,14.7-24.7,29.2v42.1c0,14.5,10.4,26.8,24.7,29.2l34,5.8
			c3.5,11.2,8.1,22.1,13.7,32.5l-19.7,27.4c-8.4,11.8-7.1,27.9,3.2,38.1l29.8,29.8c5.6,5.6,13,8.7,20.9,8.7c6.2,0,12.1-1.9,17.1-5.5
			l28.1-20c10.1,5.3,20.7,9.6,31.6,13l5.6,33.6c2.4,14.3,14.7,24.7,29.2,24.7h42.2c14.5,0,26.8-10.4,29.2-24.7l5.7-33.6
			c11.3-3.5,22.2-8,32.6-13.5l27.7,19.8c5,3.6,11,5.5,17.2,5.5l0,0c7.9,0,15.3-3.1,20.9-8.7l29.8-29.8c10.2-10.2,11.6-26.3,3.2-38.1
			l-19.8-27.8c5.5-10.5,10.1-21.4,13.5-32.6l33.6-5.6c14.3-2.4,24.7-14.7,24.7-29.2v-42.1
			C478.9,203.801,468.5,191.501,454.2,189.101z M451.9,260.401c0,1.3-0.9,2.4-2.2,2.6l-42,7c-5.3,0.9-9.5,4.8-10.8,9.9
			c-3.8,14.7-9.6,28.8-17.4,41.9c-2.7,4.6-2.5,10.3,0.6,14.7l24.7,34.8c0.7,1,0.6,2.5-0.3,3.4l-29.8,29.8c-0.7,0.7-1.4,0.8-1.9,0.8
			c-0.6,0-1.1-0.2-1.5-0.5l-34.7-24.7c-4.3-3.1-10.1-3.3-14.7-0.6c-13.1,7.8-27.2,13.6-41.9,17.4c-5.2,1.3-9.1,5.6-9.9,10.8l-7.1,42
			c-0.2,1.3-1.3,2.2-2.6,2.2h-42.1c-1.3,0-2.4-0.9-2.6-2.2l-7-42c-0.9-5.3-4.8-9.5-9.9-10.8c-14.3-3.7-28.1-9.4-41-16.8
			c-2.1-1.2-4.5-1.8-6.8-1.8c-2.7,0-5.5,0.8-7.8,2.5l-35,24.9c-0.5,0.3-1,0.5-1.5,0.5c-0.4,0-1.2-0.1-1.9-0.8l-29.8-29.8
			c-0.9-0.9-1-2.3-0.3-3.4l24.6-34.5c3.1-4.4,3.3-10.2,0.6-14.8c-7.8-13-13.8-27.1-17.6-41.8c-1.4-5.1-5.6-9-10.8-9.9l-42.3-7.2
			c-1.3-0.2-2.2-1.3-2.2-2.6v-42.1c0-1.3,0.9-2.4,2.2-2.6l41.7-7c5.3-0.9,9.6-4.8,10.9-10c3.7-14.7,9.4-28.9,17.1-42
			c2.7-4.6,2.4-10.3-0.7-14.6l-24.9-35c-0.7-1-0.6-2.5,0.3-3.4l29.8-29.8c0.7-0.7,1.4-0.8,1.9-0.8c0.6,0,1.1,0.2,1.5,0.5l34.5,24.6
			c4.4,3.1,10.2,3.3,14.8,0.6c13-7.8,27.1-13.8,41.8-17.6c5.1-1.4,9-5.6,9.9-10.8l7.2-42.3c0.2-1.3,1.3-2.2,2.6-2.2h42.1
			c1.3,0,2.4,0.9,2.6,2.2l7,41.7c0.9,5.3,4.8,9.6,10,10.9c15.1,3.8,29.5,9.7,42.9,17.6c4.6,2.7,10.3,2.5,14.7-0.6l34.5-24.8
			c0.5-0.3,1-0.5,1.5-0.5c0.4,0,1.2,0.1,1.9,0.8l29.8,29.8c0.9,0.9,1,2.3,0.3,3.4l-24.7,34.7c-3.1,4.3-3.3,10.1-0.6,14.7
			c7.8,13.1,13.6,27.2,17.4,41.9c1.3,5.2,5.6,9.1,10.8,9.9l42,7.1c1.3,0.2,2.2,1.3,2.2,2.6v42.1H451.9z"/>
		<path d="M239.4,136.001c-57,0-103.3,46.3-103.3,103.3s46.3,103.3,103.3,103.3s103.3-46.3,103.3-103.3S296.4,136.001,239.4,136.001
			z M239.4,315.601c-42.1,0-76.3-34.2-76.3-76.3s34.2-76.3,76.3-76.3s76.3,34.2,76.3,76.3S281.5,315.601,239.4,315.601z"/>
	</g>
</g>
      </svg>
    <div v-if="Render.Div === true" id="SettingsBar" >
      <button id="LogOut" @click.prevent="Logout">Logout</button>
      <button id="Account" @click.prevent="Account">Account</button>
    </div>
  </div>
  <div id="Contacts">
    <div v-for="user in Contacts.ContactedUsers" @click="HandleAccountRedirect(user.Username)" id="ContactColumn">
      <img v-if="user.Photo === null" src="src/assets/Default.jpg" alt="Profile Picture" id="ContactPfp"/>
        <img v-else-if=" user.Photo.substr(0,8) === 'iVBORw0K'" :src="`data:image/png;base64,${user.Photo }`"  alt="Profile Picture" id="ContactPfp"/>
        <img v-else  :src="`data:image/jpg;base64,${user.Photo }`" alt="Profile Picture" id="ContactPfp"/>
        <p id="ContactUsername" >{{ user.Username }}</p>
    </div>
  </div>
    
</template>
<style scoped>
  #UserPhotos{
    height: 8vh;
    width: 8vh;
    border-radius: 50%;
    margin-left: 5%;
  }
  #ContactColumn{
    width: 100%;
    height: 17vh;
    background-color: rgb(59, 58, 58);
    border-top: 1px solid black;
    border-bottom: 1px solid black;
  }
  #ContactColumn:hover{
    background-color: grey;
    cursor: pointer;
    transition: 0.3s ease;
  }
  #ContactUsername{
    font-size: 2rem;
    margin-top: -7%;
    margin-left: 25%;
  }
  #ContactPfp{
    height: 15vh;
    width: 10vw;
    margin-top: .5%;
    border-radius: 50%;
    margin-left: 5%;
  }
  #AccountHolder{ 
    align-items: center;
    display: flex;
  }
  #AccountHolder:hover{
    cursor: pointer;
    background-color: rgb(193, 191, 191);
    transition: 0.3 ease;
  }
  #FoundUserName{
    margin-left: 10%;
    font-size: 1.5rem;
    font-weight: 600;
  }
  #SearchedAccounts{
      position: absolute;
      height: 40vh;
      width: 25.5%;
      display: flex column;
      align-items: center;
      top: 0;
      z-index: 2;
      margin-top: 8.6%;
      border: 1px solid black;
      border-radius: 4px;
      margin-left: 37.2%;
      overflow: auto;
      background-color: rgb(115, 115, 115);
    }
    #Contacts{
      max-height: 100%;
      min-height: 90%;
      width: 100%;
      top: 0;
      left: 0;
      margin-top: 10%;
      background-color: rgb(35, 35, 35);
      position: absolute;
      display: flex column;
      align-items: center;
    }
    #AccountSearch{
      height: 25%;
      position: absolute;
      margin-bottom: 2.65%;
      left: 64%;
      bottom: 0;
      border-radius: 4px;
      color: black;
      background-color: blue;
      font-size: 1rem;
      font-weight: 500;
      border: 0px;
    }
    #AccountSearch:hover{
      background-color: black;
      color: white;
      transition: 0.3s ease;
      cursor: pointer;
    }
    #SettingsLogo{
      height: 40%; 
      width: 5%;
      position: absolute;
      fill: #ffffff;
      margin-top: 5%;
      right: 0;
    }
    #SettingsBar{
      border: 2px solid black;
      background-color: white;
      width: 15%;
      margin-top: 10%;
      height: 20vh;
      position: absolute;
      right: 0;
      margin-right: 1vw;
      display: flex column;
      justify-content: center;
      text-align: center;
      z-index: 1;
    }
    #Account{
      background-color: white;
      margin-top: 5%;
      border: 1px solid black;
      border-radius: 4px;
      height: 5vh;
      width: 90%;
      position: relative;
      font-weight: 600;
      font-size: 1.2rem;
    }
    #Account:hover{
      background-color: black;
      color: white;
      cursor: pointer;
      transition: 0.3s ease;
    }
    #LogOut{
      background-color: blue;
      width: 90%;
      border-radius: 4px;
      border: 1px solid black;
      height: 5vh;
      margin-top: 5%;
      font-size: 1.2rem;
      font-weight: 600;
      position: relative;
    }
    #LogOut:hover{
      background-color: black;
      color: white;
      cursor: pointer;
      transition: 0.3s ease;
    }
    #SettingsLogo:hover{
      fill: #089efb;
      cursor: pointer;
    }
    #Header{
      width: 100%;
      height: 20%;;
      position: absolute;
      left: 0;
      top: 0;
      border-bottom: 1px solid black;
      background-color: rgb(46, 46, 46);
    }
    #Header-Title{
      font-size: 5vh;
      position: absolute;
      bottom: 0;
      margin-left: 1%;
      color: white;
    }
    #ContactSearch{
      width: 25%;
      background-color: rgb(69, 69, 69);
      color: white;
      font-family: arial;
      font-size: 1rem;
      cursor: auto;
      caret-color: white;
      bottom: 0;
      margin-bottom: 2.5%;
      left: 50%;
      transform: translateX(-50%);
      border: 0px;
      border-radius: 4px;
      height: 20%;
      font-weight: 400;
      padding: 5px;
      position: absolute;
    }
    #ContactSearch:focus{
      outline: none;
    }
    #ContactSearch:focus::placeholder {
      color: rgb(135, 132, 132);
    }
    @media (max-width: 480px) {
    #SettingsLogo{
      height: 15%;
      width: 10%;
      margin-top: 3vh;
    }
    #SettingsBar{
      margin-top: 6vh;
      width: 30%;
    }
    #Header-Title{
      font-size: 1.5rem;
      top: 0;
      margin-top: 2vh;
    }
    #ContactSearch{
      top: 0;
      width: 20%;
      margin-top: 2vh;
    }
    #Contacts{
      margin-top: 10vh;
    }
    #AccountSearch{
      left: 64%;
      top: 0;
      margin-top: 4.5%;
    }
    #ContactUsername{
    font-size: 2rem;
    margin-top: -27%;
    margin-left: 40%;
  }
  #ContactPfp{
    height: 15vh;
    width: 23vw;
    margin-top: 1%;
    border-radius: 50%;
    margin-left: 5%;
  }
  #SearchedAccounts{
    margin-top: 8vh;
    width: 45vw;
    margin-left: 13vh;
  }
  #UserPhotos{
    height: 5vh;
    width: 10vw;
  }
  #FoundUserName{
    font-size: 1rem;
  }
  }
</style>

<script lang="ts">

var user = sessionStorage.getItem("User");
export default {
    data() {
    return {
      Render:{
        Div: false,
        Search: false,
      },
      SignedIn:{
        SignedUser: user
      },
      Search:{
        User: ""
      },
      Contacts:{
        ContactedUsers: []
      },
      SearchAccounts:{
        FoundUsers: null,
        FoundUserPhotos: null
      }
    }
  },
  methods: {
    Logout(event : Event) {
      console.log(event);
      sessionStorage.clear();
      this.$router.push("/");
    },
    CloseSearch(event: Event){
      console.log(event);
      this.Render.Search = !this.Render.Search;
      if(this.Render.Search === true){
        this.SearchAccounts.FoundUsers = null;
        this.SearchAccounts.FoundUserPhotos = null;
      }
    },
    Account(event: Event){
      console.log(event);
      this.$router.push("/Account")
    },
    HandleAccountRedirect(user : string){
      this.$router.push({ 
        name: 'Messages',
        query: { User: user } });
    },
    HandleAccountSearch(event: Event){
      console.log(event)
      if(this.Search.User.trim() === ""){
        return alert("Please enter a valid user")
      }
      var requester = sessionStorage.getItem("User")
      const url = `http://localhost:5000/AccountSearch?Username=${this.Search.User}&Requester=${requester}`;
      fetch(url, {
        method: 'GET',
        mode: 'cors',
        headers: {
          "Content-Type": "application/json"
        }
      }).then(response => response.json())
        .then(data => {
          console.log(data);
          this.SearchAccounts.FoundUsers = data.Data.UserList;
          this.SearchAccounts.FoundUserPhotos = data.Data.UserPhotos
        })
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
  },
  created (){
    var user = sessionStorage.getItem("User")
    const url = `http://localhost:5000/RetrieveChats?User=${user}`;
    fetch(url, {
      method: 'GET',
      mode: 'cors',
      headers: {
        "Content-Type": "application/json"
      }
    }).then(response => response.json())
      .then(data => {
        this.Contacts.ContactedUsers = data.Data;
        console.log(this.Contacts.ContactedUsers)
      }).catch(error => {
        console.error('Error fetching user data:', error);
      });
  }
}

</script>

