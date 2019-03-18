#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Version : 2.0 stable 11.27.2018 Ghost Escape

# Authors : Axel Polin, Mirna Marie-Joseph
#
# This software is distributed under GNU General Public License v3.0
#
# With  7. Additional Terms.
#  "Additional permissions" are terms that supplement the terms of this
# License by making exceptions from one or more of its conditions.
# Additional permissions that are applicable to the entire Program shall
# be treated as though they were included in this License, to the extent
# that they are valid under applicable law.  If additional permissions
# apply only to part of the Program, that part may be used separately
# under those permissions, but the entire Program remains governed by
# this License without regard to the additional permissions.
#
#  1.Prohibiting misrepresentation of the origin of that material, or
#    requiring that modified versions of such material be marked in
#    reasonable ways as different from the original version;
# https://www.gnu.org/licenses/gpl-3.0.html


import sys
import tty
import termios
import os
from generate_map import *
from tqdm._tqdm import tqdm
from random import shuffle

class Joueur:

	def __init__(self,position_x,position_y,buffer_map,coord):
		self.position_x=position_x
		self.position_y=position_y
		self.points=3
		self.refresh=0
		self.buffer_map=buffer_map
		self.coord=coord

	def keyPressed(self,event):
		sys.stdout.flush()
		if event=='\x1b[D':
			self.deplacement("left")
		if event=='\x1b[C':
			self.deplacement("right")
		if event=='\x1b[B':
			self.deplacement("down")
		if event=='\x1b[A':
			self.deplacement("up")
		return self.points

	def deplacement(self,direction):
		refresh=0
		if direction=="left":
			if self.position_x>0:
				if self.buffer_map[self.position_y][self.position_x-1]=="0" or self.buffer_map[self.position_y][self.position_x-1]!="1":

					self.position_x=self.position_x-1
				
		if direction=="right":
			if self.position_x<len(self.buffer_map[0])-1:
				if self.buffer_map[self.position_y][self.position_x+1]=="0" or self.buffer_map[self.position_y][self.position_x+1]!="1":

					self.position_x=self.position_x+1
		
		if direction=="up":
			if self.position_y>0:
				if self.buffer_map[self.position_y-1][self.position_x]=="0" or self.buffer_map[self.position_y-1][self.position_x]!="1":

					self.position_y=self.position_y-1

		if direction=="down":
			if self.position_y<len(self.buffer_map)-1:
				if self.buffer_map[self.position_y+1][self.position_x]=="0" or self.buffer_map[self.position_y+1][self.position_x]!="1" :
					self.position_y=self.position_y+1
		
		old_char=self.buffer_map[self.position_y][self.position_x]
		self.buffer_map[self.position_y][self.position_x]="C"
		print("\033c")
		print_map(self.buffer_map,self.points)
		self.buffer_map[self.position_y][self.position_x]=old_char

		[self.points,self.position_x,self.position_y,self.refresh]=event_ghost(self.position_x,self.position_y,self.coord,self.points)
		
		if self.refresh == 1:
			old_char=self.buffer_map[self.position_y][self.position_x]
			self.buffer_map[self.position_y][self.position_x]="C"
			print("\033c")
			print_map(self.buffer_map,self.points)
			self.buffer_map[self.position_y][self.position_x]=old_char
		return 0

