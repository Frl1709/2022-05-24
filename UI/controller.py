import copy
import warnings

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDD(self):
        generi = self._model.listGeneri

        for g in generi:
            self._view.ddGenere.options.append(ft.dropdown.Option(data=g, text=g.Name, on_click=self.getSelectAlbum))

    def getSelectAlbum(self, e):
        if e.control.data is None:
            self._choiceAlbum = None
        else:
            self._choiceAlbum = e.control.data

    def handleCreaGrafo(self, e):
        if self._choiceAlbum is None:
            self._view.create_alert("Inserire un genere")
            return

        self._model.builGraph(self._choiceAlbum)
        nN, nE = self._model.getGraphSize()
        self._view.txt_result.clean()
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato con {nN} nodi e {nE} archi"))

        canzoni = self._model.nodes
        for c in canzoni:
            self._view.ddCanzone.options.append(ft.dropdown.Option(data=c, text=c.Name, on_click=self.getSelectedTrack))
        self._view.update_page()

    def getSelectedTrack(self, e):
        if e.control.data is None:
            self._choiceTrack= None
        else:
            self._choiceTrack = e.control.data

    def handleDeltaMax(self, e):
        lista = self._model.getMaxDelta()
        self._view.txt_result.controls.append(ft.Text(f"Coppia Canzoni Delta massimo"))
        for l in lista:
            self._view.txt_result.controls.append(ft.Text(f"{l[0].Name} *** {l[1].Name} --> {l[2]}"))
        self._view.update_page()

    def handleGetLista(self, e):
        if self._choiceTrack is None:
            self._view.create_alert("Inserire una canzone")
            return

        try:
            memoriaMax = int(self._view.txtMemoria.value)
        except ValueError:
            self._view.clear_alert("Inserire un intero per la memoria")
            return

        bestPath = self._model.getBestPath(self._choiceTrack, memoriaMax)
        self._view.txt_result.clean()
        self._view.txt_result.controls.append(ft.Text(f"Lista contentente {len(bestPath)} elementi"))
        self._view.txt_result.controls.append(ft.Text(f"Occupa in totale {self._model.getSize(bestPath)} bytes"))
        for i in bestPath:
            self._view.txt_result.controls.append(ft.Text(f"{i.Name}"))

        self._view.update_page()
