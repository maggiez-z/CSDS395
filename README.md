# CSDS395
# Case Western Reserve University
#Sentify

Margaret Butterfield

Yash Goswami

Christine Pan

Stamatis Papadopoulos

Alexander Rambasek

Andrei Tiu

William Turner


# Background 
## Introduction
As more vaccines are administered and pandemic restrictions are beginning to loosen, people across the country are once again looking for the best dining options. Most people who consult popular restaurant review sites like Yelp and FourSquare are usually only there to look at the number of stars out of five and skim the first couple reviews towards the top of the list. Nobody has time to meticulously page through hundreds of reviews to make an informed decision about where to dine out. As a result, the vast mountain of data presented to the user is, in its current state, useless. This is where our project, Sentify, comes in.

Sentify (a combination of “sentiment” and “identify”) is a web application that aims to enhance the dining experience by extracting valuable information from user reviews and presenting it in an intuitive way. Specifically, Sentify leverages current advancements in natural language processing to extract key aspects and sentiments from user reviews. This is done by using the Bidirectional Encoder Representations from Transformers (BERT) language model developed by Google. Once the key aspects and sentiments are extracted, Sentify can use this information to score the individual qualities of the restaurant (e.g. food, atmosphere, service). Users are able to search for restaurants nearby and view these statistics generated by Sentify. Furthermore, users can explicitly filter for restaurants based on aspects they care about.

## Machine Learning Model
The machine learning model that is used for this project is Google’s BERT, as mentioned in the introduction. BERT is a state-of-the-art model in the subfield of natural language processing, and it has been successfully applied to tasks such as natural language generation and next-sentence prediction. BERT is a transformer-based model, which means that it utilizes what is known as attention. Attention mechanisms help the model learn which parts of the data are most useful for the task and subsequently construct feature representations that are more suited towards the learning task. BERT was trained on the entire English Wikipedia corpus.

In this project, we adapt BERT for a task known as Aspect-Based Sentiment Analysis (ABSA). BERT is chosen as the model framework for this project because its bidirectional structure allows it to use contextual information from surrounding words, something that is lost in a bag-of-words approach. This NLP task is an amalgamation of Named Entity Recognition (locate and classify named entities in text) and Sentiment Analysis (identify the sentiment/polarity associated with text). We have decided to combine both tasks into one to train BERT with. This task can be formalized as a multi-label classification task, with class labels {positive, negative, neutral, conflicted, none}. A conflicted sentiment is when both positive and negative sentiments are expressed in relation to the same topic. “Neutral” means that there was no polarity concerning the topic, and “none” means that the topic did not appear. The input to the model is the tokenized review text, and the model has an attention module for every aspect that is cared about (e.g., food, price, ambience, customer service). For instance, the input “It took a while for our food to arrive, but it was well worth the wait” is expected to result in {“food:” positive, “price:” none, “ambience:” none, “customer service:” negative}.

A number of papers applying BERT to ABSA exist, and this is where we are sourcing a lot of information about the specifics of the model. As shown in [1], BERT has been very successful when applied to this type of task, and this paper provides the main inspiration for our implementation of the model. A number of variations on BERT exist for this task that we hope to also incorporate. For instance, [2] describes a method for boosting the performance of BERT by post-training the model on domain-specific corpuses. Also, [3] describes an adversarial training methodology, attempting to fool BERT by presenting it with deceptive input.

The dataset that we are using to train BERT is adapted from the International Workshop on Semantic Evaluation (Sem-Eval 2014). Examples consist of short snippets of restaurant review text, accompanied by tags corresponding to aspect content and corresponding semantics. Since the dataset is unbalanced with respect to class labelings, we may amend the dataset with some of our own hand-labeled examples.

## API Calls Using AWS Lambda
Using the trained BERT model, the next part of the project is analyzing actual restaurant reviews. We have chosen to limit our scope to the Cleveland area to offer a dense array of options for our users. Using the Scale SERP API we are going to make 125 API calls a day (number of calls is limited by the API itself) to receive restaurant names and their reviews. Each of these reviews will then go through sentiment analysis to determine the positivity of our selected attributes. The information along with the original review will then be stored in a database. To run this processing and data collection, we are using Amazon Web Services Lambda tool, which is a serverless compute tool that lets users run code without provisioning resources. Lambda has the ability to make hundreds of API calls in seconds and then has a direct pipeline to our database tool. 

# Progress
Per our last report, our project should have reached a couple of milestones. We had set two personal goals, both of which are to be completed by the time this report is written. 

The first deadline we gave ourselves was to have the frontend functionality completed by October 25th. 

The second milestone to reach was to have all sentiment analysis functions finished by October 30th. 


# Future Completion Plan

| Event                                     | Date          |
| ------------------------------------------| --------------|
| Progress Report 2                         | November 1st  |
| Working Prototype with Sentiment Analysis | November 10th |
| Frontend Aesthetics Completed             | November 15th |
| Testing and Bug Fixing                    | November 20th |
| Details and Modeling of Performance       | November 27th |
| Final Project & Final Report              | December 1st  |
| Final Project Oral Presentation           | December 10th |

# Updated Management Plan

# Completed Work
Website is deployed using Elastic Beanstalk with setup HTML in place. Is load-balanced and scalable.
Lambda is set up to start automating API calls once code is finished. 
DynamoDB is set up and ready to store data.
S3 bucket is set up and ready to store data. 
BERT model plan is completed and ready to be trained.

# Member Contributions
Margaret:


Yash:


Christine:
* Set up Project Report 2
* Filled in sections of Project Report 2


Stamatis:


Alexander:


Andrei:


William:

