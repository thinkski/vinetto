# -*- coding: UTF-8 -*-
"""
module vinreport.py
-----------------------------------------------------------------------------

 Vinetto : a forensics tool to examine Thumbs.db files
 Copyright (C) 2005, 2006 by Michel Roukine
 
This file is part of Vinetto.
 
 Vinetto is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License as published
 by the Free Software Foundation; either version 2 of the License, or (at
 your option) any later version.
 
 Vinetto is distributed in the hope that it will be
 useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 General Public License for more details.
 
 You should have received a copy of the GNU General Public License along
 with the vinetto package; if not, write to the Free Software
 Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
 
-----------------------------------------------------------------------------
"""

__revision__ = "$Revision: 47 $"
__version__ = "0.02"
__author__ = 'Michel Roukine'

HtHeader = []
HtPicRow = []
HtOrphans = []
HtFooter = []
IMGTAG = "<IMG SRC=\"./__TNFNAME__.jpg\" ALT=\"__TNNAME__\">"

from time import time, ctime
from os.path import dirname, basename, abspath, getmtime
from vinetto.vinutils import getCatEntry       
from pkg_resources import resource_filename


class Report:
    """ Vinetto report SuperClass.  """
    def __init__ (self, target, outputdir, verstr):
        """ Initialize a new Report instance.  """
        self.tDBfname = basename(target)
        self.tDBdirname = abspath(dirname(target))
        self.tDBmtime = getmtime(target)
        self.outputdir = outputdir
        self.verstr = verstr


