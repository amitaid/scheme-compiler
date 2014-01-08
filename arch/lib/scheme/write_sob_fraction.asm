/* scheme/write_sob_fraction.asm
 * Take a pointer to a Scheme fraction object, and
 * prints (to stdout) the character representation
 * of that object.
 *
 * Programmer: Amitai Degani, 2014
 */

 WRITE_SOB_FRACTION:
  PUSH(FP);
  MOV(FP, SP);
  MOV(R0, FPARG(0));
  PUSH(INDD(R0, 1));
  CALL(WRITE_INTEGER);
  PUSH(IMM('/'));
  CALL(PUTCHAR);
  PUSH(INDD(R0, 2));
  CALL(WRITE_INTEGER);
  DROP(3);
  POP(FP);
  RETURN;

