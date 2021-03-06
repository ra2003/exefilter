#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
"""
ExeFilter - main module / programme principal

ExeFilter is an open-source tool and framework to filter file formats in
e-mails, web pages or files. It detects many common file formats and can remove
active content (scripts, macros, etc) according to a configurable policy.

ExeFilter permet de filtrer des fichiers, courriels ou pages web, afin de
supprimer tout code ex�cutable et tout contenu potentiellement dangereux en
termes de s�curit� informatique.

ExeFilter peut �tre employ� soit comme script (lanc� directement depuis la
ligne de commande), soit comme module (import� dans un autre script).

Lanc� comme script, ExeFilter d�pollue un ensemble de fichiers situ�s dans un
r�pertoire et place le r�sultat dans un r�pertoire destination.
La source et la destination peuvent �tre fournies en ligne de commande,
ou bien gr�ce � la fonction transfert() si ce module est import�.

Ce fichier fait partie du projet ExeFilter.
URL du projet: U{http://www.decalage.info/exefilter}

@organization: DGA/CELAR
@author: U{Philippe Lagadec<mailto:philippe.lagadec(a)laposte.net>}
@author: U{Arnaud Kerr�neur<mailto:arnaud.kerreneur(a)dga.defense.gouv.fr>}
@author: U{Tanguy Vinceleux<mailto:tanguy.vinceleux(a)dga.defense.gouv.fr>}

@contact: U{Philippe Lagadec<mailto:philippe.lagadec(a)laposte.net>}

@copyright: DGA/CELAR 2004-2008
@copyright: NATO/NC3A 2008-2011 (modifications PL apres ExeFilter v1.1.0)

@license: CeCILL (open-source compatible GPL)
          cf. code source ou fichier LICENCE.txt joint

@version: 1.18

@status: beta
"""

#==============================================================================
__docformat__ = 'epytext en'

#__author__  = "Philippe Lagadec, Tanguy Vinceleux, Arnaud Kerr�neur (DGA/CELAR)"
__date__    = "2011-08-25"
__version__ = "1.18"

#------------------------------------------------------------------------------
# LICENCE pour le projet ExeFilter:

# Copyright DGA/CELAR 2004-2008
# Copyright NATO/NC3A 2008-2010 (modifications PL apres ExeFilter v1.1.0)
# Auteurs:
# - Philippe Lagadec (PL) - philippe.lagadec(a)laposte.net
# - Arnaud Kerr�neur (AK) - arnaud.kerreneur(a)dga.defense.gouv.fr
# - Tanguy Vinceleux (TV) - tanguy.vinceleux(a)dga.defense.gouv.fr
#
# Ce logiciel est r�gi par la licence CeCILL soumise au droit fran�ais et
# respectant les principes de diffusion des logiciels libres. Vous pouvez
# utiliser, modifier et/ou redistribuer ce programme sous les conditions
# de la licence CeCILL telle que diffus�e par le CEA, le CNRS et l'INRIA
# sur le site "http://www.cecill.info". Une copie de cette licence est jointe
# dans les fichiers Licence_CeCILL_V2-fr.html et Licence_CeCILL_V2-en.html.
#
# En contrepartie de l'accessibilit� au code source et des droits de copie,
# de modification et de redistribution accord�s par cette licence, il n'est
# offert aux utilisateurs qu'une garantie limit�e.  Pour les m�mes raisons,
# seule une responsabilit� restreinte p�se sur l'auteur du programme,  le
# titulaire des droits patrimoniaux et les conc�dants successifs.
#
# A cet �gard  l'attention de l'utilisateur est attir�e sur les risques
# associ�s au chargement,  � l'utilisation,  � la modification et/ou au
# d�veloppement et � la reproduction du logiciel par l'utilisateur �tant
# donn� sa sp�cificit� de logiciel libre, qui peut le rendre complexe �
# manipuler et qui le r�serve donc � des d�veloppeurs et des professionnels
# avertis poss�dant  des  connaissances  informatiques approfondies.  Les
# utilisateurs sont donc invit�s � charger  et  tester  l'ad�quation  du
# logiciel � leurs besoins dans des conditions permettant d'assurer la
# s�curit� de leurs syst�mes et ou de leurs donn�es et, plus g�n�ralement,
# � l'utiliser et l'exploiter dans les m�mes conditions de s�curit�.
#
# Le fait que vous puissiez acc�der � cet en-t�te signifie que vous avez
# pris connaissance de la licence CeCILL, et que vous en avez accept� les
# termes.

#------------------------------------------------------------------------------
# HISTORIQUE:
# 2004-10-24 v0.01 PL: - 1�re version (Sas de d�pollution)
# 2004-2006  PL,AK,TV: - Nombreuses �volutions
# 2007-06-20 v1.01 PL: - Licence CeCILL, transformation en ExeFilter
# 2007-07-24       PL: - Appel � get_username pour ameliorer la portabilit�
# 2007-09-13       PL: - Am�lioration portabilit� constantes, imports
# 2007-10-08       PL: - Ajout option -e pour exporter la politique en HTML
#                      - Journal syslog desactive par defaut
# 2007-10-22       PL: - Ajout options antivirus
# 2008-02-29       PL: - correction banniere et rapport avec XF_VERSION/DATE
# 2008-03-23 v1.02 PL: - ajout gettext dans programme principal pour traduction
#                      - ajout _() a chaque constante chaine pour traduction
#                      - ajout parametre pour activer l'archivage (non par d�faut)
#                      - code archivage deplace de transfert vers init_archivage
# 2009-10-05 v1.03 PL: - set default encoding to Latin-1 to avoid unicode errors
# 2009-10-22 v1.04 PL: - archiving disabled by default
# 2009-11-02 v1.05 PL: - init_gettext always called, even when imported
#                      - updated parameters for gettext translation
# 2009-11-11 v1.06 PL: - added new CLI option -o for a single output file
#                      - added translation for CLI options and summary
#                      - added parameters to set exit code according to results
# 2010-02-04 v1.07 PL: - removed commun.sous_rep_temp to avoid race conditions
#                      - avoid exceptions when username or locale cannot be
#                        determined
# 2010-02-07 v1.08 PL: - added batch mode option to disable HTML report display
#                      - removed path module import
# 2010-02-09 v1.09 PL: - workaround when username cannot be determined
# 2010-02-23 v1.10 PL: - removed plx import
# 2010-04-20 v1.11 PL: - added new option -f to force filename extension
# 2010-05-02 v1.12 PL: - added display_html_report to display HTML report
# 2010-09-24 v1.13 PL: - translated log folder names to English
#                      - no log file by default
# 2010-12-03 v1.14 PL: - new command line option -l to enable log file
# 2011-02-18 v1.15 PL: - now uses the system temp dir by default
# 2011-04-17 v1.16 PL: - scan-only mode when no destination is specified
# 2011-04-30 v1.17 PL: - new functions to scan and clean files or dirs
# 2011-08-25 v1.18 PL: - added initial support for multithreading
#                      - added scan_string and clean_string functions

