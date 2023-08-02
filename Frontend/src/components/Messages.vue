<template>
    <div id ="MessageHeader">
        <h1 id="BackButton" @click.prevent="BackButton"> Back </h1>
        <img v-if="Header.HeaderPhoto === null" src="src/assets/Default.jpg" alt="Profile Picture" id="HeaderImage"/>
        <img v-else-if="Header.HeaderPhoto.substr(0,8) === 'iVBORw0K'" :src="`data:image/png;base64,${Header.HeaderPhoto }`"  alt="Profile Picture" id="HeaderImage"/>
        <img v-else  :src="`data:image/jpg;base64,${Header.HeaderPhoto }`" alt="Profile Picture" id="HeaderImage"/>
        <h3 id="HeaderUser">{{ Header.HeaderUser }}</h3>
    </div>
    <div id="MessageSection"  ref="MessageSection">
        <div v-for="message in ReceivedMessages.Messages" id="MessageBox" :key="message.MessageId">
            <div v-if="message.MessageType === 'Text'" :class="{'MessageLeft': !IsSender(message), 'MessageRight': IsSender(message)}" >{{ message.textContent }}</div>
            <img v-else-if="message.MessageType === 'Image' && message.imageContent.substr(0,8) === 'iVBORw0K'" :src="`data:image/png;base64,${message.imageContent }`"  alt="Profile Picture" :class="{'ImageLeft': !IsSender(message), 'ImageRight': IsSender(message)}"/>
            <img v-else-if="message.MessageType === 'Image' && message.imageContent.substr(0,8) !== 'iVBORw0K'" :src="`data:image/jpg;base64,${message.imageContent }`" alt="Profile Picture" :class="{'ImageLeft': !IsSender(message), 'ImageRight': IsSender(message)}"/>
            <button v-if="IsSender(message)"  id="deleteButton" @click.prevent="DeleteMessage(message)">x</button>
        </div>
    </div>
    <div id="MessageCreateArea">
        <textarea id="MessageWrite" placeholder="Write a message" v-model="TextMessageCreate.MessageContent" maxlength="250"></textarea>
        <svg @click.prevent="SendTextMessage" width="800px" height="800px" viewBox="0 0 24 24" fill="none" id="SendButton" xmlns="http://www.w3.org/2000/svg">
            <path fill-rule="evenodd" clip-rule="evenodd" d="M19.2111 2.06722L3.70001 5.94499C1.63843 6.46039 1.38108 9.28612 3.31563 10.1655L8.09467 12.3378C9.07447 12.7831 10.1351 12.944 11.1658 12.8342C11.056 13.8649 11.2168 14.9255 11.6622 15.9053L13.8345 20.6843C14.7139 22.6189 17.5396 22.3615 18.055 20.3L21.9327 4.78886C22.3437 3.14517 20.8548 1.6563 19.2111 2.06722ZM8.92228 10.517C9.85936 10.943 10.9082 10.9755 11.8474 10.6424C12.2024 10.5165 12.5417 10.3383 12.8534 10.1094C12.8968 10.0775 12.9397 10.0446 12.982 10.0108L15.2708 8.17974C15.6351 7.88831 16.1117 8.36491 15.8202 8.7292L13.9892 11.018C13.9553 11.0603 13.9225 11.1032 13.8906 11.1466C13.6617 11.4583 13.4835 11.7976 13.3576 12.1526C13.0244 13.0918 13.057 14.1406 13.4829 15.0777L15.6552 19.8567C15.751 20.0673 16.0586 20.0393 16.1147 19.8149L19.9925 4.30379C20.0372 4.12485 19.8751 3.96277 19.6962 4.00751L4.18509 7.88528C3.96065 7.94138 3.93264 8.249 4.14324 8.34473L8.92228 10.517Z" fill="#0F1729"/>
        </svg>
        <button id="SendImage" @click="ImageUpload = !ImageUpload">+</button>
    </div>
    <div v-if="ImageUpload === true" id="UploadOverlay">
        <p id="UploadOverlayExit" @click="ImageUpload = !ImageUpload">X</p>
        <input id="InputPhoto" type="file" @change="handleFileUpload" accept=".png, .jpg, .jpeg" />
        <button id="ImageUpload" @click.prevent="SendImageMessage">Upload</button>
    </div>

