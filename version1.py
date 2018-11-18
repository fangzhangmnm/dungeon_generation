import numpy as np
import random,os,time
randint=np.random.randint
choice=random.choice
map_width=40
map_height=40
total_iteration=200
map=np.zeros((map_width,map_height),dtype=np.int_)
dirs=np.array(((1,0),(0,1),(-1,0),(0,-1)))
def printMap():
	chars={0:'■',1:'　'}
	os.system('cls')
	for j in range(map_height):
		for i in range(map_width):
			print(chars[map[i,j]],end='')
		print()
def printMapDebug():
	chars={0:'■',1:'　'}
	os.system('cls')
	for j in range(map_height):
		for i in range(map_width):
			coord=np.array((i,j))
			if map[i,j]==1:
				count=emptyNeighborCount(coord)
				print(count,end=' ')
			else:
				print(chars[map[i,j]],end='')
		print()
def inMap(coord):
	return coord[0]>=0 and coord[0]<map_width and coord[1]>=0 and coord[1]<map_height
def readMap(coord):
	if not inMap(coord):
		return -1
	return map[tuple(coord)]
def setMap(coord,item):
	if not inMap(coord):
		return
	map[tuple(coord)]=item
def isSolid(coord):
	return readMap(coord) in [0]
def isRoom(coord):
	return readMap(coord) in [1]
def isEmptyRoom(coord):
	return readMap(coord) in [1]
def checkWallToDig(coord):
	if not isSolid(coord):
		return False,None
	for i in range(4):
		dx,dy=dirs[i],dirs[(i+1)%4]
		if isRoom(coord-dx) and isSolid(coord+dx) and isSolid(coord+dy) and isSolid(coord-dy) and isSolid(coord+dx+dy) and isSolid(coord+dx-dy):
			return True,(coord,i)
	return False,None
def isInRoom(coord):
	for i in range(4):
		dx,dy=dirs[i],dirs[(i+1)%4]
		if isRoom(coord) and isRoom(coord+dx) and isRoom(coord+dy) and isRoom(coord+dx+dy):
			return True
	return False
def checkRoomToDig(coord,dir,left,right,forward):
	dx,dy=dirs[dir],dirs[(dir+1)%4]
	c1=coord+dx*(forward+1)+dy*right
	c2=coord+dx-dy*left
	x1,x2,y1,y2=min(c1[0],c2[0]),max(c1[0],c2[0]),min(c1[1],c2[1]),max(c1[1],c2[1])
	for i in range(x1,x2+1):
		for j in range(y1,y2+1):
			if not isSolid((i,j)):
				return False
	for i in range(x1-1,x2+2):
		if not isSolid((i,y1-1)):
			return False
		if not isSolid((i,y2+1)):
			return False
	for j in range(y1-1,y2+2):
		if not isSolid((x1-1,j)):
			return False
		if not isSolid((x2+1,j)):
			return False
	return True
def digRoom(coord,dir,left,right,forward):
	dx,dy=dirs[dir],dirs[(dir+1)%4]
	c1=coord+dx*(forward+1)+dy*right
	c2=coord+dx-dy*left
	x1,x2,y1,y2=min(c1[0],c2[0]),max(c1[0],c2[0]),min(c1[1],c2[1]),max(c1[1],c2[1])
	setMap(coord,1)
	map[x1:x2+1,y1:y2+1]=1
def checkCorridorToDig(coord,dir):
	dx,dy=dirs[dir],dirs[(dir+1)%4]
	length=0
	while True:
		if not (isSolid(coord+length*dx) and isSolid(coord+length*dx+dy) and isSolid(coord+length*dx-dy)) :
			break
		length+=1
	if not isRoom(coord+length*dx):
		return length,0
	else:
		if isInRoom(coord+length*dx):
			return length,1
		else:
			return length,2
def digCorridor(coord,dir,length):
	for i in range(length):
		setMap(coord+dirs[dir]*i,1)
def emptyNeighborCount(coord):
	count=0
	for i in range(4):
		if isRoom(coord+dirs[i]):
			count+=1
	return count
def cleanDeadCorridors():
	found=True
	while found:
		found=False
		for i in range(map_width):
			for j in range(map_height):
				coord=np.array((i,j))
				if isEmptyRoom(coord) and emptyNeighborCount(coord)<2:
					setMap(coord,0)
					found=True
map[5:7,5:7]=1
def mainloop():
	diditer=0
	for myiter in range(total_iteration):
		did=False
		coords=np.mgrid[0:map_width,0:map_height].transpose(1,2,0).reshape(-1,2)
		walls=[i[1] for i in [checkWallToDig(i) for i in coords] if i[0]]
		if len(walls)==0:
			break
		wall,dir=choice(walls)
		roll=randint(100)
		if roll<40:
			width=randint(2,6)
			forward=randint(2,6)
			left=randint(0,width)
			if roll<10:
				width=randint(5,10)
				forward=randint(5,10)
				left=randint(0,width)
			while not checkRoomToDig(wall,dir,left,width-left-1,forward):
				if randint(2)<1:
					width-=1
					if width<2:
						break
					left=randint(0,width)
				else:
					forward-=1
					if forward<2:
						break
			if checkRoomToDig(wall,dir,left,width-left-1,forward) and width>1 and forward>1:
				did=True
				digRoom(wall,dir,left,width-left-1,forward)
		elif roll<90:
			length=randint(4,6)
			length2,endtype=checkCorridorToDig(wall,dir)
			if length<length2:
				did=True
				digCorridor(wall,dir,length)
			else:
				if endtype==1 and length2>0:
					did=True
					digCorridor(wall,dir,length2)
		else:
			cleanDeadCorridors()
			did=True
		if did:
			diditer+=1
			if diditer%5==0:
				printMap()
				#os.system('pause')
				time.sleep(0.1)

mainloop()
cleanDeadCorridors()
printMap()

