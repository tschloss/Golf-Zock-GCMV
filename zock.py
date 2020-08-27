# 0 means 'no result', 'strich'
inputByPlayer = ''
#'584453455 Thoma 11,674554775 Will 17,896774676 Cengi 26'
#'574544575 Thomas 11,684856483 Peter 16'


inputByHole = 'Thomas Hans Willy Maddin Cengiz,11 17 17 11 29,65478 97757 44555 66546 45657 63544 35555 67798 57548'
# 'Thomas Willy Peter,11 17 16 17,445 567 445 555 455 354 573 596 568'
# 'Thomas Peter Willy Horst,11 15 17 28,5768 5355 5750 4558 8778 5567 5678 5767 3245'
# 'Thomas Willy,11 17,46 56 45 55 57 44 30 75 56' #60 40 56 33 67'
# 'Thomas Rainer Willy Peter,11 13 17 16,5465 5760 4550 4565 5446 4654 5545 5577 5457'  #664 676 404 455 440 454 356 766 575'
#'Thomas Peter,11 16,56 78 44 58 45 46 54 78 53' 


coursepar18 = [4,5,3,4,4,3,4,5,4,4,4,4,3,5,4,3,5,4] # GCMV
#coursepar =[4,5,3,4,4,3,4,5,4] #GCMV 1-9
#coursepar = [4,4,4,3,5,4,3,5,4] #GCMV 10-18
#coursepar = [5,3,4,4,4,4,5,4,3] # Heddesheim 1-9
# coursepar = [5,3,4,4,3,4,4,5,4]  # Heddesheim 10-18

# first 9: +1 /2  second 9: /2. if odd on first nine
coursehcp18 = [13,3,1,9,7,15,17,11,5,8,12,14,18,10,2,16,4,6] #GCMV 
#coursehcp = [7,2,1,5,4,8,9,6,3] # GCMV 1-9
#coursehcp = [4,6,7,9,5,1,8,2,3] # GCMV 10-18

#coursehcp18 =  [11,13,3,17,7,5,1,9,15,14,16,2,18,10,4,8,6,12] # Heddesheim
#coursehcp = [6,7,2,9,4,3,1,5,8] # Heddesheim 1-9
#coursehcp = [7,8,1,9,5,2,4,3,6] # Heddesheim 1-18



def nettopts(strokes, spvg):
	p = 0
	for i in range(9):
		if strokes[i] > 0:		# falls nicht 'strich'
			p0 = 2 + coursepar[i] - strokes[i] # 1. brutto par = 2 usw
			if spvg > 18:			# 2. vorgabe über 18 = extra punkt
				p0 += 1
			if ((spvg - 1) % 18) + 1 >= coursehcp18[i]: p0 += 1		# 3. vorgabe am loch? = extra punkt
			if p0 > 0: p += p0		# 4. nur positive punkte addieren, negative = 0

	return p
	
def adv_matchplay (spvg0, spvg1):
	# strokes: diff *3/4 - halved - +0,5 if odd
	# positive advantage = player0 receives strokes
	# must be under 18 effektive stromes for 18
	advantage = round(abs(spvg0 - spvg1) * 3 / 4 + 0.1) #18 holes
	if advantage > 18: return([0,0,0,0,0,0,0,0,0]) # shoul be an error, but 0 should make it visible also
	
	if advantage % 2 == 1:
		halfstroke = True
		advantage += 1 # although on the last hole it will only be .5
	else:
		halfstroke = False
	#halfstroke = (advantage % 2 == 1) # True/False
	
	advantage = advantage // 2 # plus halfstroke eventually 
	if (spvg1 > spvg0): advantage *= -1
	
	a_s = []
	for hole in range(9):
		if abs(advantage) >= coursehcp[hole]:
			a_s.append(1)
			if (abs(advantage) == coursehcp[hole]) and halfstroke: a_s[hole] = 0.5
			if (advantage < 0): a_s[hole] *= -1
		else: a_s.append(0)
	
	## todo: this print statement should not be here but in the main loop where all output is generated
	if (spvg1 > spvg0): print(' gebe: ',prettyadvantages(a_s))
	else: print(' bekomme: ',prettyadvantages(a_s))
	
	return (a_s)

def _adv_matchplay (spvg0, spvg1):
	# strokes: diff *3/4 - halved - +0,5 if odd
	# positive advantage = player0 receives strokes
	# this methods requires that all odd difficulties are on 1-9 and even on 10-18, better treat them seperately
	advantage = round(abs(spvg0 - spvg1) * 3 / 4 + 0.1)
	if (spvg1 > spvg0): advantage *= -1
	a_s = []
	for hole in range(9):
		if abs(advantage) >= coursehcp[hole]:
			a_s.append(1)
			if (abs(advantage) == coursehcp[hole]) and (advantage % 2 == 1): a_s[hole] = 0.5
			if (advantage < 0): a_s[hole] *= -1
		else: a_s.append(0)
	#print('Vorgabevektor: ',a_s)
	return (a_s)
		
	
def matchplay (strokes0, spvg0, strokes1, spvg1):
	advantages = adv_matchplay(spvg0,spvg1)
	up = []
	for hole in range(len(strokes0)):
		if strokes0[hole] == 0 and strokes1[hole] ==  0:
			up.append(0)
		elif strokes0[hole] == 0: 
			up.append(-1)
		elif strokes1[hole] == 0:
			up.append(1)
		else:
			p0adv = strokes1[hole] - strokes0[hole] + advantages[hole]
			if p0adv > 0:
				up.append(1)
			elif p0adv < 0:
				up.append(-1)
			else: 
				up.append(0)
	
	return up 

	
