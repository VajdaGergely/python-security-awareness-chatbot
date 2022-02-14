#!/usr/bin/env python
import os
import random
import requests
import string
from datetime import date
import time

url = "http://127.0.0.1:8080/index.php"
proxy_settings = {"http" : "http://localhost:8090"}

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
	"city" : ""
}

victim_data = {
	"id" : "",
	"alias" : "",
	"gender" : "",
	"age" : "",
	"intro" : "",
}


has_identity_set = False

dialogs = {
	"greetings" : ["Hi!", "Hello!", "Hey!"],
	
	"initial_dialog" : {
		
		"part1" : [
			"Your profile is very impressive.",
			"Your profile is very interesting.",
			"I like your profile."
		],
		
		"part2" : [
			"I can't wait to get to know you better.",
			"I would like to get to know you better.",
			"I would like to chat with you."
		],
		
		"part3" : [
			"Could you tell me something about you?",
			"Say something about you.",
			"Tell me something about you.",
			"What should I know about you?",
			"How would you introduce yourself?"
		]
	},
	
	"feedbacks" : {
		
		"textual" : {
			"happy" : ["Good", "Nice", "Very good"],
			"rough" : ["Nice", "Good", "Cool"],
			"funny" : ["Hehe", "Haha", "Hahaha", "It's funny", "It's so funny"],
			"unhappy" : ["Oh", "Ohh", "I see", "I totally understand it", "I totally understand you", "Oh no",  "Sounds bad"],
			"sad" : ["Oh that's so sad", "I'm sorry", "I'm so sorry", "It is so sad", "It's very sad"],
			"neutral" : [
				"I see.",
				"Hmm.",
				"Okay.",		
			]
		},
		
		"emotes" : {
			"happy" : [":)"],
			"rough" : [";)", ":P", ";P"],
			"funny" : [":)", ":D", ":DD", ":DDD", "XD", "XDD"],
			"unhappy" : [":/"],
			"sad" : [":(", ":((", ":'("]
		}
	},
	
	"changing_topic" : {
		"part1" : [
			"Sorry for changing topic.",
			"Sorry for changing the topic.",
			"It is very interesting that you're talking about.",
			"I don't want to change the topic."
		],
		
		"part2" : [
			"But I have to tell something to you.",
			"But I have to tell something to you now.",
			"But I have to tell you something.",
			"But I have to tell you something now.",
			"But there is something that you have to know.",
			"But there is something that you have to know about me.",
			"But I have to tell you something.",
			"But I have to tell you something about me.",
			"There's a little secret that you have to know",
			"There's a little secret that you need to know",
		],
	},
	
	"changing_topic2" : {
		"There is another thing that you don't know about me yet.",
		"There is another thing that you don't know about me yet.",
	},
	
	"serious_thing_about_me" : {
		"I'm a secret agent! And I'm working for the government. I have a lots of information that I have to share with someone.",
		"I am a billionare but I never tell it to someone because I don't want people hanging with me just because I'm rich. I want to meet new people I can spend my time with.",
		"Sometimes I can read in other people's mind. I want to teach this skill to a couple of people. I hope you are interested in.",
		"I have a secret business where you can earn lots of money easily without working. No initial money nor education needed. I can tell you more about it later if you want."
	},
	
	"closing_serious_thing_topic" : {
		"I wish I could tell you more about it but maybe later.",
		"I can't tell you more about it yet. But I promise I will soon.",
		"Don't tell it to anyone. I't is very confidential thing",
		"I hope you can hold my secret" 
	},
	
	
	"random_stuff" : [
		"I love to speak with you.", 
		"Tell me more about it.", 
		"I could speak with you forever.",
		"I totally understand you."
	],
	
	"answers_to_questions" : [
		"Sorry I don't want to answer that question yet.",
		"I want to answer that question later",
		"I will write it later.",
		"I'l tell it later I promise.",
		"It is a bit hard to speak about it for me."
	],
	
	"farewells" : ["Bye", "Bye bye", "See you later"]
}

#should be convert every received message to lowercase form

#expected_stuff
postitive_answers = ["yes", "sure", "good", "ok", "okay", "alright", "yep", "yup", "fine", "ye"]
negative_answers = ["no", "nope", "not"]
negotiated_positive_answers = ["no good", "not good", "not ok", "not okay", "not alright", "not fine"]
neutral_answers = ["not sure", "dont know", "don't know", "no idea"]
farewells = ["bye", "bye bye", "see ya", "see you", "see ya later", "see you later", "good bye", "later"]
emotes = {
	":)": "happy",
	":-)": "happy",
	":))": "happy",
	":-))": "happy",
	":D" : "funny",
	":-D" : "funny",
	":DD" : "funny",
	":-DD" : "funny",
	"XD" : "funny",
	"XDD" : "funny",
	":P" : "rouge",
	":-P" : "rouge",
	":PP" : "rouge",
	":-PP" : "rouge",
	";)" : "rouge",
	";-)" : "rouge",
	";P" : "rouge",
	";-P" : "rouge",
	";PP" : "rouge",
	";-PP" : "rouge",
	":(" : "sad",
	":-(" : "sad",
	":'(" : "sad",
	":'-(" : "sad",
	":/" : "unhappy",
	":-/" : "unhappy",
	":O" : "admired",
	":-O" : "admired",
}

