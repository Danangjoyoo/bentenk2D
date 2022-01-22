import pygame as pg
import random
import time, sys
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pgr

class CThread():
	def __init__(self,event=None,execution=None):
		self.eventFunc = event
		self.execFunc = execution
		self.breakFunc = None
		self.backupFunc = {'event':None, 'exec':None, 'break': None}
		self.targetTick = 3
		self.start = False
		self.performanceLog = {'timepack':[], 'rate':0, 'init_t':time.perf_counter(), 't1':0}
		self.initTime = 0

	def __core(self, init=True):
		if init:
			pgr.GraphicsLayoutWidget()
			timer = QtCore.QTimer()
			timer.timeout.connect(lambda: self.__core(init=False))
			timer.start(self.targetTick)
			QtGui.QApplication.instance().exec_()
		else:
			if self.eventFunc:
				if self.eventFunc(): self.execFunc()
				else: QtGui.QApplication.quit()
			else:
				self.execFunc()
				QtGui.QApplication.quit()

	def run(self):
		self.__core()

	def setEvent(self, funct):
		self.eventFunc = funct
		self.backupFunc['event'] = self.eventFunc

	def setExecution(self, funct):
		self.execFunc = funct
		self.backupFunc['exec'] = self.execFunc

	def setBreak(self, funct):
		self.breakFunc = funct
		self.backupFunc['break'] = self.breakFunc

	def setTicks(self, targetTick):
		self.targetTick = targetTick

	def status(self):
		print(f'Event 		: {self.eventFunc}')
		print(f'Execution 	: {self.execFunc}')
		print(f'TargetTick 	: {self.targetTick} ms/loop')
		print(f'Is Running	: {self.start}')

	def terminateThread(self):
		self.start = False
		print(f"cppThread for {self} has terminated")

	def checkPerformance(self,func=lambda: [i for i in range(40000)],testFunc=False):
		if not testFunc:
			print(f'Performance Test on {func}..')
			self.status()
			t0 = time.perf_counter()
			tt = Thread()
			tt.setEvent(lambda: (time.perf_counter()-t0<=3))
			tt.setExecution(lambda: self.checkPerformance(func=func,testFunc=True))
			print('Please Wait...')
			tt.run()
			for tick in self.performanceLog['timepack']: self.performanceLog['rate'] += tick
			self.performanceLog['rate'] /= len(self.performanceLog['timepack'])
			n = round(self.performanceLog['rate']*1000,5)
			nd = round(((n-self.targetTick)/self.targetTick)*100, 2)
			print(f'Thread Performance 	: {n} ms/loop')
			if nd > 0: print(f'Performance Drop 	: -{nd} %')
			else: print(f'Performance Rise 	: +{abs(nd)} %')
		else:
			t1 = time.perf_counter()
			if func: func()
			else: [i for i in range(40000)]
			self.performanceLog['timepack'].append(time.perf_counter()-t1)

