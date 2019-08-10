from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from .forms import LeagueForm
from django.http import HttpResponse
# Create your views here.
import requests
import json

DIRNAME = "Data"
FPL_URL = "https://fantasy.premierleague.com/drf/"
USER_SUMMARY_SUBURL = "element-summary/"
LEAGUE_CLASSIC_STANDING_SUBURL = "leagues-classic-standings/"
LEAGUE_H2H_STANDING_SUBURL = "leagues-h2h-standings/"
TEAM_ENTRY_SUBURL = "entry/"
PLAYERS_INFO_SUBURL = "bootstrap-static"
PLAYERS_INFO_FILENAME = "allPlayersInfo.json"


USER_SUMMARY_URL = FPL_URL + USER_SUMMARY_SUBURL
PLAYERS_INFO_URL = FPL_URL + PLAYERS_INFO_SUBURL
START_PAGE = 1


# Get users in league: https://fantasy.premierleague.com/drf/leagues-classic-standings/336217?phase=1&le-page=1&ls-page=5
def getUserEntryIds(league_id, ls_page, league_Standing_Url):
    league_url = league_Standing_Url + \
        str(league_id) + "?phase=1&le-page=1&ls-page=" + str(ls_page)
    r = requests.get(league_url)
    jsonResponse = r.json()
    leaguename = jsonResponse["league"]["name"]
    standings = jsonResponse["standings"]["results"]
    if not standings:
        print("no more standings found!")
        return None

    entries = []

    for player in standings:
        entries.append(player["entry"])

    return leaguename,entries

# team picked by user. example: https://fantasy.premierleague.com/drf/entry/2677936/event/1/picks with 2677936 being entry_id of the player
def getplayersPickedForEntryId(entry_id, GWNumber):
    eventSubUrl = "event/" + str(GWNumber) + "/picks"
    playerTeamUrlForSpecificGW = FPL_URL + \
        TEAM_ENTRY_SUBURL + str(entry_id) + "/" + eventSubUrl
    r = requests.get(playerTeamUrlForSpecificGW)
    jsonResponse = r.json()
    picks = jsonResponse["picks"]
    # print(picks)
    elements = []
    captainId = 1
    for pick in picks:
        elements.append(pick["element"])
        if pick["is_captain"]:
            captainId = pick["element"]
    return elements, captainId

@csrf_exempt
def index(request):
    if request.method == 'POST':
        #getting values from post
        league = request.POST.get('league')
        gameweek = request.POST.get('gw')
        if request.POST.get('leaguetype')=='h2h':
            leaguetype = 'h2h'
        else:
            leaguetype = 'classic'
        try:
            r = requests.get(PLAYERS_INFO_URL)
            jsonResponse = r.json()
        except Exception as e:
                print(str(e))
                context={
                    'error1':"Some error occured. Please Try again"
                }
                return render(request, 'home/index.html',context)
        # return HttpResponse(json.dumps(jsonResponse), content_type='application/json')
        playerElementIdToNameMap = {}
        allPlayers=json.loads(json.dumps(jsonResponse))
        for element in allPlayers["elements"]:
            playerElementIdToNameMap[element["id"]] = element["web_name"] #.encode('ascii', 'ignore')

        countOfPlayersPicked = {}
        countOfCaptainsPicked = {}
        totalNumberOfPlayersCount = 0
        pageCount = START_PAGE
        leagueIdSelected = league
        GWNumber = gameweek
        if leaguetype == "h2h":
            leagueStandingUrl = FPL_URL + LEAGUE_H2H_STANDING_SUBURL
            print("h2h league mode")
        elif leaguetype == 'classic':
            leagueStandingUrl = FPL_URL + LEAGUE_CLASSIC_STANDING_SUBURL
            print("classic league mode")
        # leagueStandingUrl = FPL_URL + LEAGUE_CLASSIC_STANDING_SUBURL

        while (True):
            try:
                leaguename, entries = getUserEntryIds(
                    leagueIdSelected, pageCount, leagueStandingUrl)
                if entries is None:
                    print("breaking as no more player entries")
                    break

                totalNumberOfPlayersCount += len(entries)
                print("parsing pageCount: " + str(pageCount) + " with total number of players so far:" + str(
                    totalNumberOfPlayersCount))
                for entry in entries:
                    elements, captainId = getplayersPickedForEntryId(entry, GWNumber)
                    for element in elements:
                        name = playerElementIdToNameMap[element]
                        if name in countOfPlayersPicked:
                            countOfPlayersPicked[name] += 1
                        else:
                            countOfPlayersPicked[name] = 1

                    captainName = playerElementIdToNameMap[captainId]
                    if captainName in countOfCaptainsPicked:
                        countOfCaptainsPicked[captainName] += 1
                    else:
                        countOfCaptainsPicked[captainName] = 1

                listOfCountOfPlayersPicked = sorted(
                    countOfPlayersPicked.items(), key=lambda x: x[1], reverse=True)
                
                listOfCountOfCaptainsPicked = sorted(
                    countOfCaptainsPicked.items(), key=lambda x: x[1], reverse=True)

                pageCount += 1
            except Exception as e:
                print(str(e))
                context={
                    'error1':True
                }
                return render(request, 'home/index.html',context)
        context={
            'listOfCountOfCaptainsPicked':listOfCountOfCaptainsPicked, 
            'listOfCountOfPlayersPicked':listOfCountOfPlayersPicked,
            'gwnumber':GWNumber,
            'leaguename':leaguename,
        }
        # print(listOfCountOfCaptainsPicked)
        # print()
        # print(listOfCountOfPlayersPicked)
        # print('hakuna matatata')
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

# @csrf_exempt
# def leagueform(request):
#     if request.method == 'POST':
#         form = LeagueForm(request.POST)

#         if form.is_valid():
#             context = {
#                 'league': form.cleaned_data['league'],
#                 'gameweek': form.cleaned_data['gameweek'],
#                 }
#             return render(request, 'home/showdata.html', context)
#     else:
#         form = LeagueForm()
    
#     return render(request, 'home/index.html', {'form': form})

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
