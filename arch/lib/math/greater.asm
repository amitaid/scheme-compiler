/* greater.asm
 * R0 <- arg0 > arg1 > ... > arg(n-1)
 *
 * Programmer: Amitai Degani, Tal Zelig, 2014
 */

 GREATER:
  PUSH(FP);
  MOV(FP,SP);

  PUSH(R1);
  PUSH(R2);
  PUSH(R3);
  PUSH(R4);
  PUSH(R5);

  MOV(R1, FPARG(1)); // Argument number
  CMP(R1, IMM(0)); // No args, need to throw error
  JUMP_EQ(GREATER_EXIT);
  CMP(R1, IMM(1));
  JUMP_EQ(GREATER_SUCCESS);

  ADD(R1, IMM(1));  // R1 points to last argument
  MOV(R0, FPARG(R1)); // Last arg in R0

 GREATER_LOOP:
  DECR(R1);
  CMP(R1, IMM(1));
  JUMP_EQ(GREATER_SUCCESS);

  MOV(R2, INDD(R0,1));  // R2, R3 hold the later order number
  CMP(IND(R0), T_FRACTION);
  JUMP_EQ(GREATER_FRACTION_PREP_1);
  MOV(R3, IMM(1));   // R0 holds an int. Numerator only.
  JUMP(GREATER_SECOND_NUMBER);
 GREATER_FRACTION_PREP_1:
  MOV(R3, INDD(R0,2));

 GREATER_SECOND_NUMBER:
  MOV(R0, FPARG(R1));
  MOV(R4, INDD(R0,1));  // R4, R5 hold the earlier order number
  CMP(IND(R0), T_FRACTION);
  JUMP_EQ(GREATER_FRACTION_PREP_2);
  MOV(R5, IMM(1));   // R0 holds an int. Numerator only.
  JUMP(GREATER_COMPARE);
 GREATER_FRACTION_PREP_2:
  MOV(R5, INDD(R0,2));

 GREATER_COMPARE:
  MUL(R2,R5);
  MUL(R4,R3);
  CMP(R2,R4);
  JUMP_GE(GREATER_FAILURE);
  JUMP(GREATER_LOOP);

 GREATER_SUCCESS:
  MOV(R0, IMM(5));
  JUMP(GREATER_EXIT);
 GREATER_FAILURE:
  MOV(R0, IMM(3));
 GREATER_EXIT:

  POP(R5);
  POP(R4);
  POP(R3);
  POP(R2);
  POP(R1);

  POP(FP);
  RETURN;