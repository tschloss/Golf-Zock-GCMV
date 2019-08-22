inputByPlayer = '584453455 Thomas 11,674554775 Willy 17,896774676 Cengiz 26'
#'574544575 Thomas 11,684856483 Peter 16'

inputByHole = 'Tho Wil Cen,11 17 26,568 879 446 457 557 344 476 577 556'
#'Thomas Peter,11 16,56 78 44 58 45 46 54 78 53'
# 0 means 'no result', 'strich'


coursepar =[4,5,3,4,4,3,4,5,4] #GCMV 1-9
#coursepar = [4,4,4,3,5,4,3,5,4] #GCMV 10-18

coursehcp = [13,3,1,9,7,15,17,11,5,8,12,14,18,10,2,16,4,6] #GCMV
# coursesorted = [2,1,8,4,3,7,0,5,6] # manual ;)


def nettopts(strokes, spvg):
	p = 0
	for i in range(9):
		if strokes[i] > 0:		# falls nicht 'strich'
			p0 = 2 + coursepar[i] - strokes[i] # 1. brutto par = 2 usw
			if spvg > 18:			# 2. vorgabe über 18 = extra punkt
				p0 += 1
			if ((spvg - 1) % 18) + 1 >= coursehcp[i]: p0 += 1		# 3. vorgabe am loch? = extra punkt
			if p0 > 0: p += p0		# 4. nur positive punkte addieren, negative = 0

	return p
	

def adv_strokeplay (spvg0, spvg1):
	# strokes: diff *3/4 - halved - +0,5 if odd
	# positive advantage = player0 receives strokes
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
		
	
def strokeplay (strokes0, spvg0, strokes1, spvg1):
	advantages = adv_strokeplay(spvg0,spvg1)
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
			prettystring += '-'
		elif hole>0:
			prettystring += '+'
		else: 
			prettystring += '.'

		if i in (2,5): prettystring += ' '
		i+=1
		
		if resulttxt=='' and abs(match) > (9-i):
			if i==9:
				resulttxt = str(abs(match)) + 'auf'
			else:
				resulttxt = str(abs(match)) + '+' + str(9-i)
				
	if match > 0: prettystring = '++gewonnen [+'+str(abs(match))+'/'+resulttxt+']++  ('+prettystring+')'
	elif match < 0: prettystring = '--verloren [-'+str(abs(match))+'/'+resulttxt+']-- ('+prettystring+')'
	else: prettystring = '   geteilt  ('+prettystring+')'
		
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


def buildBoardByPlayer (input):
	
	# populate board (comma between players, blank between scores/name/spvg)
	board = []
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
		spvg=0
		for c in result[2]:
			if (c >= '0' and c <= '9'):
				spvg = spvg * 10 + (ord(c)-48)
		playerf.append(spvg)
		
		board.append(playerf)
	
	return board

def buildBoardByHole (input):
	board = []
	
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
		spvg=0
		for c in spvgs[player]:
			if (c >= '0' and c <= '9'):
				spvg = spvg * 10 + (ord(c)-48)
		playerf.append(spvg)
		
		board.append(playerf)
		
		
	return board

#### main ###

#board = buildBoardByPlayer(inputByPlayer)
board = buildBoardByHole(inputByHole)

# print(board) ## [[1,2,..9,'name',22],[9..,,2,1,'name',11]]

for player in board:
	netto = nettopts(player[:9],player[10])
	print (player[9],'( SpVg',player[10],')',':',netto, 'Punkte   (', prettyround(player[:9]),')')

	for player2 in board:
		if player2[9] != player[9]:
			print ('   gegen ',player2[9], end='')  #( SpVg ',player2[10],')', end='')
			print ('      ',prettymatch(strokeplay(player[:9],player[10],player2[:9],player2[10])))
