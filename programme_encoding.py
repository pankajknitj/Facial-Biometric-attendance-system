#made by pankaj kumar and ashok bishnoi

#instructions!
''' 1.press c to start attendance initialy.
     2.see face in frame if proper than press c again to save image
     3.take 5-6 image of each student to achieve accuracy
     4.need to creat new file
     5.must check the path of file given if not proper change it accordingly'''

import face_recognition as fc
import cv2 as cv
import pandas as pd
import numpy as np
v=cv.VideoCapture(0)
k=ord(input('enter c for start caputring image'))                                #to start the attendance press c

j=0     #to increase the label of atudent name

t=True
T=True          #clearify below
try:
    f=pd.read_csv(r'C:\Users\dell\AppData\Local\Programs\Python\Python36\encoded_image_dataset.csv')
    l=f['labels']
    l=np.array(l)
    j=l[-1]+1                                                                   #thease all thing to done for take data of student who left in 1st round
    print(j)
except:
    print('file is not available')
if k==ord('c'):
    print('press c to capture the image of student')
    while 1:
        state,image=v.read()
        if state==True: 
            fl=fc.face_locations(image)
            if len(fl)>0:
                for [x1,y1,x2,y2] in fl:
                    cv.rectangle(image,(y2,x1),(y1,x2),(0,0,255),3)   
                if k==ord('c'):
                    encoded_data=[]                                             #compare the live image of student with encoded data
                    label=[]
                    e1=fc.face_encodings(image,fl)[0]
                    encoded_data.append(e1)
                    label.append(j)
                    encoded=pd.DataFrame(encoded_data)
                    encoded['labels']=label                                     #label is append into list for creating dataframe
                    if j==0 and t==True:                                        #t is tacken to avoied 1st student image to overwrite
                        t=False
                        encoded.to_csv('encoded_image_dataset.csv')             #when database is not available means when start tacking image of student on 1st day it will it will creat new file with all header
                        
                    else:
                        encoded.to_csv(r'C:\Users\dell\AppData\Local\Programs\Python\Python36\encoded_image_dataset.csv',mode='a',header=False)  #append the value in data frame without header
                        
                    print('image saved successfully')
        cv.imshow('image',image)
        if k==ord('e'):                                                         #press e to register the name and email of student
            name=[]
            email=[]
            nam=input('enter the student name')
            eml=input('enter the email of student')
            name.append(nam)
            email.append(eml)
            name_email=pd.DataFrame({'name':name,'emails':email})
            if j==0 and T==True:
                T=False                                                         #same as above
                name_email.to_csv('name_email_dataset.csv')
               
            else:
                 name_email.to_csv(r'C:\Users\dell\AppData\Local\Programs\Python\Python36\name_email_dataset.csv',mode='a',header=False)
            j+=1
            
        if k==ord('q'):
            cv.destroyAllWindows()
            break
            
        k=cv.waitKey(5)

