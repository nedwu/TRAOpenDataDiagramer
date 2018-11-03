import sys
import os
from os import walk
import io
import getopt

import time

import dataprocess as dp
import svg_save

version = '0.1Alpha'
folders, dictDrawProfile = dp.diagramLayout()

def _make_next_date_filename( filename ) :
    dayMonth = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    yy = int( filename[0:4] )
    mm = int( filename[4:6] )
    dd = int( filename[6:8] )
    if yy % 4 != 0 :
        leap = False
    elif yy % 100 != 0 :
        leap = True
    elif yy % 400 != 0 :
        leap = False
    else :
        leap = True
    if dd < dayMonth[mm - 1] or mm == 2 and leap and dd < 29 :
        dd += 1
    else :
        dd = 1
        if mm < 12 :
            mm += 1
        else :
            mm = 1
            yy += 1
    return f'{yy:04d}{mm:02d}{dd:02d}.' + filename.split( '.' )[-1]

# create folder if is not existed
def _check_output_folder( path, folders ) :
    if os.path.exists( path ) == False :
        os.makedirs( path )
        diff = folders
    else :
        outputFolder = os.listdir( path )
        diff = list( set( folders ).difference( set( outputFolder ) ) )
    if len( diff ) > 0 :
        for item in diff :
            os.makedirs( path + '/' + item )
def main( jsonLocation, webSvgLocation, expertList, deleteAtExit ) :
    global version
    jsonFiles = []
    svgHandlerNext = None
    if webSvgLocation != '' :
        _check_output_folder( webSvgLocation, folders )
    for root, dirs, files in walk( jsonLocation + '/' ) :
        for item in files :
            jsonFiles.append( item )
    if len( jsonFiles ) != 0 :
        jsonFiles.sort()
        for filename in jsonFiles :            
            t1 = time.time()
            if filename.endswith( '.json' ) :
                nextFilename = _make_next_date_filename( filename )
                print( '資料檔日期：' + filename.split( '.' )[0] )
                count = 0
                trains = dp.read_json( jsonLocation, filename )
                total = len( trains )
                if svgHandlerNext is None :
                    svgHandler = svg_save.Draw( webSvgLocation, filename.split( '.' )[0], dictDrawProfile, version )
                else :
                    svgHandler = svgHandlerNext
                if os.path.exists( jsonLocation + '/' + nextFilename ) :
                    print( '有隔日資料檔 ("' + _make_next_date_filename( filename ) + '"), 跨日部分將繪製於隔日運行圖' )
                    svgHandlerNext = svg_save.Draw( webSvgLocation, nextFilename.split( '.' )[0], dictDrawProfile, version )
                    svgHandler.set_next_day_sheet( svgHandlerNext )
                else :
                    print( '沒有隔日資料檔, 跨日部分將不繪製' )
                    svgHandlerNext = None
                bar = "-" * 50
                percents = 0
                nextCount = total // 1000
                lastProcess = 0
                for trainInfo in trains :
                    trainId = trainInfo['Train']
                    count += 1
                    # update processing bar
                    if count >= nextCount :
                    	percents = count * 1000 // total
                    	nextCount = ( total * ( percents + 1 ) ) // 1000
                    	if percents // 20 != lastProcess :
                            lastProcess = percents // 20
                            bar = '=' * lastProcess + '-' * ( 50 - lastProcess )
                    sys.stdout.write( f'[{bar:s}] {( float( percents ) / 10 ):5.1f}% ...{trainId:>5s}次 處理中\r' )
                    sys.stdout.flush()
                    # find all train's passing station and time
                    trainRunTime = dp.get_all_time_for_train( trainInfo )
                    svgHandler.draw_trains( trainRunTime, trainId, trainInfo['CarClass'], trainInfo['Line'], expertList )
                svgHandler.save()
                print( f'\n資料檔處理完成！共處理 {total:d} 筆資料，有效資料有 {count:d} 筆' )
                t2 = time.time()
                print( f'使用時間 {t2 - t1:f} 秒\n' )
        if deleteAtExit :
            for filename in jsonFiles :
                os.remove( jsonLocation + '/' + filename )
    else :
        print( '沒有任何資料可處理\n' )

def _print_usage( name ) :
    print( 'usage : ' & name & ' [-d] [-f] [-h] [-i inputfolder] [-o outputfolder] [--delete] [--force] [--help] [--inputfolder inputfolder] [--outputfolder outputfolder] [trainno ...]' )
    exit()

if __name__ == '__main__' :
    inputFolder = 'JSON'
    outputFolder = 'OUTPUT'
    noEnterEmphasis = False
    deleteAtExit = False
    expertList = []
    optList = []
    trainNoList = []
    print( '台鐵Opendata運行圖繪圖程式  版本 ' + version + '\n\n' )
    if len( sys.argv ) > 1 :
        optList, trainNoList = getopt.getopt( sys.argv[1:], 'dfhi:o:', [ 'delete', 'force', 'help', 'inputfolder=', 'outputfolder=' ] )
    for opt in optList :
        if opt[0] == '-d' or opt[0] == '--delete' :
            deleteAtExit = True
        elif opt[0] == '-f' or opt[0] == '--force' :
            noEnterEmphasis = True
        elif opt[0] == '-h' or opt[0] == '--help' :
            _print_usage( sys.argv[0] )
        elif opt[0] == '-i' or opt[0] == '--inputfolder' :
            inputFolder = opt[1]
        elif opt[0] == '-o' or opt[0] == '--outputfolder' :
            outputFolder = opt[1]
    if len( trainNoList ) == 0 and not noEnterEmphasis :
        print( '設定需要加強繪圖車次\n' )
        action = input( '指定車次( 不需要請直接輸入Enter )：\n' )
        if action != '' :
            while action != '' :
                trainNoList.append( action )
                action = input( '指定車次( 設定結束請直接輸入Enter )：\n' )
    if len( trainNoList ) > 0 :
        for item in trainNoList :
            subList = item.replace( ',', ' ' ).split()
            for x in subList :
                expertList.append( x )
    main( inputFolder, outputFolder, expertList, deleteAtExit )
