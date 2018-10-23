from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import urllib.request
import zipfile
import os
import sys
import getopt

def read_url( url ) :
    jsonURL = []
    url = url.replace( ' ', '%20' )
    req = Request( url )
    a = urlopen( req ).read()
    soup = BeautifulSoup( a, 'html.parser' )
    x = ( soup.find_all( 'a' ) )
    for i in x :
        fileName = i.extract().get_text()
        newURL = url + fileName
        newURL = newURL.replace( ' ', '%20' )
        if ( fileName[-1] == '/' ) and ( fileName[0] != '.' ) :
            read_url( newURL )
        jsonURL.append( [newURL, fileName] )
    return jsonURL

def download_tra_json( jsonURL, outputFolder = './' ) :
    if str( jsonURL ).split( '/' )[-1].split( '.' )[-1].split( '\'' )[0].lower() != 'zip' :
        return
    if outputFolder[-1] != '/' :
        outputFolder = outputFolder + '/'
    try :
        print( jsonURL[1] + ' 下載中...', end ='' )
        urllib.request.urlretrieve( jsonURL[0], outputFolder + jsonURL[1] )
        if os.path.exists( outputFolder + jsonURL[1] ) :
            print( '\r' + jsonURL[1] + ' 下載成功' )
            if zipfile.is_zipfile( outputFolder + jsonURL[1] ) :
                zipHandler = zipfile.ZipFile( outputFolder + jsonURL[1], 'r' )
                print( '解壓縮... ' + zipHandler.namelist()[0] )
                zipHandler.extractall( outputFolder )
                zipHandler.close()
            os.remove( outputFolder + jsonURL[1] )
            print( jsonURL[1] + ' 已刪除  ' )
        else:
            print( '\r' + jsonURL[1] + ' 下載失敗' )
    except OSError as err :
        print( '\nOS error: {0}'.format( err ) )
    except ValueError :
        print( '\nCould not convert data to an integer.' )
    except :
        print( '\nUnexpected error:', sys.exc_info()[0] )

def print_usage( name ) :
    print( 'usage: ' + name + ' [-a] [-h] [-o outputfolder] [-p] [--all] [--help] [--outputfolder outputfolder] [--print] [date ...]' )
    exit()

# Entry point
outputFolder = 'JSON'
selectAll = False
printAll = False
optList = []
dateList = []
if len( sys.argv ) > 1 :
    optList, dateList = getopt.getopt( sys.argv[1:], 'aho:p', [ 'all', 'help', 'outputfolder=', 'print' ] )
    if len( optList ) > 0 :
        for opt in optList :
            if ( opt[0] == '-a' ) or ( opt[0] == '--all' ) :
                selectAll = True
            elif ( opt[0] == '-h' ) or ( opt[0] == '--help' ) :
                print_usage( sys.argv[0] )
            elif ( opt[0] == '-o' ) or ( opt[0] == '--outputfolder' ) :
                outputFolder = opt[1]
            elif ( opt[0] == '-p' ) or ( opt[0] == '--print' ) :
                printAll = True
            else :
                print( 'unknown option \'' & opt[0] & '\'' )
                print_usage( sys.argv[0] )
items = read_url( 'http://163.29.3.98/json/' )
items.sort()
if printAll :
    for item in items :
        print( item )
if selectAll or ( len( dateList ) == 0 ) :
    for item in items :
        download_tra_json( item, outputFolder = outputFolder + '/' )
else :
    midList = []
    handleList = []
    for dateItem in dateList :
        subList = dateItem.replace( ',', ' ' ).split()
        for x in subList :
            midList.append( x )
    midList.sort()
    needItem = midList[0]
    existItem = items[0]
    while len( midList ) > 0 and len( dateList ) > 0 :
        if existItem[1].find( needItem ) >= 0 :
            handleList.append( existItem )
            midList.remove( midList[0] )
            items.remove( items[0] )
            if len( midList ) > 0 and len( dateList ) > 0 :
                needItem = midList[0]
                existItem = items[0]
        elif needItem < existItem[1] :
            midList.remove( midList[0] )
            if len( midList ) > 0 :
                needItem = midList[0]
        else :
            items.remove( items[0] )
            if len( items ) > 0 :
                existItem = items[0]
    if len( handleList ) > 0 :
        for item in handleList :
            download_tra_json( item, outputFolder = outputFolder + '/' )
