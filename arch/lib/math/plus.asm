/* plus.asm
 * R0 <- sum(args)
 *
 * Programmer: Amitai Degani, Tal Zelig, 2014
 */

 PLUS:
  PUSH(FP);
  MOV(FP,SP);
  MOV(R0, IMM(0)); // Result numerator
  MOV(R1, IMM(1)); // Result denumerator
  MOV(R5, FPARG(1)); // Argument number
  ADD(R5, IMM(2));

 PLUS_LOOP:
  DECR(R5);
  CMP(R5,1);
  JUMP_EQ(PLUS_EXIT);
  MOV(R2, FPARG(R5));
  CMP(IND(R2), T_FRACTION);
  JUMP_EQ(PLUS_FRAC);
  CMP(IND(R2), T_INTEGER);
  JUMP_EQ(PLUS_INT);

 PLUS_INT:
  MOV(R2, INDD(R2,1)); // Number is int, only deal with numerator
  MUL(R2,R1);
  ADD(R0,R2);
  JUMP(PLUS_LOOP);

 PLUS_FRAC:
  MOV(R3, INDD(R2,2)); // Fraction denumerator
  MOV(R2, INDD(R2,1)); // Fraction numerator
  MOV(R2, INDD(R2,1));
  MOV(R3, INDD(R3,1));
  CMP(R1,R3);
  JUMP_EQ(PLUS_FRAC_SAME_DENUM);
  MUL(R2,R1);       // Mechane meshutaf
  MUL(R0,R3);
  MUL(R1,R3);
 PLUS_FRAC_SAME_DENUM:
  ADD(R0,R2);
  JUMP(PLUS_LOOP);

 PLUS_EXIT:
  PUSH(R1);
  PUSH(R0);
  CALL(MAKE_SOB_NUMBER);
  DROP(2);

  POP(FP);
  RETURN;