#------------------------------------------------------------------------------
# TODO:
# + improve scan_string and clean_string (see TODOs)
# + improve logfile support in scan/clean functions
# + add option to set log file names or "auto" for automatic name
# + add option to set log file level
# + handle assert errors with -o option
# - fix init_gettext() when application is compiled with py2exe
# + finir traduction gettext
# + traduire codes parametres en anglais (pour avoir une config homogene)
# + decouper transfert() en plusieurs fonctions pour une utilisation plus generique
#------------------------------------------------------------------------------

#=== GETTEXT =================================================================

def init_gettext():
    """
    gettext initialization, in order to translate necessary strings at runtime.
    This MUST be done before any import or usage of _() around strings.
    """
    # Gettext pour adapter certaines chaines de caracteres a la langue du
    # systeme (traduction en anglais ou francais)
    # => DOIT etre fait avant toute constante chaine _("...") et tout import
    import gettext, locale, os.path
    # repertoire "locale": normalement un sous-repertoire du script principal
    #locale_dir = os.path.join(plx.get_main_dir(), "locale")
    # locale dir is a subfolder of this script's folder:
    #TODO: fix this when compiled with py2exe...
    locale_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'locale')
    #print 'locale_dir =', locale_dir
    # initialisation de la locale (cf. doc Python): est-ce toujours necessaire ?
    locale.setlocale(locale.LC_ALL, '')
    # langue du systeme: 2 premieres lettres de la locale/lang
    try:
        lang = locale.getdefaultlocale()[0][:2]
    except:
        # workaround if locale cannot be determined
        lang = 'en'
    #print 'lang =', lang
    if lang != 'fr':
        # ordre prefere des langues: 1) systeme, 2) english, 3) francais
        languages=[lang, 'en', 'fr']
        # On charge la langue correspondante depuis le repertoire locale:
        try:
            gt = gettext.translation("ExeFilter", locale_dir, languages)
            # puis on installe la fonction de traduction _():
            gt.install(unicode=True)
        except:
            # en cas d'erreur, on doit quand meme definir _() comme une fonction
            # "builtin" qui renvoie la chaine inchangee:
            __builtins__._ = lambda text: text
    else:
        # si la langue est 'fr', on n'utilise aucune traduction:
        gettext.NullTranslations().install()
        #__builtins__._ = lambda text: text


# always init gettext first
init_gettext()


#=== IMPORTS ==================================================================

# modules standards Python:
import os, sys, time, socket, optparse, tempfile, os.path
import threading

# hack to change default encoding to Latin-1 instead of ASCII:
reload(sys)
sys.setdefaultencoding( "latin-1" )

# modules sp�cifiques � Windows:
if sys.platform == 'win32':
    try:
        import win32api , win32security
    except:
        raise ImportError, "the pywin32 module is not installed: "\
                           "see http://sourceforge.net/projects/pywin32"

# modules d'ExeFilter:
from commun import *
import Politique
import Rapport
import Journal
import Conteneur_Repertoire
import Conteneur_Fichier
import Parametres
# numero de version global (provenant de __init__.py)
from __init__ import __version__ as XF_VERSION
from __init__ import __date__ as XF_DATE

#TODO: a supprimer
import commun     # (n�cessaire pour certaines variables globales)
import Conteneur  # pour importer la variable Conteneur.RACINE_TEMP


#=== CONSTANTES ===============================================================

REP_RAPPORT    = os.path.join("log", "reports")+os.sep # log\reports\
REP_LOG        = os.path.join("log", "logs")+os.sep # log\logs\
#REP_TEMP       = "temp" + os.sep        # temp\
REP_ARCHIVE    = "archive" + os.sep   # archive\
TAILLE_TEMP    = 10000    # taille max r�pertoire temp, en Mo
TAILLE_ARCHIVE = 10000    # taille max archive, en Mo

# default exit codes for result:
EXITCODE_CLEAN   = 0    # clean content
EXITCODE_BLOCKED = 1    # blocked content
EXITCODE_CLEANED = 2    # cleaned content
EXITCODE_ERROR   = 3    # error during analysis


#=== VARIABLES GLOBALES =======================================================

#TODO: a supprimer pour permettre plusieurs transferts simultan�s
# (or use threading.local)
nom_rapport       = None
nom_journal_secu  = None
nom_journal_debug = None
transfert_termine = False

# full path of the security logfile:
path_logfile = None
# full path of the debug logfile:
path_debugfile = None

# ExeFilter parameters, with default values:
parametres = {}

#--- REPERTOIRES ---
Parametres.Parametre("rep_rapports", str, nom=_(u"R�pertoire des fichiers rapports"),
    description=_(u"R�pertoire o� sont stock�s tous les fichiers rapports"),
    valeur_defaut = REP_RAPPORT).ajouter(parametres)
Parametres.Parametre("rep_journaux", str, nom=_(u"R�pertoire des fichiers journaux"),
    description=_(u"R�pertoire o� sont stock�s tous les fichiers journaux"),
    valeur_defaut = REP_LOG).ajouter(parametres)
