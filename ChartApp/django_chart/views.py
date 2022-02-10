from django.shortcuts import render
import requests
import json
from multiprocessing import context
from django.shortcuts import redirect, render
from . models import Account
from . forms import AccountForm
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def index(request):
    accounts = Account.objects.all()

    if request.method == 'POST':
        url = 'https://etherscan.io/accounts/1?ps=100'
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(executable_path=r'C:\Users\abazy\Downloads\chromedriver_win32\chromedriver.exe', options = options) 
        driver.get(url) 
        listOfLinks = driver.find_elements_by_xpath('//a[contains(@href,"/address/")]')
        listOfLinks.pop(100) #Удаляем сотый элемент, который не адрес, а "Donate"
        balancee=[] # <= List of all balances
        for link in listOfLinks:
            url2 = 'https://api.etherscan.io/api?module=account&action=balance&address='+link.text+'&tag=latest&apikey=B6IJ4X42EPF1RRI1KSZKC9VBDK1I3NGF4C'
            response = requests.get(url2)
            content = response.json()
            result = int(content.get("result"))/1000000000000000000
            balancee.append(result)

        form = AccountForm(request.POST)
        for i in range(100):
            print(listOfLinks[i].text + "\n")
            Account.objects.create(address=listOfLinks[i].text, balance=balancee[i])
            if form.is_valid():
                form.save()
        return redirect('index')
    else:
        form = AccountForm()

    context = {
        "accounts": accounts,
        "form": form
    }

    return render(request, 'django_chart/index.html', context)


