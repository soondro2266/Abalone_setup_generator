#include <iostream>
#include <string>
#include <cstring>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <arpa/inet.h>

using namespace std;

class Client
{
public:
    Client(){}
    Client(const char* host = "127.0.0.1", int port = 9000){
        // AF_INET: IPv4, SOCK_STREAM: TCP
        sock = socket(AF_INET, SOCK_STREAM, 0);
        // set server address at `host` `port`
        sockaddr_in serv_addr;
        serv_addr.sin_family = AF_INET;
        serv_addr.sin_port = htons(port);
        inet_pton(AF_INET, host, &serv_addr.sin_addr);
        // connect to python server
        connect(sock, (struct sockaddr*)&serv_addr, sizeof(serv_addr));
    }
    ~Client(){
        // close the connection
        close(sock);
    }
    // you may want to change how data is exchange
    void send_data(string state, int action){
        // send training data
        string msg = "{\"state\":\"" + state + "\",\"action\":" + std::to_string(action) + "}";
        send(sock, msg.c_str(), msg.size(), 0);
        char buffer[10] = {0};
        recv(sock, buffer, 10, 0);
        cout << "Server Response: " << buffer << "\n";
    }
private:
    int sock;
};

