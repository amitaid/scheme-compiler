/* mult.asm
 * R0 <- product(args)
 *
 * Programmer: Amitai Degani, Tal Zelig, 2014
 */

 MULT:
  PUSH(FP);
  MOV(FP,SP);

  //PUSH(R1);
  //PUSH(R2);
  //PUSH(R3);
  //PUSH(R4);
  //PUSH(R5);

  MOV(R0, IMM(1)); // Result numerator
  MOV(R1, IMM(1)); // Result denumerator
  MOV(R5, FPARG(1)); // Argument number
  ADD(R5, IMM(2));

 MULT_LOOP:
  DECR(R5);
  CMP(R5,1);
  JUMP_EQ(MULT_EXIT);
  MOV(R2, FPARG(R5));
  CMP(IND(R2), T_FRACTION);
  JUMP_EQ(MULT_FRAC);
  CMP(IND(R2), T_INTEGER);
  JUMP_EQ(MULT_INT);

 MULT_INT:
  MOV(R2, INDD(R2,1)); // Number is int, only deal with numerator
  MUL(R0,R2);
  JUMP(MULT_LOOP);

 MULT_FRAC:
  MOV(R3, INDD(R2,2)); // Fraction denumerator
  MOV(R2, INDD(R2,1)); // Fraction numerator
  MOV(R2, INDD(R2,1));
  MOV(R3, INDD(R3,1));
  MUL(R1,R3);
  MUL(R0,R2);
  JUMP(MULT_LOOP);

 MULT_EXIT:
  PUSH(R1);
  PUSH(R0);
  CALL(MAKE_SOB_NUMBER);
  DROP(2);

  //POP(R5);
  //POP(R4);
  //POP(R3);
  //POP(R2);
  //POP(R1);

  POP(FP);
  RETURN;