positive_feelings = ["happy", "funny", "rouge"]
negative_feelings = ["sad", "unhappy"]
neutral_feelings = ["admired"]
feelings_priority_order = ["funny", "rough", "happy", "unhappy", "sad", "admired"]

"""
conversation statuses
before_speaking
chating
greeting
farewell


question_asked
got_answer_for_question


got_question
said_answer_for_question

random_stuff_said
"""

current_conversation_status = 0;

def get_random_line_from_file(filename, file_length):
	f = open(filename, "r")
	r = random.randrange(1, file_length+1, 1)
	for i in range(r):
		line = f.readline()
	f.close()
	#remove line break from the end
	return line[:-1]

def generate_random_number_with_intervals_and_weights(intervals, weights):
	if len(intervals) != len(weights) + 1:
		return "-1"
	else:
		x = random.randrange(1, sum(weights) + 1, 1)
		for i in range(len(intervals)-1):
			if x <= sum(weights[0:i+1]):
					return str(random.randrange(intervals[i], intervals[i+1], 1))
		return "-1"

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
	identity["age"] = generate_random_number_with_intervals_and_weights([18, 41, 51, 61, 81, 100], [50, 40, 5, 4, 1])
	identity["city"] = get_random_line_from_file("data/top_100_us_cities.txt", 100)
	identity["logname"] = generate_logname(identity["first_name"], identity["family_name"], identity["age"])
	identity["pass"] = generate_password()
	identity["alias"] =  generate_alias(identity["first_name"], identity["age"])
	#we dont want to fill intro in
	
	print("\n[+] New fake identity generated!\n\n")

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
	delay = 10 + random.randrange(0, 10, 1)
	print("[*] Time delay (" + delay + ") sec to imitate normal user activity!")
	time.sleep(delay)

def get_page():
	response = requests.get(url, proxies = proxy_settings)
	
	#hogyha a page letoltese utan automatikusan lefutnak ajax keresek
	#akkor azokat itt nekunk is le kell futtatni
	#es ami infot visszakapunk belole json-ben, azokat is be kell pakolnunk szepen a megfelelo helyekre
	
	print("[+] Successfull request for index.php!")
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
	time_delay(60, 60)
	response = requests.post(url + "/register", json = data, proxies = proxy_settings)
	
	#hibakat kezeljuk le
	#ha mar foglalt a logname vagy az alias, azt is kezeljuk szepen!!!
	
	print("[+] New account registered to site!")
	#if...
	#print("[-] Error occured with registration!")
	
def login_to_site(logname, password):
	time_delay(5, 10)
	response = requests.post(url + "/login", json = {"logname" : logname, "pass" : password}, proxies = proxy_settings)
	print("[+] Login was successful to site!")
	#if...
	#print("[-] Error. Can't login with given credentials!")

def set_dummy_victim():
	global victim_data
	
	victim_data["id"] = "23745723768423"
	victim_data["alias"] = "janiee"
	victim_data["gender"] = "female"
	victim_data["age"] = "24"
	victim_data["intro"] = "I'm a shy girl with big dreams. I love icecream and cats and boys :P"