Parametres.Parametre("rep_temp", str, nom=_(u"R�pertoire des fichiers temporaires"),
    description=_(u"R�pertoire o� sont stock�s tous les fichiers temporaires"),
    valeur_defaut = 'auto').ajouter(parametres)
Parametres.Parametre("rep_archives", str, nom=_(u"R�pertoire des fichiers archiv�s"),
    description=_(u"R�pertoire o� sont archiv�s tous les fichiers transf�r�s"),
    valeur_defaut = REP_ARCHIVE).ajouter(parametres)
Parametres.Parametre("taille_temp", int, nom=_(u"Taille maximale du r�pertoire temporaire (en octets)"),
    description=_(u"Taille maximale du r�pertoire o� sont stock�s tous les fichiers temporaires"),
    valeur_defaut = TAILLE_TEMP*1000000).ajouter(parametres)
Parametres.Parametre("taille_archives", int, nom=_(u"Taille maximale des archives (en octets)"),
    description=_(u"Taille maximale du r�pertoire o� sont archiv�s tous les fichiers transf�r�s"),
    valeur_defaut = TAILLE_ARCHIVE*1000000).ajouter(parametres)

#--- JOURNAUX ---
Parametres.Parametre("journal_securite", bool, nom=_(u"Ecrire un journal s�curit� dans un fichier"),
    description=_(u"Le journal s�curit� d�crit synth�tiquement les �v�nements concernant la s�curit� des transferts."),
    valeur_defaut = False).ajouter(parametres)
Parametres.Parametre("journal_syslog", bool, nom=_(u"Envoyer un journal s�curit� par syslog"),
    description=_("Le journal s�curit� d�crit synth�tiquement les �v�nements "
    "concernant la s�curit� des transferts. Syslog permet de centraliser ces "
    "journaux par le r�seau sur un serveur"),
    valeur_defaut = False).ajouter(parametres)
Parametres.Parametre("journal_debug", bool, nom=_("Ecrire un journal technique de d�bogage"),
    description=_("Le journal technique contient les �v�nements d�taill�s des "
        "transferts, pour un d�bogage en cas de probl�me."),
    valeur_defaut = False).ajouter(parametres)
Parametres.Parametre("serveur_syslog", str, nom=_("Serveur syslog (nom ou adresse IP)"),
    description=_("Nom ou adresse IP du serveur syslog qui centralise les journaux s�curit�."),
    valeur_defaut = "localhost").ajouter(parametres)
Parametres.Parametre("port_syslog", int, nom=_("Port syslog (num�ro de port UDP)"),
    description=_("Num�ro de port UDP du serveur syslog: 514 pour un serveur syslog standard."),
    valeur_defaut = 514).ajouter(parametres)

#--- AUTRES PARAMETRES ---
Parametres.Parametre("archive_after", bool, nom=_(u"Archiver tous les fichiers apres filtrage"),
    description=_(u"Pour archiver une copie de chaque fichier filtr� dans un r�pertoire d'archivage."),
    valeur_defaut = False).ajouter(parametres)

Parametres.Parametre("exitcode_clean", int, nom='Exit code when overall result is clean',
    description='Exit code (errorlevel) returned by ExeFilter when all analyzed '
        'files are clean. (only works with -o option for now)',
    valeur_defaut = EXITCODE_CLEAN).ajouter(parametres)
Parametres.Parametre("exitcode_cleaned", int, nom='Exit code when overall result is cleaned',
    description='Exit code (errorlevel) returned by ExeFilter when at least some analyzed '
        'files have been cleaned. (only works with -o option for now)',
    valeur_defaut = EXITCODE_CLEANED).ajouter(parametres)
Parametres.Parametre("exitcode_blocked", int, nom='Exit code when overall result is blocked',
    description='Exit code (errorlevel) returned by ExeFilter when all analyzed '
        'files are blocked. (only works with -o option for now)',
    valeur_defaut = EXITCODE_BLOCKED).ajouter(parametres)
Parametres.Parametre("exitcode_error", int, nom='Exit code when overall result is error',
    description='Exit code (errorlevel) returned by ExeFilter when an error '
        'occurred during the analysis. (only works with -o option for now)',
    valeur_defaut = EXITCODE_ERROR).ajouter(parametres)

#--- ANTIVIRUS ---

# ClamAV (clamd):
Parametres.Parametre("antivirus_clamd", bool, nom=_("Utiliser l'antivirus ClamAV (serveur clamd)"),
    description=_("Utiliser la version serveur de l'antivirus ClamAV (clamd) "
               "pour analyser les fichiers acceptes. Clamd doit tourner en "
               "tant que service sur la machine locale."),
    valeur_defaut = False).ajouter(parametres)
Parametres.Parametre("clamd_serveur", str, nom=_("Adresse IP ou nom du serveur antivirus clamd"),
    description=_("En general le serveur clamd tourne sur la meme machine: localhost."),
    valeur_defaut = 'localhost').ajouter(parametres)
Parametres.Parametre("clamd_port", int, nom=_("Port du serveur antivirus clamd"),
    description=_("En general le serveur clamd tourne sur le port 3310."),
    valeur_defaut = 3310).ajouter(parametres)

# F-Prot 6.x (fpscan):
Parametres.Parametre("antivirus_fpscan", bool, nom=_("Utiliser l'antivirus F-Prot 6 (fpscan)"),
    description=_("Utiliser la version ligne de commande de l'antivirus F-Prot 6 "
               "(fpscan) pour analyser les fichiers acceptes. Attention cela "
               "peut degrader significativement les performances."),
    valeur_defaut = False).ajouter(parametres)
if sys.platform == 'win32': fpscan_defaut = "c:\\Program Files\\FRISK Software\\F-PROT Antivirus for Windows\\fpscan.exe"
else:                       fpscan_defaut = "fpscan" # on suppose qu'il est dans le PATH
Parametres.Parametre("fpscan_executable", str, nom=_("Ex�cutable de l'antivirus F-Prot 6 (fpscan)"),
    description=_("Emplacement du fichier fpscan de l'antivirus F-Prot 6"),
    valeur_defaut = fpscan_defaut).ajouter(parametres)

