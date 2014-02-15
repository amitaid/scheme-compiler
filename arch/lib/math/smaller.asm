/* smaller.asm
 * R0 <- arg0 < arg1 < ... < arg(n-1)
 *
 * Programmer: Amitai Degani, Tal Zelig, 2014
 */

 SMALLER:
  PUSH(FP);
  MOV(FP,SP);

  //PUSH(R1);
  //PUSH(R2);
  //PUSH(R3);
  //PUSH(R4);
  //PUSH(R5);

  MOV(R1, FPARG(1)); // Argument number
  CMP(R1, IMM(0)); // No args, need to throw error
  JUMP_EQ(SMALLER_EXIT);
  CMP(R1, IMM(1));
  JUMP_EQ(SMALLER_SUCCESS);

  ADD(R1, IMM(1));  // R1 points to last argument
  MOV(R0, FPARG(R1)); // Last arg in R0

 SMALLER_LOOP:
  DECR(R1);
  CMP(R1, IMM(1));
  JUMP_EQ(SMALLER_SUCCESS);

  MOV(R2, INDD(R0,1));  // R2, R3 hold the later order number
  CMP(IND(R0), T_FRACTION);
  JUMP_EQ(SMALLER_FRACTION_PREP_1);
  MOV(R3, IMM(1));   // R0 holds an int. Numerator only.
  JUMP(SMALLER_SECOND_NUMBER);
 SMALLER_FRACTION_PREP_1:
  MOV(R3, INDD(R0,2));

 SMALLER_SECOND_NUMBER:
  MOV(R0, FPARG(R1));
  MOV(R4, INDD(R0,1));  // R4, R5 hold the earlier order number
  CMP(IND(R0), T_FRACTION);
  JUMP_EQ(SMALLER_FRACTION_PREP_2);
  MOV(R5, IMM(1));   // R0 holds an int. Numerator only.
  JUMP(SMALLER_COMPARE);
 SMALLER_FRACTION_PREP_2:
  MOV(R5, INDD(R0,2));

 SMALLER_COMPARE:
  MUL(R2,R5);
  MUL(R4,R3);
  CMP(R2,R4);
  JUMP_LE(SMALLER_FAILURE);
  JUMP(SMALLER_LOOP);

 SMALLER_SUCCESS:
  MOV(R0, IMM(5));
  JUMP(SMALLER_EXIT);
 SMALLER_FAILURE:
  MOV(R0, IMM(3));
 SMALLER_EXIT:

  //POP(R5);
  //POP(R4);
  //POP(R3);
  //POP(R2);
  //POP(R1);

  POP(FP);
  RETURN;