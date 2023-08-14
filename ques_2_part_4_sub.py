# -*- coding: utf-8 -*-
"""ques_2_part_4_sub.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nrPUt4J2YIUsaNirpLC2GeagudfU2v6A
"""

#used to work with arrays
import numpy as np
#used to import dataset
import pandas as pd
# used for plotting the dataset
import matplotlib.pyplot as plt
#used for largest value 
import sys
#used for random values
import random
#for doing inverse  of matrices
from numpy.linalg import inv


# dataset upload and using that url I will make a pandas frame
url="https://drive.google.com/file/d/1tRj3p8LM7sevfZbEyC3xK538gD2g2k8a/view?usp=sharing"
url='https://drive.google.com/uc?id=' + url.split('/')[-2]
# test dataset upload and using that url I will make a pandas frame
url_test="https://drive.google.com/file/d/1ee0owgOv_BbS1GEv2gLmyJej_NWlnJ2I/view?usp=sharing"
url_test='https://drive.google.com/uc?id=' + url_test.split('/')[-2]


#storing the feature names of the dataset
name=[]
for i in range (1,101):
  name.append("X"+str(i))
name.append("y")


#used the dataset url to import dataset
dataframe=pd.read_csv(url,names=name)
n=dataframe.shape[0]
one_array=np.ones(n,dtype=int)
dataframe.insert(0,'X0',one_array)
X=dataframe.iloc[:,:-1].T
y=dataframe.iloc[:,-1]
X=np.array(X,float)
#X dataframe has 2 features and 1000 data frames. “n”  is the number of data points and number of features are stored in “number_of_features”
n=len(X[0])
number_of_features=len(X)

# initialization of the parameter array
w=[]
for i in range(101):
  w.append(0)
w=np.array(w,float)


# TEst dataset load into dataframe and creating X_TEST and Y_TEST
dataframe_test=pd.read_csv(url_test,names=name)
n_TEST=dataframe_test.shape[0]
one_array=np.ones(n_TEST,dtype=int)
dataframe_test.insert(0,'X0',one_array)
X_TEST=dataframe_test.iloc[:,:-1].T
Y_TEST=dataframe_test.iloc[:,-1]
X_TEST=np.array(X_TEST,float)


# finding the parameter with closed form
XX_T=np.matmul(X,X.T)
a=np.matmul(inv(XX_T),X)
W_ml=np.matmul(a,y)

# error function
def error(X,y,w):
  return np.linalg.norm(np.matmul(X.T,w)-y)**2


def gradient_descent(X,y,w,max_iter,lambda_):
  W_array=[]
  steps=[]
  step=1
  steps.append(step)
  W_array.append(w)
  XX_T=np.matmul(X,X.T)
  for i in range(max_iter):
    # learning rate
    learning_rate = 1/step
    # gradient step
    gradient=2*np.matmul((XX_T),w)-2*np.matmul(X,y) + 2*lambda_*w
    gradient_norm = gradient /np.linalg.norm(gradient)
    # parameter updation step
    next=w-learning_rate*gradient_norm
    w=next
    W_array.append(w)
    step=step+1
    steps.append(step)

  return w,W_array,steps


# shuffling the train dataset and creating train and test data from it , we are training on the train set and doing cross validation on the test dataset
shuffled = dataframe.sample(frac=1).reset_index(drop = True)
X_shuffled=shuffled.iloc[:,:-1].T
y_shuffled=shuffled.iloc[:,-1]
X_shuffled=np.array(X_shuffled, float)
y_shuffled=np.array(y_shuffled, float)
train_X=X_shuffled[:,:8000]
test_X=X_shuffled[:,8000:]
train_y=y_shuffled[:8000]
test_y= y_shuffled[8000:]


# cross validation
def cross_validate(dataframe,max_iter):
  lambda_range=[]
  count=0
  for i in range(1000):
    lambda_range.append(count)
    count+=0.02


  error_list=[]
  # for different lambda value I am running gradient descent, with the parameter obtained I am testing the test part of training dataset
  for lambda_ in lambda_range:
      w=[]
      for i in range(101):
        w.append(0)
      w=np.array(w,float)
      # gradient descent step
      w,W_array,steps=gradient_descent(train_X,train_y,w,max_iter,lambda_)
      # storing error after running on the test part of the train dataset
      err=error(test_X,test_y,w)
      error_list.append(err)
  # plotting the figure
  plt.figure(figsize=(8,8))
  plt.plot(lambda_range,error_list)
  plt.title("Error vs lambda value")
  plt.xlabel("lambda value")
  plt.ylabel("error")
  plt.show()
  return lambda_range[error_list.index(min(error_list))]



# 1000 is the max number of times the gradient descent runs
max_iter=1000
lambda_best=cross_validate(dataframe,max_iter)



# doing the  gradient descent with the best lambda obtained
w=[]
for i in range(101):
  w.append(0)
w=np.array(w,float)
Wr,Wr_array,steps=gradient_descent(train_X,train_y,w,max_iter,lambda_best)



#print the error with newly got Wr
print("new Wr error")
print(error(X_TEST,Y_TEST,Wr))


#print the error with W_ml
print("analytical error")
error(X_TEST,Y_TEST,W_ml)
print(lambda_best)

lambda_best