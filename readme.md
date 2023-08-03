# Purpose
The purpose of this project is to create a private instant messaging app using Vue on the frontend, Flask on the backend, and MySQL as the database. I used this project as a means to learn Flask, Vue, MySQL, and web sockets, while also practicing CSS by utilizing CSS media queries to make the project mobile friendly to Iphones. 

# About
This app is an instant messaging service where users can: Sign up for an account, login to their account, update their account with details such as profile picture and username, create private one-on-one chats with other users, message other users, and delete their messages. Users can also search for other users that are signed up, and have the option of sending image files over texts. 

# Issues During Development
The biggest issue that occured to me during development of this project was simply burn out, as by the time I had started this project I had recently finished another big project, my image hoster, along with finals, and school related projects. It was also around this time that I managed to acquire my first internship, so I found it hard to keep motivation to produce code on the side as I already achieved my goal of finding work. I am happy to say that eventually I found that passion for coding again, and dedicated myself to finishing this project until it was functional. Other minor problems I encountered during the development of this application were learning how to use web sockets, learning how Vue functions worked (Created(), Data(), etc), and finally how to represent each message and user account in an SQL database.

# Future Improvements
This project is admittely flawed in many aspects, one huge one that I would like to improve upon in the future through recreating this project would be the gigantic, spaghetti code filled files. One thing that I learned about Vue in this project is that Vue likes to keep both the CSS, HTML, and Javascript functions in the same file, but very quickly this led to bloated files with hundreds of lines of code. While the code was mostly made in bulk of CSS classes and media queries, I found the strucutre very ugly and wish to cleanly separate the structure the next time I used Vue. Another mistake I made was in the creation of the server, where every piece of backend functionality and api call, including the websocket server, is included in one giant file. The file is easily over 300 lines long, and looking back, I wish I had cleanly separated the backend into a flask server for account manipulation, a websocket server for the messaging functionality, a models folder for the database, and a database conncection folder. 

# Technologies Used
   
- Vuejs
- Flask 
- FlaskSocketIO
- MySQL
- SQLAlchemy
- PyJWT
