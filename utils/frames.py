import clienttcp

def echo(host, port):
    response = clienttcp.tcpConnection(host, port, "(?)")
    if response is not None:
        return True
    return False

def checkError(frame):
    if frame[1]=="E":
        raise Exception(frame.split(",")[1])

def parseGetValuesResponse(response):
    print "parse get value response"
    result = {}
    frames = response.split(")")[:-1]
    print frames
    for frame in frames:
        checkError(frame)
        frame = frame[1:]
        splitted = frame.split(",")
        if len(splitted) == 4:
            result[splitted[1] + splitted[2]] = float(splitted[3])
        elif len(splitted) == 3:
            result[splitted[1]] = float(splitted[2])
        print result
    return result

def getParam(param, host, port):
    response = clienttcp.tcpConnection(host, port, "(G," + param +")")
    print response
    if response is not None:
        return parseGetValuesResponse(response)
    return None

def getParamFrame(param, number):
    return "(G,M," + param +"," + str(number) + ")"

def getAllParams(params, host, port):
    frames = ""
    for p in params:
        frames += "(G," + ",".join(p) + ")"
    print frames
    response = clienttcp.tcpConnection(host, port, frames)
    print response
    if response is not None:
        return parseGetValuesResponse(response)
    return {}

def setParams(params, host, port):
    frames = ""
    for p in params:
        frames += "(S," + ",".join(p) + ")"
    print frames
    response = clienttcp.tcpConnection(host, port, frames)
    if response is not None:
        return parseGetValuesResponse(response)
    return {}

def parseGetAllValuesResponse(response):
    checkError(response)
    response = response[1:-1]
    splitted = response.split(",")
    return [int(x) for x in splitted[3:]]

def getAllValues(host, port, param):
    response = clienttcp.tcpConnection(host, port, "(G," + param + ",*)")
    if response is not None:
        return parseGetAllValuesResponse(response)
    return None

def setAllValues(host, port, param, values):
    response = clienttcp.tcpConnection(host, port, "(S," + param + ",*," + ",".join([str(v) for v in values]) + ")")
    if response is not None:
        return parseGetAllValuesResponse(response)
    return None

def parseAxesVelocity(response):
    checkError(response)
    response = response[1:-1]
    splitted = response.split(",")
    return [int(x) for x in splitted[4:]]

def setAxesVelocity(host, port, values):
    response = clienttcp.tcpConnection(host, port, "(S,A,s,*," + ",".join([str(v) for v in values]) + ")")
    if response is not None:
        return parseAxesVelocity(response)
    return None

def getAxesVelocity(host, port):
    response = clienttcp.tcpConnection(host, port, "(G,A,s,*)")
    if response is not None:
        return parseAxesVelocity(response)
    return None

def setParamFrame(param):
    return "(S," + param + ")"

def getAllValuesFrame(param):
    return "(G," + param + ",*)"

def setAllValuesFrame(param, values):
    return "(S," + param + ",*," + ",".join([str(int(v)) for v in values]) + ")"

def parseAxesVelocity(response):
    checkError(response)
    response = response[1:-1]
    splitted = response.split(",")
    return [int(x) for x in splitted[4:]]

def setAxesVelocityFrame(values):
    return "(S,A,s,*," + ",".join([str(v) for v in values]) + ")"

def setAxesGearFrame(values):
    return "(S,A,g,*," + ",".join([str(v) for v in values]) + ")"

def getAxesGearFrame():
    return "(G,A,g,*)"

def getAxesVelocityFrame():
    return "(G,A,s,*)"

def getFrameTypeAndData(frame):
    if len(frame) < 5:
        raise Exception("Too short frame")
    if frame[1]=="E":
        raise Exception(frame)
    frame = frame[0:-1].split(",")
    return frame[1], frame[2:]

def parseParamResponseFrame(frame):
    if len(frame) < 5:
        raise Exception("Too short frame")
    if frame[1]=="E":
        raise Exception(frame)
    frame = frame[0:-1].split(",")
    return frame[2], frame[3], frame[4]

def changeModeFrame(mode):
    return "(S,S,m," + str(mode) + ")"

def uptimeFrame():
    return "(G,S,t)"

def outputStateFrame(num, state):
    return "(S,O," + str(num) + "," + str(state) + ")"

def zeroAxisFrame():
    return "(S,S,c,z)"