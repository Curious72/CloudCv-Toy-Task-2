from django.shortcuts import render
from django.http import HttpResponse
import json
import cv2
import os
import numpy as np
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
@csrf_exempt
def opencv(request):
    if request.method=="POST":
        if "datas" in request.POST:
            if request.POST.get("datas") is not None:
                name=request.POST.get("datas")
                stu='/home/coolsduy/new/venv/cloudcv/newapp/static/images/'
                img=cv2.imread(stu+str(name))
                mod=json.loads(request.POST.get("mod"))
                nm=""
                response_data={}
                response_data['url']=[]
                newpath='/home/coolsduy/new/venv/cloudcv/newapp/static/images/'+'folder_'+name
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
                poth='/home/coolsduy/new/venv/cloudcv/newapp/preprocessed/'+name+'/'
                if not os.path.exists(poth):
                    os.makedirs(poth)
                    f=open(poth+"tree.txt","w")
                    f.write("{}")
                    f.close()
        f=open(poth+'tree.txt',"r+")
        diction=eval(f.read())
        ty={"old":diction}
        f.close()
        l=len(mod)
        p=""
        nm=""
        dic=diction
        for i in range(0,l):
            if mod[i] in diction:
                dic=diction[mod[i]][0]
                response_data['url'].append(diction[mod[i]][1])
                diction=dic
            else:
                break
        
        print i
        print "\n"
        if i > 0:    
            nm=nm+response_data['url'][i-1]       
            img=cv2.imread(stu+'folder_'+name+'/'+response_data['url'][i-1]+'.png')
        for j in range(i,l):
            if mod[j] =="Grayscale":
                nm=nm+"0"
                img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                do={}
                dic["Grayscale"]=(do,nm)
                dic=do
            elif mod[j]=="Resize":
                nm=nm+"1"
                img=cv2.resize(img,(0,0),fx=0.5,fy=0.5)
                do={}
                dic["Resize"]=(do,nm)
                dic=do
            elif mod[j] =="GaussianBlur":
                nm=nm+"3"
                img=cv2.blur(img,(5,5))
                do={}
                dic["GaussianBlur"]=(do,nm)
                dic=do
            elif mod[j] =="ConvolutionalFiltering":
                nm=nm+"2"
                print nm
                kernel= np.ones((5,5),np.float32)/25
                img=cv2.filter2D(img,-1,kernel)
                do={}
                dic["ConvolutionalFiltering"]=(do,nm)
                dic=do
            
            
            cv2.imwrite(newpath+'/'+nm+'.png',img)
            response_data['url'].append(nm)
        fp=open(poth+"tree.txt","w")
        fp.write(json.dumps(ty["old"]))
        fp.close()
        return HttpResponse(json.dumps(response_data),content_type="application/json")
    else:
          return render(request,'index.html')

@csrf_exempt
def cloudcv(request):
    if request.method == "POST":
        if "mod" in request.POST:
            if request.POST.get("mod") is not None:
                pipe=request.POST.get("mod")
                pipeline=json.loads(pipe)
                stri=""
                for i in pipeline:
                    if i =="Grayscale":
                        stri=stri+"0"
                    elif i =="Resize":
                        stri=stri+"1"
                    elif i =="ConvolutionalFiltering":
                        stri=stri+"2"
                    elif i =="GaussianBlur":
                        stri=stri+"3"
                filename=open("pipelines/"+stri+"_pipeline.txt",'w')
                filename.write(pipe)
                filename.close()
            return HttpResponse("thank you")
