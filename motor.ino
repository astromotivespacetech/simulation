// pin definitions
#define FUEL_DIR_PIN      1
#define FUEL_STEP_PIN     2
#define FUEL_ENA_PIN      3
#define LOX_DIR_PIN       4
#define LOX_STEP_PIN      5
#define LOX_ENA_PIN       6
#define PROX_PIN          7
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



// motor class
struct Motor {
  int dirPin;
  int stepPin;
  int enaPin;
  int dirState;
  int stepState;
  int enaState;
  unsigned long prevStep;     // micros
  unsigned long stepDelay;    // micros
  int stepCount;
  int target;
  int offset;                 // number of steps relative to the prox sensor for 'closed' - must be calibrated
};

// initialize motor objects
Motor Fuel { FUEL_DIR_PIN, FUEL_STEP_PIN, FUEL_ENA_PIN, LOW, LOW, LOW, 0, step_delay, 0, 0, 0 };
Motor Lox { LOX_DIR_PIN, LOX_STEP_PIN, LOX_ENA_PIN, LOW, LOW, LOW, 0, step_delay, 0, 0, 0 };



void setup() {

  // Serial port stuff
  // pinmode stuff

  // Call valve homing function to ensure valves start in a known position.
  // Homing function will automatically enable the motor drivers.
  valveHome(&Fuel);
  valveHome(&Lox);


  // Now that our valves are in a known position, pull the enable pins low in order to disable
  // the motor drivers e.g. 'disarmed'.
  digitalWrite(Fuel.enaPin, Fuel.enaState);
  digitalWrite(Lox.enaPin, Lox.enaState);
}



void loop() {

  // Do all program stuff here e.g. sensors, state machine, send+receive  commands, etc.
  //
  //

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

  // enable the motor driver
  digitalWrite(m->enaPin, HIGH);

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


  if (proxState) {

    // if the proxState is HIGH to begin with, then we know we can rotate counterclockwise
    // to find the leading edge in the clockwise directon.
    m->dirState = LOW;
    digitalWrite(m->dirPin, m->dirState);

  } else {

    // if the proxState is LOW to begin with, let's rotate clockwise until we get a HIGH
    // reading from the proximity sensor
    m->dirState = CLOCKWISE;
    digitalWrite(m->dirPin, m->dirState);
  }


  // keep going until homed!
  while (!homed) {

    // need to find the 'leading edge' of the proximity sensor in the clockwise direction, and
    // this is our "HOME" position. From there, we can move to a "CLOSED" position by
    // moving 'X' number of steps past this based on our manual calibration, which we define in
    // our motor's 'offset' parameter.

    // check to see if motor is ready to move another step
    if (micros() - m->prevStep > m->stepDelay) {

      // increment the motor step
      m->stepState = (m->stepState) ? LOW : HIGH;  // toggle from high to low or vice versa

      // write to pin
      digitalWrite(m->stepPin, m->stepState);

      // update prevStep
      m->prevStep = micros();
    }

    // check to see if homed
    int homed = checkProx(&proxState);
  }

  // now that our valve is homed, move the valve to the closed position
  if (homed) {

    // rotate clockwise for consistency
    m->dirState = CLOCKWISE;
    digitalWrite(m->dirPin, m->dirState);

    // we can just do a loop at this point
    for (int i = 0; i <= m->offset; i++) {

      digitalWrite(m->stepPin, HIGH);
      delayMicroseconds(m->stepDelay);
      digitalWrite(m->stepPin, LOW);
      delayMicroseconds(m->stepDelay);
    }

    // valve should now be in the 'CLOSED' position, so lets set the stepCount to 0
    m->stepCount = 0;

    // now we are ready to test!
  }

}





int checkProx(int *ps) {

  status = false;

  // if proximity sensor is now reading different from proxState
  if (digitalRead(PROX_PIN) != ps) {

    // new debounce variable
    int debounce = 0;

    bool checking = true;

    // keep going until no longer checking
    while (checking) {

      // take new reading
      prox = digitalRead(PROX_PIN);

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
