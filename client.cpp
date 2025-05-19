#include <iostream>
#include <string>
#include <cstring>
#ifdef _WIN32
  #include <winsock2.h>
  #include <ws2tcpip.h>
  #pragma comment(lib, "Ws2_32.lib")
#else
  #include <sys/socket.h>
  #include <netinet/in.h>
  #include <arpa/inet.h>
  #include <unistd.h>
  #include <cerrno>
#endif
using namespace std;

class Client
{
public:
    bool connect_to(const char* host = "127.0.0.1", int port = 9000){
        // AF_INET: IPv4, SOCK_STREAM: TCP

        #ifdef _WIN32
            sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
            if (sock == INVALID_SOCKET) {
                std::cerr << "socket() failed: " << WSAGetLastError() << "\n";
                return false;
            }
        #else
            sock = socket(AF_INET, SOCK_STREAM, 0);
            if (sock < 0) {
                perror("socket");
                return false;
            }
        #endif

        // set server address at `host` `port`
        sockaddr_in serv_addr;
        serv_addr.sin_family = AF_INET;
        serv_addr.sin_port = htons(port);
        inet_pton(AF_INET, host, &serv_addr.sin_addr);



        // connect to python server
        connect(sock, (struct sockaddr*)&serv_addr, sizeof(serv_addr));
        
        #ifdef _WIN32
            if (connect(sock, (sockaddr*)&serv_addr, sizeof(serv_addr)) == SOCKET_ERROR) {
                std::cerr << "connect() failed: " << WSAGetLastError() << "\n";
                closesocket(sock);
                sock = INVALID_SOCKET;
                return false;
            }
        #else
            if (connect(sock, (sockaddr*)&serv_addr, sizeof(serv_addr)) < 0) {
                perror("connect");
                close(sock);
                sock = -1;
                return false;
            }
        #endif



        return true;
    }
    void disconnect(){
        #ifdef _WIN32
            if (sock != INVALID_SOCKET) {
                closesocket(sock);
                sock = INVALID_SOCKET;
            }
        #else
            if (sock >= 0) {
                close(sock);
                sock = -1;
            }
        #endif
    }
    // you may want to change how data is exchange
    bool send_data(string state, int action){
        // send training data
        string msg = "{\"state\":\"" + state + "\",\"action\":" + std::to_string(action) + "}";

    #ifdef _WIN32
        int sent = send(sock, msg.c_str(), static_cast<int>(msg.size()), 0);
        if (sent == SOCKET_ERROR) {
            std::cerr << "send() failed: " << WSAGetLastError() << "\n";
            return false;
        }
        char buf[64] = {0};
        int rec = recv(sock, buf, sizeof(buf), 0);
        if (rec > 0) std::cout << "Server Response: " << buf << "\n";
    #else
        ssize_t sent = send(sock, msg.c_str(), msg.size(), 0);
        if (sent < 0) {
            perror("send");
            return false;
        }
        char buf[64] = {0};
        ssize_t rec = recv(sock, buf, sizeof(buf), 0);
        if (rec > 0) std::cout << "Server Response: " << buf << "\n";
    #endif
        return true;
    }
private:
    int sock;
};

