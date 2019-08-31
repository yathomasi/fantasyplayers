from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from .forms import LeagueForm
from django.http import HttpResponse
# Create your views here.
import requests
import json
from .fpl import writeFileToOutput, readFromFile, getLeagueName
import logging, sys
import os

if not os.path.exists('output'):
    os.mkdir('output')
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
@csrf_exempt
def index(request):
    if request.method == 'POST':
        #getting values from post
        league = request.POST.get('league')
        gameweek = request.POST.get('gw')
        leaguetype = request.POST.get('leaguetype')

        playersFile = "output/GW"+str(gameweek)+" Players " + str(league) + ".csv"
        captainsFile = "output/GW"+str(gameweek)+" Captains " + str(league) + ".csv"
        if os.path.exists(playersFile):
            pass
        else:
            try:
                writeFileToOutput(league, gameweek, leaguetype)
            except Exception as e:
                    print(str(e))
                    context={
                        'error1':"Some error occured. Please Try again"
                    }
                    return render(request, 'home/index.html', context)
        
        listOfCountOfPlayersPicked = readFromFile(playersFile)
        listOfCountOfCaptainsPicked = readFromFile(captainsFile)
        GWNumber = gameweek
        leaguename = getLeagueName(league, leaguetype)
        context={
        'listOfCountOfCaptainsPicked':listOfCountOfCaptainsPicked, 
        'listOfCountOfPlayersPicked':listOfCountOfPlayersPicked,
        'gwnumber':GWNumber,
        'leaguename':leaguename
        }
        return render(request, 'home/showdata.html', context)
        

    return render(request, 'home/index.html')


@csrf_exempt
def testview(request):
    if request.method == 'POST':
        #getting values from post
        league = request.POST.get('league')
        gameweek = request.POST.get('gw')
        if request.POST.get('leaguetype')=='h2h':
            leaguetype = 'h2h'
        else:
            leaguetype = 'classic'
    
    #adding the values in a context variable 
        context = {
            'league': league,
            'gameweek': gameweek,
            'leaguetype': leaguetype,
        }
        #getting our showdata template
        return render(request, 'home/show.html', context)
        # csvfile = request.FILES['csv1']
        # data = pd.read_csv('csv1.csv')
        # data_html = data.to_html()
        # context = {'loaded_data': data_html}
        # return render(request, "home/test.html", context)
    
    return render(request, 'home/index.html')


def tastyview(request):
    GWNumber=1
    listOfCountOfCaptainsPicked=[('Agüero', 44), ('Kane', 9), ('Hazard', 7), ('Lukaku', 4), ('Aubameyang', 3), ('Salah', 3), ('Richarlison', 2), ('Sigurdsson', 1), ('Pogba', 1)]
    listOfCountOfPlayersPicked=[('Agüero', 53), ('Alonso', 47), ('Hazard', 46), ('Wan-Bissaka', 42), ('Mané', 34), ('Trippier', 31), ('Robertson', 30), ('Richarlison', 27), ('Mitrovic', 27), ('Fraser', 26), ('Ederson', 26), ('Lucas Moura', 26), ('Salah', 25), ('Zaha', 24), ('Wilson', 22), ('Alexander-Arnold', 20), ('Shaw', 19), ('Maddison', 18), ('Mendy', 16), ('Neves', 16), ('Bennett', 15), ('Speroni', 15), ('Kane', 14), ('Pogba', 14), ('Pereyra', 14), ('Kamara', 13), ('Tarkowski', 13), ('Walcott', 12), ('Alisson', 12), ('Holebas', 12), ('Etheridge', 12), ('Mkhitaryan', 11), ('Hamer', 10), ('Pickford', 10), ('Walker', 9), ('Ings', 9), ('Kanté', 9), ('Fabianski', 9), ('Hart', 8), ('Arnautovic', 8), ('De Gea', 8), ('Daniels', 8), ('Jorginho', 8), ('Firmino', 8), ('Aubameyang', 8), ('Foster', 7), ('Bernardo Silva', 7), ('Stephens', 7), ('Bellerín', 7), ('Steve Cook', 7), ('Hennessey', 6), ('Lukaku', 6), ('King', 5), ('Højbjerg', 5), ('Doherty', 5), ('Monreal', 5), ('Boruc', 5), ('Vertonghen', 5), ('Schlupp', 5), ('McCarthy', 5), ('Vardy', 5), ('Suttner', 5), ('Milner', 5), ('Patrício', 4), ('Kelly', 4), ('Cédric', 4), ('Lacazette', 4), ('Boly', 4), ('Gudmundsson', 3), ('Tomkins', 3), ('Kepa', 3), ('Morrison', 3), ('Laporte', 3), ('Guendouzi', 3), ('David Silva', 3), ('Billing', 3), ('Joselu', 3), ('Peltier', 3), ('Stankovic', 3), ('Fernandinho', 3), ('Lascelles', 3), ('Azpilicueta', 3), ('Maguire', 3), ('Bertrand', 3), ('Hudson-Odoi', 2), ('Ward', 2), ('Bednarek', 2), ('Deeney', 2), ('Schmeichel', 2), ('Calvert-Lewin', 2), ('Begovic', 2), ('Malone', 2), ('Milivojevic', 2), ('Seri', 2), ('Lennon', 2), ('Connolly', 2), ('Mee', 2), ('Baines', 2), ('Pedro', 2), ('Sánchez', 2), ('Hughes', 2), ('Willian', 2), ('Davies', 2), ('Morata', 2), ('Pereira', 2), ('Dunk', 1), ('Stones', 1), ('Mata', 1), ('Hoilett', 1), ('Valencia', 1), ('Mbemba', 1), ('Sané', 1), ('Fellaini', 1), ('Sigurdsson', 1), ('Zanka', 1), ('Oriol Romeu', 1), ('Keane', 1), ('Zohore', 1), ('Costa', 1), ('Sterling', 1), ('Gunnarsson', 1), ('McArthur', 1), ('Stekelenburg', 1), ('Batth', 1), ('Gomes', 1), ('Dier', 1), ('Alli',1), ('McDonald', 1), ('Elneny', 1), ('Quaner', 1), ('Obiang', 1), ('Tosun', 1), ('Schindler', 1), ('Bamba', 1), ('Eriksen', 1), ('Reid', 1), ('Simpson', 1), ('Schürrle', 1), ('Mooy', 1), ('Rüdiger', 1), ('van Aanholt', 1), ('Gomez', 1), ('Long', 1), ('Loftus-Cheek', 1), ('Ryan', 1), ('Lingard', 1), ('Duffy', 1), ('Xhaka', 1), ('Young', 1), ('Welbeck', 1), ('Elliot', 1), ('Gibbs-White', 1), ('Surman', 1), ('Schneiderlin', 1), ('van Dijk', 1), ('Fred', 1), ('Cork', 1), ('Westwood', 1), ('Gray', 1)]
    leaguename = "Fantastic WRC"
    context={
            'listOfCountOfCaptainsPicked':listOfCountOfCaptainsPicked, 
            'listOfCountOfPlayersPicked':listOfCountOfPlayersPicked,
            'gwnumber':GWNumber,
            'leaguename': leaguename,
        }
    return render(request, 'home/showdata.html', context)
