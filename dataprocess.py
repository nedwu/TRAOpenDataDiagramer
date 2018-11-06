import json
import csv

class _TrainLocTime :

    def __init__( self ) :
        self.stations = []
        self.gradients = []

    def _add_record( self, _stationId, _loc ) :
        self.stations.append( [_stationId, float( _loc )] )

    def _add_gradient( self, _firstLoc, _firstTime, _maxLoc, _maxTime ) :
        self.gradients.append( [float( _firstLoc ), float( _firstTime ), float( _maxLoc ), float( _maxTime )] )

    def _pack( self ) :
        temp = []
        i = 0
        lastTimePos = -1.0
        for gradient in self.gradients :
            base = gradient[1]
            slope = gradient[3] / gradient[2]
            while gradient[0] + gradient[2] >= self.stations[i][1] and i < len( self.stations ) :
                timePos = round( base + ( self.stations[i][1] - gradient[0] ) * slope, 4 )
                if lastTimePos != timePos :
                    if timePos == 1440 :
                        temp.append( [self.stations[i][0], 1440] )
                        temp.append( [self.stations[i][0], 0] )
                    elif timePos > 1440 :
                        temp.append( [-1, 1440] )
                        temp.append( [-1, 0] )
                        temp.append( [self.stations[i][0], timePos - 1440] )
                    else :
                        temp.append( [self.stations[i][0], timePos] )
                if timePos >= 1440 :
                    base -= 1440
                    lastTimePos = timePos - 1440
                else :
                    lastTimePos = timePos
                if gradient[0] + gradient[2] == self.stations[i][1] :
                    break
                i += 1
        del( self.stations )
        del( self.gradients )
        return temp

# if is this station in mountain line?
def _is_mountain_line( stationId ) :
    return stationId in ('1302', '1304', '1305', '1307', '1308', '1310', '1314', '1315', '1317', '1325', '1318', '1326', '1327', '1323', '1328', '1319', '1329', '1322', '1320', '1324', '1321')

# if is this station in coach line?
def _is_coach_line( stationId ) :
    return stationId in ('1102', '1103', '1104', '1105', '1106', '1107', '1108', '1109', '1110', '1111', '1112', '1113', '1114', '1115', '1116', '1117', '1118')

# if is this station in branch of Keelung?
def _is_keelung_branch( stationId ) :
    return stationId in ('1001', '1029')

# if is this station in branch of Suao?
def _is_suao_branch( stationId ) :
    return stationId == '1827'

# if is this station in Neiwan line?
def _is_neiwan_line( stationId ) :
    return stationId in ('2212', '2213', '2203', '2204', '2211', '2205', '2206', '2207', '2208', '2209', '2210')

# if is this station in Liujia line?
def _is_liujia_line( stationId ) :
    return stationId == '2214'

# if is this station in Jiji line?
def _is_jiji_line( stationId ) :
    return stationId in ('2702', '2703', '2704', '2705', '2706', '2707')

# if is this station in Shalun line?
def _is_shalun_line( stationId ) :
    return stationId in ('5101', '5102')

# if is this station in Pingsi line?
def _is_pingsi_line( stationId ) :
    return stationId in ('1903', '1904', '1905', '1906', '1907', '1908')

# if is this station in Shanao line?
def _is_shanao_line( stationId ) :
    return stationId in ('6103', '2003')