# F-Prot 3.x (fpcmd, obsolete):
Parametres.Parametre("antivirus_fpcmd", bool, nom=_("Utiliser l'antivirus F-Prot 3 (fpcmd)"),
    description=_("Utiliser la version ligne de commande de l'antivirus F-Prot 3 "
               "(fpcmd) pour analyser les fichiers acceptes. Attention cela "
               "peut degrader significativement les performances."),
    valeur_defaut = False).ajouter(parametres)
#TODO: verifier le chemin par defaut + am�liorer portabilit�
if sys.platform == 'win32': fpcmd_defaut = "c:\\Program Files\\FRISK Software\\F-PROT Antivirus for Windows\\fpcmd.exe"
else:                       fpcmd_defaut = "fpcmd" # on suppose que fpcmd est dans le PATH
Parametres.Parametre("fpcmd_executable", str, nom=_("Ex�cutable de l'antivirus F-Prot 3 (fpcmd)"),
    description=_("Emplacement du fichier fpcmd de l'antivirus F-Prot 3"),
    valeur_defaut = fpcmd_defaut).ajouter(parametres)



#=== FONCTIONS ================================================================

#------------------------------------------------------------------------------
# GET_JOURNAL
#-------------------
def get_journal() :
    """
    Retourne le chemin du fichier journal securite.
    Si le fichier journal n'est pas encore cr��, renvoie None

    @return: le chemin du fichier journal
    @rtype: str
    """
    return path_logfile
##    global nom_journal_secu
##    if nom_journal_secu == None:
##        #TODO: renvoyer une valeur par defaut ?
##        return None
##    else:
##        rep_journaux = path(p.parametres['rep_journaux'].valeur)
##        return (rep_journaux / nom_journal_secu).abspath()

#------------------------------------------------------------------------------
# GET_JOURNAL_DEBUG
#-------------------
def get_journal_debug() :
    """
    Retourne le chemin du fichier journal de d�bogage.
    Si le fichier journal n'est pas encore cr��, renvoie None

    @return: le chemin du fichier journal
    @rtype: str
    """
    return path_debugfile
    global nom_journal_debug
    if nom_journal_debug == None:
        #TODO: renvoyer une valeur par defaut ?
        return None
    else:
        rep_journaux = path(p.parametres['rep_journaux'].valeur)
        return (rep_journaux / nom_journal_debug).abspath()

#------------------------------------------------------------------------------
# GET_RAPPORT
#-------------------

def get_rapport() :
    """
    Retourne le chemin d'acc�s au fichier contenant le rapport au format html
    Si le fichier du rapport n'est pas encore cr��, renvoie None

    @return: chemin d'acc�s au fichier contenant le rapport au format html
    @rtype: str
    """
    if nom_rapport == None:
        chemin_rapport = None
    else:
        #chemin_rapport = REP_RAPPORT + nom_rapport
        chemin_rapport = path(p.parametres['rep_rapports'].valeur) / nom_rapport
        chemin_rapport = chemin_rapport.abspath()
    return chemin_rapport


def display_html_report():
    """
    Display HTML report in the web browser
    """
    if get_rapport():
        plx.display_html_file(os.path.abspath(get_rapport()+'.html'))


#------------------------------------------------------------------------------
# CANCEL_TRANSFERT
#-------------------

def cancel_transfert ():
    """
    Annule le transfert en cours
    """
    commun.continuer_transfert = False

#------------------------------------------------------------------------------
# GET_NB_FICHIERS
#-------------------

def get_nb_fichiers ():
    """
    Retourne le nombre de fichiers � analyser ou None si le moteur
    n'a pas encore commenc� le transfert

    @return: le nombre de fichiers � analyser
    @rtype: int
    """
    if commun.transfert_commence == True : return commun.nb_fichiers
    else : return None

#------------------------------------------------------------------------------
# GET_COMPTEUR_AVANCEMENT
#-------------------------

def get_compteur_avancement ():
    """
    Retourne le nombre fichiers d�j� analyser ou None si le moteur
    n'a pas encore commenc� le transfert

    @return: le nombre de fichiers d�j� analys�s
    @rtype: int
    """
    if commun.transfert_commence == True : return commun.compteur_avancement
    else : return None


def init_archivage(politique, taille_src):
    """
    Preparation du repertoire d'archivage avant transfert.

    @param politique: objet Politique employe pour le transfert
    @param taille_src: taille totale des fichiers source a nettoyer, en octets
    """
    # si le repertoire d'archivage n'existe pas, on le cree:
    chem_arc = path(politique.parametres['rep_archives'].valeur)
    try:
        os.makedirs(chem_arc)
    except:
        pass
    # calcul de la taille actuelle du r�pertoire archivage
    taille_arc = 0
    for f in chem_arc.walkfiles():
        taille_arc += f.size

    # test si la taille des fichiers source est sup�rieure � celle du r�p d'archivage
    # si c'est le cas, on g�n�re une exception
    if taille_src >    politique.parametres['taille_archives'].valeur:
        msg = _(u"La taille des fichiers source est superieure a la taille du repertoire d'archivage.")
        Journal.error(msg)
        raise RuntimeError, msg

    # boucle pour effacer les sous-r�p les plus anciens dans le cas o� il n'y a pas assez
    # d'espace disque dans le r�p archivage pour copier les fichiers source
    while politique.parametres['taille_archives'].valeur < taille_arc + taille_src:
        date_archive = 0
        taille_rep_archive = 0
        # boucle pour d�terminer quel est le sous-r�p archive le plus ancien
        for rep in chem_arc.dirs():
            if date_archive == 0:
                # on r�cup�re la date du 1er sous-r�p archive lu
                date_archive = os.path.getmtime(rep)
                rep_archive = rep
            # si la date du sous-r�p archive lu est inf�rieure � date_archive,
            # ce sous-r�p devient le plus ancien
            elif date_archive > os.path.getmtime(rep):
                date_archive = os.path.getmtime(rep)
                rep_archive = rep
        if os.path.exists(rep_archive):
            # calcul de la taille du sous-r�p archive le plus ancien
            for rep in rep_archive.walkfiles():
                taille_rep_archive += rep.size
            # on met � jour la taille du r�p temp principal
            taille_arc = taille_arc - taille_rep_archive
            # on efface le sous-r�p temp le plus ancien
            rep_archive.rmtree()
        else:
            # s'il n'y a plus de sous-r�p archive � effacer, on g�n�re une exception
            msg = _(u"repertoire d'archivage deja vide => taille source trop grande")
            Journal.error(msg)
            raise RuntimeError, msg



