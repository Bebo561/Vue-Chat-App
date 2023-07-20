<template>
   <div id="AccountPage">
        <h1 id="Contacts" @click.prevent="Contacts">Back</h1>
        <img v-if="ImageFile === null" src="src/assets/Default.jpg" alt="Profile Picture" id="AccountPhoto"/>
        <img v-else-if="ImageFile.substr(0,8) === 'iVBORw0K'" :src="`data:image/png;base64,${ImageFile}`"  alt="Profile Picture" id="AccountPhoto"/>
        <img v-else  :src="`data:image/jpg;base64,${ImageFile}`" alt="Profile Picture" id="AccountPhoto"/>
        <input id="UpdatePhoto" type="file" @change="handleFileChange" accept=".png, .jpg, .jpeg" />
        <h3 id="Username" >{{ User }}</h3>
        <input type="text" id="UpdateUsername" v-model="NewUsername" placeholder="Update Username"/>
        <button id="Update-Button" @click.prevent="handleSubmit">Update</button>
   </div>
</template>

<style scoped>
    #Contacts{
        font-size: 2 rem;
        font-weight: 500;
        position: absolute; 
        top: 0;
        left: 0;
        color: white;
        margin-left: 2vw;
    }
    #Contacts:hover{
        color: blue;
        cursor: pointer;
    }
    #AccountPage{
        height: 100%;
        width: 100%;
        top: 0;
        left: 0;
        position: absolute;
        display: flex;
        flex-direction: column;
        align-items: center;
        background-color: rgb(35, 35, 35);
    }
    #UpdatePhoto{
        margin-left: 10vw;
        margin-top: 1%;
        color: white;
        cursor: pointer;
    }
    #Update-Button{
        height: 5vh;
        width: 7vw;
        background-color: rgb(42, 88, 255);
        color: black;
        font-size: 1rem;
        font-family: Arial;
        font-weight: 500;
        border: 1px solid black;
        border-radius: 4px;
        margin-top: 2%;
    }
    #Update-Button:hover{
        background-color: white;
        border: 1px solid black;
        transition: 0.3s ease;
        cursor: pointer;
    }
    #Username{
        font-size: 2.5rem;
        font-family: Arial;
        color: white;
        font-weight: 600;
    }
    #UpdateUsername{
        border-radius: 6px;
        height: 5%;
        border:none;
        padding: 5px;
        width: 15vw;
        transform: translateY(-25%);
        caret-color: black;
    }
    #UpdateUsername:hover{
        outline: none;
        cursor: auto;
        transform: translateY(-25%);
    }
    #AccountPhoto{
        height: 45%;
        margin-top: 2%;
        border-radius: 50%;
    }
    @media (max-width: 480px){
        #AccountPhoto{
            height: 35%;
           
        }
        #Contacts{
            font-size: 1.5rem;
        }
        #UpdatePhoto{
            margin-top: 5%;
        }
        #Username{
            font-size: 3rem;
        }
        #UpdateUsername{
            width: 40%;
        }
        #Update-Button{
            width: 40%;
            margin-top: 5%;
            height: 7%;
        }
    }
</style>

<script lang="ts">
    export default {
        data() {
            return {
                 User: sessionStorage.getItem("User") || "Default Username",
                 ImageFile: null,
                 NewUsername: null,
                 NewImage: "",
                
            };
        },
        created() {
            this.FetchUserData()
        },
        methods: {
            FetchUserData(){
                const url = `http://localhost:5000/AccountRetrieveDetails?username=${this.User}`;
                fetch(url, {
                method: 'GET',
                mode: 'cors',
                headers: {
                    "Content-Type": "application/json"
                }
            }).then(response => response.json())
                .then(data => {
                    console.log(data);
                    this.ImageFile = data.Data.Photo;
                    
                }).catch(error => {
                    console.error('Error fetching user data:', error);
                });
            },
            Contacts(event: Event){
                console.log(event);
                this.$router.push("/Contacts");
            },
            handleSubmit(event: Event){
                console.log(event);
                var token = sessionStorage.getItem("Token");
                console.log(token);
                const url = "http://localhost:5000/AccountUpdate";
                if(this.NewImage !== ""){
                const reader = new FileReader();
                reader.readAsDataURL(this.NewImage);
                reader.onload = () => {
                    const base64String = reader.result.split(',')[1];
                    var data = {
                        Username: this.User,
                        NewUser: this.NewUsername,
                        Photo: base64String,
                        Token: token
                    };
                    fetch(url, {
                    method: 'PUT',
                    mode: 'cors',
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(data)
                }).then(response => response.json())
                    .then(data => {
                        if(data.Data === 'Invalid Token' || data.Data === "Token Expired"){
                            alert(data.Data)
                            this.$router.push("/");
                        }
                        else{
                            var UpdatedData = data.Data;
                            console.log(UpdatedData)
                            sessionStorage.setItem("User", UpdatedData.Username);
                            this.User = UpdatedData.Username;
                            this.ImageFile = UpdatedData.Photo
                        
                        }

                    });

                };
                }
                else{
                    var data = {
                        Username: this.User,
                        NewUser: this.NewUsername,
                        Photo: null,
                        Token: token
                    };
                    fetch(url, {
                    method: 'PUT',
                    mode: 'cors',
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(data)
                }).then(response => response.json())
                    .then(data => {
                        if(data.Data === 'Invalid Token' || data.Data === "Token Expired"){
                            alert(data.Data)
                            this.$router.push("/");
                        }
                        else{
                            var UpdatedData = data.Data;
                            console.log(UpdatedData)
                            sessionStorage.setItem("User", UpdatedData.Username);
                            this.User = UpdatedData.Username;
                        
                        }
                        
                    })
                }
            },
            handleFileChange(event : Event) {
                this.NewImage =  event.target.files[0];
                
                console.log(this.NewImage)
            }
        },
    }
</script>