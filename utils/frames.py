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
            result[splitted[1] + splitted[2]] = int(splitted[3])
        elif len(splitted) == 3:
            result[splitted[1]] = int(splitted[2])
        print result
    return result

def getParam(param, host, port):
    response = clienttcp.tcpConnection(host, port, "(G," + param +")")
    print response
    if response is not None:
        return parseGetValuesResponse(response)
    return None

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
    response = clienttcp.tcpConnection(host, port, "(S," + param + ",*," + ",".join(values) + ")")
    if response is not None:
        return parseGetAllValuesResponse(response)
    return None

def parseAxesVelocity(response):
    checkError(response)
    response = response[1:-1]
    splitted = response.split(",")
    return [int(x) for x in splitted[4:]]

def setAxesVelocity(host, port, values):
    response = clienttcp.tcpConnection(host, port, "(S,A,s,*," + ",".join(values) + ")")
    if response is not None:
        return parseAxesVelocity(response)
    return None

def getAxesVelocity(host, port):
    response = clienttcp.tcpConnection(host, port, "(G,A,s,*)")
    if response is not None:
        return parseAxesVelocity(response)
    return None