</template>
<style scoped>
    #MessageHeader{
        background-color: rgb(46, 46, 46);
        position: absolute;
        top: 0;
        left: 0;
        height: 15%;
        width: 100%;
        border-bottom: 1px solid black;
    }
    #UploadOverlayExit{
        top: 0;
        left: 1;
        position: absolute;
        color: white;
        font-size: 3rem;
    }
    #UploadOverlayExit:hover{
        cursor: pointer;
        color: blue;
        transition: 0.3s all;
    }
    #UploadOverlay{
        height: 60vh;
        width: 70vh;
        margin-left: 20vw;
        margin-top: 20vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        border: 1px solid black;
        align-items: center;
        border-radius: 4px;
        position: absolute;
        background-color: rgb(60, 60, 60);
    }
    #ImageUpload{
        color: black;
        background-color: blue;
        height: 7vh;
        margin-top: 10%;
        border: 1px solid black;
        border-radius: 8px;
        width: 5vw;
    }
    #ImageUpload:hover{
        background-color: white;
        transition: 0.3s ease;
        cursor: pointer;
    }
    #deleteButton{
        width: 2vw;
        border: 1px solid black;
        border-radius: 50%;
        background-color: black;
        color: red;
        font-size: 1rem;
        font-weight: 500;
        align-self: flex-end; 
        display: inline-block;
        margin-bottom: 15px;
    }
    #deleteButton:hover{
        cursor: pointer;
        background-color: red;
        color: black;
        transition: 0.3s ease;
    }
    #BackButton{
        color: rgb(226, 218, 218);
        height: 2rem;
        margin-left: 2%;
        margin-top: 2%;
        width: 5%;
        height: 5vh;
    }
    #HeaderImage{
        height: 12vh;
        width: 12vh;
        margin-left: 40vw;
        margin-top: 1%;
        top: 0;
        position: absolute;
        border-radius: 50%;
    }
    #HeaderUser{
        color: rgb(226, 218, 218);
        font-size: 2rem;
        position: absolute;
        margin-left: 48vw;
        top: 0;
    }
    #BackButton:hover{
        color: blue;
        cursor: pointer;
    }
    #MessageSection{
        background-color: rgb(35, 35, 35);
        position: absolute;
        top: 0;
        left: 0;
        margin-top: 14vh;
        height: 64%;
        width: 98.6%;
        overflow-x: hidden;
        display: flex;
        flex-direction: column;
        padding: 10px;
    }
    #MessageBox{
        display: flex;
        flex-direction: column;
    }
    .MessageRight{
        background-color: white;
        max-width: 70%;
        word-wrap: break-word;
        display: inline-block;
        padding: 10px 15px;
        border-radius: 10px;
        align-self: flex-end; 
        margin-bottom: 10px;
        
    }
    .MessageLeft{
        background-color: white;
        max-width: 70%;
        word-wrap: break-word;
        display: inline-block;
        padding: 10px 15px;
        border-radius: 10px;
        align-self: flex-start; 
        margin-bottom: 10px;
    }
    .ImageRight{
        width: 20vw;
        height: 30vh;
        display: inline-block;
        align-self: flex-end;
    }
    .ImageLeft{
        width: 20vw;
        height: 30vh;
        display: inline-block;
        align-self: flex-start;
    }
    #MessageCreateArea{
        background-color: rgb(46, 46, 46);
        position: absolute;
        top: 0;
        left: 0;
        margin-top: 79vh;
        height: 24%;
        width: 100%;
        border-top: 1px solid black;
    }
    #MessageWrite{
        height: 10vh;
        width: 40vw;
        font-size: 1rem;
        border: 1px solid white;
        background-color: rgb(42, 40, 40);
        font-weight: 500;
        color: rgb(226, 218, 218);
        border-radius: 16px;
        position: absolute;
        margin-left: 45vw;
        margin-top: 2%;
        resize: none;
        padding: 10px;
    }
    #SendButton{
        height: 13vh;
        width: 16vh;
        position: absolute;
        margin-left: 89vw;
        margin-top: 2%;
        background-color: blue;
        border-radius: 50%;
    }
    #SendButton:hover{
        background-color: white;
        transition: 0.3 ease;
        cursor: pointer;
    }
    #SendImage{
        position: absolute;
        height: 15vh;
        width: 15vh;
        border-radius: 50%;
        border: 1px solid black;
        margin-top: 1.5%;
        margin-left: 35vw;
        font-size: 5rem;
        font-weight: 600;
    }
    #SendImage:hover{
        background-color: black;
        color: white;
        transition: 0.3s ease;
        cursor: pointer;
    }
    @media (max-width: 480px) {
        #HeaderUser{
            margin-left: 67vw;
            font-size: 1.5rem;
            margin-top: 10%;
        }
        #SendImage{
            margin-left: 3vw;
            height: 10vh;
            width: 10vh;
            margin-top: 10%;
        }
        #MessageWrite{
            margin-top: 7%;
            margin-left: 28vw;
        }
        #MessageSection{
            width: 95%;
        }
        #SendButton{
            height: 10vh;
            margin-top: 10%;
            width: 10vh;
            margin-left: 75vw;
        }
        .ImageLeft{
            width: 50vw;

        }
        .ImageRight{
            width: 50vw;
        }
        #deleteButton{
            margin-right: 1vw;
            width: 7vw;
        }
        #InputPhoto{
            width: 10vw;
        }
        #UploadOverlay{
            width: 60vw;
            margin-left: 10vw;
        }
        #ImageUpload{
            width: 20vw;

        }
    }
</style>

