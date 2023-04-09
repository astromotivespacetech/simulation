// pin definitions
#define FUEL_DIR_PIN      2
#define FUEL_STEP_PIN     3
#define FUEL_ENA_PIN      4
#define FUEL_PROX_PIN     5
#define LOX_DIR_PIN       6
#define LOX_STEP_PIN      7
#define LOX_ENA_PIN       8
#define LOX_PROX_PIN      9
#define CLOCKWISE         LOW
#define COUNTERCLOCKWISE  HIGH




// microstepping parameter [dip switches on driver to set]. This is the # of steps per full revolution.
int microsteps = 400;

// define a speed (revolutions per second)
int speed = 0.25; // e.g. 90 deg turn in one second

// gearbox ratio
int ratio = 10;

// number of steps per second
float steps_per_sec = microsteps * speed * ratio;

// define a step delay interval (each step requires a HIGH and a LOW, so divide by 2) [micros]
unsigned long step_delay = (unsigned long)(1.0 / steps_per_sec * 0.5 * 1e6);


// note: you could specify a lox_step_delay and a fuel_step_delay if you want different actuation speeds


// motor class
struct Motor {
  int dirPin;
  int stepPin;
  int enaPin;
  int proxPin;
  int dirState;
  int stepState;
  int enaState;
  unsigned long prevStep;     // micros
  unsigned long stepDelay;    // micros
  int stepCount;
  int target;
  int offset;                 // number of steps relative to the prox sensor for 'closed' - must be calibrated
};


// tune your homing procedure by changing these values until the valves are in a closed position
int fuel_offset = 50;
int lox_offset = 50;

// initialize motor objects
Motor Fuel { FUEL_DIR_PIN, FUEL_STEP_PIN, FUEL_ENA_PIN, FUEL_PROX_PIN, LOW, LOW, LOW, 0, step_delay, 0, 0, fuel_offset };
Motor Lox { LOX_DIR_PIN, LOX_STEP_PIN, LOX_ENA_PIN, LOX_PROX_PIN, LOW, LOW, LOW, 0, step_delay, 0, 0, lox_offset };



void setup() {

  // Serial port stuff
  Serial.begin(115200);

  // pinmode stuff
  pinMode(FUEL_DIR_PIN, OUTPUT);
  pinMode(FUEL_STEP_PIN, OUTPUT);
  pinMode(FUEL_ENA_PIN, OUTPUT);
  pinMode(FUEL_PROX_PIN, INPUT);
  pinMode(LOX_DIR_PIN, OUTPUT);
  pinMode(LOX_STEP_PIN, OUTPUT);
  pinMode(LOX_ENA_PIN, OUTPUT);
  pinMode(LOX_PROX_PIN, INPUT);


  // Enable the drivers so that we can run the homing function
  Fuel.enaState = HIGH;
  Lox.enaState = HIGH;
  digitalWrite(Fuel.enaPin, Fuel.enaState);
  digitalWrite(Lox.enaPin, Lox.enaState);


  // Call valve homing function to ensure valves start in a known position.
  valveHome(&Fuel);
  valveHome(&Lox);


  // Now that our valves are in a known position, pull the enable pins low in order to disable
  // the motor drivers e.g. 'disarmed'.
  Fuel.enaState = LOW;
  Lox.enaState = LOW;
  digitalWrite(Fuel.enaPin, Fuel.enaState);
  digitalWrite(Lox.enaPin, Lox.enaState);
}



void loop() {

  // Do all program stuff here e.g. sensors, state machine, send+receive  commands, etc.
  //

  // Here you can update the motor target
  Fuel.target = 0;
  Lox.target = 0;

  // Here you can enable or disable the motor drivers
  int fuelEnaState = LOW;
  int loxEnaState = LOW;

  // check if the above enable command differs from the motor enaState variable
  if (fuelEnaState != Fuel.enaState) {
    Fuel.enaState = fuelEnaState;
    digitalWrite(Fuel.enaPin, Fuel.enaState);
  }

  if (loxEnaState != Lox.enaState) {
    Lox.enaState = loxEnaState;
    digitalWrite(Lox.enaPin, Lox.enaState);
  }

  // call valve operate with each motor
  valveOperate(&Fuel);
  valveOperate(&Lox);

}



