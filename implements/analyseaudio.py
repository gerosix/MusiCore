# -*- coding: utf-8 -*-

# Analyse BPM
from __future__ import print_function
import librosa
import os
import csv
import sys

# Analyse Tonale
from pylab import plot, show, title, xlabel, ylabel, subplot, savefig
from scipy import fft, arange, ifft
from numpy import sin, linspace, pi
from scipy.io.wavfile import read, write
import numpy

# ----------------------------- Analyse Musique -------------------------------
'''
Permet d'effectuer des analyses de musiques
fonctionne pour le mp3, wav
'''


class analyse:
    '''
    classe définissant l'analyse d'une musique. On a l'analyse bpm et l'analyse de la tonalité
    '''

    def __init__(self, PathToFile, NomFichierCsv):  # méthode constructeur
        self.NomCsv = NomFichierCsv  # chemin du fichier csv donnant
        self.PathToFile = PathToFile  # chemin du fichier audio
        self.PathToCsv = '/home/bettini/Dev/MusiCoreTest/BDDMusic/BDDMusic'  # chemin par défaut du fichier csv étant la base de donnée

    def extraire_path(self):
        """
        :param path: chemin absolue d'une fichier audio
        :return: list =[nom fichier, chemin du repertoire du dossier contenant le fichier audio]
        Comment: permet d'extraire d'un chemin absolu le nom du fichier une list:
        """

        # path1=path[::-1]
        k = 0
        while self.PathToFile[len(self.PathToFile) - k - 1] != "/":
            k = k + 1
        return [self.PathToFile[len(self.PathToFile) - k:],
                self.PathToFile[:len(self.PathToFile) - k - 1]]  # path to directory , file name

    def ecrirecsv(self, list):

        # verifie si on peut ouvrir le fichier
        try:
            with open(self.PathToCsv):
                pass
        except IOError:
            print("Erreur! Le fichier n'a pas pu etre ouvert")
            sys.exit(0)

        fname = self.PathToCsv
        # l'option 'a' permet de ne pas ecraser le fichier
        if os.path.isfile(self.PathToCsv) == True:  # si le fichier existe:
            try:  # rajoute seulement les lignes voulu
                print('le fichier csv existe, rajout des donnees dans le csv')
                file = open(fname, "a")
                # Creation de l'ecrivain'' CSV
                writer = csv.writer(file)

                # Ecriture des donnees.
                writer.writerow(list)

            finally:
                # Fermeture du fichier source
                file.close()

        else:  # si le fichier n'existe pas
            try:  # rajoute une entete
                print("le fichier csv n'existe pas, creation d'un nouveau fichier csv")
                file = open(fname, "wb")
                # Creation de l'ecrivain'' CSV
                writer = csv.writer(file)

                # Ecriture de la ligne d'en-tete avec le titre des colonnes.

                writer.writerow(('Emplacement', 'NomFichier', 'BpmMoyen', 'BpmDebut', 'BpmFin'))
                #
                # Ecriture des quelques donnees.
                writer.writerow(list)
            finally:
                # Fermeture du fichier source
                file.close()

    def islineincsc(self, titre):

        fname = self.PathToCsv
        file = open(fname, "rb")

        try:
            reader = csv.reader(file)
            for row in reader:
                #
                # N'affiche que certaines colonnes
                #
                if (row[1] = titre):
                    print('le fichier existe deja dans la base de donnée')
                    # TODO: mettre le fichier de la base de donnée dans le fichier csv en cour d'écriture
                print(row[1])
        finally:
            file.close()

        return

    def extrairedatamusic(self):

        path = self.extraire_path()[1]
        filename = self.extraire_path()[0]  # filename le fichier qui va etre analyse

        # On l'emplacement courant a dossier ou se situe la musique
        os.chdir(self.extraire_path()[1])
        # on load le fichier de musique
        return librosa.load(filename)

    def analyse_bpm(self, y, sr):
        """
        :param pathtofile: chemin absolue du fichier audio dont on veut analyser le bpm
        :param fichier_csv: fichier csv dans lequel sera enregistre les bpms du morceau (nom de la playlist en cours)
        Comment:ecrit dans le fichier csv a la fin
        """

        self.islineincsc(analyse1.extraire_path())

        # back: path=self.extraire_path()[1]
        # back: filename = self.extraire_path()[0]    #filename le fichier qui va etre analyse

        # On l'emplacement courant a dossier ou se situe la musique
        # back: os.chdir(self.extraire_path()[1])

        # creation de la liste qui va etre exportee dans le csv

        ElemCsv = [self.PathToFile, analyse1.extraire_path()[0]]

        # enregistrement du fichier audio comme une forme d'onde 'y' ; enrigistrement de taux d'echantillon en 'sr'
        # TODO: cette fonction est le goulot d'etranglement du programme, a ameliorer...
        # back: y, sr = librosa.load(filename)

        # execution du tracker bpm par default
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

        # affichage du bpm moyen
        # print('tempo moyen: {:.2f} BPM'.format(tempo))

        # Converti les sequences d'indice de beat en un chronogramme
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)

        # calcul du bpm du debut et de la fin de la musique dans le cas d'un changement au cours de la musique
        bpm_d = 0
        bpm_f = 0
        for i in range(100):
            bpm_d = bpm_d + (beat_times[i + 1] - beat_times[i])
            bpm_f = bpm_f + (beat_times[len(beat_times) - i - 1] - beat_times[len(beat_times) - i - 2])
        # print("BPM_debut = %s" %(60/(bpm_d/100)))

        # on complete la lste qui va etre mis dans le csv
        ElemCsv.append(tempo)
        ElemCsv.append(60 / (bpm_d / 100))
        ElemCsv.append(60 / (bpm_f / 100))
        print(ElemCsv)

        # ecriture des donnees dans le fichier csv
        self.ecrirecsv(ElemCsv)

    def analysefft(self, y, Fs):

        n = len(y)  # lungime semnal
        k = arange(n)
        T = n / Fs
        frq = k / T  # two sides frequency range
        frq = frq[range(n / 2)]  # one side frequency range

        Y = fft(y) / n  # fft computing and normalization
        Y = Y[range(n / 2)]

        plot(frq, abs(Y), 'r')  # plotting the spectrum
        xlabel('Freq (Hz)')
        ylabel('|Y(freq)|')
        Fs = 44100;  # sampling rate
        # rate,data=read('Deorro.wav')
        y = data[: 441000]
        lungime = len(y)
        timp = len(y) / 44100
        t = linspace(0, timp, len(y))
        print(len(y))
        print(len(t))

    def recherchenote(self):
        '''

        :param self:
        :return:
        '''

        return


# test
analyse1 = analyse("/home/bettini/Musique/Deorro.wav", "fichier_csv")
# print(analyse1.extraire_path())
y, sr = analyse1.extrairedatamusic()
analyse1.analyse_bpm(y, sr)
