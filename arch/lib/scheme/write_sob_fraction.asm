/* scheme/write_sob_fraction.asm
 * Take a pointer to a Scheme fraction object, and
 * prints (to stdout) the character representation
 * of that object.
 *
 * Programmer: Amitai Degani, 2014
 */

 WRITE_SOB_FRACTION:
  PUSH(FP);
  PUSH(R1);
  MOV(FP, SP);
  MOV(R0, FPARG(0));
  MOV(R1, INDD(R0, 2));
  PUSH(INDD(R1, 1));
  CALL(WRITE_INTEGER);
  DROP(1);
  PUSH(IMM('/'));
  CALL(PUTCHAR);
  DROP(1);
  MOV(R1, INDD(R0, 1));
  PUSH(INDD(R1, 1));
  CALL(WRITE_INTEGER);
  DROP(1);
  POP(FP);
  RETURN;

