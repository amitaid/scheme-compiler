/* minus.asm
 * R0 <- arg0 - sum(args[1..])
 *
 * Programmer: Amitai Degani, Tal Zelig, 2014
 */

 MINUS:
  MOV(R0, FPARG(1));
  MOV(R1, FPARG(0));
 MINUS_LOOP:
  CMP(R1, IMM(1));
  JUMP_EQ(PLUS_EXIT);
  SUB(R0, FPARG(R1));
  SUB(R1, IMM(1));
  JUMP(PLUS_LOOP);
 MINUS_EXIT:
  POP(FP);
  RETURN;