class _StationNode :

    def __init__( self, listStation, lineDir, line = '0', catagory = False ) :
        self._cumulative100Meter = 0
        self._iterStation = iter( listStation )
        self._nowStationId = next( self._iterStation )[0]
        self._nextItem = next( self._iterStation )
        self._nextStationId = self._nextItem[0]
        self._lineDir = lineDir
        if catagory :
            self._mode = 0 # catagory mode
            self._line = '0'
            for sta in listStation :
                if _is_mountain_line( sta ) :
                    self._line = '1' # mountain line
                    break
                elif _is_coach_line( sta ) :
                    self._line = '2' # coast line
                    break
            self._cwItem = 2
            self._ccwItem = 3
        else :
            self._mode = 1 # passing stop mode
            self._line = line
            self._cwItem = 4
            self._ccwItem = 5
        if _is_mountain_line( listStation[0][0] ) and self._lineDir == '0' :
            for item in listStation :
                if _is_coach_line( item[0] ) :
                    self.lineDir = '1'
                    break

    def __next__( self ) :
        stationId = self._nowStationId
        meter = self._cumulative100Meter
        if self._nextItem is not None :
            if self._nowStationId == '1002' and _is_keelung_branch( self._nextStationId ) :
                self._nowStationId = list( _stations[stationId][self._cwItem].keys() )[1]
                self._cumulative100Meter += _stations[stationId][self._cwItem][self._nowStationId]
            elif self._nowStationId == '1024' and ( _is_neiwan_line( self._nextStationId ) or _is_liujia_line( self._nextStationId ) ) :
                self._nowStationId = list( _stations[stationId][self._cwItem].keys() )[1]
                self._cumulative100Meter += _stations[stationId][self._cwItem][self._nowStationId]
            elif self._nowStationId == '1028' and ( _is_coach_line( self._nextStationId ) or ( self._lineDir == '1' and self._line == '2' ) ) :
                self._nowStationId = list( _stations[stationId][self._ccwItem].keys() )[1]
                self._cumulative100Meter += _stations[stationId][self._ccwItem][self._nowStationId]
            elif self._nowStationId == '1321' and _is_coach_line( self._nextStationId ) :
                self._nowStationId = list( _stations[stationId][self._ccwItem].keys() )[1]
                self._cumulative100Meter += _stations[stationId][self._ccwItem][self._nowStationId]
                self._lineDir = '0' if self._lineDir == '1' else '1'
            elif self._nowStationId == '1118' and _is_mountain_line( self._nextStationId ) :
                self._nowStationId = list( _stations[stationId][self._ccwItem].keys() )[1]
                self._cumulative100Meter += _stations[stationId][self._ccwItem][self._nowStationId]
                self._lineDir = '0' if self._lineDir == '1' else '1'
            elif self._nowStationId == '1119' and ( _is_coach_line( self._nextStationId ) or ( self._lineDir == '0' and self._line == '2' ) ) :
                self._nowStationId = list( _stations[stationId][self._cwItem].keys() )[1]
                self._cumulative100Meter += _stations[stationId][self._cwItem][self._nowStationId]
            elif self._nowStationId == '1207' and _is_jiji_line( self._nextStationId ) :
                self._nowStationId = list( _stations[stationId][self._ccwItem].keys() )[1]
                self._cumulative100Meter += _stations[stationId][self._ccwItem][self._nowStationId]
            elif self._nowStationId == '1230' and _is_shalun_line( self._nextStationId ) :
                self._nowStationId = list( _stations[stationId][self._ccwItem].keys() )[1]
                self._cumulative100Meter += _stations[stationId][self._ccwItem][self._nowStationId]
            elif self._nowStationId == '1826' and _is_suao_branch( self._nextStationId ) :
                self._nowStationId = list( _stations[stationId][self._cwItem].keys() )[1]
                self._cumulative100Meter += _stations[stationId][self._cwItem][self._nowStationId]
            elif self._nowStationId == '1806' and _is_pingsi_line( self._nextStationId ) :
                self._nowStationId = list( _stations[stationId][self._cwItem].keys() )[1]
                self._cumulative100Meter += _stations[stationId][self._cwItem][self._nowStationId]
            elif self._nowStationId == '1804' and _is_shanao_line( self._nextStationId ) :
                self._nowStationId = list( _stations[stationId][self._ccwItem].keys() )[1]
                self._cumulative100Meter += _stations[stationId][self._ccwItem][self._nowStationId]
            elif self._nowStationId == '2203' and _is_liujia_line( self._nextStationId ) :
                self._nowStationId = list( _stations[stationId][self._cwItem].keys() )[1]
                self._cumulative100Meter += _stations[stationId][self._cwItem][self._nowStationId]
            elif self._lineDir == '0' :
                self._nowStationId = list( _stations[stationId][self._cwItem].keys() )[0]
                self._cumulative100Meter += _stations[stationId][self._cwItem][self._nowStationId]
            else :
                self._nowStationId = list( _stations[stationId][self._ccwItem].keys() )[0]
                self._cumulative100Meter += _stations[stationId][self._ccwItem][self._nowStationId]
            if self._nowStationId == self._nextStationId :
                try :
                    self._nextItem = next( self._iterStation )
                except StopIteration :
                    self._nextItem = None
                    del( self._iterStation )
                if self._nextItem is not None :
                    self._nextStationId = self._nextItem[0]
        return stationId, meter

