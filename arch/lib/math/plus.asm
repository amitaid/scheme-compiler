/* plus.asm
 * R0 <- sum(args)
 *
 * Programmer: Amitai Degani, Tal Zelig, 2014
 */

 PLUS:
  PUSH(R1);
  PUSH(R2);
  MOV(R0, IMM(0));
  MOV(R1, STARG(1));
  ADD(R1, IMM(1));
 PLUS_LOOP:
  MOV(R2, STARG(R1));
  ADD(R0, INDD(R2,1));
  DECR(R1);
  CMP(R1, IMM(1));
  JUMP_NE(PLUS_LOOP);
 PLUS_EXIT:
  POP(R2);
  POP(R1);
  RETURN;