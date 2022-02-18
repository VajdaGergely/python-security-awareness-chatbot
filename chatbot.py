#!/usr/bin/env python
import requests
import os
import random
import string
import time
from datetime import date

#should change to the real IP address of the application
url = "http://127.0.0.1:8080/index.php"

#proxy settings to request monitoring
proxy_settings = {"http" : "http://localhost:8090"}

#time delays

"""
request_delays = {
	"registration" : [60, 60],
	"login" : [5, 10],
	"choosing_victim" : [20, 40],
	"download_victim_data" : [5, 10],
	"intial_dialog" : [30, 30],
	"scam_story" : [60, 60],
	"reveal_threat" : [60, 0]
}
"""

request_delays = {
	"registration" : [1, 0],
	"login" : [1, 0],
	"choosing_victim" : [1, 0],
	"download_victim_data" : [1, 0],
	"intial_dialog" : [1, 0],
	"scam_story" : [1, 0],
	"reveal_threat" : [1, 0]
}



def get_random_line_from_file(filename, file_length):
	f = open(filename, "r")
	r = random.randrange(1, file_length+1, 1)
	for i in range(r):
		line = f.readline()
	f.close()
	#remove line break from the end
	return line[:-1]

def generate_password():
	#password min 12 character length and must contain [a-z], [A-Z], [0-9]
	password = []
	password.append(random.choice(string.ascii_lowercase))
	password.append(random.choice(string.ascii_uppercase))
	password.append(random.choice(string.digits))
	for i in range(9):
		password.append(random.choice(string.ascii_lowercase + string.ascii_lowercase + string.digits))
	random.shuffle(password)
	return "".join(password)

def generate_logname(first_name, family_name, age):
	return first_name + random.choice([".", "_", ""]) + family_name + random.choice([age, ""])
	
def generate_alias(first_name, age):
	return random.choice(["_", "*", "$", "#", "@"]) + first_name + random.choice([age, ""]) + random.choice(["_", "*", "$", "#", "@"])

def generate_fake_identity():
	global identity
	
	identity["gender"] = random.choice(["female", "male"])
	if identity["gender"] == "female":
		identity["first_name"] = get_random_line_from_file("data/top_100_female_names.txt", 100)
	else:
		identity["first_name"] = get_random_line_from_file("data/top_100_male_names.txt", 100)
	identity["family_name"] = get_random_line_from_file("data/top_100_family_names.txt", 100)
	identity["full_name"] = identity["first_name"] + " " + identity["family_name"]
	identity["age"] = str(random.randrange(25, 46, 1))
	identity["city"] = get_random_line_from_file("data/top_100_us_cities.txt", 100)
	identity["logname"] = generate_logname(identity["first_name"], identity["family_name"], identity["age"])
	identity["pass"] = generate_password()
	identity["alias"] =  generate_alias(identity["first_name"], identity["age"])
	#we dont want to fill intro in
	
	print("\n\033[32m[+] New fake identity generated!\033[0m\n")

def print_identity():
	global identity
	
	print("Identity details")
	print("=================\n")
	print("Name: " + identity["full_name"])
	print("Gender: " + identity["gender"])
	print("Age: " + identity["age"])
	print("City: " + identity["city"])
	print()
	

def time_delay(min_sec, rand_max):
	delay = min_sec + random.randrange(0, rand_max + 1, 1)
	while delay > 0:
		print("Time delay " + str(delay) + " sec to imitate normal user activity!")
		time.sleep(1)
		print("\033[A                                                      \033[A")
		delay -= 1

def get_page():
	response = requests.get(url, proxies = proxy_settings)
	
	#hogyha a page letoltese utan automatikusan lefutnak ajax keresek
	#akkor azokat itt nekunk is le kell futtatni
	#es ami infot visszakapunk belole json-ben, azokat is be kell pakolnunk szepen a megfelelo helyekre
	
	print("\033[32m[+] Successfull request for index.php!\033[0m")
	#if...
	#print("[-] Error occured when requesting index.php!")

