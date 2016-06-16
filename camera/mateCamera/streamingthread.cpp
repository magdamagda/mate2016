#include "streamingthread.h"

streamingThread::streamingThread(QString &host, int port, int camNum)
    : fstop(false), cameraPort(port), host(host), camNum(camNum)
{

}

void streamingThread::run(){
    fstop = false;
    streamImage();
}

void streamingThread::streamImage(){
    try {

            UDPSocket sock(cameraPort);

            char buffer[BUF_LEN]; // Buffer for echo string
            int recvMsgSize; // Size of received message
            string sourceAddress; // Address of datagram source
            unsigned short sourcePort; // Port of datagram source

            clock_t last_cycle = clock();
            while (!fstop) {
                // Block until receive message from a server
               do {
                    cout<<"wait for message"<<endl;
                    recvMsgSize = sock.recvFrom(buffer, BUF_LEN, sourceAddress, sourcePort);
                } while (recvMsgSize > sizeof(int));
                int total_pack = ((int * ) buffer)[0];

                cout << "expecting length of packs:" << total_pack << endl;
                char * longbuf = new char[PACK_SIZE * total_pack];
                for (int i = 0; i < total_pack; i++) {
                    recvMsgSize = sock.recvFrom(buffer, BUF_LEN, sourceAddress, sourcePort);
                    if (recvMsgSize != PACK_SIZE) {
                        cerr << "Received unexpected size pack:" << recvMsgSize << endl;
                        cout<< buffer <<endl;
                        continue;
                    }
                    memcpy( & longbuf[i * PACK_SIZE], buffer, PACK_SIZE);
                }

                cout << "Received packet from " << sourceAddress << ":" << sourcePort << endl;

                cv::Mat rawData = cv::Mat(1, PACK_SIZE * total_pack, CV_8UC1, longbuf);
                cv::Mat frame = imdecode(rawData, CV_LOAD_IMAGE_COLOR);
                if (frame.size().width == 0) {
                    cerr << "decode failure!" << endl;
                    continue;
                }
                //imshow("recv", frame);
                emit cameraRetrived(frame);
                free(longbuf);

                //cv::waitKey(1);
                clock_t next_cycle = clock();
                double duration = (next_cycle - last_cycle) / (double) CLOCKS_PER_SEC;
               cout << "\teffective FPS:" << (1 / duration) << " \tkbps:" << (PACK_SIZE * total_pack / duration / 1024 * 8) << endl;

                //cout << next_cycle - last_cycle;
                last_cycle = next_cycle;
            }

        } catch (SocketException & e) {
            cerr << e.what() << endl;
            exit(1);
        }
}

void streamingThread::stopStreaming(){
    fstop = true;
}