def event_ghost(position_x,position_y,coord,life_points):
		refresh=0

		for key in coord:
			if key=="Paradise" and coord[key]==[position_y,position_x]:
				life_points=999

			if key=="M" and coord[key]==[position_y,position_x]:
				print "You meet the master of the castel !!"
				[position_y,position_x]=coord["Reception"]
				refresh=1

			if key=="F" and coord[key]==[position_y,position_x]:
				print "You meet the mad scientist !! "
				life_points-=1
				[position_y,position_x]=coord[coord.keys()[randint(0,len(coord)-1)]][0:2]
				refresh=1

			if key[0]=="B" and coord[key]==[position_y,position_x]:
				print "You meet a bibbendum marshmallow !!" 
				life_points-=2

			if key[0]=="P" and key[1]!="a" and coord[key][0:2]==[position_y,position_x]:
				if coord[key][2]!=0:
					print "Life youhou"
					life_points+=coord[key][2]
					coord[key][2]=0

			if key=="M" and (coord[key]==[position_y,position_x+1] or coord[key]==[position_y,position_x-1] or coord[key]==[position_y+1,position_x] or coord[key]==[position_y-1,position_x]):
				print "Cling Cling Clang Cling"

			if key=="F" and (coord[key]==[position_y,position_x+1] or coord[key]==[position_y,position_x-1] or coord[key]==[position_y+1,position_x] or coord[key]==[position_y-1,position_x]):
				print "MOUHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAH"

			if key[0]=="B" and (coord[key]==[position_y,position_x+1] or coord[key]==[position_y,position_x-1] or coord[key]==[position_y+1,position_x] or coord[key]==[position_y-1,position_x]):
				print "You smell a strawberry marshmallow !"

		return [life_points,position_x,position_y,refresh]

def Convert_map(content):

	content_tran=content.split("\n")
	
	num_line=len(content)/len(content_tran[0])
	content=content.replace("\n","")
	
	remap=[[0 for j in range(0,len(content_tran[0]))] for i in range(0,num_line)]
	
	k=0
	for i in range(0,num_line):
		for j in range(0,len(content_tran[0])):
			remap[i][j]=content[k]
			k+=1
	return remap

def print_welcome():
	print "WELCOME AT GHOST ESCAPE"
        print "Here you are, Casper, in the castle you deciced to haunt a while ago. You've put off for a while to leave this place, the people living there were quite weird, but overall friendly. But the time finally came, all your friend are at the other side and you need to see them again. "
        print "However the friendly people you met actually had ulterior motive and now they won't let you go! You'll have to dodge the master of the castle who keeps moving you to the reception, the mad scientist who found a way to harm you, and his delicious minion."
        print "Thankfully, they are quite a noisy and wonderfully smelling bunch so you just have to keep your guard up to know where they are. You've also left barrel of your favourite ectoplasma all over the place which can give you stamina. Hopefully you won't need them..."
        print " "
	print "	Press arrow keys to move"
	print " Enjoy ;)"

def print_map(content_map,life_pts):

        print ""
	print "Life : "+"# "*life_pts+"\t"+"(Enter END to exit properly or ^C)"
	print ""
        str = ""

	for i in range(0,len(content_map)):
                str="@ "

		for j in range(1,len(content_map[0])-1):
			if content_map[i][j]=="0" or content_map[i][j]=="S":
				str+="  "
			if content_map[i][j]=="1":
				str+="@ "
			if content_map[i][j]=="P":
				str+="P "
			if content_map[i][j]=="R":
				str+="R "
			if content_map[i][j]=="C":
				str+="C "
			if content_map[i][j]=="M" or content_map[i][j]=="B" or content_map[i][j]=="E":
				str+="  "
                        
		print str+"@ "
	print ""

def placement(content_map,mode):
	coord={}
	salle=[]
	max_points=3
	k=0
	
	for i in range(0,len(content_map)):
		for j in range(0,len(content_map[0])):
			if content_map[i][j]=="S" :
				coord["S"+str(k)]=[i,j]
				k+=1
	
	T=range(len(coord))			
	shuffle(T)
	
	for i in range(len(T)):
		salle.append("S"+str(T[i]))

	ennemies=mode[0]
	pintes=mode[1]
	nb_pintes=randint(0,len(pintes)-1)
	stat_pintes=partition_borne(len(pintes),max_points)[nb_pintes]

	for i in range(len(ennemies)):
		coord[ennemies[i]]=coord[salle[i]]
		del coord[salle[i]]

	for i in range(0,len(stat_pintes)):
		coord[pintes[i]]=coord[salle[i+1+len(ennemies)]]
		del coord[salle[i+1+len(ennemies)]]
		coord[pintes[i]].append(stat_pintes[i])
	
	for i in range(0,len(content_map)):
		for j in range(0,len(content_map[0])):
			if content_map[i][j]=="R" :
				coord["Reception"]=[i,j]
			if content_map[i][j]=="P" :
				coord["Paradise"]=[i,j]
	return coord

