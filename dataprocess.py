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
            while gradient[0] + gradient[2] >=  self.stations[i][1] and i < len( self.stations ) :
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

# Find all station and time for specific train through
def _find_pass_stations_and_time( listStopStas, line, lineDir, makeCatagory = False ) :
    global _stations
    if makeCatagory :
        cwItem = 2
        ccwItem = 3
        temp = []
    else :
        cwItem = 4
        ccwItem = 5
        locTime = _TrainLocTime()
        lastLoc = -1.0
        lastTime = -1
    # special case, if train is operated between Chenggong and Jhuifen, direction adjustment is needed
    if _is_mountain_line( listStopStas[0][0] ) and lineDir == '0' :
        for item in listStopStas :
            if _is_coach_line( item[0] ) :
                lineDir = '1'
                break
    # return null list if stop is not in operation station
    if makeCatagory :
        for item in listStopStas :
            if _stations[item[0]][1] == 'NA' :
                return temp
    km = 0.0
    stationId = listStopStas[0][0]
    for i in range( len( listStopStas ) - 1 ) :
        nextStationId = listStopStas[i + 1][0]
        if makeCatagory :
            temp.append( [stationId, _stations[stationId][0], _stations[stationId][1], km] )
        else :
            if lastLoc >= 0 :
                locTime._add_gradient( lastLoc, lastTime, km - lastLoc, ( int( _timeValue[listStopStas[i][1]] ) - lastTime ) % 1440 )
            lastLoc = km
            lastTime = int( _timeValue[listStopStas[i][2]] )
            locTime._add_record( stationId, km )
        while stationId != nextStationId :
            if stationId != listStopStas[i][0] :
                if makeCatagory :
                    temp.append( [stationId, _stations[stationId][0], _stations[stationId][1], km] )
                else :
                    locTime._add_record( stationId, km )
            if stationId == '1002' and _is_keelung_branch( nextStationId ) :
                key = list( _stations[stationId][cwItem].keys() )[1]
                km += float( _stations[stationId][cwItem][key] )
            elif stationId == '1024' and ( _is_neiwan_line( nextStationId ) or _is_liujia_line( nextStationId ) ) :
                key = list( _stations[stationId][cwItem].keys() )[1]
                km += float( _stations[stationId][cwItem][key] )
            elif stationId == '1028' and ( _is_coach_line( nextStationId ) or ( lineDir == '1' and line == '2' ) ) :
                key = list( _stations[stationId][ccwItem].keys() )[1]
                km += float( _stations[stationId][ccwItem][key] )
            elif stationId == '1321' and _is_coach_line( nextStationId ) :
                key = list( _stations[stationId][ccwItem].keys() )[1]
                km += float( _stations[stationId][ccwItem][key] )
                if lineDir == '1' :
                    lineDir = '0'
                else :
                    lineDir = '1'
            elif stationId == '1118' and _is_mountain_line( nextStationId ) :
                key = list( _stations[stationId][ccwItem].keys() )[1]
                km += float( _stations[stationId][ccwItem][key] )
                if lineDir == '1' :
                    lineDir = '0'
                else :
                    lineDir = '1'
            elif stationId == '1119' and ( _is_coach_line( nextStationId ) or ( lineDir == '0' and line == '2' ) ) :
                key = list( _stations[stationId][cwItem].keys() )[1]
                km += float( _stations[stationId][cwItem][key] )
            elif stationId == '1207' and _is_jiji_line( nextStationId ) :
                key = list( _stations[stationId][ccwItem].keys() )[1]
                km += float( _stations[stationId][ccwItem][key] )
            elif stationId == '1230' and _is_shalun_line( nextStationId ) :
                key = list( _stations[stationId][ccwItem].keys() )[1]
                km += float( _stations[stationId][ccwItem][key] )
            elif stationId == '1826' and _is_suao_branch( nextStationId ) :
                key = list( _stations[stationId][cwItem].keys() )[1]
                km += float( _stations[stationId][cwItem][key] )
            elif stationId == '1806' and _is_pingsi_line( nextStationId ) :
                key = list( _stations[stationId][cwItem].keys() )[1]
                km += float( _stations[stationId][cwItem][key] )
            elif stationId == '1804' and _is_shanao_line( nextStationId ) :
                key = list( _stations[stationId][ccwItem].keys() )[1]
                km += float( _stations[stationId][ccwItem][key] )
            elif stationId == '2203' and _is_liujia_line( nextStationId ) :
                key = list( _stations[stationId][cwItem].keys() )[1]
                km += float( _stations[stationId][cwItem][key] )
            elif lineDir == '0' :
                key = list( _stations[stationId][cwItem].keys() )[0]
                km += float( _stations[stationId][cwItem][key] )
            else :
                key = list( _stations[stationId][ccwItem].keys() )[0]
                km += float( _stations[stationId][ccwItem][key] )
            stationId = key
    if makeCatagory :
        temp.append( [stationId, _stations[stationId][0], _stations[stationId][1], km] )
        return temp
    locTime._add_gradient( lastLoc, lastTime, km - lastLoc, ( int( _timeValue[listStopStas[-1][1]] ) - lastTime ) % 1440 )
    locTime._add_record( stationId, km )
    return locTime._pack()

