#made by pankaj kumar and ashok bishnoi

#details!
'''take attendance of every period and send mai to absent student'''

import cv2 as cv
import numpy as np
import face_recognition as fc
import pandas as pd
from datetime import date
import time as t
import smtplib
att_sheet=pd.read_csv(r'C:\Users\dell\AppData\Local\Programs\Python\Python36\name_email_dataset.csv')           #read attendance sheet  (name_email_dataset).
encoded_sheet=pd.read_csv(r'C:\Users\dell\AppData\Local\Programs\Python\Python36\encoded_image_dataset.csv')    #read encoded data set 
del(att_sheet['Unnamed: 0'])                                    #when att_sheet save again it creat a new indexing so the first indexing must be deleted
name=att_sheet['name']
emails=att_sheet['emails']
condition=True
encoded_data=np.array(encoded_sheet)
en_data=list(encoded_data[:,1:129])
label=encoded_data[:,129]                                       #data goes to their corresponding variable
v=cv.VideoCapture(0)
period=1
while True:
    time=t.ctime()
    time=time.split(' ')
    time=time[3]
    time=time.split(':')                                        #time taken in hour and minute by spliting and converting it in integer
    for i in [0,1,2]:
        time[i]=int(time[i])
    hour=time[0]
    minute=time[1]
    if hour>=10 and hour<16 and minute<=5 and hour!=13:        #will take attendance for each period,allowed time 5 minute.
        
        print('attendence is going on')
        if condition==True:
            global attendance
            attendence=np.zeros((1,len(name)))
            condition=False
        date=date.today()
        status,image=v.read()
        if status==True:
            fL=fc.face_locations(image)
            if(len(fL)>0):
                for [x1,y1,x2,y2] in fL:
                    
                    cv.rectangle(image,(y2,x1),(y1,x2),(255,255,255),5)
                    E=fc.face_encodings(image,fL)[0]
                    res=fc.compare_faces(en_data,E)
                    if True in res:
                        font=cv.FONT_HERSHEY_SIMPLEX                                        #FRame and name on image 
                        text=name[int(label[res.index(True)])]
                        cv.putText(image,text,(y2,x1),font,0.8,(0,255,0),2,cv.LINE_AA)
                        cv.imshow('my image',image)
                        cv.waitKey(3)
                        attendence[0,int(label[res.index(True)])]=1
                        att_sheet[str(date)+'-'+str(period)]=attendence[0]                      #attendance 0 becos it a 2d matrix so taken 1st row
                        att_sheet.to_csv(r'C:\Users\dell\AppData\Local\Programs\Python\Python36\name_email_dataset.csv')
                    else:
                        print('false')


    if hour>=10 and hour<16 and minute==6:                   #at 6th minute mail send to thair parents     
            
            
            cv.destroyAllWindows()
            sender_mail=['abcd@gmail.com','******']
            s=smtplib.SMTP('smtp.gmail.com',587)
            s.starttls()
            s.login(sender_mail[0],sender_mail[1])
            for i in range(len(emails)):
                if attendence[0,i]==0:
                    message='your pari/para is absent in period '+str(period)           #message if str with that period in which student absent
                    s.sendmail(sender_mail[0],emails[i],message)
                
            s.quit()
            t.sleep(60)
            print('attendance done')
            period+=1
        
    
    



    