#------------------------------------------------------------------------------
# TRANSFERT
#-------------------

# lock for multithreading
lock_transfert = threading.Lock()

def transfert(liste_source, destination, type_transfert="entree", handle=None,
              pol=None, dest_is_a_file=False, force_extension=None,
              logfile=None):
    """
    Main function to scan or clean files and directories.
    (thread safe: uses a lock to make sure only one thread runs it)

    Lance le transfert et l'analyse des r�pertoires et/ou fichiers source

    @param liste_source: la liste des sources � transf�rer
    @type  liste_source: list

    @param destination: destination directory, or None/'' for scan-only mode
    @type  destination: str

    @param type_transfert: le type de transfert pour charger la politique de filtre
    @type  type_transfert: str

    @param handle: le handle de connexion a utiliser pour ex�cuter le filtre
    @type  handle: pyHandle

    #@param taille_temp: taille maximale du r�pertoire temporaire, en octets. Taille par d�faut 10Go (DVD double couche)
    #@type  taille_temp: int

    @param dest_is_a_file: False if destination is a dir (default),
                           True if it's a filename.
    @type dest_is_a_file: bool

    @param force_extension: if set, force filename extension to a specific value
                            (used to control which filters are applied)
                            Note: force_extension may be "" or must start with a dot
    @type  force_extension: str, unicode
    """
    # run the function with a lock to make sure only one thread can run it at a
    # time:
    with lock_transfert:
        exitcode = _transfert_not_threadsafe(liste_source, destination,
            type_transfert, handle, pol, dest_is_a_file, force_extension,
            logfile)
    return exitcode


def _transfert_not_threadsafe(liste_source, destination, type_transfert="entree", handle=None,
              pol=None, dest_is_a_file=False, force_extension=None,
              logfile=None):
    """
    Main function to scan or clean files and directories.
    Not thread safe: should not be called directly, use transfert() instead.
    """
    global nom_journal_secu
    global path_logfile
    global nom_journal_debug
    global path_debugfile
    global nom_rapport
    global p

    # obsolete, to be removed?
    if sys.platform == 'win32':
        if handle != None :
            win32security.ImpersonateLoggedOnUser(handle)

    taille_src = 0

    # on r�cup�re le nom de l'utilisateur qui lance ExeFilter, avec nom de
    # domaine (ou de machine) sous Windows:
    try:
        username = get_username()
        username_withdomain = get_username(with_domain=True)
    except:
        # workaround if user name cannot be determined
        username = username_withdomain = 'unknown'

    # cr�ation du tronc commun pour les noms des journaux et des rapports:
    nom_machine = socket.gethostname()
    date = time.strftime("%Y-%m-%d", time.localtime())
    heure = time.strftime("%Hh%Mm%Ss", time.localtime())
    nom_commun = date + "_" + nom_machine + "_" + username + "_" + heure

