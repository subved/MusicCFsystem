# -*- coding: UTF-8 -*- 
# coding = utf-8

import random
import csv
import sys
import math
import codecs
# from pyechonest import song
from operator import itemgetter


class ItemBasedCF():
    # 初始化参数
    def __init__(self):
        # 找到相似的20部，为目标用户推荐10部
        self.n_sim_song = 20
        self.n_rec_song = 10

        # 将数据集划分为训练集和测试集
        self.trainSet = {}
        self.testSet = {}

        # 用户相似度矩阵
        self.song_sim_matrix = {}
        self.song_popular = {}
        self.song_count = 0

        print('Similar song number = %d' % self.n_sim_song)
        print('Recommneded song number = %d' % self.n_rec_song)

    # 读文件得到“用户-音乐”数据
    def get_dataset(self, filename, pivot=0.75):
        trainSet_len = 0
        testSet_len = 0

        for line in self.load_file(filename):
            rating = 1.0
            user, userName, song, art, playcount = line.split(",")
            if (int(playcount) >= 3 and int(playcount) < 6):
                rating = 2.0
            elif (int(playcount) >= 6 and int(playcount) < 9):
                rating = 3.0
            elif (int(playcount) >= 9 and int(playcount) < 12):
                rating = 4.0
            elif (int(playcount) >= 12):
                rating = 5.0

            if (1):
                self.trainSet.setdefault(user, {})
                self.trainSet[user][song] = rating
                trainSet_len += 1
            # else:
            #     self.testSet.setdefault(user, {})
            #     self.testSet[user][song] = rating
            #     testSet_len += 1
        # print('Split trainingSet and testSet success!')
        print('TrainSet = %s' % trainSet_len)
        # print('TestSet = %s' % testSet_len)

    # # 读文件得到音乐名称数据
    # def get_title(self,key):
    #     songs_file = 'songs.csv'
    #
    #     #pattern = re.compile('"(.*)"')
    #
    #     #print pattern.findall(rec_songs[0])
    #
    #
    #     print('get song title, build recommend list!')
    #     # 打开文件，用with打开可以不用去特意关闭file了，python3不支持file()打开文件，只能用open()
    #     with open(songs_file, "r") as csvfile:
    #         # 读取csv文件，返回的是迭代类型
    #         reader = csv.reader(csvfile)
    #         songId = [row[0] for row in reader]
    #         songName = [row[1] for row in reader]
    #         print(songId)
    #         song = dict(zip(songId,songName))
    #
    #         for i in songId:
    #             if i in key:
    #                 print(song.get(i))
    #
    #     print('build recommend list success!')

    # 读文件，返回文件的每一行
    def load_file(self, filename):
        with open(filename, 'r') as f:
            for i, line in enumerate(f):
                # if i == 0:  # 去掉文件第一行的title
                #     continue
                yield line.strip('\r\n')
        print('Load %s success!' % filename)

    # 读文件，打印音乐名称
    def getSongName(self, filename, songList):
        file = open(filename)
        lines = file.readlines()
        songNameList = []
        for line in lines:
            songId, songName = line.split(",")
            if songId in songList:
                print(songName)
                songNameList.append(songName)

        print('print songName success!')
        return songNameList

    # 计算音乐之间的相似度
    def calc_song_sim(self):
        for user, songs in self.trainSet.items():
            for song in songs:
                if song not in self.song_popular:
                    self.song_popular[song] = 0
                self.song_popular[song] += 1

        self.song_count = len(self.song_popular)
        print("Total song number = %d" % self.song_count)

        for user, songs in self.trainSet.items():
            for m1 in songs:
                for m2 in songs:
                    if m1 == m2:
                        continue
                    self.song_sim_matrix.setdefault(m1, {})
                    self.song_sim_matrix[m1].setdefault(m2, 0)
                    self.song_sim_matrix[m1][m2] += 1

        # for user, songs in self.trainSet.items():
        #     for m1 in songs:
        #         print(self.song_sim_matrix[m1])
        print("Build co-rated users matrix success!")

        # 计算音乐之间的相似性
        print("Calculating song similarity matrix ...")
        for m1, related_songs in self.song_sim_matrix.items():
            for m2, count in related_songs.items():
                # 注意0向量的处理，即某音乐的用户数为0
                if self.song_popular[m1] == 0 or self.song_popular[m2] == 0:
                    self.song_sim_matrix[m1][m2] = 0
                else:
                    self.song_sim_matrix[m1][m2] = count / math.sqrt(self.song_popular[m1] * self.song_popular[m2])
        print('Calculate song similarity matrix success!')

    # 针对目标用户U，找到K部相似的音乐，并推荐其N部音乐
    def recommend(self, user, targetUserID):
        # sys.stdout = codecs.getwriter('utf8')(sys.stdout)
        K = self.n_sim_song
        N = self.n_rec_song
        rank = {}

        # print(user)
        listened_songs = self.trainSet[user]
        # print (listened_songs)

        for song, rating in listened_songs.items():
            for related_song, s in sorted(self.song_sim_matrix[song].items(), key=itemgetter(1), reverse=True)[:K]:
                if related_song in listened_songs:
                    continue
                rank.setdefault(related_song, 0)

                rank[related_song] += s * float(rating)
        if user == targetUserID:
            rec_songsId = rank.keys()
            songList = []
            count = 0
            for i in rec_songsId:
                songList.append(i)
                count = count + 1
                if count > 9:
                    break
            # print(songList)

            return self.getSongName("SongId3.csv", songList)

            # s = song.Song('SOLUHKP129F0698D49')
            # print s.title
            # song_ids = ['SOBSLVH12A8C131F38', 'SOXMSGY1338A5D5873', 'SOJPHZO1376210AFE5', 'SOBHNKR12AB0186218',
            #             'SOSJAHD13770F4D40C']
            # songs = song.profile(song_ids,buckets=['audio_summary'])
            # print(songs)

        # self.get_title(rec_songsId)
        # return sorted(rank.items(), key=itemgetter(1), reverse=True)[:N]

    # 产生推荐并通过准确率、召回率和覆盖率进行评估
    def evaluate(self, targeruUserID):
        # targeruUserID = input('Please enter your id')
        print('Evaluating start ...')
        N = self.n_rec_song
        return self.recommend(targeruUserID, targeruUserID)

        # 准确率和召回率
        hit = 0
        rec_count = 0
        test_count = 0
        # 覆盖率
        all_rec_songs = set()
        # 打印id为344的人的推荐音乐
        # self.testSet.get('344', {})
        # rec_songs = self.recommend('12')
        # print (rec_songs)
        # self.get_title(songs_file,rec_songs)


""""
        for i, user in enumerate(self.trainSet):
            #print(user)
            test_moives = self.testSet.get(user, {})
            rec_songs = self.recommend(user,targeruUserID)
            if user == targeruUserID:
            #    print(rec_songs)
                return rec_songs

            for song, w in rec_songs:
                if song in test_moives:
                    hit += 1
                all_rec_songs.add(song)
            rec_count += N
            test_count += len(test_moives)

        precision = hit / (1.0 * rec_count)
        # recall = hit / (1.0 * test_count)
        coverage = len(all_rec_songs) / (1.0 * self.song_count)
        print("precisioin=%.4f\t coverage=%.4f " % (precision,  coverage))
        return rec_songs
"""

if __name__ == '__main__':
    rating_file = 'trainMusicID10W.csv'
    itemCF = ItemBasedCF()
    itemCF.get_dataset(rating_file)
    itemCF.calc_song_sim()
    itemCF.evaluate()
