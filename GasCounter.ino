
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

#include <Wire.h>
#include <DS3231.h>
#include <Time.h>
#include <TimeLib.h>
#include <SPI.h>
#include <SD.h>
#include <string.h>
#include <Ethernet.h>
#include <UbidotsEthernet.h>



bool century=false;
bool h12,PM;
int connections[30],status_Reed[30],ip=30,pin=22,Status,tip=30;
int Statistics[30][30][1] = {0}; //30 gas counter, 30 days for each, total volume for each day
String Day, Month, Year, T_Date, Hour, Min, Second, files[30];

const int rows = 30;
const int columns = 4; //time, hour rate, minute rate, day rate
int Volumes[30];

unsigned long timeNow = 0,timeLast = 0;
int startingHour,start_sec=0,start_min,start_hours,compute_days = 0,old_days=0;
int dailyErrorFast = 0; // set the average number of milliseconds your microcontroller's time is fast on a daily basis
int dailyErrorBehind = 0; // set the average number of milliseconds your microcontroller's time is behind on a daily basis
int correctedToday = 1; // do not change this variable, one means that the time has already been corrected today for the error in your boards crystal. This is true for the first day because you just set the time when you uploaded the sketch.  
 


File currentFile;
DS3231 rtc; //initialize the RTC


void setup() {
  Serial.begin(9600);
  Wire.begin(); // Initialize the rtc object linked to the real time clock

  if (!SD.begin(4)) {
    Serial.println("initialization SD failed!");
    while (1);
  }

  Day = String(rtc.getDate(),DEC);
  Month =String(rtc.getMonth(century),DEC);
  Year = String(rtc.getYear(),DEC);

  startingHour=rtc.getHour(h12, PM);
  start_hours=startingHour;
  start_min=rtc.getMinute();
  
  if (Day.toInt() < 10) {Day = "0" + Day;}
  if (Month.toInt() < 10) {Month = "0" + Month;}

  //Setup the input pins and insert in an array as well as the reed switch status.
  memset(Volumes, 0, sizeof(Volumes));

  for (int i = 0; i < 30; i++)
  {
    status_Reed[i] = 0;
    connections[i] = pin;
    pinMode(connections[i], INPUT);
    files[i] = Year + Month + Day + "-" + "GC" + String(i) + ".csv"; //Initialize files
    initializeFile(i);
    pin++;
  }
}

void loop() {
 timeNow = millis()/1000;
 start_sec = timeNow - timeLast;
 
 if (start_sec == 60) {
  timeLast = timeNow;
  start_min = start_min + 1;
 }

  if (start_min == 60){ 
  start_min = 0;
  start_hours = start_hours + 1;
  }

  if (start_hours == 24){
  start_hours = 0;
  compute_days = compute_days + 1;
  }

  if (start_hours ==(24 - startingHour) && correctedToday == 0){
  delay(dailyErrorFast*1000);
  start_sec = start_sec + dailyErrorBehind;
  correctedToday = 1;
  }

  if (start_hours == 24 - startingHour + 2) { 
  correctedToday = 0;
  }
  
  Year = String(rtc.getYear(), DEC);
  Month = String(rtc.getMonth(century), DEC);
  Day = String(rtc.getDate(), DEC);

  for (int j; j < 30; j++) {
    Hour = String(rtc.getHour(h12, PM), DEC);
    Min = String(rtc.getMinute(), DEC);
    Second = String(rtc.getSecond(), DEC);
    if(compute_days>old_days){
      Volumes[j]=0;
    }
    status_Reed[j] = digitalRead(connections[j]);
    if (status_Reed[j] == HIGH){
      Status = CheckFile(j);
      if (Status) {
        initializeFile(j);
      }
      Volumes[j]=Volumes[j]+tip;
      
      Statistics[j][compute_days][0]=Volumes[j];
      currentFile = SD.open(files[j], FILE_WRITE);
      currentFile.print(Year + "/" + Month + "/" + Day + "," + Hour + ":" + Min + ":" + Second + ","+String(Volumes[j],DEC));
      currentFile.close();
    }
  }
  old_days=compute_days;
}

int CheckFile(int id)
{
  if (SD.exists(files[id])) {
    String fileDate = files[id].substring(0,8); 
    int fileYear = (fileDate.substring(0, 4)).toInt();
    int fileMonth = (fileDate.substring(4, 6)).toInt();
    int fileDay = (fileDate.substring(6)).toInt();

    tmElements_t date1 = {0, 0, 0, 0, fileDay, fileMonth, CalendarYrToTm(fileYear)},
    date2 = {0, 0, 0, 0, rtc.getDate(), rtc.getMonth(century), CalendarYrToTm(rtc.getYear())};

    uint32_t difference = (uint32_t)(makeTime(date2) - makeTime(date1)); //Substract old date with today's date
    uint16_t Days = difference / (86400); //Get the difference value in days

    currentFile = SD.open(files[id]);
    int Filesize = (currentFile.size()) / (pow(10, -6));
    if (Filesize >= 10 || Days >= 30) {
    SD.remove(files[id]);
    Volumes[id]=0;
      files[id] = "";
      return 1;
    }
  }
  return 0;
}

void initializeFile(int id)
{
  currentFile = SD.open(files[id], FILE_WRITE);
  currentFile.print("Date,Time,Volume");
  currentFile.close();
}

int getDay(){
  
}
