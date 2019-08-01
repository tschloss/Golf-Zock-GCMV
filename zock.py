input = '463540366 Helmut 16,564663406 Willy 17,575544555 Thomas 11'

 #'454553454 Thomas 11,564644465 Hans 16,603604460 Peter 16'

#'074064586 Willy 16,464545085 Thomas 11,474554067 Peter 16,566454565 Rudi 11'
 
#'666350377 Thomas 12,706474466 Willy 18,555456486 Peter 16'

#'675540050 Willy 17,464543560 Thomas 11,463573454 Rainer 13'

# board = [[6,7,5,5,4,0,0,5,0,'Willy',17],[4,6,4,5,4,3,5,6,0,'Thomas',11],[4, 6,3,5,7,3,4,5,4,"Rainer",13]]

#[[4,5,10,5,6,3,4,4,6,'Rory', 12],[4,5,10,3,6,6,4,5,4,'Tiger',13],[5,6,6,3,4,5,5,4,4,'Dustin',11],[6,6,4,8,6,4,5,8,5,'Hacker',26]]

coursepar =[4,5,3,4,4,3,4,5,4]
#coursepar = [4,4,4,3,5,4,3,5,4]

coursehcp = [13,3,1,9,7,15,17,11,5,8,12,14,18,10,2,16,4,6]
# coursesorted = [2,1,8,4,3,7,0,5,6] # manual ;)


def nettopts (strokes, spvg):
	p = 0
	for i in range(9):
		if strokes[i] > 0:			# 0 means no result = no points
			p0 = 2 + coursepar[i] - strokes[i]
			if spvg > 18: 
				p0 += 1
			if ((spvg-1)%18)+1 >= coursehcp[i]: p0 += 1
			if p0 > 0: p += p0
		
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
		if strokes0[hole] == 0 and strokes1[hole] == 0: 
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

# populate board (comma between players, blank between scores/name/spvg)
board = []
for player in input.split(','):
	playerf = []
	result = player.split(' ')		# score digits / name / spvg
	# score digits, 0 = 0 (means none)
	for c in result[0]:
		if (c >= '0' and c <= '9'):
			playerf.append(ord(c)-48)
	if len(playerf) != 9: print('Error: not exactly 9 scores')
	
	# name
	playerf.append(result[1])
	
	# spvg
	spvg=0
	for c in result[2]:
		if (c >= '0' and c <= '9'):
			spvg = spvg * 10 + (ord(c)-48)
	playerf.append(spvg)
	
	board.append(playerf)


# print(board)

for player in board:
	netto = nettopts(player[:9],player[10])
	print (player[9],'( SpVg',player[10],')',':',netto, 'Punkte   (', prettyround(player[:9]),')')

	for player2 in board:
		if player2[9] != player[9]:
			print ('   gegen ',player2[9], end='')  #( SpVg ',player2[10],')', end='')
			print ('      ',prettymatch(strokeplay(player[:9],player[10],player2[:9],player2[10])))