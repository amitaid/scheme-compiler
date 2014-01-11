/* divide.asm
 * R0 <- arg0 / product(args[1..])
 *
 * Programmer: Amitai Degani, Tal Zelig, 2014
 */

 DIVIDE:
  MOV(R0, FPARG(1));
  MOV(R1, FPARG(0));
 DIVIDE_LOOP:
  CMP(R1, IMM(1));
  JUMP_EQ(DIVIDE_EXIT);
  DIV(R0, FPARG(R1));
  SUB(R1, IMM(1));
  JUMP(DIVIDE_LOOP);
 DIVIDE_EXIT:
  RETURN;