#    on transmet � transfert :
#            soit un objet Politique d�j� configur�,
#            soit un nom de fichier de config directement,
#            soit une liste de fichiers de config,
#            soit un mot-cl� " entree " ou " sortie " d�crivant le type de transfert,
#            afin de conserver la compatibilit� avec l'IHM actuelle. Dans ce cas le fichier de config filtres.cfg doit �tre analys� correctement.
    if pol != None:
        if isinstance(pol, Politique.Politique):
            p = pol
        elif isinstance (pol,  [file, str, unicode, list]):
            p = Politique.Politique(pol)
    # obsolete, to be removed?
    elif type_transfert in ("entree", "sortie"):
            # v�rifier si le fichier existe
            # si le fichier existe alors on le charge
            # sinon politque par d�faut
            # p = Politique.Politique("politique_%s.cfg" % type_transfert)
            p = Politique.Politique()
    else:
        # politique par d�faut
        p = Politique.Politique()

    # store policy in a global variable: to be removed for multithreading
    commun.politique = p

    # nom des fichiers log = nom de la machine + date et heure du transfert
    if logfile == 'auto':
        print 'logfile=auto'
        # generate log filename automatically (one per session):
        nom_journal_secu = nom_commun + ".log"
        # set full path in logs folder:
        logs_folder = path(p.parametres['rep_journaux'].valeur)
        # make sure the logs folder exists (if logging to file is enabled):
        if (not os.path.exists(logs_folder)) and p.parametres['journal_securite'].valeur:
            logs_folder.makedirs()
        path_logfile = (logs_folder / nom_journal_secu).abspath()
    elif logfile:
        print 'logfile=%s' % logfile
        # use provided log filename:
        nom_journal_secu = logfile
        # set full path directly:
        path_logfile = path(nom_journal_secu).abspath()
    else:
        nom_journal_secu = None
        path_logfile = None

    # debug logfile: only handled via policy, auto name
    nom_journal_debug = "debug_" + nom_commun + ".log"
    # set full path in logs folder:
    logs_folder = path(p.parametres['rep_journaux'].valeur)
    # make sure the logs folder exists (if logging to file is enabled):
    if (not os.path.exists(logs_folder)) and p.parametres['journal_debug'].valeur:
        logs_folder.makedirs()
    path_debugfile = (logs_folder / nom_journal_debug).abspath()


    # cr�ation du journal d'�v�nements:
    Journal.init_journal(p, journal_secu = path_logfile, journal_debug = path_debugfile)

    # cr�ation des sous-r�pertoires temp et archivage:
    commun.sous_rep_archive = "transfert_" + nom_commun

    Journal.important(_(u"ExeFilter v%s lanc� par utilisateur %s sur la machine %s") %
        (XF_VERSION, username_withdomain, nom_machine))

    # on ajoute la politique dans le journal:
    p.journaliser()
    Journal.info2(_(u"D�but de l'analyse"))

    Rapport.liste_resultats = []

    # liste des r�pertoires et/ou fichiers source
    liste_conteneurs_source = []

    # initialisation des variables globales
    commun.nb_fichiers = commun.compteur_avancement = 0
    commun.continuer_transfert = True
    commun.transfert_commence = False

    # if destination is a single file, check if source is one file:
    if dest_is_a_file:
        assert(len(liste_source)==1)
        assert(os.path.isfile(liste_source[0]))

    # if destination is empty (None or ''), set mode to scan-only instead of clean:
    if destination:
        commun.clean_mode = True
        Journal.debug('Analysis mode: clean')
    else:
        commun.clean_mode = False
        Journal.debug('Analysis mode: scan only')
    Journal.debug('clean_mode=%s' % commun.clean_mode)


    # boucle pour lire chaque r�pertoire et/ou fichier contenu dans    la liste
    for source in liste_source :
        # on v�rifie le type de source: r�pertoire ou fichier ?
        if os.path.isdir(source):
            #rep_source = Conteneur_Repertoire.Conteneur_Repertoire (source, destination)

            # si source est G:/tutu/tata, rep_relatif_source = tata
            (head, tail) = os.path.split(source)
            rep_relatif_source = tail
            rep_source = Conteneur_Repertoire.Conteneur_Repertoire (source,
                destination, rep_relatif_source, politique=p)

            # calcul de la taille du r�pertoire source
            taille_src += rep_source.compter_taille_rep()

        else:
            #rep_source = Conteneur_Fichier.Conteneur_Fichier (source, destination)

            rep_relatif_source = ""
            rep_source = Conteneur_Fichier.Conteneur_Fichier (source,
                destination, rep_relatif_source, politique=p,
                dest_is_a_file=dest_is_a_file, force_extension=force_extension)

            # calcul de la taille du fichier source
            taille_src += os.stat(source).st_size

        # on ajoute les conteneurs source � la liste
        liste_conteneurs_source.append(rep_source)
        # on incr�mente le compteur nombre de fichiers total
        commun.nb_fichiers += rep_source.compter_nb_fichiers()

    # test si la taille des fichiers source est sup�rieure � celle du r�p temp
    # si c'est le cas, on g�n�re une exception
    #if taille_src > taille_temp:
    if taille_src >    p.parametres['taille_temp'].valeur:
        msg = "La taille des fichiers source est superieure a la taille du repertoire temporaire."
        Journal.error(msg)
        raise RuntimeError, msg

    # initialisation de l'archivage:
    if parametres['archive_after'].valeur:
        init_archivage(p, taille_src)
    commun.transfert_commence = True

    # boucle d'analyse de chaque conteneur source contenu dans la liste
    for conteneur_source in liste_conteneurs_source:
        Journal.info2(u"Analyse de contenu de %s ..." % conteneur_source)

        # ici il faudrait un try pour g�rer toutes les exceptions, journaliser
        # et nettoyer s'il y a des erreurs.
        # ou alors lancer un thread...

        # test de l'interruption de transfert par l'utilisateur
        if commun.continuer_transfert == True:
            # s'il n'y a pas d'interruption, on lance le nettoyage
            liste_resultat = conteneur_source.nettoyer(p)
        # s'il y a eu une interruption pendant nettoyer(), on s'arr�te
        if commun.continuer_transfert == False:
            break

    # g�n�ration du rapport
    nom_rapport = "rapport_" + nom_commun
    Journal.info2(u"G�n�ration du rapport: %s ..." % nom_rapport)
    chemin_rapport = p.parametres['rep_rapports'].valeur + nom_rapport
    resume = Rapport.generer_rapport(chemin_rapport,
                                      ', '.join(liste_source),  destination ,
                                      XF_VERSION,  XF_DATE, commun.continuer_transfert)
    Journal.info2(u"Fin de l'analyse")
    # log du r�sum� de la d�pollution
    Journal.important(_(u'R�sum� : %d fichiers analys�s ; '
        u'%d fichiers accept�s ; %d fichiers nettoy�s ; %d fichiers refus�s ; %d erreurs')
        % (resume[0], resume[1], resume[2], resume[3], resume[4]))

    if commun.continuer_transfert == False:
        Journal.warning(u"TRANSFERT ANNULE par l'utilisateur")

    # return exit code according to results:
    #TODO: use results from containers instead of this quick hack:
    clean   = resume[1]
    cleaned = resume[2]
    blocked = resume[3]
    errors  = resume[4]
    if errors:
        exitcode = p.parametres['exitcode_error'].valeur
    elif (clean+cleaned>0) and (cleaned+blocked>0):
        exitcode = p.parametres['exitcode_cleaned'].valeur
    elif (clean>0) and (cleaned+blocked == 0):
        exitcode = p.parametres['exitcode_clean'].valeur
    elif (blocked>0) and (clean+cleaned == 0):
        exitcode = p.parametres['exitcode_blocked'].valeur
    else:
        raise ValueError, 'Summary values look wrong...'
    Journal.debug('Exit code: %d' % exitcode)

    Journal.fermer_journal()
    return exitcode

    #return


def clean_dir(source_dir, dest_dir, policy=None, logfile=None):
    """
    Clean all files of a directory (source_dir) according to the specified
    policy, store the result in dest_dir.
    Optionally write log to logfile.
    Return an exit code according to the overall result (see doc).
    """
    # TODO: force logfile option in policy if logfile is set
    exitcode = transfert([source_dir], dest_dir, pol=policy, logfile=logfile)
    return exitcode


def scan_dir(source_dir, policy=None, logfile=None):
    """
    Scan all files of a directory (source_dir) according to the specified
    policy.
    Optionally write log to logfile.
    Return an exit code according to the overall result (see doc).
    """
    exitcode = transfert([source_dir], None, pol=policy, logfile=logfile)
    return exitcode


