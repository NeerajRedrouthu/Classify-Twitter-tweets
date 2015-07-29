# Classify-Twitter-tweets
It was a group project in Information Retrieval class. We chose a classification problem and used twitter tweets as  our data. Our objective was to take the top 20 tweets of any account, perform text classification using the 2 models  we have discussed in class, and classify the account type.

*You'll need steming and tweepy python libraries for the code to work*

A Probabilistic approach to classify Twitter tweets.	

Introduction:		
In this project worked with text classification thought to us in this course, we implemented it on the twitter tweets (which is our data) to identify theirs category. Ex: Sports, Education, Games, News.

Aim:	
The aim of this project was to create a Naïve Bayes and a Bernoulli model that can classify the text in the tweets and categorize them to their appropriate class labels.

Approach: 
We build Naïve Bayes multinomial model and multivariate Bernoulli Naïve Bayes model to classify the tweets and then show the results of each model.

Code for the Tweet Classifier:
Multinomial NB Model:
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


Bernoulli NB Model:
voc2=[]
    proclass2={}
    for classname in classes:
         i=0
                                                                                
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

OUTPUT:
Twitter Account : CNN
20 Tweets retrieved for testing
#####################################################################
				1-Multinomial NB model:
#####################################################################
The Probability of class News is -1274
The Probability of class Education is -1340
The Probability of class Games is -1325
The Probability of class Sports is -1338
{'News': -1274.2633810759435, 'Education': -1340.5994634296785, 'Games': -1325.1717594832135, 'Sports': -1338.3201848431222}
The class of this document is News
#####################################################################
				 2-Multivariate Bernoulli model:
#####################################################################
The Probablility of class News is -606
The Probablility of class Education is -642
The Probablility of class Games is -637
The Probablility of class Sports is -647
The class of this document is News

Conclusion:
Both the models worked really well and predicted the class of the given test twitter account correctly.

Group Members:
Neeraj Redrouthu and Mohammed Alessa.