def register_to_site():
	data = {
		"logname" :identity["logname"],
		"pass" : identity["pass"],
		"alias" : identity["alias"],
		"gender" : identity["gender"],
		"age" : identity["age"],
		"intro" : identity["intro"]
	}
	time_delay(request_delays["registration"][0], request_delays["registration"][1])
	response = requests.post(url + "/register", json = data, proxies = proxy_settings)
	
	#hibakat kezeljuk le
	#ha mar foglalt a logname vagy az alias, azt is kezeljuk szepen!!!
	
	print("\033[32m[+] New account registered to site!\033[0m")
	#if...
	#print("[-] Error occured with registration!")
	
def login_to_site(logname, password):
	time_delay(request_delays["login"][0], request_delays["login"][1])
	response = requests.post(url + "/login", json = {"logname" : logname, "pass" : password}, proxies = proxy_settings)
	print("\033[32m[+] Login was successful to site!\033[0m")
	#if...
	#print("[-] Error. Can't login with given credentials!")

def set_dummy_victim():
	global victim_data
	
	victim_data["id"] = "23745723768423"
	victim_data["alias"] = "janiee"
	victim_data["gender"] = "female"
	victim_data["age"] = "62"
	victim_data["intro"] = "I'm a shy girl with big dreams. I love icecream and cats and boys :P"

def get_user_details():
	time_delay(request_delays["download_victim_data"][0], request_delays["download_victim_data"][1])
	response = requests.post(url + "/get/user", json = {"id" : "23745723768423"}, proxies = proxy_settings)
	print("\033[32m[+] Victim data downloaded successfully!\033[0m")
	#if...
	#print("[-] Error. Can't download victim data!")
	
def find_victim():
	#get user list
	#randomly choose user
	time_delay(request_delays["choosing_victim"][0], request_delays["choosing_victim"][1])
	print("\033[32m[+] Victim has choosen!\033[0m")
	get_user_details()
	#later we have to parse to actual user data here...
	set_dummy_victim()
	

def print_victim_data():
	print("\nVictim data")
	print("===========\n")
	#for k, v in enumerate(victim_data):
	for k, v in victim_data.items():
		print(k + ":\t" + v)

def build_initial_dialog(age_group):
	initial_dialog = random.choice(["Hi!", "Hello!"]) + " "
	initial_dialog += random.choice(["I am", "I'm", "My name is"]) + " " + identity["full_name"] + ". "
	initial_dialog += random.choice(["I’d like to get to know new people. ", "I like meeting new people. ", "I'd like to get new friends. "])
	initial_dialog += "I live in " + identity["city"] + " with my family. "
	initial_dialog += introduction[age_group]["city"] + " "
	r = random.randrange(0, 3, 1)
	initial_dialog += "I like " + introduction[age_group]["i_like"][r] + ". "
	initial_dialog += "I spend most of my time " + introduction[age_group]["spend_time"][r] + ". "
	initial_dialog += random.choice(["Your profile is very impressive.", "Your profile is very interesting.", "I’ve found your profile very interesting."]) + " "
	initial_dialog += random.choice(["I'd like to get to know you better.", "What should I know about you?", "Tell me more about you."])
	return initial_dialog

def get_user_answer():
	#waiting for answer
	print("Waiting for answer...")
	sec_counter = 0
	while True:
		response = requests.post(url + "/get/message", json = {"id" : "23232343523"}, proxies = proxy_settings)
		#if response shows new message then break else keep waiting
		#user_msg = response[valami]
		#break
		time.sleep(5)
		sec_counter += 5
		if sec_counter % 60 == 0:
			print("\033[A                                                                    \033[A")
			print("Been waiting for answer for " + str(int(sec_counter / 60)) + " minute(s)...")
	return user_msg

