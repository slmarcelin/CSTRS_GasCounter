
//The code should be able to handle at least 30 simultaneous gas counter connections.
//We will setup an array which has a maximum capacity of 30 and store the pin values in there
//Every time a signal is generated via reed switch record the time stamp from RTC
// The flow rate should be displayed as chart and should be selectable between m,h,d we need to calculate rate per minute, hour and day depending on the times found
//Will the Arduino be always connected? if the code is ran again, the values will be reset.
//  Serial.println(rtc.getTimeStr());

#include <config.h>
#include <Wire.h>
#include "ds3231.h"
#include "Time.h>"
#include <TimeLib.h>
#include <SPI.h>
#include <SD.h>

int tip=30;
int connections[30];
int status_Reed[30]; 
int pin=22;
String Day,Month,Year,T_Date, files[30];
const int rows = 30;
const int columns = 4; //time, hour rate, minute rate, day rate
int rates[rows][columns]; //Will hold the rates for each reactor
File currentFile;
dS3231 rtc(SDA, SCL); //initialize the RTC

void setup(){
   rtc.begin(); // Initialize the rtc object linked to the real time clock   
   Serial.print("Initializing SD card...");
    
  if (!SD.begin(4)) {
    Serial.println("initialization failed!");
    while (1);
  }
  time_t t = now(); // Store the current time in time
  
  Day=day(t);
  Month=month(t);
  Year=year(t);
  
  if(day(t)<10){Day="0"+day(t));
  if(month(t)<10){Month="0"+month(t));
  
  //Setup the input pins and insert in an array as well as the reed switch status.
  memset(rates,0,sizeof(rates));
  T_Date=rtc.getDateStr(); //Today's date (important);
  
  for(int i=0;i<30;i++)
  {
    status_Reed[i]=0;
    connections[i]=pin;
    pinMode(connections[i], INPUT);
    files[i]=Year+Month+Day+"-"+"GC"+String(i)+".csv"; //Initialize files
    currentFile = SD.open(files[i], FILE_WRITE);
    currentFile.close();
    pin++;
  }


  
}

void loop(){
  for(int j; j<30;i++){
  status_Reed[j] = digitalRead(connections[j]); 
  if (status_Reed[j] == HIGH){
    //Get Time from reed switch
    }
  }
}

void SetupFiles(int id)
{
  
}
