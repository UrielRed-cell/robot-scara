#include <Arduino.h>
#include <laso.h>
#include <Servo.h>

Serialparser router;
Servo servo_1,servo_2,servo_3;

#define pin_servo_1 1
#define pin_servo_2 2
#define pin_servo_3 3

struct ServoArgs{
    float theta1;
    float theta2;
    laso::u8bit tool;
}__attribute__((packed));

void set_deg(laso::u8bit* payload, laso::u8bit size) { 
    if(size!=sizeof(ServoArgs)) 
        return;
    ServoArgs args;
    memcpy(&args,payload,sizeof(ServoArgs));
    servo_1.write(args.theta1); 
    servo_2.write(args.theta2);
    if(args.tool==1)
        servo_3.write(90);
    else
        servo_3.write(0);
}

void setup(){
    Serial.begin(115200);
    servo_1.attach(pin_servo_1);
    servo_2.attach(pin_servo_2);
    servo_3.attach(pin_servo_3);
    router.addCommand(0x01,&set_deg);
}

void loop(){
    while(Serial.available()){
        router.eatByte(Serial.read());
    }
}
