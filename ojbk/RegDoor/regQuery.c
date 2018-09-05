#include <stdio.h>
#include <windows.h>

void main(){
    long lRet;
    HKEY hKey;
    TCHAR tchData[64];

    DWORD dwSize;

    char sub[] = "HARDWARE\\DESCRIPTION\\System\\CentralProcessor\\0";
    lRet = RegOpenKeyEx(HKEY_LOCAL_MACHINE, sub, 0, KEY_QUERY_VALUE, &hKey);

    if(lRet == ERROR_SUCCESS){  //open success
        dwSize = sizeof(tchData);
        lRet = RegQueryValueEx(hKey, "ProcessorNameString", NULL, NULL, (LPBYTE)tchData, &dwSize);

        if(lRet == ERROR_SUCCESS)
            printf("CPU info: %s\n", tchData);
        else
            printf("CPU info: Unknow\n");

        RegCloseKey(hKey);
    }
}