void valveOperate(Motor *m) {

  // check if motor is enabled
  if (m->enaState == HIGH) {

    // check to see if the motor position is different from it's target
    if (m->stepCount != m->target) {

      // set the direction (may need to reverse this)
      int dirState = (m->stepCount < m->target) ? CLOCKWISE : COUNTERCLOCKWISE;

      // update the motor's dirState and write to driver
      if (dirState != m->dirState) {
        m->dirState = dirState;
        digitalWrite(m->dirPin, m->dirState);
      }

      // check to see if motor is ready to move another step
      if (micros() - m->prevStep > m->stepDelay) {

        // increment the motor step
        m->stepState = (m->stepState) ? LOW : HIGH;  // toggle from high to low or vice versa

        // only increment when stepState is HIGH. If dir is 0, then it will multiply by
        // -1, thus decrementing stepCount, otherwise if dir is 1, then it will multiply
        // by 1, incrementing stepCount
        m->stepCount += (1 * m->stepState) * (2 * m->dirState - 1);

        digitalWrite(m->stepPin, m->stepState);

        // update prevStep
        m->prevStep = micros();
      }

    }

  }

}



void valveHome(Motor *m) {

  // not homed yet
  bool homed = false;

  // variable for proximity sensor reading
  int proxState = 0;

  // lets make sure we debounce our proximity sensor
  int proxDebounce = 0;

  // need to get 5 consecutive readings
  while (proxDebounce < 5) {

    // get reading from proximity sensor
    int prox = digitalRead(PROX_PIN);

    // increment proxDebounce if we get consistent readings, otherwise start over
    if (prox == proxState) {
      proxDebounce++;
    } else {
      proxDebounce = 0;
    }

    // set proxState to the most recent reading
    proxState = prox;
  }


  // update the target, depending on the current proxState. This will automatically result in
  // either a clockwise or counterclockwise rotation
  if (proxState) {
    m->target = -microsteps;
  } else {
    m->target = microsteps
  }


  // keep going until homed!
  while (!homed) {

    // need to find the 'leading edge' of the proximity sensor in the clockwise direction, and
    // this is our "HOME" position. From there, we can move to a "CLOSED" position by
    // moving 'X' number of steps past this based on our manual calibration, which we define in
    // our motor's 'offset' parameter.

    valveOperate(&m);

    // check to see if homed
    int homed = checkProx(&proxState, m->proxPin);
  }

  // now that our valve is homed, move the valve to the closed position
  if (homed) {

    // let's zero out the stepCount
    m->stepCount = 0;

    // and let's set the target to be the motor offset, and since the stepCount is zero,
    // the target will be greater so it should automatically rotate clockwise
    m->target = m->offset;

    // keep going until we reach the target
    while (m->stepCount != m->target) {
      valveOperate(&m);
    }

    // valve should now be in the 'CLOSED' position, so lets set the stepCount to 0
    m->stepCount = 0;

    // now we are ready to test!
  }

}





int checkProx(int *ps, int proxPin) {

  status = false;

  // if proximity sensor is now reading different from proxState
  if (digitalRead(proxPin) != ps) {

    // new debounce variable
    int debounce = 0;
    bool checking = true;

    // keep going until no longer checking
    while (checking) {

      // take new reading
      prox = digitalRead(proxPin);

      // increment proxDebounce if we get consistent readings, otherwise start over
      if (prox == ps) {
        debounce++;

      } else {
        debounce = 0;
        checking = false;
      }

      // if we get 5 consecutive readings, then we can confirm!
      if (debounce == 5) {
        status = true;
        checking = false;
      }

    }

  }

  // returns false by default
  return status
}
