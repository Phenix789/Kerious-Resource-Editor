#!/usr/bin/env python

"""
.. module:: useful_1
   :platform: Unix, Windows
   :synopsis: A useful module indeed.

.. moduleauthor:: Andrew Carter <andrew@invalid.com>


"""

import gtk

from status import KSEStatusView
from error import ErrorMessage
from utils import is_contained_by

class KSETree(gtk.TreeView):
    def __init__(self):
        self.treestore = gtk.TreeStore(str)
        gtk.TreeView.__init__(self, self.treestore)
        self.show()
        self.set_size_request(400, 250)

class KSEWorkzone(gtk.VPaned):
    """
    Contained by : Sections
    Workzones contain two things : An xml prettifier displaying the content of
    their managed section, and a "Status view", for lack of a better word,
    where the user can interact with the content, for example the atlases.
    @cvar current : Path of the current atlas in the model
    """
    def __init__(self):
        gtk.VPaned.__init__(self)
        self.treeview = KSETree()
        self.notebook = KSEStatusView(self)
        self.add1(self.treeview)
        self.add2(self.notebook)
        self.show()

    def export(self):
        pass

class KSEGraphicWorkzone(KSEWorkzone):
    def __init__(self):
        KSEWorkzone.__init__(self)
        self.sectionCallbacks = [self._getAtlasFromPath]
        self.current = None

    def createTree(self, tree):
        self.tree = tree
        self.model = gtk.TreeStore(str)
        self.treeview.set_model(self.model)
        self._addAtlases()
        self.treeview.connect("row-activated", self._newSelectionCb)

    def addAtlas(self, node):
        self.model.append(self.model.get_iter((0,)), [node.attrib["name"]])
        self.atlases = self.tree.findall("atlas")

    def addSpriteForAtlas(self, atlasNode, node):
        atlas = self.model.get_iter(self.current)
        self.model.append(atlas, [node.attrib["name"]])

    def export(self):
        atlas = self._getAtlasFromPath(self.current[1])
        self.notebook.export(atlas.attrib["path"])

    def getSpriteFromXY(self, event):
        atlas = self._getAtlasFromPath(self.current[1])
        sprites = atlas.findall("sprite")
        x = event.get_coords()[0]
        y = event.get_coords()[1]
        #FIXME : hack, accounting for the possible margin between the
        # event box bounds and the atlas bounds. I'm ashamed
        diff = self.notebook.get_allocation().width - int(self._getAtlasFromPath(self.current[1]).attrib["width"])
        if diff > 0:
            x -= diff / 2
        for sprite in sprites:
            try:
                print x, y
                print int(sprite.attrib["texturex"]), int(sprite.attrib["texturey"]), int(sprite.attrib["texturew"]), int(sprite.attrib["textureh"])
                if is_contained_by(x, y,
                                   int(sprite.attrib["texturex"]),
                                   int(sprite.attrib["texturey"]),
                                   int(sprite.attrib["texturew"]),
                                   int(sprite.attrib["textureh"])):
                    print sprite.attrib["name"], " was clicked"
            except KeyError:
                pass

    #INTERNAL

    def _addAtlases(self):
        self.atlases = self.tree.findall("atlas")
        atlases = gtk.TreeViewColumn("Graphics")
        cell = gtk.CellRendererText()
        atlases.pack_start(cell, True)
        atlases.add_attribute(cell, "text", 0)
        it = self.model.append(None, ["Atlases"])
        for elem in self.atlases:
            at = self.model.append(it, [elem.attrib["name"]])
            sprites = elem.findall("sprite")
            for el in sprites:
                self.model.append(at, [el.attrib["name"]])
        self.treeview.append_column(atlases)

    def _getAtlasFromPath(self, path):
        return self.atlases[path]

    def _newSelectionCb(self, treeview, path, view_column):
        node = self.sectionCallbacks[path[0]](path[1])
        self.current = path
        filePath = None
        try:
            filePath = node.attrib["path"]
            self.notebook.openPath(node, filePath)
        except KeyError:
            ErrorMessage("No Path for this node :/")

    def mergeResource(self, width, height, path):
        coords = self.notebook.mergeResource(width, height, path)
        return coords