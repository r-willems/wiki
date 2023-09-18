import random
from django import forms
from django.shortcuts import render
from markdown2 import Markdown
from . import util

LIST = util.list_entries() # original list of entries

# Helper functions:
def convert_to_case(input):
    """
Use case insensitive input and check if they are in the array of entries,
if so, return the case-sensitive entry
    """
    for i in range(len(LIST)):
        if input.lower() == LIST[i].lower():
            return LIST[i]
    return None

#Main functions:
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def view_entry(request, title):
    """
Return entry as a route to a html page
    """
    entry_name = convert_to_case(title)
    if entry_name and entry_name in LIST:
        md_content = util.get_entry(entry_name)
        print(f"The title is {entry_name} and the text is {md_content}")
        html_content = Markdown().convert(md_content)
        if html_content:
            return render(request, f"encyclopedia/entry.html", {
                "title": entry_name,
                "text": html_content,
                "name": entry_name,
                "plaintext": md_content})
    else:
        return render(request, "encyclopedia/error.html")

def search(request):
    """
Search through entries, route to entry page if successful,
show suggestions if partly successfull
    """
    if request.method == "POST":
        input = request.POST['q'].strip().lower()
        if input:
            query = convert_to_case(input)
            if util.get_entry(query):
                return view_entry(request, query)
            else:
                results = find_results(input)
                names = [convert_to_case(name) for name in results]
                if results:
                    return render(request, "encyclopedia/search.html", {
                        "text": f"Showing results for: {input}",
                        "output": zip(results, names)
                })
                else:
                    return render(request, "encyclopedia/search.html",{
                        "text": f"No results were found for {input}"
                    })
        else:
            return render(request, "encyclopedia/search.html", {
                "text": "Please add a search query!"
            })

def find_results(input):
    matches = []
    decapitalized_list = [item.lower() for item in LIST]
    for entry in decapitalized_list:
        if input in entry:
            matches.append(entry)
    return matches


def editor(request):
    if request.method == "POST":
        # Using the edit button on an entry page
        return render(request, "encyclopedia/editor.html", {
            "title": request.POST["nameBox"],
            "text": request.POST["textBox"],
            "edit_bool": False,
            "able_title": "disabled"
        })
    else:
        # Clicking the link to create new page
        return render(request, "encyclopedia/editor.html", {
            "title": '',
            "text": '',
            "edit_bool": True,
            "able_title": ""
        })

def submit(request):
    if request.method == "POST":
        title = request.POST["titleBox"].strip()
        content = request.POST.get('textBox', '')
        if title and content: 
            if request.POST["creatingNew"] == "True":
            #Ik denk dat het te maken heeft met hoe get_entry werkt
                print("new")
                if title in LIST:
                    print("no") #title already exists
                    return
                else:
                    util.save_entry(title, content)
                    return render(request, f"encyclopedia/entry.html", {
                        "title": title,
                        "text": Markdown().convert(content),
                        "name": title,
                        "plaintext": content})
            else:
                print("edit")
                util.save_entry(title, content)
                return view_entry(request, title)
                
    return render(request, "encyclopedia/error.html")


def random_page(request):
    n = random.randrange(0, len(LIST))
    return view_entry(request, LIST[n])

