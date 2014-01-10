/* mult.asm
 * R0 <- product(args)
 *
 * Programmer: Amitai Degani, Tal Zelig, 2014
 */

 MULT:
  MOV(R0, IMM(1));
  MOV(R1, FPARG(0));
 MULT_LOOP:
  CMP(R1, IMM(0));
  JUMP_EQ(PLUS_EXIT);
  MUL(R0, FPARG(R1));
  SUB(R1, IMM(1));
  JUMP(PLUS_LOOP);
 MULT_EXIT:
  POP(FP);
  RETURN;