<script lang="ts">
import SocketIO from "socket.io-client"
import { ref } from "vue";
var Sender = sessionStorage.getItem("User");

    export default {
        created() {
            const url = `http://localhost:5000/AccountRetrieveDetails?username=${this.$route.query.User}`;
            fetch(url, {
                method: 'GET',
                mode: 'cors',
                headers: {
                    "Content-Type": "application/json"
                }
            }).then(response => response.json())
                .then(data => {
                    this.Header.UserID = data.Data.ID;
                    this.Header.HeaderPhoto = data.Data.Photo
                    var SenderUserID = sessionStorage.getItem("Userid").toString();
            var receiverID = this.Header.UserID.toString();
            
            
            const urlTwo = `http://localhost:5000/RetreiveChatID?UserOne=${Sender}&UserTwo=${this.$route.query.User}`
            fetch(urlTwo, {
                method: 'GET',
                mode: 'cors',
                headers: {
                    "Content-Type": "application/json"
                }
            }).then(response => response.json())
            .then(data => {
                console.log(data)
                if (data.Data === "No RoomId") {
                    var roomIDComponents = [SenderUserID, receiverID].sort();
                    this.Header.RoomID = parseInt(roomIDComponents.join(''));
                    console.log("No RoomID")
                } else {
                    console.log("RoomID Received")
                    this.Header.RoomID = data.Data.RoomId;
                }

                // Now that the data is available, establish the WebSocket connection
                this.Socket = SocketIO("http://localhost:5000", { transports: ["polling", "websocket"] });
                
                console.log(this.Header.RoomID);
                this.Socket.emit('join_room', { room: this.Header.RoomID });

                this.Socket.on("private_message", data => {
                   
                    this.ReceivedMessages.Messages.push(data)
                    
                });

                this.Socket.on("media_message", data => {
                    this.ReceivedMessages.Messages.push(data);
                })

                const urlThree = `http://localhost:5000/RetrieveMessageHistory?RoomID=${this.Header.RoomID}`;
                fetch(urlThree, {
                    method: 'GET',
                    mode: 'cors',
                    headers: {
                        "Content-Type": "application/json"
                    }
                }).then(response => response.json())
                    .then(data => {
                        if (data.Data !== "No message history") {
                            this.ReceivedMessages.Messages.push(...data.Data);
                        }
                        console.log(this.ReceivedMessages.Messages)
                    }).catch(error => {
                        console.error('Error fetching user data:', error);
                    });
            }).catch(error => {
                console.error('Error fetching user data:', error);
            }); 
                }).catch(error => {
                    console.error('Error fetching user data:', error);
                });

             
            

            
        },
    updated() {
        this.scrollMessageSectionToBottom();
    },
    data() {
        return {
            Socket: null,
            ImageUpload: false,
            Header:{
                HeaderUser: this.$route.query.User,
                HeaderPhoto: null,
                UserID: 0,
                RoomID: 0
            },
            ReceivedMessages: ref({
                Messages: []
            }),
            TextMessageCreate:{
                MessageContent: "",
                Recipient: this.$route.query.User,
                Sender: Sender,
                MessageType: "",
                ImageFile: ""
            }
        }
    },
    methods: {
        BackButton(event: Event ){
            console.log(event);
            this.$router.push("/Contacts")
        },
        SendTextMessage(event: Event){
            console.log(event);
            var sender = sessionStorage.getItem("User")
            this.Socket.emit("private_message", {
                MessageContent: this.TextMessageCreate.MessageContent,
                Recipient: this.TextMessageCreate.Recipient,
                Sender: sender,
                MessageType: "Text",
                RoomID: this.Header.RoomID
            });

            this.TextMessageCreate.MessageContent = "";
            
        },
        handleFileUpload(event : Event) {
                this.TextMessageCreate.ImageFile =  event.target.files[0];  
                console.log(this.TextMessageCreate.ImageFile)
        },
        SendImageMessage(event: Event){
            console.log(event);
            if(this.TextMessageCreate.ImageFile ===""){
                return alert("Please enter an Image")
            }
            const reader = new FileReader();
                reader.readAsDataURL(this.TextMessageCreate.ImageFile);
                reader.onload = () => {
                    const base64String = reader.result.split(',')[1];
                    this.Socket.emit("media_message", {
                        imageContent: base64String,
                        Recipient: this.TextMessageCreate.Recipient,
                        Creator: this.TextMessageCreate.Sender,
                        MessageType: "Image",
                        RoomID: this.Header.RoomID
                });
            }
            this.TextMessageCreate.ImageFile = "";
            
        },
        DeleteMessage(message : any){
            console.log(message.MessageId)
            const url = `http://localhost:5000/DeleteMessage?MessageID=${message.MessageId}`
            fetch(url, {
                method: 'DELETE',
                mode: 'cors',
                headers: {
                    "Content-Type": "application/json"
                }
            }).then(response => response.json())
            .then(data => {
                console.log(data)
                const index = this.ReceivedMessages.Messages.findIndex(m => m.MessageId === message.MessageId);
                if (index !== -1) {
                    this.ReceivedMessages.Messages.splice(index, 1);
                }
            }).catch(error => {
                console.error('Error deleting the message:', error);
            });
        },
        IsSender(message : object){
            var user = sessionStorage.getItem("User");
            return message.Creator === user;
        },
        scrollMessageSectionToBottom() {
            const messageSection = this.$refs.MessageSection;
            messageSection.scrollTop = messageSection.scrollHeight;
        }
    }
}
</script>