# A Facebook chatbot!
## This chatbot can read messages sent to it and store the activities that users send to it, as well as display it to the users if they request it

### Chatbot Side Functionality
- If the user tags the chatbot in a message, the chatbot should read that message and parse the message for the activity
- Once the activity is parsed, the chatbot should store it in a database so that it can be retrieved whenever
- The user should be able to tag the chatbot and ask it to list all the current activities in the bucket list as well as when these activites should occur, listed in chronological order
- The user should be able to tag the chatbot and send just a google maps link to a specific location. The chatbot should be able to parse the google maps link and figure out where the user wants to go
- The user should be able to delete activities that they no longer want to do from the list using the chatbot as well

### Website Side Functionality
- The user can go to the website, see the list of activities, and set a time/date that these activities to be done
- The user should be able to do all CRUD (Create, Read, Update, Delete) operations on the activites listed as well

### Nice to have features
- A login page so that the todo list is privated
- Allow the user/users to upload photos of the activity so that there's a timeline/visual indicator of these bucket list activites being done (big big strech goal)
- For activities that have locations provided, provide a google maps integration widget to show distance from user's home location
- Activities should be filtered into categories (Food, Drink, Activity, Other etc etc)

### Issues encountered during development that should be noted
- PAGE_ACCESS_TOKEN environment variable is set by Apache in /etc/apache/envvars
- During Apache HTTPS setup, use fullchain.pem instead of cert.pem for SSLCertificateFile field

### General debugging tips
- /var/log/apache2/error.log for Apache errors
- /var/log/bucketlistbot.log for Django logs
- `sudo service apache2 restart` to restart the Apache service
