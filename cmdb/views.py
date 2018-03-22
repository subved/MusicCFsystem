from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.views.decorators import csrf
from cmdb import itemCF
# Create your views here.


def index(request):
    if request.method=="POST":
        print("post")
        targeruUserID = request.POST.get('userID', None)
        rating_file = 'trainMusicID10W.csv'
        itemCF.itemCFSearch = itemCF.ItemBasedCF()
        itemCF.itemCFSearch.get_dataset(rating_file)
        itemCF.itemCFSearch.calc_song_sim()
        rec_songs = itemCF.itemCFSearch.evaluate(targeruUserID)
        print(rec_songs)
        songDict = {}
        for i in range(0,len(rec_songs)):
            songDict[i] = rec_songs[i]
        return render(request, "index.html",{'songDict':songDict})
    if request.method=="GET":
        print("get")
        return render(request,'index.html')

