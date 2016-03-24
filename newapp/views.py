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
        if "filename" in request.POST:
            if request.POST.get("filename") is not None:
                name=request.POST.get("filename")
                stu='/home/coolsduy/new/venv/cloudcv/newapp/static/images/'
                img=cv2.imread(stu+str(name))
                pipeline=json.loads(request.POST.get("pipeline"))
                output_image_name=""
                response_data={}
                response_data['url']=[]
                response_data['array']=pipeline
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
        read_dict=eval(f.read())
        cache={"old":read_dict}
        f.close()
        l=len(pipeline)
        
        current_dict=read_dict
        flag=0
        for i in range(0,l):
            if pipeline[i] in read_dict:
                current_dict=read_dict[pipeline[i]][0]
                response_data['url'].append(read_dict[pipeline[i]][1])
                read_dict=current_dict
            else:
                flag=1
                break
        
        
        
            
        if flag == 0:
            i=l
            
        if i > 0:
            output_image_name=output_image_name+response_data['url'][i-1]
            img=cv2.imread(stu+'folder_'+name+'/'+response_data['url'][i-1]+'.png')
        for j in range(i,l):
            if pipeline[j] =="Grayscale":
                output_image_name=output_image_name+"0"
                img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                empty_dict={}
                current_dict["Grayscale"]=(empty_dict,output_image_name)
                current_dict=empty_dict
            elif pipeline[j]=="CannyEdge":
                output_image_name=output_image_name+"1"
                img=cv2.Canny(img,100,200)
                empty_dict={}
                current_dict["CannyEdge"]=(empty_dict,output_image_name)
                current_dict=empty_dict
            elif pipeline[j] =="GaussianBlur":
                output_image_name=output_image_name+"3"
                img=cv2.blur(img,(5,5))
                empty_dict={}
                current_dict["GaussianBlur"]=(empty_dict,output_image_name)
                current_dict=empty_dict
            elif pipeline[j] =="ConvolutionalFiltering":
                output_image_name=output_image_name+"2"
                kernel= np.ones((5,5),np.float32)/25
                img=cv2.filter2D(img,-1,kernel)
                empty_dict={}
                current_dict["ConvolutionalFiltering"]=(empty_dict,output_image_name)
                current_dict=empty_dict
            
            
            cv2.imwrite(newpath+'/'+output_image_name+'.png',img)
            response_data['url'].append(output_image_name);
        fp=open(poth+"tree.txt","w")
        fp.write(json.dumps(cache["old"]))
        fp.close()
        return HttpResponse(json.dumps(response_data),content_type="application/json")
    else:
          return render(request,'index.html')

@csrf_exempt
def cloudcv(request):
    if request.method == "POST":
        if "pipeline" in request.POST:
            if request.POST.get("pipeline") is not None:
                pipe=request.POST.get("pipeline")
                pipeline=json.loads(pipe)
                stri=""
                for i in pipeline:
                    if i =="Grayscale":
                        stri=stri+"0"
                    elif i =="CannyEdge":
                        stri=stri+"1"
                    elif i =="ConvolutionalFiltering":
                        stri=stri+"2"
                    elif i =="GaussianBlur":
                        stri=stri+"3"
                filename=open("pipelines/"+stri+"_pipeline.txt",'w')
                filename.write(pipe)
                filename.close()
            return HttpResponse("thank you")
