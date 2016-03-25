current_pipeline=[];
loaded_pipeline=[];
var ptr=1;
var count=1;

var create_pipeline=function(name){
    current_pipeline.push(name);
    div=document.getElementById("pipeline");
    dragg=document.createElement("div");
    dragg.style="float:left;width:auto;height:30px";
    span=document.createElement("span");
    span.className="label label-default";
    text=document.createTextNode(name);
    div.appendChild(dragg);
    dragg.appendChild(span);
    span.appendChild(text);
};

var delete_pipeline = function(){
    current_pipeline=[];
    var myNode= document.getElementById("pipeline");
    while (myNode.firstChild) {
        myNode.removeChild(myNode.firstChild);
    }
};        

var undo = function() {        
    current_pipeline.pop();   
};

var concatenate_pipeline= function(id){
    $('#'+id).click(function(){
        current_pipeline=current_pipeline.concat(loaded_pipeline);
        var iter=0;
        var length =loaded_pipeline.length;
        for(iter=0;iter<length;iter++){
            div=document.getElementById("pipeline");
            dragg=document.createElement("div");
            dragg.style="float:left;width:auto;height:30px";
            span=document.createElement("span");
            span.className="label label-default";
            text=document.createTextNode(loaded_pipeline[t]);
            div.appendChild(dragg);
            dragg.appendChild(span);
            span.appendChild(text);
        }
    });    
};
     
var upload_pipeline = function(event){
    input=event.target;
    var reader = new FileReader();
    reader.onload=function(){
        var text=reader.result;
        loaded_pipeline=JSON.parse(text);
        if (ptr==1) {
            go=document.createElement("input");
            go.type="button";
            go.id="conc"
            go.className="btn btn-primary"
            go.value="Concatenate Pipelines"
            document.getElementById("pipe").appendChild(go);
            ptr=0;
            concatenate_pipeline(go.id);
        }
    }
    reader.readAsText(input.files[0]);
};
            
var save= function(){
    $.ajax({
        url:"savej/",
        type:"POST",
        data:{'pipeline':JSON.stringify(current_pipeline)}
    });
};

var openFile = function(event) {
    input = event.target;
    var reader = new FileReader();
    reader.onload = function(){
        var dataURL = reader.result;
        var output = document.getElementById('output');
        output.src = dataURL;
    };
    reader.readAsDataURL(input.files[0]);
    filename= input.files[0].name; 
};



var rm_image= function(id,id1,id2){    
    $('#'+id).click(function(){
        document.getElementById(id1).remove();
    });
    
    $('#'+id2).click(function(){
        var url=document.getElementById(id2).getAttribute("src");
        document.getElementById('output').setAttribute("src",url);
        var index =url.lastIndexOf("images");
        filename=url.substring(index+7);
    });    
};

var run_pipeline = function(event){
    event.preventDefault();
    $.ajax({
        url:"opencv/",
        type:"POST",
        data:{'pipeline':JSON.stringify(current_pipeline),'filename':filename},
        success:function(json){
            var iter=0;
            var len=json.url.length;
            for(iter=len-1;iter>=0;iter--){ 
                y=document.createElement("div");
                y.style="width:auto;height:auto";
                thumb=document.createElement("div");
                thumb.style="width:auto;height:auto";
                thumb.className="thumbnail" 
                s=count.toString();
                y.setAttribute("id",s);
                ar=document.createElement("a");
                z=document.createElement("img");
                z.setAttribute("src",'static/images/'+'folder_'+filename+'/'+json.url[iter]+'.png');
                z.className="img-responsive";
                ar.className="img-thumbnail";
                lab=document.createElement("div");
                lab.className="caption"
                head=document.createElement("h5");
                text=document.createTextNode((iter+1)+" . "+json.array[iter]);
                head.appendChild(text);
                lab.appendChild(head);
                z.id="c"+s;
                panel=document.createElement("div");
                anchor=document.createElement("a");
                panel.setAttribute("class","panel");
                panel.id="a"+s;
                anchor.id="b"+s;
                anchor.setAttribute("class","close");
                y.className="col-sm-6 col-md-4";
                grid=document.getElementById("grid");
                grid.insertBefore(y,grid.firstChild);
                y.appendChild(panel);
                panel.appendChild(thumb);
                thumb.appendChild(anchor);
                thumb.appendChild(ar);
                thumb.appendChild(lab);
                ar.appendChild(z);
                count=count+1;
                rm_image(anchor.id,y.id,z.id);       
            }
        }
    });
};