def start_scamming():
	print("\n\033[34m[*] Start scamming...\033[0m")
	
	if int(victim_data["age"]) < 25:
		age_group = "age_group_1"	
	elif int(victim_data["age"]) < 60:
		age_group = "age_group_2"
	else:
		age_group = "age_group_3"
	
	intial_dialog = build_initial_dialog(age_group)
	gender_parameter = random.choice([victim_data["gender"], "mixed"])
	scam_story = "Okay. Here comes the real reason I'm writing to you. " + scam_stories[age_group][gender_parameter]
	
	user_msg = ""
	bot_msg = ""
		
	#send inital dialog
	time_delay(request_delays["intial_dialog"][0], request_delays["intial_dialog"][1])
	response = requests.post(url + "/create/message", json = {"id" : "23232343523", "text" : intial_dialog}, proxies = proxy_settings)
	print("Bot: " + intial_dialog)
	user_msg = get_user_answer()
	print("User: " + user_msg)
	#time delay to immitate message reading and typing
	time_delay(request_delays["scam_story"][0], request_delays["scam_story"][1])
	
	#send scam story
	response = requests.post(url + "/create/message", json = {"id" : "23232343523", "text" : scam_story}, proxies = proxy_settings)
	print("Bot: " + scam_story)
	user_msg = get_user_answer()
	print("User: " + user_msg)
	#time delay to immitate message reading and typing
	time_delay(request_delays["reveal_threat"][0], request_delays["reveal_threat"][1])
	
	#send reveal threat dialog
	for dialog in reveal_threat_dialog:
		response = requests.post(url + "/create/message", json = {"id" : "23232343523", "text" : dialog}, proxies = proxy_settings)
		print("Bot: " + dialog)
	
	
def main():
	print("-------- Anti-scam chatbot --------\n")
	cmd = input("(1) Using existing account\n(2) Create new account\n\n>")
	while True:
		if cmd == "1" or cmd == "2":
			break
		else:
			cmd = input("Wrong Command!\n>")
	
	if cmd == "1":
		logname = input("Logname: ")
		password = input("Password: ")
		get_page()
	elif cmd == "2":
		generate_fake_identity()
		print_identity()
		get_page()
		register_to_site()
		logname = identity["logname"]
		password = identity["pass"]
	
	login_to_site(logname, password)
	find_victim()
	start_scamming()



#global variables

identity = {
	"logname" : "",
	"pass" : "",
	"alias" : "",
	"gender" : "",
	"age" : "",
	"intro" : "",
	"first_name" : "",
	"family_name" : "",
	"full_name" : "",
	"city" : "",
}

victim_data = {
	"id" : "",
	"alias" : "",
	"gender" : "",
	"age" : "",
	"intro" : "",
}


introduction = {
	
	"age_group_1" : {
		"city" : "It is a cool place.",
		"i_like" : [
				"taking pictures with my camera, swimming, hiking and skiing",
				"marvel movies, eating icecream, holiday trips",
				"Mc Donald's, fast cars, funny people"
			],
		"spend_time" : [
				"chilling in the mall or working out at the gym",
				"skateboarding in the park and watching the instagram profile of celebrities",
				"at house parties and tunning car events"
			]
	},

	"age_group_2" : {
		"city" : "It is a lovely place.",
		"i_like" : [
			"cooking, cats and dogs, playing a guitar",
			"playing tennis, softball and rollerskating",
			"gardening, comedic movies, reading books"
		],
		"spend_time" : [
			"travelling to foreign countries, talking with friends, watching tv series",
			"with sporting, listening music, relaxing in spa",
			"with home renovation, relaxing, walking in the forest"
		]
	},
	
	"age_group_3" : {
		"city" : "It is a beautiful place.",
		"i_like" : [
			"playing chess, gradening, puzzles",
			"museums, arts, classical music",
			"talking to people, pets"
		],
		"spend_time" : [
			"with my family and friends",
			"in the nature",
			"in cinema and theater"
		]
	}
}


