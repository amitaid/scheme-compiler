/* car.asm
 * Takes a pair object and returns the first item
 *
 * Programmer: Amitai Degani, Tal Zelig, 2014
 */

 CAR:
  PUSH(FP);
  MOV(FP,SP);

  MOV(R0, FPARG(1));
  CMP(R0, IMM(1));

  // ERROR

  MOV(R0, FPARG(2));
  CMP(IND(R0), T_PAIR);

  // ERROR

  MOV(R0, INDD(R0,1));

  POP(FP);
  RETURN;