def prettymatch(holes):
	prettystring=''
	resulttxt=''
	i=0
	match=0
	for hole in holes:
		match += hole
		
		
		if hole<0:
			prettystring += '▼'
		elif hole>0:
			prettystring += '▲'
		else: 
			prettystring += '◦'

		if i in (2,5): prettystring += ' '
		i+=1
		
		if resulttxt=='' and abs(match) > (9-i):
			if i==9:
				resulttxt = str(abs(match)) + 'auf'
			else:
				resulttxt = str(abs(match)) + '+' + str(9-i)
				
	if match > 0: prettystring = '✔︎ gewonnen [+'+str(abs(match))+'/'+resulttxt+']  ('+prettystring+')'
	elif match < 0: prettystring = '✘ verloren [-'+str(abs(match))+'/'+resulttxt+'] ('+prettystring+')'
	else: prettystring = '⦁ geteilt  ('+prettystring+')'
		
	return prettystring


def prettyround(holes):
	prettystring=''
	i=0
	for hole in holes:
		if hole==0:
			prettystring += '-'
		else: 
			prettystring += str(hole)
		if i in (2,5): prettystring += ' '
		i+=1
		
	return prettystring

def prettyadvantages (holes):
	prettystring=''
	i=0
	for hole in holes:
		if hole==0:
			prettystring += '◦'
		elif abs(hole) == 1:
			prettystring += '●'
		else:
			prettystring += '◐'
		if i in (2,5): prettystring += ' '
		i+=1
		
	return prettystring
	
	
def holeranks9 (holeranks18):
	#input: list of difficulties, lower is more difficult
	#output-list: idx = holenumber, value tells rank starting with 1 for the most difficult
	
	l = []
	for idx, value in enumerate(holeranks18):
		#print (value,"is at",idx)
		l.append ([value,idx]) # check how it works with tuple instad field

	#print(l)
	l.sort (reverse=False) # sortieren nach den Values, niedrigster Wert zuerst, idx ist die urspgl. Position (das Loch)
	#print(l)

	# jetzt mit map neuen Vektor y erzeugen ; mal mit map versuchen!?
	y=[0,0,0,0,0,0,0,0,0] 
	for i in range(9):
		#y[i] = l[i][1]+1 # idx0 tells number of most difficult hole
		y[l[i][1]] = i+1 # 
	
	#print("Scorekarte:",v,"Vorgabenverteilung 9:",y)
	
	return(y)


## BuildBoard = populate the internal data structure from various input options

def buildBoardByPlayer (board, input):
	
	# populate board (comma between players, blank between scores/name/spvg)
	#board = []
	for player in input.split(','):
		playerf = []
		result = player.split(' ')		# score digits / name / spvg
		# score digits, 0 = 0 (means none)
		for c in result[0]:
			if (c >= '0' and c <= '9'):
				playerf.append(ord(c)-48)
		if len(playerf) > 9: print('Error: more than 9 scores')
		elif len(playerf) < 9: 
			for i in range(9 - len(playerf)): playerf.append(0)
		
		# name
		playerf.append(result[1])
		
		# spvg
		#spvg=0
		#for c in result[2]:
		#	if (c >= '0' and c <= '9'):
		#		spvg = spvg * 10 + (ord(c)-48)
		spvg = int(result[2])
		playerf.append(spvg)
		
		board.append(playerf)
	
	return

def buildBoardByHole (board, input):
	#board = []
	
	sections = input.split(',') # 0:names 1:spvg 2:holebyhole
	names = sections[0].split(' ')
	spvgs = sections[1].split(' ')
	holes = sections[2].split(' ')
	
	for player in range(len(names)):
		playerf=[]
		
		# holes
		for holestring in holes:
			playershole = holestring[player]
			playerf.append(ord(playershole)-48)
		for i in range(9 - len(holes)): playerf.append(0)
		
		# name
		playerf.append(names[player])
		
		# spvg
		#spvg=0
		#for c in spvgs[player]:
		#	if (c >= '0' and c <= '9'):
		#		spvg = spvg * 10 + (ord(c)-48)
		spvg = int(spvgs[player])
		playerf.append(spvg)
		
		board.append(playerf)
		
		
	return

#### main ###

#board = buildBoardByPlayer(inputByPlayer)
board = []
if len(inputByHole) > 0: buildBoardByHole(board, inputByHole)
if len(inputByPlayer) > 0: buildBoardByPlayer(board, inputByPlayer) 

coursehcp = holeranks9(coursehcp18[:9]) # first 9 = [:9] or last 9 = [9:]
coursepar = coursepar18[:9]

# print(board) ## [[1,2,..9,'name',22],[9..,,2,1,'name',11]]

for player in board:
	netto = nettopts(player[:9],player[10])
	print (player[9],'( SpVg',player[10],')',':',netto, 'Punkte   (', prettyround(player[:9]),')')

	for player2 in board:
		if player2[9] != player[9]:
			print ('   gegen ',player2[9], end='')  #( SpVg ',player2[10],')', end='')
			print ('      ',prettymatch(matchplay(player[:9],player[10],player2[:9],player2[10])))
