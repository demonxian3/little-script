#include <stdio.h>
#include <windows.h>

int main(){
    char szModule[MAX_PATH];
    HKEY hRoot = HKEY_LOCAL_MACHINE, hKey;
    char *szSubKey = "Software\\Microsoft\\Windows\\CurrentVersion\\Run";
    DWORD dwDisposition = REG_OPENED_EXISTING_KEY;  //if key is exist , open it
    //REG_CREATED_NEW_KEY  #if key is not exist , create it

    LONG lRet = RegCreateKeyEx(hRoot, szSubKey, 0, NULL, REG_OPTION_NON_VOLATILE, 
            KEY_ALL_ACCESS, NULL, &hKey, &dwDisposition);

    if (lRet != ERROR_SUCCESS){
        return 1;
    }

    //get current execute filename
    GetModuleFileName(NULL, szModule, MAX_PATH);
    lRet = RegSetValueEx(hKey, "SelfRunDemo", 0, REG_SZ, (BYTE*)szModule, strlen(szModule));

    if (lRet == ERROR_SUCCESS)
        printf("self write to auto run sucess\n");
    else if(lRet == 5)
        printf("permission deny, please run as administrator\n");
    else
        printf("ret is : %ld\n", lRet);

    RegCloseKey(hKey);

    return 0;
}
