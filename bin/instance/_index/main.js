// `data` is global variable. see data.js

const gentd_tag = function(_taglist){ // e.g. ["hoge","fuga"]
    let td1=document.createElement('td');
    if(_taglist){
        for(let i=0;i<_taglist.length;i++){
            let span1=document.createElement('span');
            span1.setAttribute('class','tag');
            span1.innerHTML = _taglist[i];
            td1.appendChild(span1);
        }
    }
    return td1.outerHTML;
}

// return id set of row which contains specified tags.
const getIdlistByTagnames = function(_taglist){ // e.g. ["hoge","fuga"]
    let idlist = []
    for(let i=0;i<data.length;i++){
        flag = false;
        if("tags" in data[i]){
            for(var j=0;j<data[i]["tags"].length;j++){
                if(_taglist.indexOf(data[i]["tags"][j]) > -1){flag = true;}
            }
            if(flag){idlist.push(i);}
        }
    }
    return idlist;
}

// show only selected rows
const showByIdlist = function(_idlist){ // e.g. [0,3,4]
    for(var i=0;i<data.length;i++){
        if(_idlist.indexOf(i) > -1){ // i in _idlist returns different things.
            document.getElementById(String(i)).style.display = "table-row";
            //console.log(String(i)+": show "+String(_idlist.indexOf(i)));
        }else{
            document.getElementById(String(i)).style.display = "none";
            //console.log(String(i)+": hidden "+String(_idlist.indexOf(i)));
        }
    }
    return _idlist
}

// just a reversed function of showByIdlist
const hideByIdlist = function(_idlist){ // e.g. [0,3,4]
    for(var i=0;i<data.length;i++){
        if(_idlist.indexOf(i) > -1){
            document.getElementById(String(i)).style.display = "none";
        }else{
            document.getElementById(String(i)).style.display = "table-row";
        }
    }
    return _idlist
}

// enable tag click on tags in the table
const enableTagClick = function(){
    tags = document.getElementsByClassName("tag");
    for(var i=0;i<tags.length; i++){
        tags[i].onclick = function(){
            //console.log(this);
            showByIdlist(getIdlistByTagnames([this.textContent]));
            return false;
        }
    }
}

// add special tag button (redundant but easy to read)
const addSpecialTagButton = function(){
    let p = document.getElementById("special_tags");
    let span1=document.createElement('span');
    span1.setAttribute('class','tag');
    span1.innerHTML = "show all";
    span1.onclick = function(){
        hideByIdlist([]);
        return false;
    }
    p.appendChild(span1);
    let span2=document.createElement('span');
    span2.setAttribute('class','tag');
    span2.innerHTML = "show all except * tags";
    span2.onclick = function(){
        hideByIdlist(getIdlistByTagnames(["*archived","*abandoned","*wanna"]));
        return false;
    }
    p.appendChild(span2);
    let span3=document.createElement('span');
    span3.setAttribute('class','tag');
    span3.innerHTML = "*archived";
    span3.onclick = function(){
        showByIdlist(getIdlistByTagnames(["*archived"]));
        return false;
    }
    p.appendChild(span3);
    let span4=document.createElement('span');
    span4.setAttribute('class','tag');
    span4.innerHTML = "*abandoned";
    span4.onclick = function(){
        showByIdlist(getIdlistByTagnames(["*abandoned"]));
        return false;
    }
    p.appendChild(span4);
    let span5=document.createElement('span');
    span5.setAttribute('class','tag');
    span5.innerHTML = "*wanna";
    span5.onclick = function(){
        showByIdlist(getIdlistByTagnames(["*wanna"]));
        return false;
    }
    p.appendChild(span5);
    return p;
}

//`Markup file Container` can contain other than mc.markdown. hide only edit button of those.
const getEditClass = function(_mediatype){
    if(_mediatype=="text/markdown"){
        return ""
    }else{
        return " class=\"hidden\" "
    }
}

window.onload = function(){
    const title = document.URL.match("\/([^/]+?)\/(?:[^/]*?)$")[1];
    document.getElementById("title").innerText = title;
    document.getElementById("console_link").href = "mclog://console/?"+document.URL.slice(8,-10);
    for(let i=0;i<data.length;i++){
        let tbody=document.getElementById("tbody");
        let tr1=document.createElement('tr');
        tr1.setAttribute('id',String(i));
        //console.log(data[i]["x-originalpath"].replace(/\\/g,"/"));
        tr1.innerHTML = "<td>"+data[i]["modified"].slice(0,-8)+"</td>";
        tr1.innerHTML += "<td>"+data[i]["created"].slice(0,-8)+"</td>";
        tr1.innerHTML += "<td><a href=\""+data[i]["x-originalpath"].replace(/\\/g,"/")+"/index.md\">"+data[i]["title"]+"</a></td>";
        tr1.innerHTML += "<td><a href=\"mclog://edit/"+data[i]["x-originalpath"].replace(/\\/g,"/")+"\""+getEditClass(data[i]["rootfile"]["media-type"])+"><img src=\"./_index/edit.png\" /></a> <a href=\"mclog://edit-metadata/"+data[i]["x-originalpath"].replace(/\\/g,"/")+"\"><img src=\"./_index/tag.png\" /></a> <a href=\"mclog://dir/"+data[i]["x-originalpath"].replace(/\\/g,"/")+"/\"><img src=\"./_index/folder.png\" /></a> <a href=\"mclog://create-assets-list/"+data[i]["x-originalpath"].replace(/\\/g,"/")+"\"><img src=\"./_index/list.png\" /></a></td>"+gentd_tag(data[i]["tags"]);
        tbody.appendChild(tr1)
    }
    new Tablesort(document.getElementById('table'),{descending: true});
    enableTagClick();
    addSpecialTagButton();
    //default view is "show all except * tags". see addSpecialTagButton function.
    hideByIdlist(getIdlistByTagnames(["*archived","*abandoned","*wanna"]));
}
