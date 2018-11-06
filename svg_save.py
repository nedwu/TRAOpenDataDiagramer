import time
import math

dictCarClass = {
    '1100' : 'DMU',
    '1101' : 'PP',
    '1102' : 'TAROKO',
    '1103' : 'DMU',
    '1107' : 'PUYUMA',
    '1108' : 'PP',
    '1109' : 'PP',
    '110A' : 'PP',
    '110B' : 'EMU',
    '110C' : 'EMU',
    '110D' : 'DMU',
    '110E' : 'DMU',
    '110F' : 'DMU',
    '1110' : 'PC_CK',
    '1111' : 'PC_CK',
    '1114' : 'PC_CK',
    '1115' : 'PC_CK',
    '1120' : 'PC_FS',
    '1131' : 'LOCAL',
    '1132' : 'LOCAL',
    '1140' : 'ORDINARY',
    '0000' : 'SPECIAL'
}

class Draw :

    class _Draw :

        class _Svg :

            def __init__( self, filename, width, height ) :
                self.fileHandler = open( filename, 'w', encoding = 'utf-8' )
                self.fileHandler.write( '<?xml version="1.0" encoding="utf-8" ?>' )
                self.fileHandler.write( '<svg xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" style="font-family: Tahoma;" width="' + str( width ) + '" height="' + str( height ) + '" version="1.1">' )

            def insertClass( self ) :
                self.fileHandler.write( '<style>' )
                self.fileHandler.write( 'line { stroke-width: 0.3; } ' )
                self.fileHandler.write( 'path { stroke-width: 2.0; fill: none; } ' )
                self.fileHandler.write( '.hour_line { stroke: #000000; } ' )
                self.fileHandler.write( '.min10_line { stroke: #a18cfc; } ' )
                self.fileHandler.write( '.min30_line { stroke: #0105e0; } ' )
                self.fileHandler.write( '.station_line { stroke: #000000; } ' )
                self.fileHandler.write( '.station_na_line { stroke: #bfbfbf; } ' )
                self.fileHandler.write( '.TAROKO { stroke: #f88000; } ' )
                self.fileHandler.write( '.PUYUMA { stroke: #f00c08; } ' )
                self.fileHandler.write( '.PP { stroke: #c87030; } ' )
                self.fileHandler.write( '.DMU { stroke: #c0b520; } ' )
                self.fileHandler.write( '.EMU { stroke: #d08820; } ' )
                self.fileHandler.write( '.PC_CK { stroke: #ffe020; } ' )
                self.fileHandler.write( '.PC_FS { stroke: #70d0fc; } ' )
                self.fileHandler.write( '.LOCAL { stroke: #3520fc; stroke-width: 1.2; } ' )
                self.fileHandler.write( '.ORDINARY { stroke: #203078; stroke-width: 1.2; } ' )
                self.fileHandler.write( '.SPECIAL { stroke: #cc2f8d; } ' )
                self.fileHandler.write( '</style>' )

            def _text( self, x, y, string, _color = None, _class = None, transform = None ) :
                transformStr = ''
                if transform is not None :
                    transformStr = ' transform="' + transform + '"'
                if _class is not None :
                    self.fileHandler.write( '<text class="' + _class + '" x="' + x + '" y="' + y + '"' + transformStr + '>' + string + '</text>' )
                elif _color is not None :
                    self.fileHandler.write( '<text stroke="' + _color + '" x="' + x + '" y="' + y + '"' + transformStr + '>' + string + '</text>' )
                else :
                    self.fileHandler.write( '<text x="' + x + '" y="' + y + '"' + transformStr + '>' + string + '</text>' )

            def _line( self, x1, y1, x2, y2, _color = None, _class = None ) :
                if _class is not None :
                    self.fileHandler.write( '<line class="' + _class + '" x1="' + x1 + '" x2="' + x2 + '" y1="' + y1 + '" y2="' + y2 + '" />' )
                elif _color is not None :
                    self.fileHandler.write( '<line stroke="' + _color + '" x1="' + x1 + '" x2="' + x2 + '" y1="' + y1 + '" y2="' + y2 + '" />' )
                else :
                    self.fileHandler.write( '<line x1="' + x1 + '" x2="' + x2 + '" y1="' + y1 + '" y2="' + y2 + '" />' )

            def _path( self, pathList, lineId, _color = None, _class = None, _emphasis = False ) :
                emphasisStr = '" style="stroke-width: 4" />' if _emphasis else '" />'
                if _class is not None :
                    self.fileHandler.write( '<path class="' + _class + '" d="' + pathList + '" id="' + lineId + emphasisStr )
                elif _color is not None :
                    self.fileHandler.write( '<path stroke="' + _color + '" d="' + pathList + '" id="' + lineId + emphasisStr )
                else :
                    self.fileHandler.write( '<path d="' + pathList + '" id="' + lineId + emphasisStr )

            def _final( self ) :
                self.fileHandler.write( '</svg>')
                self.fileHandler.close()

        def __init__( self, location, sheetTitle, date, line, listStaTable, dictStaLocation, version ) :
            self.nextDayObj = None
            if location == '' :
                location = 'OUTPUT/' + line + '_'
            self.filename = location + date + '.svg'
            self.title = sheetTitle
            self.date = date
            self.line = line
            self.listStaTable = listStaTable
            self.dictStaLocation = dictStaLocation
            self.height = self.listStaTable[-1][2]
            localtime = time.asctime( time.localtime( time.time() ) )
            self.drawHandler = self._Svg( self.filename, '14500', f'{self.height + 100:.2f}' )
            self.drawHandler.insertClass()
            self.drawHandler._text( '5', '20', self.title + ' 日期：' + self.date, _color = '#000000' )
            self.drawHandler._text( '50', f'{self.height + 70:.2f}', '轉檔運行圖程式版本：' + version + ' 轉檔時間：' + localtime + ' 資料來源：臺鐵公開時刻表JSON版（http://163.29.3.98/json/）', _color = '#000000' )
            self.drawHandler._text( '50', f'{self.height + 90:.2f}', '聲明：產出運行圖僅供參考，恕無法保證與實際運行狀況相符，請自行斟酌使用', _color = '#fc0808' )
            for i in range( 25 ) :
                x = 50 + i * 600
                self.drawHandler._line( f'{x:.2f}', '50', f'{x:.2f}', f'{self.height + 50:.2f}', _class = 'hour_line' )
                for j in range( int( self.height + 299 ) // 300 ) :
                    self.drawHandler._text( f'{x:.2f}', f'{49 + j * 300:.2f}', f'{i:>02d}' + '00', _color = '#999966' )
                if i != 24 :
                    for j in range( 5 ) :
                        x = 50 + i * 600 + ( j + 1 ) * 100
                        if j != 2 :
                            self.drawHandler._line( f'{x:.2f}', '50', f'{x:.2f}', f'{self.height + 50:.2f}', _class = 'min10_line' )
                        else :
                            self.drawHandler._line( f'{x:.2f}', '50', f'{x:.2f}', f'{self.height + 50:.2f}', _class = 'min30_line' )
                            for k in range( int( self.height + 299 ) // 300 ) :
                                self.drawHandler._text( f'{x:.2f}', f'{49 + k * 300:.2f}', '30', _color = '#999966' )
            for item in self.listStaTable :
                y = float( item[2] ) + 50
                self.drawHandler._line( '50', f'{y:.2f}', '14450', f'{y:.2f}', _class = 'station_na_line' if item[3] == 'NA' else 'station_line' )
                for i in range( 25 ) :
                    self.drawHandler._text( f'{5 + i * 600:.2f}', f'{y - 5:.2f}', item[1], _color = '#bfbfbf' if item[3] == 'NA' else '#999966' )

        def _draw_trains( self, dfTrainTime, trainId, carClass, line, expertList ) :
            className = dictCarClass.get( carClass, 'ordinary' )
            midnightMeter = -1
            lastTime = -1
            baseTime = -1
            nextMarkerTime = -1
            nextDay = False
            segment = 0
            inRange = False
            testList = []
            markerList = []
            for i in range( len( dfTrainTime ) ) :
                if self.dictStaLocation.__contains__( dfTrainTime[i][0] ) :
                    if dfTrainTime[i][0] not in testList :
                        testList.append( dfTrainTime[i][0] )
                    if not inRange :
                        inRange = True
                elif inRange :
                    inRange = False
                    if len( testList ) == 1 :
                        testList.remove( testList[0] )
            if len( testList ) > 1 :
                path = ''
                for i in range( len( dfTrainTime ) ) :
                    if dfTrainTime[i][1] < lastTime :
                        if not nextDay :
                            self._draw_line( trainId, path, className, trainId + f'_{segment:02d}', markerList, expertList )
                            if self.nextDayObj is None :
                                break
                            nextDay = True
                            segment = 0
                            markerList = []
                            nextMarkerTime = -1
                            if 'x' in locals() :
                                del( x )
                            if 'y' in locals() :
                                del( y )
                        elif self.nextDayObj is not None :
                            self.nextDayObj._draw_line( trainId, path, className, trainId + f'_prev_{segment:02d}', markerList, expertList )
                        path = ''
                        markerList = []
                        nextMarkerTime = -1
                        if 'x' in locals() :
                            del( x )
                        if 'y' in locals() :
                            del( y )
                    if self.dictStaLocation.__contains__( dfTrainTime[i][0] ) :
                        x = round( dfTrainTime[i][1] * 10 + 50, 4 )
                        y = round( self.dictStaLocation[dfTrainTime[i][0]] + 50, 4 )
                        if path == '' :
                            path += f'M{x:.2f},{y:.2f}'
                        else :
                            path += f'L{x:.2f},{y:.2f}'
                    elif dfTrainTime[i][0] == -1 :
                        if midnightMeter < 0 :
                            try :
                                before = i - 1
                                while True :
                                    if dfTrainTime[before][0] != -1 :
                                        break
                                    before = before - 1
                                after = i + 1
                                if not self.dictStaLocation.__contains__( dfTrainTime[before][0] ) :
                                    continue
                                while True :
                                    if dfTrainTime[after][0] != -1 :
                                        break
                                    after = after + 1
                                if not self.dictStaLocation.__contains__( dfTrainTime[after][0] ) :
                                    continue
                                midnightMeter = self.dictStaLocation[dfTrainTime[before][0]] + ( self.dictStaLocation[dfTrainTime[after][0]] - self.dictStaLocation[dfTrainTime[before][0]] ) * ( dfTrainTime[i][1] - dfTrainTime[before][1] ) / ( dfTrainTime[after][1] - dfTrainTime[before][1] + 1440 )
                            except :
                                print( f'\nerror, Train No={trainId:>5s} before={before:>2d} after={after:>2d}\n' )
                                print( dfTrainTime )
                        x = round( dfTrainTime[i][1] * 10 + 50, 2 )
                        y = round( midnightMeter + 50, 2 )
                        if path == '' :
                            path += f'M{x:.2f},{y:.2f}'
                        else :
                            path += f'L{x:.2f},{y:.2f}'
                    else :
                        if path != '' :
                            if not nextDay :
                                self._draw_line( trainId, path, className, trainId + f'_{segment:02d}', markerList, expertList )
                            elif self.nextDayObj is not None :
                                self.nextDayObj._draw_line( trainId, path, className, trainId + f'_prev_{segment:02d}', markerList, expertList )
                            segment += 1
                            path = ''
                            markerList = []
                            nextMarkerTime = -1
                            if 'x' in locals() :
                                del( x )
                            if 'y' in locals() :
                                del( y )
                    if 'x' in locals() and ( nextMarkerTime <= x or nextMarkerTime < 0 ) :
                        if nextMarkerTime < 0 :
                            nextMarkerTime = x
                        if len( dfTrainTime ) > ( i + 1 ) and dfTrainTime[i][0] != dfTrainTime[i + 1][0] and self.dictStaLocation.__contains__( dfTrainTime[i + 1][0] ) :
                            markerList.append( [x, y, round( math.atan2( self.dictStaLocation[dfTrainTime[i + 1][0]] + 50 - y, dfTrainTime[i + 1][1] * 10 + 50 - x ) * 180 / math.pi, 4 )] )
                            nextMarkerTime = nextMarkerTime + 300
                    lastTime = dfTrainTime[i][1]
                if path != '' :
                    if not nextDay :
                        self._draw_line( trainId, path, className, trainId + f'_{segment:02d}', markerList, expertList )
                    elif self.nextDayObj is not None :
                        self.nextDayObj._draw_line( trainId, path, className, trainId + f'_prev_{segment:02d}', markerList, expertList )
                    if 'x' in locals() :
                        del( x )
                    if 'y' in locals() :
                        del( y )

        def _draw_line( self, trainId, path, className, lineId, textAnchor, expertList ) :
            if path != '' :
                if path.count( 'L' ) < 2 :
                    startL = path.find( 'L' )
                    firstY = path.find( ',', 1 ) + 1
                    secondY = path.find( ',', startL + 1 ) + 1
                    if path[firstY:startL] == path[secondY:] :
                        return
                if len( expertList ) > 0 and trainId in expertList :
                    self.drawHandler._path( path, lineId, _class = className, _emphasis = True )
                else :
                    self.drawHandler._path( path, lineId, _class = className )
                for item in textAnchor :
                    self.drawHandler._text( f'{item[0]:.2f}', f'{item[1]:.2f}', trainId, _class = className, transform = f'rotate({item[2]:.4f} {item[0]:.2f}, {item[1]:.2f})' )

        def _set_next_day_sheet( self, nextDayObj ) :
            self.nextDayObj = nextDayObj

        def _save( self ) :
            self.drawHandler._final()

    def __init__( self, location, date, dictDrawProfile, version ) :
        self.subDraw = []
        for item in dictDrawProfile :
            if location == '' :
                newSubDraw = self._Draw( '', dictDrawProfile[item][2], date, item, dictDrawProfile[item][3], dictDrawProfile[item][4], version )
            else :
                newSubDraw = self._Draw( location + '/' + dictDrawProfile[item][0] + '/' + dictDrawProfile[item][1], dictDrawProfile[item][2], date, item, dictDrawProfile[item][3], dictDrawProfile[item][4], version )
            self.subDraw.append( newSubDraw )

    def draw_trains( self, dfTrainTime, trainId, carClass, line, expertList ) :
        for subDraw in self.subDraw :
            subDraw._draw_trains( dfTrainTime, trainId, carClass, line, expertList )

    def set_next_day_sheet( self, nextDayObj ) :
        for i in range( len( self.subDraw ) ) :
            self.subDraw[i]._set_next_day_sheet( nextDayObj.subDraw[i] )

    def save( self ) :
        for subDraw in self.subDraw :
            subDraw._save()
