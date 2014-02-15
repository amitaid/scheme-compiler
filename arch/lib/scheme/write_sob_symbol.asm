/* scheme/write_sob_symbol.asm
 * Take a pointer to a Scheme symbol object, and
 * prints (to stdout) the character representation
 * of that object.
 *
 * Programmer: Mayer Goldberg, 2010
 */

 WRITE_SOB_SYMBOL:

  PUSH(FP);
  MOV(FP, SP);
  PUSH(R1);
  PUSH(R2);
  PUSH(R3);

  MOV(R0, FPARG(0));
  MOV(R0, INDD(R0,1));
  MOV(R0, IND(R0));

  MOV(R1, INDD(R0, 1));
  MOV(R2, R0);
  ADD(R2, IMM(2));
 
 L_WRITE_SYMBOL_LOOP:
  CMP(R1, IMM(0));
  JUMP_EQ(L_WRITE_SYMBOL_EXIT);
  
  PUSH(IND(R2));
  CALL(PUTCHAR);
  DROP(1);

 L_WRITE_SYMBOL_LOOP_CONT:
  INCR(R2);
  DECR(R1);
  JUMP(L_WRITE_SYMBOL_LOOP);
 L_WRITE_SYMBOL_EXIT:

  POP(R3);
  POP(R2);
  POP(R1);
  POP(FP);
  RETURN;