def partition_borne(n,max_part):
	if n==0:
		return [[]]
	result = []
	for i in range(min(n,max_part), 0, -1):
		for p in partition_borne( n-i, i ):
			result.append( [i] + p )
	return result

def found_init_pos(content_map):
	for i in range(0,len(content_map)):
		for j in range(0,len(content_map[0])):
			if content_map[i][j]=="R" :
				return [j,i]
	return 1

def level_difficulty():
        print "Do you want to play in 'peacefull' mode, 'normal' mode, 'hard' mode or 'nightmare' mode? [Default : Normal]"
        print "Enter the level (nothing for normal): "
        mode=raw_input()
        if mode=="peacefull":
                ennemie=["M"]
                pintes=["P1","P2","P3","P4","P5","P6","P7","P8","P9","P10"]
                return [ennemie,pintes]
        if mode=="normal":
                ennemies=["B1","B2","B3","M","F"]
                pintes=["P1","P2","P3","P4","P5"]
                return [ennemies,pintes]
        if mode=="hard":
                ennemies=["B1","B2","B3","B4","B5","M","F"]
                pintes=["P1","P2","P3","P4","P5","P6","P7","P8","P9","P10"]
                return [ennemies,pintes]
        if mode=="nightmare":
                ennemies=["B1","B2","B3","B4","B5","M","F"]
                pintes=["P1","P2","P3","P4","P5"]
		return [ennemies,pintes]
	if mode != "peacefull" or mode != "normal" or mode != "hard" :
		ennemies=["B1","B2","B3","M","F"]
                pintes=["P1","P2","P3","P4","P5"]
                return [ennemies,pintes]

def main():
	coord={}
	nb_map=1
	x_max=60
	y_max=40
	
	mode_level=level_difficulty()
	
	if mode_level == [["B1","B2","B3","B4","B5","M","F"],["P1","P2","P3","P4","P5"]] or mode_level == [["B1","B2","B3","B4","B5","M","F"],["P1","P2","P3","P4","P5","P6","P7","P8","P9","P10"]] :
		print "Generating maps..."
		
		for i in tqdm(range(nb_map)):
			seed()
			x=randint(50,x_max)
			y=randint(30,y_max)
			map_txt=gen_map(x,y)
	
			with open(name="MAPS/map_"+str(i)+".txt",mode="w") as fd :
				for j in range(y):
					for k in range(x):
						try :
							fd.write(map_txt[j][k])
						except :
							print "ERROR while writting maps files sorry exiting..."
							return 1
					fd.write('\n')
			x,y,map_txt=0,0,""
		
		print "Maps generated !"
		
		maps=randint(0,nb_map)
		with open(name="MAPS/map_"+str(maps)+".txt",mode="r") as fd :
			content=fd.read()
	else :
		with open(name="map_s.txt",mode="r") as fd :
			content=fd.read()
	
	remap=Convert_map(content)
	
	init_pos=found_init_pos(remap)
	if init_pos == 1 :
		print "ERROR RECEPTION not FOUND"
		return 1

	init_pos_x=init_pos[0]
	init_pos_y=init_pos[1]
	
	
	print_welcome()
	old_char=remap[init_pos_y][init_pos_x]
	
	remap[init_pos_y][init_pos_x]="C"
	
	print_map(remap,3)
        
	remap[init_pos_y][init_pos_x]=old_char

	coord=placement(remap,mode_level)
	joueur=Joueur(init_pos_x,init_pos_y,remap,coord)
	
	old_settings = termios.tcgetattr(sys.stdin)
	tty.setcbreak(sys.stdin)

	while(1):
		try :
			event_key=sys.stdin.read(3)
			if event_key=='END':
				print "Quitting game bye bye..."
				break
			value=joueur.keyPressed(event_key)
			if value <= 0 :
				print("\033c")
				print "GAME OVER"
				break
			if value == 999 :
				print("\033c")
				print "YOU WIN !!"
				break
		except :
			#print "AN ERROR OCCURED... Exiting..."
			break
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
	return 0

if __name__ == '__main__':
	sys.exit(main())
