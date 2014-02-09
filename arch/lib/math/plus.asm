/* plus.asm
 * R0 <- sum(args)
 *
 * Programmer: Amitai Degani, Tal Zelig, 2014
 */

 PLUS:
  MOV(R0, IMM(0));
  MOV(R1, FPARG(1));
  ADD(R1, IMM(2));
 PLUS_LOOP:
  CMP(R1, IMM(1));
  JUMP_EQ(PLUS_EXIT);
  ADD(R0, FPARG(R1));
  SUB(R1, IMM(1));
  JUMP(PLUS_LOOP);
 PLUS_EXIT:
  RETURN;
