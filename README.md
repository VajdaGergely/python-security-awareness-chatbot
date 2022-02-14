# python-security-awareness-chatbot
Python coded chatbot to warn users of online scamming activity (under development)


This is a coding project for practicing HTTP communication in Python and implementing an online scamming campaign with a whitehat attitude :)

The Python script accomplishes web based chatbot functionality on a PHP web chat platform (also coded by me: https://github.com/VajdaGergely/php-chat-application). It makes HTTP GET and POST requests to the backend API of the chat application with JSON encoded data within the messages. HTTP messaging is achieved by the “requests” Python library.


The script automates the client side user registration, login and text messaging operations to execute an anti-scam campaign with
  * registering fake accounts
  * spoofing users with fake stories
  * requesting contact information
  * revealing its true identity
  * warning of potential scam activities on online platforms
  * and offering IT security awareness websites.

Technical details
  * HTTP GET and POST messaging
  * JSON encoded data


Scamming features
  * randomly generated profile data using prebuilt lists
  * different scam stories based on the victim’s gender and age
  * pretending normal user activity with time delays between requests, following page navigation order and spoofing user agent headers

Future plans
  * handling CSRF tokens and other security solutions
  * making a list about contacted users and avoid writing them again
  * using IP spoofing to avoid IP address banning
  * fully automated operation with infinite targets


Disclamer
  * Any misuse of the application will not be the responsibility of the author.
  * Chatbot generates fake identities by combining the most common US family names,
cities and other parameters from public top 100 lists. Any correspondence to real life persons is just statistical coincidence.
  * Received data from victims of the simulated scamming campaign is only printed to the terminal screen but not stored locally because it is a whitehat project so this data is not needed.

