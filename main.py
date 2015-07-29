import tweepy
import time
import re
import sys
import string
from stemming.porter2 import stem
import pickle
from decimal import *
import math
import csv
from math import *

# retrieve the tweets from accounts---------------------------------------------
def getStatus(classes):
                                                                                # fetch account array
    for listitem in classes:
        terms=[]
        print listitem
        accountList=classes[listitem]

        print accountList
        for account in accountList:
                                                                                # limit the tweets to 5 just to try
            result=api.user_timeline(id=account,count=200)
            for status in result:
                print status.text
                text=status.text
                text.encode(encoding='UTF-8',errors='ignore')
                terms.append(text)
            print terms

            print " Done with account %s\n"%account
            print " Enter a waiting for 15 second for twitter limited query PH\n"
            time.sleep(11)
            fp=open(listitem,"w")
        for item in terms:
            try:
                fp.writelines("%s\n" % item.encode('utf-8'))
            except fp.errors as e:
                print "some error"
                continue
        fp.close()

    print "Done"
#-------------------------------------------------------------------------------

# From the tweets seperate all the terms----------------------------------------
def getTerms(classes):
    # clean up the terms and the thing wwe need to take care of for twitter tweets:
    # 1 delete twitter keyword such as RT,..
    # 2 remove links,hashtags form tweets
    # for link this regular expression is fine ((([A-Za-z]{3,9}:(?:\/\/)?)(?:[-;:&=\+\$,\w]+@)?[A-Za-z0-9.-]+|(?:www.|[-;:&=\+\$,\w]+@)[A-Za-z0-9.-]+)((?:\/[\+~%\/.\w-_]*)?\??(?:[-\+=&;%@.\w_]*)#?(?:[\w]*))?)
    # 3 remove stopwords, single characters, periods, commas
    # 4 remove numbers
    # then check and see if we need to add something here

# open up the files and clean up the terms line by line

    for classname in classes:
        fp=open(classname,"r")
        rawtext=fp.read()
        filename=str(classname) +'terms'
        cfp=open(filename,'w')
        terms=[]

        pattern="((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)"
        i=0
        for line in rawtext.split('\n'):

            if line!='':

                                                                                # start cleaing up
                for term in line.split(' '):
                    term=term.lower()

                                                                                #remove any url
                    url=re.search(pattern,term)
                    if not url:
                                                                                # remove metions @username
                        metion=re.search("^@\w+:?$",term)
                        if not metion :
                                                                                #remove hashtags #hashtag
                            hashtag=re.search("^#\w+.?$",term)
                            if not hashtag:
                                                                                #elemineate numbers
                                np=re.search("^\d+",term)
                                if not np:
                                    if term not in stopwords:
                                                                                #terms.append(term)
                                                                                #if term not in ["rt","it's"]:
                                                                                # last thing to trim the puctioations
                                        exclude = set(string.punctuation)
                                        term = ''.join(ch for ch in term if ch not in exclude)
                                        term=''.join(e for e in term if e.isalnum())
                                                                                # one more thing since this a twitter a lot of spelling errors
                                                                                # sytemming using porter
                                        term=stem(term)
                                                                                # ignore single char. and punctionations
                                        if len(term) > 2 and len(term) < 28:
                                            i+=1
                                            cfp.write("%s\n"% term)
        print "Done with catigory " , classname," terms in this class ", i
        cfp.close()

#-------------------------------------------------------------------------------

def buildIndex(classes):
    tr=[]
    tf=[]
    for classname in classes:
        dict1={}
        j=0
        filename=classname+"terms"
        terms=open(filename,"r").read()
        for term in terms.split('\n'):
            j+=1
            if term not in tr:
                tr.append(term)
            if term in dict1:
                count=dict1[term]
                count +=1
                dict1[term]=count
            else:
                count=1
                dict1[term]=count
        tf.append(j)
        print dict1
        pickle.dump(dict1,open(classname+"index","w"))
        print "terms in class" ,j
    print "voc " ,len(tr)
    fp=open("termcount","w")
    for item in tf:
        print>>fp,item

    open("voc","w").write("%s"%len(tr))
#-------------------------------------------------------------------------------

# classify the tweets-----------------------------------------------------------
def tweetClassifier(classes):
##################    Multinomial Naive Bayes Method   #########################
                                                                                # load vocabulary ccount from file voc
    voc=open('voc','r').read()
    tf=[]
    for line in open('termcount','r').read().split('\n'):
        tf.append(line)
    tweet=raw_input("Enter a twitter account to give it a class \n");
    print " Twitter Acoount : %s" % tweet
                                                                                # limit the tweets to 20 for testing
    result=api.user_timeline(id=tweet,count=20)
    tweets=''
    for status in result:
        text=status.text
        text.encode(encoding='UTF-8',errors='ignore')
        tweets+=text
    print "20 Tweets retrived for testing"
    tweettokens=getTerm(tweets)
    proclass={}
    print "#####################################################################"
    print "\t\t\t\t1-Multinomial NB model:"
    print "#####################################################################"
    for classname in classes:
         i=0
                                                                                # load the pickeled index
         indexname=str(classname)+"index"
         dict1=pickle.load( open(indexname, "r" ))

                                                                                 # compute the probability of each term in the test docuemt
                                                                                 # the log(p(c1)) = log(1000/4000) = log(0.25)

         p1=0
         p1+=math.log(0.25,2)
         for term in tweettokens:
            tf=tf[i]
            pp=Decimal(0)

            if term in dict1:
                                                                                # log(count +1) / (|V| + terms count)
                                                                                #print dict1[term]
                count=dict1[term]
                                                                                #  compute the probability of term
                pp=Decimal((float(count)+1)/(float(tf)+float(voc)))
                p1+=math.log(pp,2)

            else:
                pp=Decimal(1/(float(tf)+float(voc)))
                p1+=math.log(pp,2)
         proclass[classname]=p1
         i+=1
         print "The Probablility of class %s is %d"%(classname,p1)
    print proclass
    print "\nThe class of this document is " , max(proclass,key=proclass.get)

