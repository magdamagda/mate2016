import SocketServer
import sys
from random import randint

class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print "{} wrote:".format(self.client_address[0])
        answer = self.generateFakeAnswer()
        print answer
        # just send back the same data, but upper-cased
        self.request.sendall(answer)

    def generateFakeAnswer(self):
        answer=""
        frames = self.data.split("(")
        for frame in frames:
            frame = frame[0:-1]
            splitted = frame.split(",")
            if len(splitted) == 2 and splitted[1] == "G": # get param
                answer += "(" + splitted[0] + ",R," + str(randint(0, 50)) + ")"
        return answer


if __name__ == "__main__":
    if len(sys.argv)>1:
        HOST, PORT = "localhost", int(sys.argv[1])
    else:
        HOST, PORT = "localhost", 9998

    print "starting server at " + HOST + " " + str(PORT)

    try:
        # Create the server, binding to localhost on port 9999
        server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
    except Exception as e:
        print str(e)