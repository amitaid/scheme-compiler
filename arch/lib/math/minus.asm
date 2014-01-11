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
  JUMP_EQ(MINUS_EXIT);
  SUB(R0, FPARG(R1));
  SUB(R1, IMM(1));
  JUMP(MINUS_LOOP);
 MINUS_EXIT:
  RETURN;