# load station table
def _load_stations() :
    stations = {}
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
                    neighber[neighberIdx][row[columnIdx]] = row[columnIdx + 1]
                columnIdx += 2
            stations[row[0]] = [row[1], row[2], neighber[0], neighber[1], neighber[2], neighber[3]]
    return stations

def _make_catagory_range( lineName, passSta, direction ) :
    line = '0'
    if direction == 'CCW' :
        lineDir = '1'
    else :
        lineDir = '0'
    for sta in passSta :
        if _is_mountain_line( sta ) :
            line = '1' # mountain line
            break
        elif _is_coach_line( sta ) :
            line = '2' # coast line
            break
    temp = _find_pass_stations_and_time( passSta, line, lineDir, makeCatagory = True )
    listStaTable = []
    dictStaLocation = {}
    for item in temp :
        # List columns are 'Station ID', 'Station Name'. 'Sheet Line Position'
        listStaTable.append( [item[0], item[1], float( item[3] ) * 32, item[2]] )
        # Add sheet line position into dictionary with indexed by station ID
        if item[2] != 'NA' :
            dictStaLocation[item[0]] = float( item[3] * 32  )
    return listStaTable, dictStaLocation

def _make_time_dict() :
    _timeValue = {}
    for hh in range( 24 ) :
        for mm in range( 60 ) :
            _timeValue[f'{hh:02d}:{mm:02d}:00'] = hh * 60 + mm
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
    for item in data['TrainInfos'] :  # Append all trainTable,
        trains.append( item )
    return trains

def diagramLayout() :
    folders = []
    dictDrawProfile = {}
    with open( 'CSV/DiagramLayout.csv', newline = '', encoding = 'utf8' ) as csvFile :
        reader = csv.reader( csvFile )
        for item in reader :
            if item[0].find( '#' ) == 1 :
                continue
            listStaTable, dictStaLocation = _make_catagory_range( item[0], [[item[3]], [item[4]], [item[5]]], item[6] )
            # List columns are 'subfolder', 'prefix', 'catagroy describe', 'line position table', 'station List'
            # indexed by 'catagory ID'
            dictDrawProfile[item[0]] = [item[1], item[2], item[7], listStaTable, dictStaLocation]
            folders.append( item[1] )
    return folders, dictDrawProfile
                    
# generate a dictionary for trainInfo
def get_all_time_for_train( trainInfo ) :
    listStopStas = []
    # find all stop stations' data
    for timeInfos in trainInfo['TimeInfos'] :
        listStopStas.append( [timeInfos['Station'], timeInfos['ArrTime'], timeInfos['DepTime']] )
    # find all pass stations and time
    return _find_pass_stations_and_time( listStopStas, trainInfo['Line'], trainInfo['LineDir'] )