def get_user_details:
	time_delay(5, 10)
	response = requests.post(url + "/get/user", json = {"id" : "23745723768423", proxies = proxy_settings)
	print("[+] Victim data downloaded successfully!")
	#if...
	#print("[-] Error. Can't download victim data!")
	
def find_victim():
	#get user list
	#randomly choose user
	print("[+] Victim has choosen!")
	get user details()
	#later we have to parse to actual user data here...
	set_dummy_victim()
	

def print_victim_data():
	print("\nVictim data")
	print("===========\n")
	#for k, v in enumerate(victim_data):
	for k, v in victim_data.items():
		print(k + ":\t" + v)

def calc_delay_after_get_msg(user_msg, bot_msg):
	#Normal human reading speed:	250 words / min (4.16666666 chars / sec)
	#Average english word length:	4.7 chars 
	#Normal human typing speed:		40 words / min (3.13333333 chars / sec)
	
	usr_msg_read_time = len(user_msg) * 4.16666666
	bot_msg_thinking_time = random.randrange(2, 21, 1)
	bot_msg_write_time = len(bot_msg) * 3.13333333
	return = usr_msg_read_time + bot_msg_thinking_time + bot_msg_write_time + random.randrange(0, 31, 1)

def start_scamming():
	print("\nStart scamming...")
	
	#tmp stuff...
	init_message = ""
	second_msg = ""
	third_msg = ""
	i = 0
	messages = [
		init_message,
		second_msg,
		third_msg
	]
	user_msg = ""
	bot_msg = ""
	
	while True:
		#send message
		response = requests.post(url + "/create/message", json = {"id" : "23232343523", "text" : messages[i]}, proxies = proxy_settings)
		print("Bot: " + messages[i])
		
		#waiting for answer
		print("Waiting for answer...")
		sec_counter = 0
		while True:
			#itt a time delay-t bonyolult modon fogjuk kiszamolni!!!
			time_delay(5, 10)
			response = requests.post(url + "/get/message", json = {"id" : "23232343523"}, proxies = proxy_settings)
			#if response shows new message then break else keep waiting
			#user_msg = response[valami]
			#time.sleep(calc_delay_after_get_msg(user_msg, bot_msg), 1)
			#break
			time.sleep(5)
			sec_counter += 5
			if sec_counter % 60 == 0:
				print("Wating for (" str(sec_counter / 60) + ") minutes ...")
		i++

def examine_feelings(user_message):
	user_message = user_message.upper()
	feelings = []
	
	#search emotes with different paddings and positions 
	for k, v in emotes.items():
		
		if (user_message == k) or (" " + k + " " in user_message) or (user_message[0:len(k) + 1] == k + " ") or (user_message[-(len(k) + 1):] == " " + k):
			feelings.append(v) #emote found with high possibility
		elif (k in user_message):
			feelings.append(v) #emote found with low possibility
	
	#examine found emotes
	if len(feelings) == 0:
		return False
	elif len(feelings) == 1:
		return feelings
	else:
		feelings = list(set(feelings)) #remove repeated values from array
		if len(feelings) == 1:
			return feelings
		else:
			#examine if opposite feelings found
			positive_feeling_found = False
			negative_feeling_found = False
			for feeling in feelings:
				if feeling in positive_feelings:
					positive_feeling_found = True
				if feeling in negative_feelings:
					negative_feeling_found = True
				if positive_feeling_found and negative_feeling_found:
					result = ["mixed"]
					return result
			
			#no mixed feelings
			return feelings

def generate_feedback(feeling, interaction_count):
	#get textual and emote dialogs by feeling
	text = random.choice(dialogs["feedbacks"]["textual"][feeling])
	if feeling != "neutral":
		emote = random.choice(dialogs["feedbacks"]["emotes"][feeling])
	else:
		emote = ""
	
	#forcing textual and emote feedbacks at the beginning
	#and using weighted randomization later
	feedback = ""
	if(interaction_count == 0):
		feedback = text + " " + emote
	elif(interaction_count == 1):
		feedback = emote
	else:
		#after 1 interaction
		#attach textual feeling material in 20% of messages
		#attach emote feeling material in 50% of messages
		
		r = random.randrange(0, 5, 1)
		if r == 4:
			feedback = text
		
		r = random.randrange(0, 2, 1)
		if r == 0:
			if feedback != "":
				feedback += " "
			feedback += emote
		else: #when no emotes, "." or "!" used at the end of the feedback
			if feedback != "":
				if random.randrange(0, 2, 1) == 0:
					feedback += "."
				else:
					feedback += "!"
	
	return feedback


def do_conversation():
	global dialogs
	
	interaction_count = 0
	
	#bot should end the conversation with increasing chance
	#bot should understand when we want end the conversation, and he should cooperate with the ending
	
	#starting conversation
	initial_message = random.choice(dialogs["greetings"]) + " " + random.choice(dialogs["initial_dialog"]["part1"])
	if random.randrange(0, 2, 1) == 0: #sometimes send 
		initial_message += " " + random.choice(dialogs["initial_dialog"]["part2"])
	initial_message += " " + random.choice(dialogs["initial_dialog"]["part3"])
	print("Bot: " + initial_message)
	
	while True:
		bot_message = ""
		user_message = input("Me:  ")
		
		#handle feelings
		feelings = examine_feelings(user_message)
		if (feelings != False) and (feelings[0] != "mixed"):
			for feeling_from_prior in feelings_priority_order:
				if feeling_from_prior in feelings:
					bot_message += generate_feedback(feeling_from_prior, interaction_count)
		else:
			bot_message += generate_feedback("neutral", interaction_count)
		print("Bot: " + bot_message)
		
		#handle received questions
		
		#flaterry
		
		#print("Bot: " + random.choice(dialogs["random_stuff"]))
		interaction_count += 1


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
		print()
	elif cmd == "2":
		generate_fake_identity()
		print_identity()
		get_page()
		time.sleep(10)
		register_to_site()
		logname = identity["logname"]
		password = identity["pass"]
	
	login_to_site(logname, password)
	find_victim()
	print_victim_data()
	start_scamming()
	
#start
main()
























