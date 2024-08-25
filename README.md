Hello there Hecker...Hacker ? What should I call you ?
Let's call you Paul !!

Now listen Paul !!
I have created the above project where we have a Desktop Application which the User can use for Brute-Force Attack on their choice of Wifi Network.

Basically what happens is that we have a python script which when executed shows a User Interface Window with two Input Boxes :
1) Enter the Wifi Network Name :
2) Select the Dictionary :

In the first one you enter the Wifi Network Name and in the second one you select a .txt file which contains the data or list of the most common passwords or the most used ones.
When you have clicked the "Start Brute Force Attack" button for the above, the python script will keep trying the passwords that are available in the dictionary which we selected.

For testing the application, I disconnected from my Wifi network and Clicked forget for the Wifi Network and after this I entered the Wifi Name in the application's 1st Input Box and then selected a file named passwords.txt,
I had already entered the password for my Wifi Network in the passwords.txt file but after 3-4 dummy passwords, so that when I execute the Python Script it will try the first 3-4 passwords in the "passwords.txt" file
and then when it reaches the original password and tries to connect to my Wifi Network which I specified I am successfully connected to it.

Remember the above application has limitations due to the limited passwords available in the file which contains dictionary of passwords, now in your case it completely depends on the passwords available in the password
dictionary file. Also one more limitation is that the Bruteforce Attack doesn't guarantee connectivity with the Wifi network specified.

In your case you could also download the "rockyou.txt" file which contains millions of leaked or common passwords being used all over the world.