def clean_file(source_file, dest_file, policy=None, logfile=None):
    """
    Clean a single file (source_file) according to the specified policy,
    store the result in dest_file.
    Optionally write log to logfile.
    Return an exit code according to the overall result (see doc).
    """
    exitcode = transfert([source_file], dest_file, pol=policy, logfile=logfile,
        dest_is_a_file=True)
    return exitcode


def clean_file_to_dir(source_file, dest_dir, policy=None, logfile=None):
    """
    Clean a single file (source_file) according to the specified policy,
    store the result in a file with the same name in a destination directory
    (dest_dir).
    Optionally write log to logfile.
    Return an exit code according to the overall result (see doc).
    """
    exitcode = transfert([source_file], dest_dir, pol=policy, logfile=logfile)
    return exitcode


def scan_file(source_file, policy=None, logfile=None):
    """
    Scan a single file (source_file) according to the specified policy.
    Optionally write log to logfile.
    Return an exit code according to the overall result (see doc).
    """
    exitcode = transfert([source_file], None, pol=policy, logfile=logfile)
    return exitcode

# mapping from content-types to extensions corresponding to ExeFilter filters:
# (sources http://en.wikipedia.org/wiki/Internet_media_type,
#  http://www.iana.org/assignments/media-types/index.html
#  and http://www.w3schools.com/media/media_mimeref.asp)
# Note: we could have used mimetypes.guess_extension, but it does not work very
# well, for example for 'text/plain' it returns '.ksh'...
CT_to_ext = {
	'application/msword':       '.doc',
	'application/pdf':          '.pdf',
    'application/rtf':          '.rtf',
	'application/soap+xml':     '.xml',
	'application/vnd.ms-excel': '.xls',
	'application/vnd.ms-powerpoint': '.ppt',
    #TODO: add also the macro enabled versions from IANA, just in case
	'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': '.xlsx',
	'application/vnd.openxmlformats-officedocument.presentationml.presentation':   '.pptx',
	'application/vnd.openxmlformats-officedocument.wordprocessingml.document':   '.docx',
	'application/xhtml+xml':    '.html',
	'application/xml':          '.xml',
    'application/zip':          '.zip',
    'audio/mpeg':               '.mp3',
    'audio/vnd.wave':           '.wav',
    'image/gif':                '.gif',
    'image/jpeg':               '.jpg',
    'image/png':                '.png',
    'image/x-ms-bmp':           '.bmp',
	'message/rfc822':           '.eml',
	'text/html':                '.html',
	'text/plain':               '.txt',
	'text/xml':                 '.xml',
	'video/x-msvideo':          '.avi',
    }


def scan_string(data, filename=None, content_type=None, policy=None, logfile=None):
    """
    Scan a string according to the specified policy. The filename and/or the
    content-type may be provided (at least one of them is required).
    It will be used to select the right filter(s).

    If only the content-type is provided, a default file extension will be used.
    If both filename and content-type are given, content-type is ignored.
    The string will be written to a temporary file for analysis.
    NOTE: this is a quick and dirty solution which will be improved in future
          versions

    Optionally write log to logfile.
    Return an exit code according to the overall result (see doc).
    """
    if filename is not None:
        # only keep the filename, in case it contains a path with directories:
        # (to avoid directory traversal and other issues)
        fname = os.path.basename(filename)
        #ext = os.path.splitext(filename)[1]
    elif content_type is not None:
        if content_type not in CT_to_ext:
            #TODO: here we should return a "blocked" result rather than an exception
            raise ValueError, 'Content-type not allowed: "%s"' % content_type
        ext = CT_to_ext[content_type]
        # use a temporary filename = temp.ext
        fname = 'temp'+ext
    else:
        raise RuntimeError, 'Either filename or content-type is required'
    # create a new temporary dir to store the file with its original filename
    tempdir = tempfilemgr.newTempDir()
    fpath = os.path.join(tempdir, fname)
    #f, fname = tempfilemgr.newTempFile(suffix=ext)
    f = open(fpath, 'wb')
    f.write(data)
    f.close()
    exitcode = transfert([fpath], None, pol=policy, logfile=logfile)
    # remove temp file and dir:
    os.remove(fpath)
    os.rmdir(tempdir)
    return exitcode


def clean_string(data, filename=None, content_type=None, policy=None, logfile=None):
    """
    Clean a string according to the specified policy. The filename and/or the
    content-type may be provided (at least one of them is required).
    It will be used to select the right filter(s).

    If only the content-type is provided, a default file extension will be used.
    If both filename and content-type are given, content-type is ignored.
    The string will be written to a temporary file for analysis.
    NOTE: this is a quick and dirty solution which will be improved in future
          versions

    Optionally write log to logfile.
    Return a tuple (exitcode, cleaned_data):
    - exit code according to the overall result (see doc).
    """
    if filename is not None:
        # only keep the filename, in case it contains a path with directories:
        # (to avoid directory traversal and other issues)
        fname = os.path.basename(filename)
        #ext = os.path.splitext(filename)[1]
    elif content_type is not None:
        if content_type not in CT_to_ext:
            #TODO: here we should return a "blocked" result rather than an exception
            raise ValueError, 'Content-type not allowed: "%s"' % content_type
        ext = CT_to_ext[content_type]
        # use a temporary filename = temp.ext
        fname = 'temp'+ext
    else:
        raise RuntimeError, 'Either filename or content-type is required'
    # create a new temporary dir to store the file with its original filename
    tempdir = tempfilemgr.newTempDir()
    fpath = os.path.join(tempdir, fname)
    f = open(fpath, 'wb')
    f.write(data)
    f.close()
    # temp file for the cleaned destination:
    f, fdest = tempfilemgr.newTempFile()
    f.close()
    exitcode = transfert([fpath], fdest, pol=policy, logfile=logfile,
        dest_is_a_file=True)
    cleaned_data = open(fdest, 'rb').read()
    # remove temp files and dir:
    os.remove(fdest)
    os.remove(fpath)
    os.rmdir(tempdir)
    return (exitcode, cleaned_data)



