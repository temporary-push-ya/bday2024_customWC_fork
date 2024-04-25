from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from urllib.parse import urlencode
import matplotlib.pyplot as plt 
import mpld3
from custom_wordcloud.custom_wc import wc_generator

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('matches')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'wordmatch/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def matches(request):
    if request.method == 'POST':
        mask = request.POST.get('radio')
        query = request.POST.get('text_input')
        print(query, mask)

        wordcloud = wc_generator(query, mask)

        fig = wordcloud.generate()

        # Convert plot to HTML
        html = mpld3.fig_to_html(fig)
        context = {'plot_html': html, 'img_path':False}

    else: # only at the start when nothing is types
        context = {'plot_html': None, 'image':True}

    return render(request, 'wordmatch/matches.html', context)