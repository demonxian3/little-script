#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <getopt.h>
#include <sys/time.h>
#include <assert.h>
#ifndef WIN32
#include <syslog.h>
#endif
#include <signal.h>
#include <sys/types.h>
#include <errno.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <termios.h>

//==========version:1.6================
//=====================================
//              文件路径
//=====================================
char mqttorder[30] = "/root/mqttorder";
char mqttpid[30]   = "/root/mqttpid";
char mqttlog[30]   = "/root/mqttlog";

//延迟时间单位微秒
unsigned delay = 200000;

//=====================================
//              串口变量 
//=====================================
int fd=0,fdi=0;
char serbuff[200]="";


/******************************************************************************
描述:   打开与arduino板连接的串口设备
输入值: int serial device, int port number
输出值: int serial device
******************************************************************************/
int open_port(int fd,int comport){
  switch(comport){
     case 1:
	fd = open("/dev/ttyS0", O_RDWR|O_NOCTTY|O_NDELAY);
        if(-1 == fd){perror("Can't open serial port");exit(-1);}
	else printf("open ttyS0 ... \n");
	break;

     case 2:
	fd = open( "/dev/ttyS1", O_RDWR|O_NOCTTY|O_NDELAY);
	if(-1 == fd){perror("Can't open serial port");exit(-1);}
	else printf("open ttyS1 ... \n");
	break;

     case 3:
	fd = open( "/dev/ttyS2", O_RDWR|O_NOCTTY|O_NDELAY);
	if(-1 == fd){perror("Can't open serial port");exit(-1);}
	else printf("open ttyS2 ... \n");
	break;
  }

    if(fcntl(fd, F_SETFL, 0)<0)
        printf("fcntl failed!\n");
    else
        printf("fcntl=%d\n",fcntl(fd, F_SETFL,0));


    if(isatty(STDIN_FILENO)==0)
        printf("standard input is not a terminal device\n");
    else
        printf("isatty success!\n");


    printf("fd-open=%d\n",fd);
    return fd;
}


/******************************************************************************
描述:   为串口设置参数
输入值: serial device, speed , bits, event, stop 
输出值: 0(success),-1(failed)
******************************************************************************/
int set_opt(int fd,int nSpeed, int nBits, char nEvent, int nStop)
{
    struct termios newtio,oldtio;
    if  (tcgetattr(fd,&oldtio) != 0){ 
        perror("SetupSerial 1");
        return -1;
    }
    bzero( &newtio, sizeof( newtio ) );
    newtio.c_cflag  |=  CLOCAL | CREAD; 
    newtio.c_cflag &= ~CSIZE; 

    switch(nBits){
    case 7:
        newtio.c_cflag |= CS7;
        break;
    case 8:
        newtio.c_cflag |= CS8;
        break;
    }

    switch(nEvent){
    case 'O':                     //奇校验
        newtio.c_cflag |= PARENB;
        newtio.c_cflag |= PARODD;
        newtio.c_iflag |= (INPCK | ISTRIP);
        break;
    case 'E':                     //偶校验
        newtio.c_iflag |= (INPCK | ISTRIP);
        newtio.c_cflag |= PARENB;
        newtio.c_cflag &= ~PARODD;
        break;
    case 'N':                    //无校验
        newtio.c_cflag &= ~PARENB;
        break;
    }

    switch(nSpeed){
    case 2400:
        cfsetispeed(&newtio, B2400);
        cfsetospeed(&newtio, B2400);
        break;
    case 4800:
        cfsetispeed(&newtio, B4800);
        cfsetospeed(&newtio, B4800);
        break;
    case 9600:
        cfsetispeed(&newtio, B9600);
        cfsetospeed(&newtio, B9600);
        break;
    case 115200:
        cfsetispeed(&newtio, B115200);
        cfsetospeed(&newtio, B115200);
        break;
    default:
        cfsetispeed(&newtio, B9600);
        cfsetospeed(&newtio, B9600);
        break;
    }

    if( nStop == 1 )
        newtio.c_cflag &=  ~CSTOPB;
    else if ( nStop == 2 )
        newtio.c_cflag |=  CSTOPB;

    newtio.c_cc[VTIME]  = 0;
    newtio.c_cc[VMIN] = 0;
    tcflush(fd,TCIFLUSH);

    if((tcsetattr(fd,TCSANOW,&newtio))!=0){
        perror("com set error");
        return -1;
    }

    printf("set done!\n");
    return 0;
}


/******************************************************************************
描述:   用于初始化清空mqttorder文件
输入值：void
输出值：void
******************************************************************************/
void clearfile(void){
     char command[100] = "echo >";
     strcat(command,mqttorder);
     system(command);
}


