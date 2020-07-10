from django.shortcuts import render
import markdown2
from markdown2 import Markdown
from django.http import HttpResponseRedirect
import secrets
from . import util


def index(request):
    if request.method=="GET":
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })

    else:
        bool = True
        query = request.POST['q']
        entries = util.list_entries()
        if query in entries:
             return  HttpResponseRedirect(f'/wiki/{query}')
        queries = [s for s in entries if query in s]
        if len(queries)<1:
            mybool = False
        else:
            mybool = True

        return render(request, "encyclopedia/search_index.html", {
            "entries": queries,
            "bool" : mybool
        })

def entry(request,title):
    content = util.get_entry(title)
    if content==None:
        return render(request, "encyclopedia/error.html")
    else:
        markdowner = Markdown()
        content = markdowner.convert(content)
        return render(request, "encyclopedia/entry.html",{
            "header":title,
            "content":content
        })

def newpage(request):
    if request.method=="GET":
        boolean = True
        return render(request,"encyclopedia/newpage.html", {
            "boolean":boolean
        })
    else:
        title = request.POST['title']
        content = request.POST['content']
        entries = util.list_entries()
        if title in entries:
            boolean = False
            return render(request,"encyclopedia/newpage.html", {
                "boolean":boolean,
                "message":"Title has been taken"
            })
        else:
            util.save_entry(title, content)
            return  HttpResponseRedirect(f'/wiki/{title}')

def edit(request,title):
    print(title)
    content = util.get_entry(title)
    if request.method=="GET":
        if content==None:
            return render(request, "encyclopedia/error.html")
        else:
            return render(request,"encyclopedia/edit.html",{
                "content":content,
                "header":title
            })
    else:
        content = request.POST['content']
        util.save_entry(title, content)
        return  HttpResponseRedirect(f'/wiki/{title}')

def random(request):
    entries = util.list_entries()
    stop = len(entries)
    index = secrets.randbelow(stop)
    title = entries[index]
    return  HttpResponseRedirect(f'/wiki/{title}')