################# Multivariate Bernoulli Naive Bayes Method ####################

    voc2=[]

    proclass2={}
    for classname in classes:
         i=0
                                                                                # load the pickeled index
         indexname=str(classname)+"index"
         dict2=pickle.load( open(indexname, "r" ))
         for term in dict2:
            if term not in voc2:
                voc2.append(term)
    for tweet in tweettokens:
        if tweet not in voc2:
            voc2.append(tweet)
    print "\n\n#####################################################################"
    print "\t\t\t\t 2-Multivariate Bernoulli model:"
    print "#####################################################################"
    for classname in classes:
        p2=0
        indexname=str(classname)+"index"
        dict2=pickle.load( open(indexname, "r" ))
        bpp=0
        p2+=math.log(0.25)
        for term in voc2:

            count=0
            if term in dict2:
                count=dict2[term]
            else:
                count=0
            bpp=Decimal((float(count)+1)/1002)
            if term in tweettokens:
                p2+=math.log(bpp)
            else:
                p2+=math.log(1-bpp)

        print "The Probablility of class %s is %d"%(classname,p2)
        proclass2[classname]=p2
    print "\nThe class of this document is " , max(proclass2,key=proclass2.get)

#-------------------------------------------------------------------------------

def getTerm(line):
    terms=[]
    pattern="((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)"
    for term in line.split(' '):
        term=term.lower()

                                                                                #remove any url
        url=re.search(pattern,term)
        if not url:
                                                                                # remove mentions @username
            metion=re.search("^@\w+:?$",term)
            if not metion :
                                                                                #remove hash-tags #hashtag
                hashtag=re.search("^#\w+.?$",term)
                if not hashtag:
                                                                                #eliminate numbers
                    np=re.search("^\d+",term)
                    if not np:
                        if term not in stopwords:
                                                                                #if term not in ["rt","it's"]:
                                                                                # last thing to trim the puctioations
                            exclude = set(string.punctuation)
                            term = ''.join(ch for ch in term if ch not in exclude)

                            term=''.join(e for e in term if e.isalnum())
                                                                                # one more thing since this a twitter a lot of spelling errors

                                                                                # stemming using porter
                            newterm=stem(term)
                                                                                # ignore single char. and punctuation
                            if len(newterm) > 2 and len(newterm) < 28:
                                terms.append(newterm)
    return terms
#-------------------------------------------------------------------------------

if __name__=='__main__':
    consumer_key = 'tsmm09gjp9zn5ZyPy6EznKZnE'
    consumer_secret = 'GUCslpXHUywn8xSV3gCZquHEmOEFZ3JLUU5N5feS2jqU9WJDeY'
    access_token = '2431326895-LUDG61cdiXkASnuTUctys78hSs1WZIItLBF9cGt'
    access_token_secret = 'rNPqhdL1gmIAzcM06cS5BrO22zCJAvM1VP6uHW4l0Rg11'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token,access_token_secret)

    api = tweepy.API(auth)
                                                                                # this array contains the categories and the twitter accounts for each category
                                                                                # testing set
    classes={
    'News':['CNN','FoxNews','nytimes','Reuters','BBCWorld'],
    'Sports':['nba','espn','SportsCenter','realmadriden','FCBarcelona'],
    'Games':['PlayStation','Xbox','NintendoAmerica','Treyarch','EASPORTSFIFA'],
    'Education':['MTSUNews','MITnews','Yale','UCBerkeley','Harvard']}
                                                                                # for test SueCasella has 2284 tweets let's see how much tweets we can retrive
    usr='SueCasella'
    voccount=0
                                                                                # keep trace of the terms count in each class
    classcount=[]
    stopwords=[]

    for word in open("stopwords","r").readlines():
        stopwords.append(word.rstrip('\n'))

                                                                                # for now we can work with the data we already got
                                                                                # we do not need this code nuless for recollect the data
                                                                                # we already collect 200 tweets for each account in each category
                                                                                # so we have 1000 tweets for each category 4*200
                                                                                # and 800 tweets for the 4 categories
                                                                                #getStatus(classes)
                                                                                # the terms are ready in the files we did all the elimination so we can start build the naive classifier


    #getTerms(classes)                                                          # retrieves the tweets from the listed accounts
    #buildIndex(classes)                                                        # creates indexes of the tweets
    #computePro(classes)                                                        # compute the probability values for the tweets in the given documents
    tweetClassifier(classes)                                                    # tweet classifier.. it consists of Multinomial NB and Bernoulli NB Models