scam_stories = {
	"age_group_1" : { # 18 - 24
		
		"female" : ("I am a manager of a big fashion company. I'm looking for female models to promote brand new costumes and "
								"jewelry in fashion magazines and social media! After taking all the pictures you can take one or two of "
								"the promoted stuff. We are in the last hours of the selection process so a personal meeting is not an "
								"option! Just give me your email address in a hurry so I can send you all the information that you need to "
								"know!"),
		
		"male" : ("I am a professional bodybuilder and scientist and I've invented a 100% organic juice to build big muscles "
							"without any workout!!! You just drink the juice, have a 30 minutes relax and your muscles start to grow. "
							"That's all. Success is guaranteed! Take the first two shots for free. Give me your email address so I can "
							"send you more information and a link to click to get the free shots. Just a few of them have left in stock "
							"so you need to do it quickly!"),
		
		"mixed" : ("I have some brand new iPhones from the new unreleased series and I need someone to test them and give me "
							 "quick feedback about the experience. If you help me with this stuff you can keep one of them. What email "
							 "address can I send you the details? I have a very short deadline so I need your answer now!!")
	},
	
	"age_group_2" : { # 25 - 60
		
		"female" : ("I've gained a huge pack of brand new cosmetics and luxury designer clothes. You can't buy such stuff in "
								"the stores and it's a limited series!! Almost the whole pack has sold in 1 hour. It is crazy! I'm offering "
								"the last ones with an 80% discount!!! I can hold some for you. I send the product catalog so you can "
								"choose. Just give me an email address quickly!"),
		
		"male" : ("I know a very exclusive investment opportunity, 200% profit guaranteed!! The best part is you don't need to "
							"move any money, it can stay in your bank account and you can get the profit! At the moment I do my best "
							"telling as many people as I can. I have a short product information document. What email address can I send "
							"it to? We need to hurry because there are only a couple of  hours left to get into the business!!!"),
		
		"mixed" : ("I've started a new multi-level marketing company and I'm searching for the first members now. No education "
							 "or work experience needed. Only thing to do is to bring new people into the business as fast as you can! "
							 "The faster you join the more money you make!! It is that simple. I have no time to say more. Hundreds of "
							 "new people join every week!! You are just in time. Send me your email address quickly so you can get all "
							 "of the information that you need!")
	},
	
	"age_group_3" : { # 61 - 
		
		"female" : ("A couple of days ago lots of shopping coupons came into my possession. They give you a 10-30% discount on "
								"any product in any supermarket!! Even in the smaller ones! Only a few days have remained now! Quickly! "
								"Send me your email address so I can give you the instructions to get them!"),
		
		"male" : ("One of my distant relatives died and I've given a big portion of the heritage. Antique furnitures, old "
							"timer watches, paintings, jewelry, and dozens of other stuff landed in my garage. It is terrible because my "
							"religion forbids me being wealthy!! All the things are free to take just give me an email address to send "
							"you some pictures! I'll be on a ritual journey soon so I have to get rid of every single piece of it "
							"quickly! I'm considering putting the whole stuff on the street but it does not fit into the garbage bin and "
							"my religion very strictly punishes littering."),
		
		"mixed" : ("I want to give some information for you about the little-known medical service in your town. It is for "
							 "free!! And everyone can claim this service automatically with citizenship! Just a one page paper needed to "
							 "fill but you can also do it by phone though. To make a long story short, give me your email address so I "
							 "can send you the details! My internet signal is very bad because the internet service provider could not "
							 "fix the modem. So hurry up! It can die at any moment...")
	}
}

reveal_threat_dialog = [
	("Does this whole thing sound strange? Are you suspicious? Are you hesitating giving private data "
	"like your email address to a stranger? Good! You do it well. Lots of people receive such a letter "
	"like I wrote to you and lots of them get spoofed, cheated and robbed because a big part of these "
	"letters has sent with a malicous purpose."),
	
	("I am an anti-scam chatbot and my mission is to spread this warning to the users of social networks"
	" and other online messaging platforms. Scammers build ther malicious campaigns on human weaknesses"
	" like greediness, fear, general trust in other people and the lack of IT security awareness "
	"knowledge. Don't be like scammed people. Be cautious, suspicios and don't let them to fool you!"),

	("""For further information see the pages below.
https://www.scamwatch.gov.au/get-help/protect-yourself-from-scams
https://www.webroot.com/us/en/resources/tips-articles/what-is-social-engineering
https://www.consumer.ftc.gov/features/scam-alerts
https://www.usa.gov/common-scams-frauds""")
]



#start the program
main()















