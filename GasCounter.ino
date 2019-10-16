
/*    CODE ONLINE REFERENCES
Title: Arduino and DS3231 Real Time Clock Tutorial 
Author: Dejan
Date: August 2016
Availability: https://howtomechatronics.com/tutorials/arduino/arduino-ds3231-real-time-clock-tutorial/

Title: Time Difference 
Author: Unknown
Date: Oct. 8, 2015
Availability: https://pastebin.com/sfEjA94n

Title: Timekeeping on ESP8266 & Arduino Uno WITHOUT an RTC (Real Time Clock)?
Author: Ruben Marc Speybrouck
Date: Oct. 8, 2015
Availability: https://www.instructables.com/id/TESTED-Timekeeping-on-ESP8266-Arduino-Uno-WITHOUT-/

 */

#include <config.h>
#include <Wire.h>
#include <Ds3231.h>
#include <Time.h>
#include "TimeLib.h"
#include <SPI.h>
#include <SD.h>

int tip=30;
int connections[30];
int status_Reed[30]; 
int pin=22;
int Status;
int Statistics[30][30][2]={0};  //30 Gas counter, for 30 days, need to see the day and the sum volume for that day
String Day,Month,Year,T_Date, files[30];
const int rows = 30;
const int columns = 4; //time, hour rate, minute rate, day rate
int Volumes[30];
int rates[rows][columns]; //Will hold the rates for each reactor

File currentFile;
DS3231 rtc(SDA, SCL); //initialize the RTC
time_t t = now(); // Store the current time in time

void setup(){
   Wire.begin(); // Initialize the rtc object linked to the real time clock   
   Serial.print("Initializing SD card...");
    
  if (!SD.begin(4)) {
    Serial.println("initialization failed!");
    while (1);
  }
  
  Day=day(t);
  Month=month(t);
  Year=year(t);
  
  if(day(t)<10){Day="0"+day(t));
  if(month(t)<10){Month="0"+month(t));
  
  //Setup the input pins and insert in an array as well as the reed switch status.
  memset(rates,0,sizeof(rates));
  memset(Volumes,0,sizeof(Volumes));
  T_Date=rtc.getDateStr(); //Today's date (important);
  
  for(int i=0;i<30;i++)
  {
    status_Reed[i]=0;
    connections[i]=pin;
    pinMode(connections[i], INPUT);
    files[i]=Year+Month+Day+"-"+"GC"+String(i)+".csv"; //Initialize files
    initializeFile(i);
    pin++;
  } 
}

void loop(){
  for(int j; j<30;i++){
  status_Reed[j] = digitalRead(connections[j]); 
  if (status_Reed[j] == HIGH){
    Status=CheckFile(j);
    if(Status){
      initializeFile(j);
    }
    
  }
 }
}

int CheckFile(int id)
{
  if (SD.exists(files[id])) {
      String fileDate=files[id].readStringUntil('-'); 
      fileDay=(fileDate.substring(6,8)).toInt();
      fileMonth=(fileDate.substring(4,6)).toInt();
      fileYear=(fileDate.substring(0,4)).toInt();
      
      tmElements_t date1 = {0, 0, 0, 0, fileDay, fileMonth, CalendarYrToTm(fileYear))}, // 0:00:00 1st Jan 2015 //Yet to know how this works
                   date2 = {0, 0, 0, 0, day(t), month(t), CalendarYrToTm(year(t)))}; // 0:00:00 8th Oct 2015 (today)
 
    uint32_t difference = (uint32_t)(makeTime(time2) - makeTime(time1)); //Substract old date with today's date
    uint16_t Days=difference/(86400); //Get the difference value in days
    
    currentFile=SD.open(files[id]));
    Filesize=(currentFile.size)/(pow(10,-6));
    if(Filesize>=10 || Days>=30){
      SD.remove(files[id]);
      files[id]="";
      return 1;
    }
  }
  return 0;
}

void initializeFile(id)
{
  currentFile = SD.open(files[id], FILE_WRITE);
  currentFile.println("Date,Time,Volume");
  currentFile.close();
}
  