# Find all station and time for specific train through
def _find_pass_stations_and_time( listStopStas, line, lineDir ) :
    locTime =_TrainLocTime()
    lastLoc = -1.0
    lastTime = -1
    # special case, if train is operated between Chenggong and Jhuifen, direction adjustment is needed
    if _is_mountain_line( listStopStas[0][0] ) and lineDir == '0' :
        for item in listStopStas :
            if _is_coach_line( item[0] ) :
                lineDir = '1'
                break
    node = _StationNode( listStopStas, lineDir, line = line )
    stationId, meter = next( node )
    for i in range( len( listStopStas ) - 1 ) :
        nextStationId = listStopStas[i + 1][0]
        if lastLoc >= 0 :
            locTime._add_gradient( lastLoc, lastTime, meter - lastLoc, ( int( _timeValue[listStopStas[i][1]] ) - lastTime ) % 1440 )
        lastLoc = meter
        lastTime = int( _timeValue[listStopStas[i][2]] )
        locTime._add_record( stationId, meter )
        while stationId != nextStationId :
            if stationId != listStopStas[i][0] :
                locTime._add_record( stationId, meter )
            stationId, meter = next( node )
    locTime._add_gradient( lastLoc, lastTime, meter - lastLoc, ( int( _timeValue[listStopStas[-1][1]] ) - lastTime ) % 1440 )
    locTime._add_record( stationId, meter )
    return locTime._pack()

# load station table
def _load_stations() :
    # load station table
    _stations = {}
    with open( 'CSV/Stations.csv', newline = '', encoding = 'utf8' ) as csvFile :
        reader = csv.reader( csvFile )
        for row in reader :
            if row[0].find( '#' ) == 1 :
                continue
            columnIdx = 3
            neighberIdx = 0
            neighber = [{}, {}, {}, {}]
            while columnIdx < len( row ) and neighberIdx < 4 :
                if row[columnIdx] == '' :
                    columnIdx += 1
                    neighberIdx += 1
                    continue
                if row[columnIdx] != '-1' :
                    neighber[neighberIdx][row[columnIdx]] = int( row[columnIdx + 1] )
                columnIdx += 2
            _stations[row[0]] = [row[1], row[2], neighber[0], neighber[1], neighber[2], neighber[3]]
    return _stations

def _make_time_dict() :
    _timeValue = {}
    for hh in range( 24 ) :
        for mm in range( 60 ) :
            _timeValue[f'{hh:02d}:{mm:02d}:00'] = int( hh * 60 + mm )
    return _timeValue

_stations = _load_stations()
_timeValue = _make_time_dict()

# Read timetable from JSON, and store all JSON Train Data.
def read_json( folder, filename ) :
    trains = []
    if folder == '' :
        folder = 'JSON'
    with open( folder + '/' + filename, 'r', encoding='utf8' ) as data_file :
        data = json.load( data_file )
    for item in sorted( data['TrainInfos'], key = lambda x : x['CarClass'], reverse = True ) :  # Append all trainTable
        temp = []
        for timeItem in item['TimeInfos'] :
            temp.append( [timeItem['Station'], timeItem['ArrTime'], timeItem['DepTime']] )
        trains.append( [item['Train'], item['CarClass'], item['Line'], item['LineDir'], temp] )
    return trains

def diagramLayout() :
    folders = []
    dictDrawProfile = {}
    with open( 'CSV/DiagramLayout.csv', newline = '', encoding = 'utf8' ) as csvFile :
        reader = csv.reader( csvFile )
        for item in reader :
            if item[0].find( '#' ) == 1 :
                continue
            lineDir = '1' if item[6] == 'CCW' else '0'
            listStaTable = []
            dictStaLocation = {}
            node = _StationNode( [[item[3]], [item[4]], [item[5]]], lineDir, catagory = True )
            while True :
                stationId, meter = next( node )
                # List columns are 'Station ID', 'Station Name'. 'Sheet Line Position'
                listStaTable.append( [stationId, _stations[stationId][0], float( meter ) * 3.2, _stations[stationId][1]] )
                # Add sheet line position into dictionary with indexed by station ID
                if _stations[stationId][1] != 'NA' :
                    dictStaLocation[stationId] = float( meter ) * 3.2
                if stationId == item[5] :
                    break
            del( node )
            # List columns are 'subfolder', 'prefix', 'catagroy describe', 'line position table', 'station List'
            # indexed by 'catagory ID'
            dictDrawProfile[item[0]] = [item[1], item[2], item[7], listStaTable, dictStaLocation]
            folders.append( item[1] )
    return folders, dictDrawProfile
                    
# generate a dictionary for trainInfo
def get_all_time_for_train( trainInfo ) :
    # find all pass stations and time
    return _find_pass_stations_and_time( trainInfo[4], trainInfo[2], trainInfo[3] ) # timeinfos, line, linedir