class char():
    def __init__(self, parent, side, picpack, hitpack, x, y , speed):
        self.parent = parent
        self.side = side
        if self.side == 'r':
            self.selfStand = standred
        elif self.side == 'b':
            self.selfStand = standblue
        self.headB, self.headR, self.headT, self.headL = picpack[0],picpack[1],picpack[2],picpack[3]
        self.hitB, self.hitR, self.hitT, self.hitL = hitpack[0],hitpack[1],hitpack[2],hitpack[3]
        self.x = x
        self.y = y
        self.w = char_scale
        self.spd, self.spdAnchor = speed, speed
        self.head = 0
        self.hit_motion = None
        self.hit = False
        self.energy_dur = fps*2
        self.t1 = 0
        self.t2 = 0
        self.t3 = 0
        self.endB, self.endR, self.endT, self.endL = False, False, False, False
        self.allies_around = 0
        self.enemies_around = 0
        if idx1 == 0 or idx1 == 2:
            self.allyPos = [(None, None), (None, None), (None, None), (None, None), (None, None)]
            self.enemyPos = [(None, None), (None, None), (None, None), (None, None), (None, None)]
        else:
            self.enemyPos = [(None, None), (None, None), (None, None), (None, None), (None, None), (None, None),
                            (None, None), (None, None), (None, None)]
            self.allyPos = [(None, None)]
        self.getAttacked = False
        self.disarm = False

    def run(self):
        self.keys = pg.key.get_pressed()
        if self.keys[pg.K_w]:
            self.head = 2
            if self.y > self.parent.y + (self.parent.h*0.01):
                #bg1.y += self.spd
                #standblue.y += self.spd
                self.y -= self.spd
        elif self.keys[pg.K_s]:
            self.head = 0
            if self.y < self.parent.y+self.parent.h-(self.parent.h*0.07):
                #bg1.y -= self.spd
                #standblue.y -= self.spd
                self.y += self.spd
        if self.keys[pg.K_d]:
            self.head = 1
            if self.x < self.parent.x+self.parent.w-(self.parent.w*0.07):
                #bg1.x -= self.spd
                #standblue.x -= self.spd
                self.x += self.spd
        elif self.keys[pg.K_a]:
            self.head = 3
            if self.x > self.parent.x + (self.parent.w*0.01):
                #bg1.x += self.spd
                #standblue.x += self.spd
                self.x -= self.spd
        if self.keys[pg.K_SPACE]:
            self.hit = True

    def hitStand(self):
        global runGame
        global winner, end
        if self.hit_motion.colliderect(self.bentengA):
            self.energy_dur = 200
            self.t2 = 0
            self.t1 = 0
        elif self.hit_motion.colliderect(self.bentengE):
            if self.t1 // int(fps * 0.1) == 3:
                runGame = False
                end = True
                if self.side == 'r':
                    winner = 'r'
                elif self.side == 'b':
                    winner = 'b'

    def draw(self):
        global runGame, end
        if runGame:
            self.t2 += 1
            if not self.getAttacked:
                if self.t2%3 == 0:
                    if self.energy_dur <= 5:
                        self.energy_dur = 1
                        self.spd = 0.9
                    elif self.energy_dur > 5:
                        self.energy_dur -= 1
                        self.spd = self.spdAnchor
            else:
                self.disarm = True
                self.energy_dur = 1
                self.spd = 0

            pg.draw.rect(win, (200, 150, 100),
                         (self.x-int(self.headB.get_rect().size[0]*0.2*(fps/100)),
                          self.y-int(self.headB.get_rect().size[1]*0.5*(fps/100)),
                          (global_scale*0.1*self.energy_dur), global_scale*5))
            if self.side == 'r':
                self.bentengA = standred.surface
                self.bentengE = standblue.surface
            elif self.side == 'b':
                self.bentengA = standblue.surface
                self.bentengE = standred.surface

            self.run()

            if self.hit:
                self.t1 += 1

            if self.head == 0:
                win.blit(self.headB, (self.x,self.y))
                if self.hit and self.t1 < int(fps*0.4):
                    if not self.disarm:
                        self.hit_motion = win.blit(self.hitB[self.t1//int(fps*0.1)], (self.x, self.y+3))
                        self.hitStand()
                        if self.side == 'r':
                            self.attackEnemy(self.hit_motion, self.enemyPos, blueTeam)
                            self.tapFriends(self.hit_motion, self.allyPos, redTeam)
                        elif self.side == 'b':
                            self.attackEnemy(self.hit_motion, self.enemyPos, redTeam)
                            self.tapFriends(self.hit_motion, self.allyPos, blueTeam)
                elif self.t1 > 60:
                    self.t1 = 0
                    self.hit = False
            elif self.head == 1:
                win.blit(self.headR, (self.x, self.y))
                if self.hit and self.t1 < int(fps*0.4):
                    if not self.disarm:
                        self.hit_motion = win.blit(self.hitR[self.t1//int(fps*0.1)], (self.x+3, self.y))
                        self.hitStand()
                        if self.side == 'r':
                            self.attackEnemy(self.hit_motion, self.enemyPos, blueTeam)
                            self.tapFriends(self.hit_motion, self.allyPos, redTeam)
                        elif self.side == 'b':
                            self.attackEnemy(self.hit_motion, self.enemyPos, redTeam)
                            self.tapFriends(self.hit_motion, self.allyPos, blueTeam)
                elif self.t1 > 60:
                    self.t1 = 0
                    self.hit = False
            elif self.head == 2:
                win.blit(self.headT, (self.x, self.y))
                if self.hit and self.t1 < int(fps*0.4):
                    if not self.disarm:
                        self.hit_motion = win.blit(self.hitT[self.t1//int(fps*0.1)], (self.x, self.y-3))
                        self.hitStand()
                        if self.side == 'r':
                            self.attackEnemy(self.hit_motion, self.enemyPos, blueTeam)
                            self.tapFriends(self.hit_motion, self.allyPos, redTeam)
                        elif self.side == 'b':
                            self.attackEnemy(self.hit_motion, self.enemyPos, redTeam)
                            self.tapFriends(self.hit_motion, self.allyPos, blueTeam)
                elif self.t1 > 60:
                    self.t1 = 0
                    self.hit = False
            elif self.head == 3:
                win.blit(self.headL, (self.x, self.y))
                if self.hit and self.t1 < int(fps*0.4):
                    if not self.disarm:
                        self.hit_motion = win.blit(self.hitL[self.t1//int(fps*0.1)], (self.x-3, self.y))
                        self.hitStand()
                        if self.side == 'r':
                            self.attackEnemy(self.hit_motion, self.enemyPos, blueTeam)
                            self.tapFriends(self.hit_motion, self.allyPos, redTeam)
                        elif self.side == 'b':
                            self.attackEnemy(self.hit_motion, self.enemyPos, redTeam)
                            self.tapFriends(self.hit_motion, self.allyPos, blueTeam)
                elif self.t1 > 60:
                    self.t1 = 0
                    self.hit = False
            if not runGame:
                global idx1
                if winner == 'b':
                    if idx1 == 3:
                       #win.blit(base_bluewin_hc, (0,0))
                       screen.blit(pg.image.load('data/bluewin_hc.png'), (0, 0))
                    else:
                        #win.blit(base_bluewin, (0,0))
                        screen.blit(pg.image.load('data/bluewin.png'), (0, 0))
                elif winner == 'r':
                    if idx1 == 1:
                        #win.blit(base_redwin_hc, (0,0))
                        screen.blit(pg.image.load('data/redwin_hc.png'), (0, 0))
                    else:
                        #win.blit(base_redwin, (0,0))
                        screen.blit(pg.image.load('data/redwin.png'), (0, 0))

    def tapFriends(self, rect, allyPos, allyPack):
        for pos in allyPos:
            if pos:
                idx = allyPos.index(pos)
                ally = allyPack[idx]
                if rect.colliderect(ally.charRect()):
                    ally.transferEnergy()

    def transferEnergy(self):
        self.disarm = False
        self.getAttacked = False
        self.spd = self.spdAnchor

    def attackEnemy(self, rect, enemyPos, enemyPack):
        for pos in enemyPos:
            if pos:
                idx = enemyPos.index(pos)
                enemy = enemyPack[idx]
                if rect.colliderect(enemy.charRect()):
                    enemy.attacked()

    def charRect(self):
        rect = pg.transform.scale(pg.image.load('data/transparent.png'), (char_scale, char_scale))
        rect = win.blit(rect, (self.x-3, self.y-3))
        return rect

    def attacked(self):
        self.getAttacked = True

    def getRadar(self):
        self.radarObject = pg.image.load('data/transparent.png')
        self.radarObject = win.blit(self.radarObject, (self.x - 10, self.y - 10))
        # self.radarObject = pg.draw.rect(win, (10, 250, 10), (self.x - 10, self.y - 10, 20, 20))
        return self.radarObject

    def radarCheck(self, playerPack, enemyPack):
        self.allies_around = 0
        self.enemies_around = 0
        self.radar = self.getRadar()
        for player in enumerate(playerPack):
            player_radar = player[1].getRadar()
            if self.x != player[1].x and self.y != player[1].y:
                if self.radar.colliderect(player_radar):
                    self.allyPos.pop(player[0])
                    self.allyPos.insert(player[0], (player[1].x, player[1].y))
                    self.allies_around += 1
                else:
                    self.allyPos.pop(player[0])
                    self.allyPos.insert(player[0], (None, None))

        for enemy in enumerate(enemyPack):
            enemy_radar = enemy[1].getRadar()
            if self.radar.colliderect(enemy_radar):
                self.enemyPos.pop(enemy[0])
                self.enemyPos.insert(enemy[0], (enemy[1].x, enemy[1].y))
                self.enemies_around += 1
            else:
                self.enemyPos.pop(enemy[0])
                self.enemyPos.insert(enemy[0], (None, None))

class computerUnit():
    def __init__(self, parent, side, picpack, hitpack, x, y , speed, targetObject):
        self.parent = parent
        self.side = side
        if self.side == 'r':
            self.selfStand = standred
        elif self.side == 'b':
            self.selfStand = standblue
        self.headB, self.headR, self.headT, self.headL = picpack[0],picpack[1],picpack[2],picpack[3]
        self.hitB, self.hitR, self.hitT, self.hitL = hitpack[0],hitpack[1],hitpack[2],hitpack[3]
        self.x = x
        self.y = y
        self.w = char_scale
        self.spd, self.spdAnchor = speed, speed
        self.head = random.choice((0,1,2,3))
        self.hit_motion = None
        self.hit = False
        self.energy_dur = fps*2
        self.t1 = 0
        self.t2 = 0
        self.t3 = 0
        self.endB, self.endR, self.endT, self.endL = False, False, False, False
        self.moveB, self.moveR, self.moveT, self.moveL = True, False, False, False
        self.attacking = False
        self.target = targetObject
        self.allies_around = 0
        self.enemies_around = 0
        global idx1
        if idx1 == 0 or idx1 == 2:
            self.allyPos = [(None,None),(None,None),(None,None),(None,None),(None,None)]
            self.enemyPos = [(None,None),(None,None),(None,None),(None,None),(None,None)]
        else:
            self.allyPos = [(None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None)]
            self.enemyPos = [(None, None)]
        self.getAttacked = False
        self.disarm = False
        self.lastBlit = [[[None],[None],[None]],[[None],[None],[None]]]

    def autom(self):
        if self.head == 2:
            if self.y > self.parent.y + (self.parent.h*0.01):
                self.y -= self.spd
            else:
                self.head = random.choice((0,1,2,3))
        elif self.head == 0:
            if self.y < self.parent.y+self.parent.h-(self.parent.h*0.07):
                self.y += self.spd
            else:
                self.head = random.choice((0,1,2,3))
        elif self.head == 1:
            if self.x < self.parent.x+self.parent.w-(self.parent.w*0.07):
                self.x += self.spd
            else:
                self.head = random.choice((0,1,2,3))
        elif self.head == 3:
            if self.x > self.parent.x + (self.parent.w*0.01):
                self.x -= self.spd
            else:
                self.head = random.choice((0,1,2,3))
        if self.attacking:
            self.hit = True

    def hitStand(self):
        global runGame
        global winner, end
        if self.hit_motion.colliderect(self.bentengA):
            self.energy_dur = 200
            self.t2 = 0
            self.t1 = 0
        elif self.hit_motion.colliderect(self.bentengE):
            if self.t1//int(fps*0.1) == 3:
                runGame = False
                end = True
                if self.side == 'r':
                    winner = 'r'
                elif self.side == 'b':
                    winner = 'b'


    def draw(self):
        global runGame, end
        if runGame:
            self.t2 += 1
            if not self.getAttacked:
                if self.t2%3 == 0:
                    if self.energy_dur <= 10:
                        self.energy_dur = 1
                        self.spd = 0.5
                    elif self.energy_dur > 10:
                        self.spd = self.spdAnchor
                        self.energy_dur -= 1
            else:
                self.disarm = True
                self.energy_dur = 1
                self.spd = 0

            #energy bar
            pg.draw.rect(win, (200, 150, 100),
                         (self.x-int(self.headB.get_rect().size[0]*0.2*(fps/100)),
                          self.y-int(self.headB.get_rect().size[1]*0.5*(fps/100)),
                          (global_scale*0.1*self.energy_dur), global_scale*5))
            if self.side == 'r':
                self.bentengA = standred.surface
                self.bentengE = standblue.surface
            elif self.side == 'b':
                self.bentengA = standblue.surface
                self.bentengE = standred.surface

            if self.getRadar().colliderect(self.bentengA):
                self.hit = True
            elif self.getRadar().colliderect(self.bentengE):
                self.hit = True

            self.autom()

            if self.hit:
                self.t1 += 1
                self.t3 = 0
            else:
                if self.t3 < 10:
                    self.t3 += 1
                    self.radar = self.getRadar()
                    if self.side == 'r':
                        self.head = random.choice((0,1))
                    elif self.side == 'b':
                        self.head = random.choice((2,3))

            if self.head == 0:
                pic = self.headB
                win.blit(self.headB, (self.x,self.y))
                if self.hit and self.t1 < int(fps*0.4):
                    if not self.disarm:
                        hit_fig = self.hitL[self.t1//int(fps*0.1)]
                        hit_x, hit_y = self.x, self.y + 3
                        self.hit_motion = win.blit(self.hitB[self.t1//int(fps*0.1)], (self.x, self.y+3))
                        self.hitStand()
                        if self.side == 'r':
                            self.attackEnemy(self.hit_motion, self.enemyPos, blueTeam)
                            self.tapFriends(self.hit_motion, self.allyPos, redTeam)
                        elif self.side == 'b':
                            self.attackEnemy(self.hit_motion, self.enemyPos, redTeam)
                            self.tapFriends(self.hit_motion, self.allyPos, blueTeam)
                elif self.t1 > 60:
                    self.t1 = 0
                    self.hit = False
            elif self.head == 1:
                pic = self.headR
                win.blit(self.headR, (self.x, self.y))
                if self.hit and self.t1 < int(fps*0.4):
                    if not self.disarm:
                        hit_fig = self.hitR[self.t1//int(fps*0.1)]
                        hit_x, hit_y = self.x+3, self.y
                        self.hit_motion = win.blit(self.hitR[self.t1//int(fps*0.1)], (self.x+3, self.y))
                        self.hitStand()
                        if self.side == 'r':
                            self.attackEnemy(self.hit_motion, self.enemyPos, blueTeam)
                            self.tapFriends(self.hit_motion, self.allyPos, redTeam)
                        elif self.side == 'b':
                            self.attackEnemy(self.hit_motion, self.enemyPos, redTeam)
                            self.tapFriends(self.hit_motion, self.allyPos, blueTeam)
                elif self.t1 > 60:
                    self.t1 = 0
                    self.hit = False
            elif self.head == 2:
                pic = self.headT
                win.blit(self.headT, (self.x, self.y))
                if self.hit and self.t1 < int(fps*0.4):
                    if not self.disarm:
                        hit_fig = self.hitT[self.t1//int(fps*0.1)]
                        hit_x, hit_y = self.x, self.y -3
                        self.hit_motion = win.blit(self.hitT[self.t1//int(fps*0.1)], (self.x, self.y-3))
                        self.hitStand()
                        if self.side == 'r':
                            self.attackEnemy(self.hit_motion, self.enemyPos, blueTeam)
                            self.tapFriends(self.hit_motion, self.allyPos, redTeam)
                        elif self.side == 'b':
                            self.attackEnemy(self.hit_motion, self.enemyPos, redTeam)
                            self.tapFriends(self.hit_motion, self.allyPos, blueTeam)
                elif self.t1 > 60:
                    self.t1 = 0
                    self.hit = False
            elif self.head == 3:
                pic = self.headL
                win.blit(self.headL, (self.x, self.y))
                if self.hit and self.t1 < int(fps*0.4):
                    if not self.disarm:
                        hit_fig = self.hitL[self.t1//int(fps*0.1)]
                        hit_x, hit_y = self.x-3, self.y
                        self.hit_motion = win.blit(self.hitL[self.t1//int(fps*0.1)], (self.x-3, self.y))
                        self.hitStand()
                        if self.side == 'r':
                            self.attackEnemy(self.hit_motion, self.enemyPos, blueTeam)
                            self.tapFriends(self.hit_motion, self.allyPos, redTeam)
                        elif self.side == 'b':
                            self.attackEnemy(self.hit_motion, self.enemyPos, redTeam)
                            self.tapFriends(self.hit_motion, self.allyPos, blueTeam)
                elif self.t1 > 60:
                    self.t1 = 0
                    self.hit = False
            if not runGame:
                if winner == 'b':
                    screen.blit(pg.image.load('data/bluewin.png'), (0,0))
                    #win.blit(base_bluewin, (0,0))
                elif winner == 'r':
                    #win.blit(base_redwin, (0,0))
                    screen.blit(pg.image.load('data/redwin.png'), (0, 0))

    def saveLastBlit(self, pic1, pic1x, pic1y, hitpic, hitpicx, hitpicy):
        self.lastBlit[0][0].pop(0)
        self.lastBlit[0][0].insert(0, pic1)
        self.lastBlit[0][1].pop(0)
        self.lastBlit[0][1].insert(0, pic1x)
        self.lastBlit[0][2].pop(0)
        self.lastBlit[0][2].insert(0, pic1y)
        if not self.hit and not self.disarm:
            self.lastBlit[0][0].pop(0)
            self.lastBlit[1][0].insert(0, hitpic)
            self.lastBlit[1][1].pop(0)
            self.lastBlit[1][1].insert(0, hitpicx)
            self.lastBlit[1][2].pop(0)
            self.lastBlit[1][2].insert(0, hitpicy)

    def tapFriends(self, rect, allyPos, allyPack):
        for pos in allyPos:
            if pos:
                idx = allyPos.index(pos)
                ally = allyPack[idx]
                if rect.colliderect(ally.charRect()):
                    ally.transferEnergy()

    def transferEnergy(self):
        self.spd = self.spdAnchor
        self.disarm = False
        self.getAttacked = False

    def attackEnemy(self, rect, enemyPos, enemyPack):
        for pos in enemyPos:
            if pos:
                idx = enemyPos.index(pos)
                enemy = enemyPack[idx]
                if rect.colliderect(enemy.charRect()):
                    enemy.attacked()

    def charRect(self):
        rect = pg.transform.scale(pg.image.load('data/transparent.png'), (char_scale, char_scale))
        rect = win.blit(rect, (self.x-3, self.y-3))
        return rect

    def attacked(self):
        self.getAttacked = True

    def getRadar(self):
        self.radarObject = pg.image.load('data/transparent.png')
        self.radarObject = win.blit(self.radarObject, (self.x-10, self.y-10))
        #self.radarObject = pg.draw.rect(win, (10, 250, 10), (self.x - 10, self.y - 10, 20, 20))
        return self.radarObject

    def radarCheck(self, playerPack, enemyPack):
        self.allies_around = 0
        self.enemies_around = 0
        self.radar = self.getRadar()
        for player in enumerate(playerPack):
            player_radar = player[1].getRadar()
            if self.x != player[1].x and self.y != player[1].y:
                if self.radar.colliderect(player_radar) :
                    self.allyPos.pop(player[0])
                    self.allyPos.insert(player[0], (player[1].x, player[1].y))
                    self.allies_around += 1
                    if not self.hit:
                        if player[1].disarm:
                            self.hit = True
                else:
                    self.allyPos.pop(player[0])
                    self.allyPos.insert(player[0], (None, None))

        for enemy in enumerate(enemyPack):
            enemy_radar = enemy[1].getRadar()
            if self.radar.colliderect(enemy_radar):
                self.enemyPos.pop(enemy[0])
                self.enemyPos.insert(enemy[0], (enemy[1].x, enemy[1].y))
                self.enemies_around += 1
                self.bravery = random.choice((1,0,0,0,0,0,0,0,0,0))
                if not self.hit:
                    if self.bravery:
                        self.hit = True
                    else:
                        if self.head == 1:
                            self.head = random.choice((0,2,3))
                        elif self.head == 2:
                            self.head = random.choice((0, 1, 3))
                        elif self.head == 3:
                            self.head = random.choice((0, 1, 2))
                        elif self.head == 0:
                            self.head = random.choice((1, 2, 3))
            else:
                self.enemyPos.pop(enemy[0])
                self.enemyPos.insert(enemy[0], (None, None))

class basepic():
    def __init__(self, pic, x, y, stand=False, parentsBg=None):
        self.pic = pic
        self.x = x
        self.y = y
        self.stand = stand
        if self.stand:
            self.rect = self.pic.get_rect()
        self.parent = parentsBg
        self.w = self.pic.get_rect().size[0]
        self.h = self.pic.get_rect().size[1]
        self.surface = win.blit(self.pic, (self.x, self.y))

    def draw(self):
        if self.parent:
            self.surface = win.blit(self.pic, (self.parent.x+self.x, self.parent.y+self.y))
        else:
            self.surface = win.blit(self.pic, (self.x, self.y))

    def getRadar(self):
        self.radarObject = pg.transform.scale(pg.image.load('data/transparent.png'),(int(global_scale*75),int(global_scale*75)))
        self.radarObject = win.blit(self.radarObject, (self.x - 10, self.y - 10))
        return self.radarObject

    def hitArea(self):
        hitArea = pg.transform.scale(pg.image.load('data/transparent.png'), (stand_scale, stand_scale))
        hitArea = win.blit(hitArea, (self.x-(stand_scale/2), self.y-(stand_scale/2)))
        return hitArea

#Insert picture
global_scale = 0.4

char_scale = int(global_scale * 15)
blue_pic = [pg.transform.scale(pg.image.load('data/blue_30x30_self.png'), (char_scale,char_scale)),
            pg.transform.scale(pg.image.load('data/blueR_30x30_self.png'), (char_scale,char_scale)),
            pg.transform.scale(pg.image.load('data/blueB_30x30_self.png'), (char_scale,char_scale)),
            pg.transform.scale(pg.image.load('data/blueL_30x30_self.png'), (char_scale,char_scale))
            ]
blueCPU_pic = [pg.transform.scale(pg.image.load('data/blue_30x30_other.png'), (char_scale,char_scale)),
            pg.transform.scale(pg.image.load('data/blueR_30x30_other.png'), (char_scale,char_scale)),
            pg.transform.scale(pg.image.load('data/blueB_30x30_other.png'), (char_scale,char_scale)),
            pg.transform.scale(pg.image.load('data/blueL_30x30_other.png'), (char_scale,char_scale))
            ]
red_pic = [pg.transform.scale(pg.image.load('data/red_30x30_self.png'), (char_scale,char_scale)),
            pg.transform.scale(pg.image.load('data/redR_30x30_self.png'), (char_scale,char_scale)),
            pg.transform.scale(pg.image.load('data/redB_30x30_self.png'), (char_scale,char_scale)),
            pg.transform.scale(pg.image.load('data/redL_30x30_self.png'), (char_scale,char_scale))
            ]
redCPU_pic = [pg.transform.scale(pg.image.load('data/red_30x30_other.png'), (char_scale,char_scale)),
            pg.transform.scale(pg.image.load('data/redR_30x30_other.png'), (char_scale,char_scale)),
            pg.transform.scale(pg.image.load('data/redB_30x30_other.png'), (char_scale,char_scale)),
            pg.transform.scale(pg.image.load('data/redL_30x30_other.png'), (char_scale,char_scale))
            ]
stand_scale = int(global_scale*20)
standblue_pic = pg.transform.scale(pg.image.load('data/blue_stand20x20.png'), (stand_scale, stand_scale))
standred_pic = pg.transform.scale(pg.image.load('data/red_stand20x20.png'), (stand_scale, stand_scale))

hit_scale = int(global_scale*20)
hit_pic_Unscaled = [[pg.image.load('data/slashB1.png'),pg.image.load('data/slashB2.png'),pg.image.load('data/slashB3.png'),pg.image.load('data/slashB4.png')],
       [pg.image.load('data/slashR1.png'),pg.image.load('data/slashR2.png'),pg.image.load('data/slashR3.png'),pg.image.load('data/slashR4.png')],
       [pg.image.load('data/slashT1.png'),pg.image.load('data/slashT2.png'),pg.image.load('data/slashT3.png'),pg.image.load('data/slashT4.png')],
       [pg.image.load('data/slashL1.png'),pg.image.load('data/slashL2.png'),pg.image.load('data/slashL3.png'),pg.image.load('data/slashL4.png')]]
hit_pic = [[],[],[],[]]
for i in enumerate(hit_pic_Unscaled):
    for ii in i[1]:
        pic = pg.transform.scale(ii,(hit_scale,hit_scale))
        hit_pic[i[0]].append(pic)
base_scale = int(global_scale*300)
baseblue_pic = pg.transform.scale(pg.image.load('data/bg1_300x300.png'), (base_scale*4//3, base_scale*3//3))
base_bluewin = pg.transform.scale(pg.image.load('data/bluewin.png'), (base_scale*4//3, base_scale*3//3))
base_bluewin_hc = pg.transform.scale(pg.image.load('data/bluewin_hc.png'), (base_scale*4//3, base_scale*3//3))
base_redwin = pg.transform.scale(pg.image.load('data/redwin.png'), (base_scale*4//3, base_scale*3//3))
base_redwin_hc = pg.transform.scale(pg.image.load('data/redwin_hc.png'), (base_scale*4//3, base_scale*3//3))
base_menu = [[pg.image.load('data/start/rn1.png'), pg.image.load('data/start/rn2.png'), pg.image.load('data/start/rn3.png')],
             [pg.image.load('data/start/rh1.png'), pg.image.load('data/start/rh2.png'), pg.image.load('data/start/rh3.png')],
             [pg.image.load('data/start/bn1.png'), pg.image.load('data/start/bn2.png'), pg.image.load('data/start/bn3.png')],
             [pg.image.load('data/start/bh1.png'), pg.image.load('data/start/bh2.png'), pg.image.load('data/start/bh3.png')]
             ]
base_loading = [pg.image.load('data/start/load1.png'),pg.image.load('data/start/load2.png'),pg.image.load('data/start/load3.png'),pg.image.load('data/start/load4.png')]
#PG INITIALIZATION
pg.init()
scr_w = 160*6
scr_h = 120*6
screen = pg.display.set_mode((scr_w, scr_h), pg.HWSURFACE & pg.DOUBLEBUF)
caption = pg.display.set_caption('BENTENG!')
sf_w = 160
sf_h = 120
win = pg.Surface((sf_w,sf_h))

pg.mixer.init()
pg.mixer.music.load('data/bentenk2.mp3')
pg.mixer.music.play(-1)

clock = pg.time.Clock()
fps = 60
run = True
runStart = True
runTime = 0
runGame = False
winner = 0
end = False
opening = True
loading = False

def initialize():
    global scr_w, scr_h, screen, caption, sf_w, sf_h, win, clock, fps, run, runStart, runTime, runGame, winner, end, opening, loading
    pg.init()
    scr_w = 160 * 6
    scr_h = 120 * 6
    screen = pg.display.set_mode((scr_w, scr_h), pg.HWSURFACE | pg.DOUBLEBUF)
    caption = pg.display.set_caption('BENTENG!')
    sf_w = 160
    sf_h = 120
    win = pg.Surface((sf_w, sf_h))

    pg.mixer.init()

    pg.mixer.music.load('data/bentenk2.mp3')
    pg.mixer.music.play(-1)

    clock = pg.time.Clock()
    fps = 60
    run = True
    runStart = True
    runTime = 0
    runGame = False
    winner = 0
    end = False
    loading = True

def loadingScreen():
    global runTime, loading, runGame
    runTime += 1
    screen.blit(base_loading[runTime//15], (0,0))
    if runTime > 50:
        loading = False


#OBJECT MAKING
bg1, standred, standblue = 0,0,0
blue,blue1,blue2,blue3,blue4,blueTeam = 0,0,0,0,0,0,
red1,red2,red3,red4,red5,redTeam = 0,0,0,0,0,0

def initializeGame(mode):
    global bg1, standred, standblue, blue,blue1,blue2,blue3,blue4,blueTeam,red1,red2,red3,red4,red5,redTeam, loading
    bg1, standred, standblue = 0, 0, 0
    blue, blue1, blue2, blue3, blue4, blueTeam = 0, 0, 0, 0, 0, 0,
    red1, red2, red3, red4, red5, redTeam = 0, 0, 0, 0, 0, 0
    if runGame:
        bg1 = basepic(baseblue_pic, 0, 0)
        standred = basepic(standred_pic, int(0.03*base_scale), int(0.03*base_scale), stand=True, parentsBg=bg1)
        standblue = basepic(standblue_pic, bg1.x+(0.9*base_scale*1.35), bg1.y+(0.9*base_scale))

        blue = computerUnit(bg1, 'b', blueCPU_pic, hit_pic, int(sf_w*0.6)+5,int(sf_w*0.4)+45,1 , standred)
        blue1 = computerUnit(bg1, 'b', blueCPU_pic, hit_pic, int(sf_w*0.6)+15,int(sf_w*0.4)+35,1, standred)
        blue2 = computerUnit(bg1, 'b', blueCPU_pic, hit_pic, int(sf_w*0.6)+25,int(sf_w*0.4)+25,1, standred)
        blue3 = computerUnit(bg1, 'b', blueCPU_pic, hit_pic, int(sf_w*0.6)+35,int(sf_w*0.4)+15,1, standred)
        blue4 = computerUnit(bg1, 'b', blueCPU_pic, hit_pic, int(sf_w*0.6)+45,int(sf_w*0.4)+5,1, standred)

        red1 = computerUnit(bg1, 'r', redCPU_pic, hit_pic, int(sf_w*0.1)+5,int(sf_w*0.1)+45,1, standblue)
        red2 = computerUnit(bg1, 'r', redCPU_pic, hit_pic, int(sf_w*0.1)+15,int(sf_w*0.1)+35,1, standblue)
        red3 = computerUnit(bg1, 'r', redCPU_pic, hit_pic, int(sf_w*0.1)+25,int(sf_w*0.1)+25,1, standblue)
        red4 = computerUnit(bg1, 'r', redCPU_pic, hit_pic, int(sf_w*0.1)+35,int(sf_w*0.1)+15,1, standblue)
        red5 = computerUnit(bg1, 'r', redCPU_pic, hit_pic, int(sf_w*0.1)+45,int(sf_w*0.1)+5,1, standblue)
        blueTeam = [blue, blue1, blue2, blue3, blue4]
        redTeam = [red1, red2, red3, red4, red5]

        if mode == 0:
            red1 = char(bg1,'r',red_pic,hit_pic,sf_w/2, sf_h/2,1)
            redTeam = [red1, red2, red3, red4, red5]
        elif mode == 1:
            blue1 = computerUnit(bg1, 'b', blueCPU_pic, hit_pic, int(sf_w * 0.2) + 15, int(sf_w * 0.4) + 35, 1, standred)
            blue2 = computerUnit(bg1, 'b', blueCPU_pic, hit_pic, int(sf_w * 0.2) + 25, int(sf_w * 0.4) + 25, 1,standred)
            blue3 = computerUnit(bg1, 'b', blueCPU_pic, hit_pic, int(sf_w * 0.2) + 35, int(sf_w * 0.4) + 15, 1,standred)
            blue4 = computerUnit(bg1, 'b', blueCPU_pic, hit_pic, int(sf_w * 0.2) + 45, int(sf_w * 0.4) + 5, 1, standred)
            red1 = char(bg1,'r',red_pic,hit_pic,sf_w*0.1, sf_h*0.1,1)
            red2 = computerUnit(bg1, 'b', blueCPU_pic, hit_pic, int(sf_w * 0.1) + 15, int(sf_w * 0.1) + 35, 1, standred)
            red3 = computerUnit(bg1, 'b', blueCPU_pic, hit_pic, int(sf_w * 0.1) + 25, int(sf_w * 0.1) + 25, 1, standred)
            red4 = computerUnit(bg1, 'b', blueCPU_pic, hit_pic, int(sf_w * 0.1) + 35, int(sf_w * 0.1) + 15, 1, standred)
            red5 = computerUnit(bg1, 'b', blueCPU_pic, hit_pic, int(sf_w * 0.1) + 45, int(sf_w * 0.1) + 5, 1, standred)
            blueTeam = [blue, blue1, blue2, blue3, blue4,red2, red3, red4, red5]
            redTeam = [red1]
        elif mode == 2:
            blue = char(bg1, 'b', blue_pic, hit_pic, sf_w / 2, sf_h / 2, 1)
            blueTeam = [blue, blue1, blue2, blue3, blue4]
        elif mode == 3:
            blue = char(bg1, 'b', blue_pic, hit_pic, sf_w*0.6, sf_h*0.6, 1)
            blue1 = computerUnit(bg1, 'r', redCPU_pic, hit_pic, int(sf_w * 0.1) + 15, int(sf_w * 0.4) + 35, 1,standblue)
            blue2 = computerUnit(bg1, 'r', redCPU_pic, hit_pic, int(sf_w * 0.1) + 25, int(sf_w * 0.4) + 25, 1,standblue)
            blue3 = computerUnit(bg1, 'r', redCPU_pic, hit_pic, int(sf_w * 0.1) + 35, int(sf_w * 0.4) + 15, 1,standblue)
            blue4 = computerUnit(bg1, 'r', redCPU_pic, hit_pic, int(sf_w * 0.1) + 45, int(sf_w * 0.4) + 5, 1, standblue)
            red1 = computerUnit(bg1, 'r', redCPU_pic, hit_pic, int(sf_w * 0.1) + 5, int(sf_w * 0.1) + 45, 1, standblue)
            red2 = computerUnit(bg1, 'r', redCPU_pic, hit_pic, int(sf_w * 0.1) + 15, int(sf_w * 0.1) + 35, 1, standblue)
            red3 = computerUnit(bg1, 'r', redCPU_pic, hit_pic, int(sf_w * 0.1) + 25, int(sf_w * 0.1) + 25, 1, standblue)
            red4 = computerUnit(bg1, 'r', redCPU_pic, hit_pic, int(sf_w * 0.1) + 35, int(sf_w * 0.1) + 15, 1, standblue)
            red5 = computerUnit(bg1, 'r', redCPU_pic, hit_pic, int(sf_w * 0.1) + 45, int(sf_w * 0.1) + 5, 1, standblue)
            redTeam = [red1, blue1, blue2, blue3, blue4, red2, red3, red4, red5]
            blueTeam = [blue]

    else:
        bg1, standred, standblue = 0,0,0
        blue,blue1,blue2,blue3,blue4,blueTeam = 0,0,0,0,0,0,
        red1,red2,red3,red4,red5,redTeam = 0,0,0,0,0,0

#FUNGSI DRAW SURFACE
#blitted_pic = base_menu[0][0]
play = 0
idx1 = 0
idx2 = 0
def startMenu():
    global play, runGame, runStart, runTime, idx1, idx2, opening, loading
    if opening:
        screen.blit(pg.image.load('data/start/start.png'), (0,0))
        if pg.key.get_pressed()[pg.K_SPACE]:
            opening = False
    else:
        if runStart:
            blitted_pic = base_menu[idx1][idx2]
            screen.blit(blitted_pic, (0,0))
            key = pg.key.get_pressed()
            if runTime%5 == 0:
                if idx1 == 0:
                    if idx2 == 0:
                        if key[pg.K_s]:
                            idx2 = 1
                        if key[pg.K_RETURN]:
                            play = 1
                    elif idx2 == 1:
                        if key[pg.K_w]:
                            idx2 = 0
                        elif key[pg.K_s]:
                            idx2 = 2
                        if key[pg.K_RETURN]:
                            idx1 = 2
                    elif idx2 == 2:
                        if key[pg.K_w]:
                            idx2 = 1
                        if key[pg.K_RETURN]:
                            idx1 = 1
                elif idx1 == 1:
                    if idx2 == 0:
                        if key[pg.K_s]:
                            idx2 = 1
                        if key[pg.K_RETURN]:
                            play = 1
                    elif idx2 == 1:
                        if key[pg.K_w]:
                            idx2 = 0
                        elif key[pg.K_s]:
                            idx2 = 2
                        if key[pg.K_RETURN]:
                            idx1 = 3
                    elif idx2 == 2:
                        if key[pg.K_w]:
                            idx2 = 1
                        if key[pg.K_RETURN]:
                            idx1 = 0
                elif idx1 == 2:
                    if idx2 == 0:
                        if key[pg.K_s]:
                            idx2 = 1
                        if key[pg.K_RETURN]:
                            play = 1
                    elif idx2 == 1:
                        if key[pg.K_w]:
                            idx2 = 0
                        elif key[pg.K_s]:
                            idx2 = 2
                        if key[pg.K_RETURN]:
                            idx1 = 0
                    elif idx2 == 2:
                        if key[pg.K_w]:
                            idx2 = 1
                        if key[pg.K_RETURN]:
                            idx1 = 3
                elif idx1 == 3:
                    if idx2 == 0:
                        if key[pg.K_s]:
                            idx2 = 1
                        if key[pg.K_RETURN]:
                            play = 1
                    elif idx2 == 1:
                        if key[pg.K_w]:
                            idx2 = 0
                        elif key[pg.K_s]:
                            idx2 = 2
                        if key[pg.K_RETURN]:
                            idx1 = 1
                    elif idx2 == 2:
                        if key[pg.K_w]:
                            idx2 = 1
                        if key[pg.K_RETURN]:
                            idx1 = 2
            runTime += 1
            if play:
                blitted_pic = base_menu[idx1][idx2]
                runStart = False
                loading = True
                play, runTime = 0, 0
                runGame = True
                initializeGame(idx1)

def drawAllUnit():
    for unit in blueTeam:
        unit.draw()
    for unit in redTeam:
        unit.draw()

def activateAllRadar():
    for unit in blueTeam:
        unit.radarCheck(blueTeam, redTeam)
    for unit in redTeam:
        unit.radarCheck(redTeam, blueTeam)

def drawWindow():
    global runGame, loading
    if loading:
        loadingScreen()
    else:
        if runGame:
            activateAllRadar()
            pg.draw.rect(win,(10,10,10),(bg1.x-100, bg1.y-100,500,500))
            bg1.draw()
            standred.draw()
            standblue.draw()
            drawAllUnit()
            if not end:
                screen.blit(pg.transform.scale(win, (scr_w, scr_h)), (0, 0))
        else:
            if pg.key.get_pressed()[pg.K_SPACE] and end:
                pg.quit()
                initialize()


while run:
    startMenu()
    clock.tick(fps)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    keys = pg.key.get_pressed()
    drawWindow()
    pg.display.update()

pg.quit()