//=====================================
//              主函数
//=====================================
int main(void){
  
 int i;
 char buff[20]={0};
 char buffbak[20]={0};
 char command[200]={0};
 char srt[4]={0};
 int  len;


//status状态标记,用于标记启动了哪个模块防止重复启动,及标识哪些传感器需要上报数据
   struct STA{
    unsigned camera:1;
    unsigned motion:1;
    unsigned wifipr:1;  
    unsigned temper:1;  //传感器
    unsigned infra:1;   //传感器
    unsigned sound:1;   //传感器
  }status;


//初始化：0关闭 1启动
  status.camera=0;
  status.motion=0;
  status.wifipr=0;
  status.temper=0;
  status. infra=0;
  status.sound=0;
//=====================================
//              开始执行
//=====================================

//清空mqttorder文件
clearfile();

//开启串口
if((fd=open_port(fd,1))<0){
  perror("open_port error");
  exit(-1);
}

//设置串口参数
if((fdi=set_opt(fd,9600,8,'N',1))<0){
  perror("set_opt error");
  exit(-1);
}

//订阅mqtt服务器
system("killall -9 mosquitto_sub >/dev/null 2>&1");
int cmd = system("mosquitto_sub  -t  888888888888 -h 120.25.172.6 &");
if(cmd){
   perror("mosquitto_pub excute failed:");
   exit(-1);
}


//主流程
 while(1){ 

   /*====================   读取mqttorder指令   ======================*/

   FILE * pf = fopen(mqttorder,"r");
   len = fread(buff,1,20,pf) - 1;

   //与上次命令比较是否相同，防止重复执行
   if(strcmp(buff,buffbak) != 0 && len > 0 ){
   	 strncpy(srt,buff,3);

//=====================================
//	           摄像头行为模块 
//=====================================

      if(strncmp(srt,"cam",3) == 0){
	  //开启摄像头
	  if	 (strncmp(buff,"campic-on",len) == 0){
	    if(status.camera != 1){
		system("nohup mjpg_streamer -i \"input_uvc.so -d /dev/video0 -r 320x240 -f 3\" -o \"output_file.so -f /tmp -d 400\" &");//1
		status.camera = 1;
	    }
	  }

	  //关闭摄像头
	  else if(strncmp(buff,"campic-off",len) == 0){
	    if(status.camera != 0){
		system("killall -9 mjpg_streamer 2>/dev/null");
		status.camera = 0;
	    }
	  }

      //注意：这里需要len-2是因为收到的指令是camera-up-1或者camera-up-0
      //所以如果长度不减少2的话会导致匹配不上，至于为什么要设置成camera-up-1
      //和camera-up-0，我想是因为摄像头是允许连续发送指令给arduino的
	  else if(strncmp(buff,"camera-up",len-2) == 0){    
		char *contt = {"a"};
		write(fd,contt,strlen(contt));
		printf("a\n");
	  }
	  else if(strncmp(buff,"camera-right",len-2) == 0){
		char *contt = {"b"};
		write(fd,contt,strlen(contt));
		printf("b\n");
	  }
	  else if(strncmp(buff,"camera-down",len-2) == 0){
		char *contt = {"c"};
		write(fd,contt,strlen(contt));
		printf("c\n");
	  }
	  else if(strncmp(buff,"camera-left",len-2) == 0){
		char *contt = {"d"};
		write(fd,contt,strlen(contt));
		printf("d\n");
	  }
	  else if(strncmp(buff,"camera-center",len-2) == 0){
		char *contt = {"e"};
		write(fd,contt,strlen(contt));
		printf("e\n");
	  }
	
      }
//=====================================
//	           小车行为模块
//=====================================
	else if(strncmp(srt,"car",3) == 0){
	  if	 (strncmp(buff,"car-up",len) == 0){
		char *contt = {"A"};
		printf("A\n");
		write(fd,contt,strlen(contt));
	  }
	  else if(strncmp(buff,"car-right",len) == 0){
		char *contt = {"B"};
		printf("B\n");
		write(fd,contt,strlen(contt));
	  }
	  else if(strncmp(buff,"car-back",len) == 0){
		char *contt = {"C"};
		printf("C\n");
		write(fd,contt,strlen(contt));
	  }
	  else if(strncmp(buff,"car-left",len) == 0){
		char *contt = {"D"};
		printf("D\n");
		write(fd,contt,strlen(contt));
	  }
	  else if(strncmp(buff,"car-stop",len) == 0){
		char *contt = {"E"};
		printf("E\n");
		write(fd,contt,strlen(contt));
	  }
	}
//=====================================
//	           移动侦测模块
//=====================================
	else if(strncmp(srt,"mot",3) == 0){

	  //开启移动侦测motion
	  if	 (strncmp(buff,"motionpic-on",len) == 0){
	    if(status.motion != 1){
		system("nohup motion -c /etc/motion.conf &");
		status.motion = 1;
	    }
	  }

	  //关闭移动侦测motion
	  else if(strncmp(buff,"motionpic-off",len) == 0){
	    if(status.motion != 0){
		system("killall -9 motion 2>/dev/null");
		status.motion = 0;
	    }
	  }
	}

//=====================================
//	            探针模块
//=====================================
	else if(strncmp(srt,"wif",3)==0){

	  //开启探针wifiprobe
	  if	 (strncmp(buff,"wifiprobe-on",len) == 0){
	    if(status.wifipr != 1){
		system("nohup /usr/sbin/iwcap -i mon0 -o aa  -f  -P &");
		status.wifipr=1;
	    }
	  }

	  //关闭探针wifiprobe
	  else if(strncmp(buff,"wifiprobe-off",len) == 0){
	    if(status.wifipr != 0){
		system("killall -9 iwcap 2>/dev/null");
		status.wifipr=0;
	    }
	  }
	}

//=====================================
//	             红外模块
//=====================================
	else if(strncmp(srt,"inf",3)==0){
	  if	 (strncmp(buff,"infralarm-on",len) == 0){
             if(status.infra != 1){
		char *contt = {"N"};
		write(fd,contt,strlen(contt));
		printf("infon\n");
                status.infra = 1;    //开启红外
             }
	  }


	  else if(strncmp(buff,"infralarm-off",len) == 0){
              if(status.infra != 0){
		char *contt = {"n"};
		write(fd,contt,strlen(contt));
		printf("infof\n"); 
                status.infra = 0;    //关闭红外数据读取
              }
	  }
	}

//=====================================
//	           温度模块 
//=====================================
	else if(strncmp(srt,"tem",3) == 0){
	  if	 (strncmp(buff,"temp-on",len) == 0){
             if(status.temper != 1){
		char *contt = {"T"};
		write(fd,contt,strlen(contt));
		printf("temon\n");
                status.temper = 1;    //开启温度
             }
	  }

	  else if(strncmp(buff,"temp-off",len) == 0){
             if(status.temper != 0){
		char *contt = {"t"};
		write(fd,contt,strlen(contt));
		printf("temoff\n");
                status.temper= 0;   //关闭温度
             }
	  }
	}

//=====================================
//	           LED灯模块
//=====================================
	else if(strncmp(srt,"led",3) == 0){
	  if	 (strncmp(buff,"ledctrl-on",len) == 0){
		char *contt = {"l"};
		write(fd,contt,strlen(contt));
		printf("lighton\n");
	  }
	  else if(strncmp(buff,"ledctrl-off",len) == 0){
		char *contt = {"L"};
		write(fd,contt,strlen(contt));
		printf("lightoff\n");
	  }
	}


//=====================================
//	            声音模块
//=====================================
	else if(strncmp(srt,"sou",3)==0){
	  if	 (strncmp(buff,"soundalarm-on",len) == 0){
             if(status.sound != 1){
		char *contt = {"M"};
		write(fd,contt,strlen(contt));
		printf("soundon\n");
                status.sound = 1;   //开启声音
             }
	  }

	  else if(strncmp(buff,"soundalarm-off",len) == 0){
             if(status.sound != 0){
		char *contt = {"m"};
		write(fd,contt,strlen(contt));
		printf("soundoff\n");
                status.sound = 0;   //关闭声音
             }
	  }
	}


	//记录本次指令防止重复执行
	strcpy(buffbak,buff);
   }

   //清空buff，关闭文件流
   memset(buff,0,sizeof(buff));
   fclose(pf);


   /*=================  上传传感数据到服务器  ======================*/
   //注意：read函数不能直接使用，否则会导致进程处于阻塞状态等待串口获取数据
   //如果数据一直不来，那么进程将会一直阻塞而无法进行其他任务。所以只有在传
   //感器功能开启后，才调用read函数读取。
   
     
        //上报温度
        if(status.temper == 1){
          if(read(fd,serbuff,200)>0){
            printf("[read]:%s\n",serbuff);
            if(strstr(serbuff,":")){
               strcpy(command,"mosquitto_pub -t 888888888888/temp -h 120.25.172.6 -m ");
               strcat(command,serbuff);
               system(command);
            }
          }
        }
        
        //上报红外
        if(status.infra == 1){
          if(read(fd,serbuff,200)>0){
            printf("[read]:%s\n",serbuff);
            if(strstr(serbuff,"o")){
               strcpy(command,"mosquitto_pub -t 888888888888/infralarm -h 120.25.172.6 -m ");
               strcat(command,serbuff);
               system(command);
            }
          }
        }

        /*上报声音，这个功能还没做先注释
        if(status.sound == 1){
          if(read(fd,serbuff,200)>0){
            //printf("[read]:%s\n",serbuff);
            if(strstr(serbuff,"sound")){
               strcpy(command,"mosquitto_pub -t 888888888888/sound -h 120.25.172.6 -m ");
               strcat(command,serbuff);
               system(command);
            }
          }
        }
        */

   bzero(serbuff,sizeof(serbuff)); //清除串口接收缓存区
   usleep(delay);                  //周期执行降低cpu
 }
}
