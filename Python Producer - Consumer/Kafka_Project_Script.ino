#include <OneWire.h> 
#include <DallasTemperature.h>

// Define inputs for all 3 sensors
#define LIGHT_SENSOR A0 // Light level sensor (LDR)
#define TEMP_SENSOR 2  // Temperature Sensor (Digital)
#define VOLT_SENSOR A2  // Voltage sensor (Resistor step down)
/********************************************************************/
// Setup a oneWire instance to communicate with any OneWire devices  
// (not just Maxim/Dallas temperature ICs) 
OneWire oneWire(TEMP_SENSOR); 
/********************************************************************/
// Pass our oneWire reference to Dallas Temperature. 
DallasTemperature sensors(&oneWire);
/********************************************************************/ 

// Floats for ADC voltage & Input voltage
float adc_voltage = 0.0;
float in_voltage = 0.0;
 
// Floats for resistor values in divider (in ohms)
float R1 = 30000.0;
float R2 = 7500.0; 
 
// Float for Reference Voltage
float ref_voltage = 5.0;

// Integer for ADC value
int adc_value = 0;

// Float for light sensor input
float LightValue = 0;

//Float for temperature sensor input
float TempValue = 0;

void setup(void)
{
  Serial.begin(9600);
  sensors.begin(); 
}

void loop(void)
{
  sensors.requestTemperatures();
  
  LightValue = analogRead(LIGHT_SENSOR);
  TempValue = sensors.getTempCByIndex(0);
  adc_value = analogRead(VOLT_SENSOR);

  adc_voltage  = (adc_value * ref_voltage) / 1024.0; 
   
   // Calculate voltage at divider input
  in_voltage = adc_voltage / (R2/(R1+R2));
  
  Serial.print(TempValue, 2);
  Serial.print(",");
  Serial.print(LightValue, 2);
  Serial.print(",");
  Serial.println(in_voltage, 2);

  delay(1000);
}
