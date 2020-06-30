# COVID Ticketing

### Background
All of us are going through the hardest times in our lifetime. Everyone expected  the next big thing to be World War III but then COVID-19 happened. A war can be stopped if humans cooperate and come to an agreement but stopping a pandemic is harder than that but doesn't mean it is impossible. The best solution as of now to curb this rapid spread of COVID-19 is social distancing, washing hands regularly and wearing masks. This project is a step towards achieving the goal of social distancing when we visit stores to get essentials, which is an inevitable routine task for people. This app solves the problem of overcrowded stores by making store owners to define small available time slots for customer to come in. Customers can book these available timeslots and hence providing a smaller assigned window for everyone and greatly avoids overcrowded stores. This will welcome more people to the store as they have better chance of keeping social/physical distancing. Social distancing, wearing mask and washing hands are the new civic duties of every citizen.

### How to use the app

The app primarily has 2 users, A Customer and A Store Owner.

#### Owner
1. You can sign up as an ```Owner``` using the ```Signup``` from home page. Select Owner radio button.
2. An ```Owner``` can create new stores using the ```Stores tab``` when logged in as owner. The Name, Address and Phone are the three inputs that needs to be provided.
3. Once a store is created, owner can also create availability slots for a particular date. As an example say I created the store, Target, and now I am planning to create availability slots from ```10:00``` to ```12:00``` with ```30 min``` increments. This creates 4 availability slots (10:00,10:30),(10:30,11:00),(11:00,11:30),(11:30,12:00) for the selected date. This can be done using the ```Availability tab``` when you log in as owner and choose the Store for which you need to create time slot from  stores ```dropdown``` list, choose the date from the ```date``` widget
4. The owner can also see all the reservations made by different customers for the stores he own.
5. The owner can even delete reservations if needed and the customer would be notified about the removal of reservation.
6. The owner can delete an entire store listing as well which will inturn delete all the previous reservations customers made with that store earlier.

#### Customer
1. You can sign up as a customer using the ```Signup``` from home page. Make sure the phone number provided is the one where you intend to get notifications regarding your reservation status via text message.
2. A customer as soon he/she logs in can see all the reservations made he/she to different stores in the ```Reservations``` tabs. There is also an option to ```Delete``` the reservation. If a reservation is deleted, that particular time slot goes back to the availability slot for that store.
3. The ```Find Availability``` tab helps in showing customer all the availability listings from different stores. The customer can choose any convenient availability slot and ```Reserve``` it. As soon as reservation is successful, text message would be received to mobile phone number attached to customer. The delete reservation also sends a reservation status via text message.


### Prerequisite: 
1. [Python 3.x](https://www.python.org/downloads/)
2. [Pip](https://pip.pypa.io/en/stable/installing/)

### How to run locally

1. Clone this project.
2. Run ```pip install requirements.txt```. Requirements file has all the necessary modules that needs to be installed on your machine to run the app.
3. Client folder has the UI code and ```app.py``` has the backend api code. You can refer to ```localhost:8080/api/v1/docs``` to see swagger documentation of all APIs used. These are public as of now for ease of use and visibility but can definitely be hidden if required.
5. To run the backend server open a terminal/cmd and run command ```python app.py```
6. Now go to ```http://localhost:8080``` to access the home page

### Note

#### Technolgoies used

1. Python flaskrestplus for Backend/APIs
2. MongoDB for database: [mlab](https://mlab.com/welcome/)
3. Jquery, HTML for Frontend/UI

#### Requirements.txt

To generate requirements.txt I have used ```pipreqs``` module. You can run
```
   1. pip install pipreqs
   2. pipreqs --force <absolute-path-to-project-backend-folder> 
```
In this project this file is already created and stored in ```/server``` folder.