#==============================================================================
# PROGRAMME PRINCIPAL
#=====================
# ne sert que si on appelle le module ExeFilter.py directement, sans passer par
# le module go.py qui lance la m�thode transfert du module ExeFilter.py dans un
# thread.

if __name__ == '__main__':
    # si compilation py2exe, il faut fixer ici le codec par d�faut, car il n'y
    # a pas de sitecustomize.py:
    if hasattr(sys,"setdefaultencoding"):
            sys.setdefaultencoding("iso-8859-1")

    # Banniere
    print "-"*79
    print "ExeFilter v%s - %s" % (XF_VERSION, XF_DATE)
    print "-"*79
    print ""

    # on cr�e un objet optparse.OptionParser pour analyser la ligne de commande:
    op = optparse.OptionParser(usage =
        _("%prog [options] <fichiers ou repertoires a nettoyer>"))

    op.add_option("-c", "--config", dest="config", default="",
        help=_("Fichier de configuration general pour ExeFilter"))
    op.add_option("-p", "--policy", dest="politique", default="",
        help=_("Fichier de configuration pour la politique de filtrage"))
    op.add_option("-d", "--dest", dest="destination", default="",
        help='Output directory for cleaned files (or scan-only mode if omitted)')
    op.add_option("-o", "--output", dest="output_file", default="",
        help="Output file (may only be used when source is a single file, instead of -d).")
    op.add_option("-v", "--verbose", action="store_true", dest="debug",
        default=False, help=_("Mode Debug (pour le developpement)"))
    op.add_option("-n", "--new", dest="nouv_politique", default='',
        help=_("Creer une nouvelle politique dans un fichier INI/CFG"))
    op.add_option("-e", "--export", dest="export_html", default='',
        help=_("Exporter la politique dans un fichier HTML"))
    op.add_option("-b", "--batch", action="store_true", dest="batchmode",
        default=False, help=_("Batch mode (do not open HTML report after analysis)"))
    op.add_option("-f", "--force-ext", dest="force_extension", default=None,
        help='Force filename extension to control which filters are applied')
    op.add_option("-l", "--logfile", dest="logfile", default='',
        help='Log messages to a file with the provided filename, '
            +'or "auto" for an automatic name in the logs folder')

    # on parse les options de ligne de commande:
    (options, args) = op.parse_args(sys.argv[1:])

    # si aucun fichier/r�pertoire � nettoyer, et si la destination n'est pas
    # sp�cifi�e, on force l'affichage de l'aide:
    if (len(args)==0 or (options.destination!="" and options.output_file!=""))\
        and options.export_html==''\
        and options.nouv_politique=='':
        op.print_help()
        print ""
        print 'Please specify files to be analyzed, and an optional destination.'
##        print _("Il faut indiquer les fichiers/repertoires a nettoyer, ainsi qu'une destination.")
        sys.exit(parametres['exitcode_error'].valeur)

    # on exploite les �ventuelles options
    if options.debug:
        mode_debug(True)

    # init console logging (after setting the debug mode if -v option):
    Journal.init_console_logging()

    # On cr�e d'abord une politique par d�faut:
    pol = Politique.Politique()
    # ensuite on charge le fichier de config g�n�ral si pr�cis�:
    if options.config:
        pol.lire_config(options.config)
    # puis le fichier de la politique:
    if options.politique:
        pol.lire_config(options.politique)

    # si l'option nouvelle politique est active on sauve la politique dans un
    # fichier INI:
    if options.nouv_politique != '':
        pol.ecrire_fichier(options.nouv_politique)
        print _('Politique sauvee dans le fichier %s') % options.nouv_politique
        sys.exit()

    # si l'option export est active on exporte la politique dans un fichier HTML:
    if options.export_html != '':
        pol.ecrire_html(options.export_html)
        print _('Politique exportee dans le fichier %s') % options.export_html
        sys.exit()

    # check force_extension option (-f):
    if options.force_extension is not None:
        # should be empty or start with a dot
        if options.force_extension != '' \
        and not options.force_extension.startswith('.'):
            # add the dot if missing:
            options.force_extension = '.' + options.force_extension

    # check logfile option (-l):
    if options.logfile:
        # force logfile parameter:
        #TODO: enable debug logfile instead if -v option?
        pol.parametres['journal_securite'].set(True)


    # enfin on lance le transfert:
    # (les r�pertoires et/ou fichiers source sont dans la liste args)
    try:
        if not options.output_file:
            # destination is a directory or none (scan-only mode):
            exitcode = transfert(args, options.destination, pol=pol,
                logfile=options.logfile)
        else:
            # destination is a filename:
            exitcode = transfert(args, options.output_file, pol=pol,
                                 dest_is_a_file=True,
                                 force_extension=options.force_extension,
                                 logfile=options.logfile)
    except:
        raise
        Journal.exception('Error during analysis')
        exitcode = pol.parametres['exitcode_error'].valeur

    # display HTML report in browser, unless batch mode is enabled:
    if not options.batchmode:
        display_html_report()

    sys.exit(exitcode)



# POUBELLE: code � utiliser plus tard ou � supprimer:

#/    op.add_option("-a", "--archive", dest="archive",
#/        default=parametres["rep_archives"].valeur_defaut,
#/        help="Repertoire d'archivage des fichiers nettoyes [%default]")
#/    op.add_option("-j", "--journaux", dest="journaux",
#/        default=parametres["rep_journaux"].valeur_defaut,
#/        help="Repertoire de stockage des journaux [%default]")
#/    op.add_option("-r", "--rapports", dest="rapports",
#/        default=parametres["rep_rapports"].valeur_defaut,
#/        help="Repertoire de stockage des rapports [%default]")
#/    op.add_option("-t", "--temp", dest="temp",
#/        default=parametres["rep_temp"].valeur_defaut,
#/        help="Repertoire pour les fichiers temporaires [%default]")
#/    op.add_option("-s", "--syslog", dest="syslog",
#/        default=parametres["serveur_syslog"].valeur_defaut+":"
#/        + str(parametres["port_syslog"].valeur_defaut), metavar="SERVEUR:PORT",
#/        help="Adresse IP ou nom du serveur syslog, et port UDP [%default]")