class HtRep(Report):
    """ Html vinetto elementary mode report Class.  """
    def __init__ (self, tDBfname, outputdir, charset, verstr):
        """ Initialize a new HtRep instance.  """
        Report.__init__(self, tDBfname, outputdir, verstr)
        self.rownumber = 0
        separatorID = 0
        
        for ligne in open(resource_filename('vinetto', 'data/HtRepTemplate.html'), "r").readlines():
            if ligne.find("__CHARSET__") > 0:
                ligne = ligne.replace("__CHARSET__", charset)
            if ligne.find("__ITS__") >= 0:
                separatorID += 1
                continue
                
            if separatorID == 0:
                HtHeader.append(ligne)
            elif separatorID == 1:
                HtPicRow.append(ligne)
            elif separatorID == 2:
                HtOrphans.append(ligne)
            elif separatorID == 3:
                HtFooter.append(ligne)
              
        self.TNidList = []
        self.TNtsList = []
        self.TNnameList = []
    
    
    def SetFileSection (self, FileSize, md5):
        """ Initialize data of the report file section.  """
        self.FileSize = FileSize
        self.md5 = md5
        
        
    def SetREtst (self, REtst):
        """ Initialize data of the report file section.  """
        self.REtst = REtst
       
        
    def headwrite (self):
        """ Writes report header.  """
        self.repfile = open(self.outputdir + "index.html", "w")    
        for ligne in HtHeader:
            ligne = ligne.replace("__DATEREPORT__", "Report date : " + ctime(time()))
            ligne = ligne.replace("__TDBDIRNAME__", self.tDBdirname)
            ligne = ligne.replace("__TDBFNAME__", self.tDBfname)
            ligne = ligne.replace("__TDBMTIME__", ctime(self.tDBmtime))
            ligne = ligne.replace("__FILESIZE__", str(self.FileSize))
            ligne = ligne.replace("__MD5__", self.md5)
            ligne = ligne.replace("__ROOTENTRYTST__", \
                                  "Root Entry modify timestamp : " + self.REtst)
            self.repfile.write(ligne)


    def close(self, statstring):
        """ Terminate processing HtRep instance.  """
            
        for ligne in HtFooter:
            ligne = ligne.replace("__TYPEXTRACT__", statstring)
            ligne = ligne.replace("__VVERSION__", "Vinetto " + self.verstr)
            self.repfile.write(ligne)
        self.repfile.close()

        
    def rowflush(self):
        """ Process a report line.  """
        self.rownumber += 1
        for ligne in HtPicRow:
            ligne = ligne.replace("__ROWNUMBER__", str(self.rownumber))
            for j in range(len(self.tnId)):
                ligne = ligne.replace("__TNfilled__" + str(j), "1")
                buff = IMGTAG.replace("__TNFNAME__", self.tnFname[j])
                buff = buff.replace("__TNNAME__", self.tnName[j])
                ligne = ligne.replace("__IMGTAG__" + str(j), buff)                
                ligne = ligne.replace("__TNID__" + str(j), self.tnId[j])
            for j in range(len(self.tnId),5):
                ligne = ligne.replace("__TNfilled__" + str(j), "0")
                ligne = ligne.replace("__IMGTAG__" + str(j), " &nbsp; ")
                ligne = ligne.replace("__TNID__" + str(j), " ")

            self.repfile.write(ligne)
            
        self.repfile.write("<TABLE WIDTH=\"720\"><TR><TD>&nbsp;</TD></TR>" + \
                           "<TR><TD><P ALIGN=\"LEFT\">")
        for i in range(len(self.tnId)):
            if self.tnName[i] != "":
                self.repfile.write("<TT>" + self.tnId[i] + " -- " + \
                               self.tnTs[i].replace("  ", " &nbsp;") + " -- " + \
                               self.tnName[i] + "</TT><BR>\n")
            else:
                self.repfile.write("<TT STYLE=\"color: blue\">" + self.tnId[i] + " ** " + \
                                   " no matching Catalog entry found " + \
                                   " ** " + "</TT><BR>\n")
                               
        self.repfile.write("</P></TD></TR><TR><TD>&nbsp;</TD></TR></TABLE>")
        
        self.tnId    = []
        self.tnFname = []
        self.tnTs    = []
        self.tnName  = []


    def printOrphanCatEnt(self, OrphanICat):
        """ Print orphan catalog entry.  """    
        if OrphanICat != []:
            endOrphanSection = False
            for ligne in HtOrphans:
                if ligne.find("__ORPHANENTRY__") >= 0:
                    oprhanLine = ligne
                    break
                else:
                    self.repfile.write(ligne)

            for iCat in OrphanICat:
                catEntry = getCatEntry (iCat)
                Ts = catEntry[0][0]
                Name = catEntry[0][1]
                str = "<TT>" + ("%04i" % iCat) + " -- " + \
                      Ts.replace("  ", " &nbsp;") + " -- " + Name + "</TT><BR>\n"
                ligne = oprhanLine.replace("__ORPHANENTRY__", str)
                self.repfile.write(ligne)
                           
            for ligne in HtOrphans:
                if ligne.find("__ORPHANENTRY__") < 0:
                    if endOrphanSection:
                        self.repfile.write(ligne)
                else:
                    endOrphanSection = True
        
            
    def flush(self, statstring):
        """ Process the report body and the report end.  """
        from vinutils import TNStreams
        from vinutils import Catalog

        self.headwrite()

        self.rownumber = 0
        self.tnId    = []
        self.tnFname = []
        self.tnTs    = []
        self.tnName  = []
        
#        for (iTN, vType, filename) in TNStreams:
        for iTN in TNStreams:
            for (vType, filename) in TNStreams[iTN]:
                self.tnId.append("%04i" % iTN)
                self.tnFname.append(filename)
                catEntry = getCatEntry (iTN)
                if len(catEntry) == 0:
                    Ts = ""
                    Name = ""
                elif len(catEntry) >= 1:
                # duplicate index numbers not properly handled !!!
                    Ts = catEntry[0][0]
                    Name = catEntry[0][1]
                self.tnTs.append(Ts)
                self.tnName.append(Name)
                if len(self.tnId) >= 5:
                    self.rowflush()
            
        if len(self.tnId) > 0:
            self.rowflush()
            
        # Scanning for orphan catalog entries
        OrphanICat = []
        for iCat in Catalog:
            if not TNStreams.has_key(iCat):
                OrphanICat.append(iCat)
        self.printOrphanCatEnt(OrphanICat)
        
        self.close(statstring)
