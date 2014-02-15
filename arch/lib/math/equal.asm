/* equal.asm
 * R0 <- arg0 = arg1 = ... = arg(n-1)
 *
 * Programmer: Amitai Degani, Tal Zelig, 2014
 */

 EQUAL:
  PUSH(FP);
  MOV(FP,SP);

  //PUSH(R1);
  //PUSH(R2);
  //PUSH(R3);
  //PUSH(R4);
  //PUSH(R5);

  MOV(R1, FPARG(1)); // Argument number
  CMP(R1, IMM(0)); // No args, need to throw error
  JUMP_EQ(EQUAL_EXIT);
  CMP(R1, IMM(1));
  JUMP_EQ(EQUAL_SUCCESS);

  ADD(R1, IMM(1));  // R1 points to last argument
  MOV(R0, FPARG(R1)); // Last arg in R0

 EQUAL_LOOP:
  DECR(R1);
  CMP(R1, IMM(1));
  JUMP_EQ(EQUAL_SUCCESS);

  MOV(R2, INDD(R0,1));  // R2, R3 hold the later order number
  MOV(R2, INDD(R2,1));
  CMP(IND(R0), T_FRACTION);
  JUMP_EQ(EQUAL_FRACTION_PREP_1);

  MOV(R3, IMM(1));   // R0 holds an int. Numerator only.
  MOV(R0, INDD(R0,1));
  JUMP(EQUAL_SECOND_NUMBER);

 EQUAL_FRACTION_PREP_1:
  MOV(R3, INDD(R0,2));
  MOV(R3, INDD(R3,1));

 EQUAL_SECOND_NUMBER:
  MOV(R0, FPARG(R1));
  MOV(R4, INDD(R0,1));  // R4, R5 hold the earlier order number
  MOV(R4, INDD(R4,1));

  CMP(IND(R0), T_FRACTION);
  JUMP_EQ(EQUAL_FRACTION_PREP_2);

  MOV(R5, IMM(1));   // R0 holds an int. Numerator only.
  JUMP(EQUAL_COMPARE);

 EQUAL_FRACTION_PREP_2:
  MOV(R5, INDD(R0,2));
  MOV(R5, INDD(R5,1));

 EQUAL_COMPARE:
  MUL(R2,R5);
  MUL(R4,R3);
  CMP(R2,R4);
  JUMP_NE(EQUAL_FAILURE);
  JUMP(EQUAL_LOOP);

 EQUAL_SUCCESS:
  MOV(R0, IMM(5));
  JUMP(EQUAL_EXIT);
 EQUAL_FAILURE:
  MOV(R0, IMM(3));
 EQUAL_EXIT:

  //POP(R5);
  //POP(R4);
  //POP(R3);
  //POP(R2);
  //POP(R1);

  POP(FP);
  RETURN;