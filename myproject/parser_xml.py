# !/usr/bin/python3
# -*- coding: utf-8 -*-

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from xml.sax.saxutils import escape, unescape
import sys

class myContentHandler(ContentHandler):

    def __init__ (self):
        self.dataType = 'contenido'

        self.inContent = True
        self.theContent = ""

        self.dataSection = ['NOMBRE', 'DESCRIPCION', 'ACCESIBILIDAD', 'CONTENT-URL','BARRIO', 'DISTRITO','LATITUD', 'LONGITUD']
        self.inSection = False
        self.atrSection = ''

        self.ParkingList = {}
        self.Park = []

    def startElement (self, name, attrs):

        if name == 'atributo' and attrs['nombre'] in self.dataSection:
            self.atrSection = attrs['nombre']
            self.inSection = True
        elif name == 'atributo' and attrs['nombre'] == 'LOCALIZACION' and attrs['nombre'] in self.dataSection:
            self.atrSection = attrs['nombre']
            self.inSection = True

    def endElement (self, name):

        if name == 'atributo' and self.atrSection in self.dataSection:
            self.ParkingList[self.atrSection] = self.theContent
            self.atrSection = ""
        if name == 'atributo'and self.atrSection == 'LOCALIZACION' and self.atrSection in self.dataSection:
            self.ParkingList[self.atrSection] = self.theContent
            self.atrSection = ""

        if name == self.dataType:
            self.Park.append(self.ParkingList)
            self.ParkingList = {}
        if self.inSection:
            self.inSection = False
            self.atrSection = ""
            self.theContent = ""
    def characters (self, chars):
        html_escape_table = {
            "&quot;" : '"',
            "&apos;" : "'",
            "&iexcl" : u'¡',
            "&iquest" : u'¿',
            "&aacute;" : u'á',
            "&iacute;" : u'í',
            "&oacute;" : u'ó',
            "&uacute;" : u'ú',
            "&eacute;" : u'é',
            "&ntilde;" : u'ñ',
            "&Ntilde;" : u'Ñ',
            "&Aacute;" : u'Á',
            "&Iacute;" : u'Í',
            "&Oacute;" : u'Ó',
            "&Uacute;" : u'Ú',
            "&Eacute;" : u'É',
            "&Ocirc;" : u'Ô',
            "&ocirc;" : u"ô",
            "&uuml;" : u'ü',
            "&Uuml;" : u'Ü',
            "&nbsp;" : '\n',
            "&rdquo;" : '"',
            "&ldquo;" : '"',
            "&lsquo;" : "'",
            "&rsquo;" : "'",
        }
        if self.inSection:
         text = self.theContent + chars
         self.theContent = unescape(text, html_escape_table)

def getParking ():
#Load parser and driver
    theParser = make_parser()
    theHandler = myContentHandler()
    theParser.setContentHandler(theHandler)
# Ready, set, go!
    theParser.parse('http://datos.munimadrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=202584-0-aparcamientos-residentes&mgmtid=e84276ac109d3410VgnVCM2000000c205a0aRCRD&preview=full')
    Parks = theHandler.Park
    return Parks
