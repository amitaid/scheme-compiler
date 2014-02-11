/* scheme/make_sob_fraction.asm
 * Takes two integers, numerator and denumerator.
 * Determines whether they represent an int or fraction,
 * and returns the corresponding object.
 *
 * Programmer: Amitai Degani, 2014
 */

 MAKE_SOB_NUMBER:
  PUSH(FP);
  MOV(FP, SP);

  MOV(R0, FPARG(0));
  MOV(R1, FPARG(1));
  MOV(R2,R0);
  REM(R2,R1);
  CMP(R2,IMM(0));
  JUMP_NE(MAKE_NUMBER_FRAC);

 MAKE_NUMBER_INT:
  DIV(R0,R1);
  PUSH(R0);
  CALL(MAKE_SOB_INTEGER);
  DROP(1);
  JUMP(MAKE_NUMBER_EXIT);

 MAKE_NUMBER_FRAC:
  PUSH(R0);
  CALL(MAKE_SOB_INTEGER);
  DROP(1);
  MOV(R2, R0);
  PUSH(R1);
  CALL(MAKE_SOB_INTEGER);
  DROP(1);
  PUSH(R0);
  PUSH(R2);
  CALL(MAKE_SOB_FRACTION);
  DROP(2);

 MAKE_NUMBER_EXIT:
  POP(FP);
  RETURN;
