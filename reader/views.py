from django.shortcuts import render, redirect
from django.conf import settings
from . forms import ParagraphForm
from . models import Paragraph
import os
import random
first_list = []
final_list = []
context = ""


def index(request):

    if request.method == "POST":
        form = ParagraphForm(request.POST)
        print (form.errors)
        if form.is_valid():
            print (form.errors)
            # clear old objects
            Paragraph.objects.all().delete()
            # get submitted number
            num = form.cleaned_data['number_of_paragraphs']
            # Open text file and read, splitting into paragraphs
            file = open(os.path.join(
                settings.BASE_DIR, 'static/text/text.txt'))
            text = file.read().split('!')
            # Break into separate paragraphs
            for line in text:
                second_split = line.split('\n')
                first_list.append(second_split)
            list_length = len(first_list)
            # Grab random paragraph
            for x in range(num):
                index_int = random.randint(0, list_length - 1)
                result = first_list[index_int]
                paragraph = form.save(commit=False)
                string = " ".join(str(x) for x in result)
                paragraph.text += '\n' + string + '.' + '\n'
            paragraph.save()
            
            return redirect('index')
        else:
            form = ParagraphForm(initial={'number_of_paragraphs': 1})
            return render(request, 'index.html', {'form': form})
    else:
        context = Paragraph.objects.all()
        form = ParagraphForm(initial={'number_of_paragraphs': 1})
        return render(request, 'index.html', {'form': form, 'context': context,})
