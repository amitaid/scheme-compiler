/* cons.asm
 * Takes two parameters and puts them in a new pair object
 *
 * Programmer: Amitai Degani, Tal Zelig, 2014
 */

 CONS:
  PUSH(FP);
  MOV(FP,SP);

  MOV(R0, FPARG(1));
  CMP(R0, IMM(2));

  // ERROR

  PUSH(FPARG(3));
  PUSH(FPARG(2));
  CALL(MAKE_SOB_PAIR));
  DROP(2);

  POP(FP);
  RETURN;


