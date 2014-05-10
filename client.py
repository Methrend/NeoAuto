######################################################
################NeoAuto BETA - Darkbyte##########
######################################################
############Open Source Neopets Automation############
######################################################


#Neobot is a tool created to play neopets for you. It does this by simulating data real games
#Or webpages send to the server , tricking neopets into thinking we are a legit user

#All this uses one principle
#Get Data - > Do some new event based on this data - >  Get Event result and store it


#Credits:
#Darkbyte - Main Code
#Infamous Joe - Work on altador plot chart finder (bot uses cks chart finder)
#Zach - Work on altador plot chart finder(bot uses cks chart finder)
######################################################Imports######################################################
import urllib2, re
from cookielib import CookieJar
from urllib import urlencode
import urllib
import threading
import sys
import time
import random
import ConfigParser
from classes.InventoryManager import InventoryManager
from pyamf.remoting.client import RemotingService #Pyamf class used for amf request (slightly edited)
from classes.NeoAccount import NeoAccount
from classes.settings import settings
from classes.dailys import dailys
from classes.habi import habi
from classes.mobileservices import mobileservices
from classes.nomobileservices import nomobileservices
from classes.hotel import hotel
from classes.battle import battle




from classes.shopmanager import shopmanager


from classes.altadorauto import altador
from classes.bankmanager import bankmanager
from classes.autotrainer import autotrainer
from classes.avatar import avatar
from classes.gamerunner  import gamerunner
from classes.habi import habi
#from classes.nq2 import nq2
######################################################End Imports##################################################
config1 = ConfigParser.RawConfigParser()
strcookie= []
CJ=CookieJar() #Cookies
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(CJ))

Dodebugmode = 1
neouser = "" #Neopets username
neopass = "" #Neopets password
neopin = "" #Neopets pin number (if used , leave as "" if not used)
proxy = "" #localhost:8888 or 123.123.123.123:8080 ect - "" for none

if neouser == "":
    #Todo add a user input option here if neouser not set
    print 'Username not set , exiting in 10 seconds...'
    time.sleep(10)
    sys.exit()


if neopass == "":
    #Todo add a user input option here if neopass not set
    print 'Username not set , exiting in 10 seconds...'
    time.sleep(10)
    sys.exit()


pyamfhandler = RemotingService('http://habitarium.neopets.com/amfphp/gateway.php')


def dologin(debugmode=1): #Debug mode is optional and set to 1 by default



    if proxy == "": #No proxy
        theacc = NeoAccount(neouser,neopass,neopin)
    else: #if proxy is anything but "" , use it

        theacc = NeoAccount(neouser,neopass,neopin,proxy)


    login_return = theacc.login() #Login here
    if login_return[0] == False: #Bad login
        print 'Login Failed - ' + login_return[1] + ' Closing myself in 10 seconds'
        time.sleep(10)
        sys.exit()
    else:
        print "Logged in as - " + theacc.user
    #Check result was valid:

    return theacc


acc = dologin(Dodebugmode) #Do login trys to login and returns a new instance of NeoAccount



settingsmanager = settings(acc.user) #Load settings for this account , store data/class in sessionmanager
habihander = habi(acc,pyamfhandler,proxy,settingsmanager) #Setup habi hander module

depositfile =  settingsmanager.getvalue("Settings","depositlist") #Deposit list items
doaltador =settingsmanager.getvalue("misc","altador_on") #Altador on off switch
inventorymanager = InventoryManager(acc,depositfile,settingsmanager)
shopmanager = shopmanager (acc,settingsmanager)
lastlogintime = time.time()


#nq2handler= nq2(acc,settingsmanager)

dailyshander =  dailys(acc,settingsmanager) #Setup dailys hander module
mobilehandler = mobileservices (acc,settingsmanager) #Mobile services , uses a seperate login to main neo
if not mobilehandler.usemobileservices == 'on': #mobile handler = off , so sets our bot to replace mobilehandler with nomobilehandler
    mobilehandler = nomobileservices (acc,settingsmanager) #Mobile services , uses a seperate login to main neo

battlemanager = battle(acc,mobilehandler,settingsmanager)

hotelmanager =  hotel(acc,settingsmanager,mobilehandler) #Lol hotelmanager i made a funny...... I'll see myself out
bankhandler = bankmanager(acc,mobilehandler,settingsmanager)
althandler = altador(acc,settingsmanager,bankhandler)
gamerunnerhandler =  gamerunner(acc,settingsmanager,mobilehandler) #Setup dailys hander module
avatarhandler = avatar(acc,settingsmanager,mobilehandler)
traininghandler =autotrainer(acc,mobilehandler,settingsmanager,inventorymanager)

#bankhandler.checknpbalance() #Check we have enough np on hand once before run


test = 1
while test ==1:


   # battlemanager.dotick()
   # time.sleep(10)
  #  continue
#

    try:




        if battlemanager.battle_on == 'on':
            if (time.time() - float(battlemanager.lastbattletime) > 86400): #Auto Battle check everyday (time only updates when we stope earning prizes)
                battlemanager.dotick()
                print 'Battle manager'
                continue #Done something so exit

            #We did nothing if this runs.. so check for punchbag bob and process it if needed
            if battlemanager.punchbag_on == 'on':
                #Check is needed by the user
                battlemanager.startpunchbag()





        if hotelmanager.autohotel_on == 'on':
            if (time.time() - float(hotelmanager.lasthoteltime) > 86400): #Auto hotel check every day
                hotelmanager.dotick()
                continue #Done something so exit



        if inventorymanager.invenotrymanageron == 'on':
            if (time.time() - float(inventorymanager.lastsdbticktime) > 900): #Invenotry manager check every half hour
                inventorymanager.Depositall()

                continue #Done something so exit


        if shopmanager.withdrawtill == 'on':
            if (time.time() - float(shopmanager.lasttilltime) > 300): #till check every 5 mins
                shopmanager.checktill()
                continue #Done something so exit


        if shopmanager.withdrawtill == 'on':
            if (time.time() - float(shopmanager.lasttilltime) > 300): #till check every 5 mins
                shopmanager.checktill()
                continue #Done something so exit
        if shopmanager.autoprice_on == 'on':
            if (time.time() - float(shopmanager.lastpricetime) > 900): #price items every half hour
                shopmanager.priceitems()
                continue #Done something so exit


        if avatarhandler.avataron == 'on':
            if (time.time() - float(avatarhandler.lastavatartime) > 300): #grab a avatar every 5 mins
                avatarhandler.getavatar()

                continue #Done something so exit


        if doaltador == 'on':
            if althandler.DoTick() == 999:#Done if 999
                doaltador ='off'

        gamerunnerhandler.rungames()


        if dailyshander.DoTick(mobilehandler) == 0:# Nothing was done

               if habihander.habi_on == 'on':
                   habihander.DoLoop()
                   time.sleep(30)

    except:
        time.sleep(10)
        continue
#