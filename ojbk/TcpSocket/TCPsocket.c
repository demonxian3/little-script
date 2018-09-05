#pragma comment(lib, "ws2_32.lib")
#include <winsock2.h>
#include <stdio.h>

int main(){
	SOCKET srcSock, dstSock;

	struct sockaddr_in srcAddr;
	struct sockaddr_in dstAddr;

	int sin_size;

	WSADATA wsa;
	WSAStartup(MAKEWORD(2,2), &wsa); //≥ı ºªØwin socket

	srcSock = socket(AF_INET, SOCK_STREAM, 0);

	srcAddr.sin_family = AF_INET;
	srcAddr.sin_port = htons(1234);
	srcAddr.sin_addr.s_addr = INADDR_ANY;

	bind(srcSock, (struct sockaddr*)&srcAddr, sizeof(struct sockaddr));

	listen(srcSock, 10);

	printf("listening...");

	sin_size = sizeof(struct sockaddr_in);
	dstSock = accept(srcSock, (struct sockaddr *)&dstAddr, &sin_size);

	send(dstSock, "Hello!\n", sizeof("Hello!\n"), 0);

	printf("send ok !!\n");
	closesocket(srcSock);
	closesocket(dstSock);
	return 0;
}
