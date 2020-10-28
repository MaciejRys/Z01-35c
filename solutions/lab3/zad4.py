import sys, random

if __name__ == "__main__":
	print('Podaj liczbę rund:')
	rounds = int(input())
	wins = 0
	loses = 0;
	draws = 0;
	while rounds != 0:	
		print('Wpisz swój wybór: papier kamień lub nożyce')
		userChoice = input()
		while userChoice != "papier" and userChoice != "kamień" and userChoice != "nożyce" :
			print('Niepoprawny wybór. spróbuj jeszcze raz: papier kamień lub nożyce')
			userChoice = input()
		choices = ["papier", "kamień", "nożyce"]
		compChoice = random.choice(choices)
		print("Komputer wybrał " + compChoice)
		if userChoice == compChoice:
			draws += 1
			print("Remis")
		elif userChoice == "papier" and compChoice == "kamień":
			wins += 1
			print("Wygrana")
		elif userChoice == "papier" and compChoice == "nożyce":
			loses += 1
			print("Przegrana")
		elif userChoice == "kamień" and compChoice == "papier":
			loses += 1
			print("Przegrana")
		elif userChoice == "kamień" and compChoice == "nożyce":
			wins += 1
			print("Wygrana")
		elif userChoice == "nożyce" and compChoice == "kamień":
			loses += 1
			print("Przegrana")
		elif userChoice == "nożyce" and compChoice == "papier":
			wins += 1
			print("Wygrana")
		rounds -= 1
	print("Koniec gry\nWygrałeś: " + str(wins) + " razy\nPrzegrałeś: " + str(loses) + " razy\nByło " + str(draws) + " remisów")
				