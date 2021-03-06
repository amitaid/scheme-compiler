/* append.asm
 * concatenate lists
 *
 * Programmer: Amitai Degani, Tal Zelig, 2014
 */

 APPEND:
  PUSH(FP);
  MOV(FP,SP);

  //PUSH(R1);
  //PUSH(R2);
  //PUSH(R3);
  //PUSH(R4);
  //PUSH(R5);

  MOV(R1, IMM(2)); // Result holder
  MOV(R5, IMM(2));
  MOV(R2, FPARG(1));
  CMP(R2, IMM(0));
  JUMP_LE(APPEND_EXIT);

  ADD(R2, IMM(1));  // Last argument pointer
  MOV(R3, IMM(2));  // First argument pointer

 APPEND_EXTERNAL_LOOP:
  CMP(R2, R3);
  JUMP_LE(APPEND_EXTERNAL_LOOP_EXIT);
  MOV(R4, FPARG(R3));

 APPEND_INNER_LOOP:
  CMP(R4, IMM(2));
  JUMP_EQ(APPEND_INNER_LOOP_EXIT);

  // Error, check for pairs

  PUSH(IMM(2));
  PUSH(INDD(R4, 1));
  CALL(MAKE_SOB_PAIR);
  DROP(2);      // R0 NOW HOLDS THE LAST PAIR IN THE LIST

  CMP(R1, IMM(2));
  JUMP_NE(NOT_FIRST_PAIR);
  MOV(R1, R0);
  MOV(R5, R0);
  JUMP(FIRST_PAIR);

 NOT_FIRST_PAIR:
  MOV(INDD(R5,2), R0);
  MOV(R5, R0);

 FIRST_PAIR:
  MOV(R4, INDD(R4,2)); //Next pair
  JUMP(APPEND_INNER_LOOP);

 APPEND_INNER_LOOP_EXIT:
  INCR(R3);
  JUMP(APPEND_EXTERNAL_LOOP);


 APPEND_EXTERNAL_LOOP_EXIT:
  CMP(R5, IMM(2));
  JUMP_NE(APPEND_LAST_ARG);
  MOV(R1, FPARG(R3));
  JUMP(APPEND_EXIT);

 APPEND_LAST_ARG:
  MOV(INDD(R5,2), FPARG(R3));

 APPEND_EXIT:
  MOV(R0, R1);

  //POP(R5);
  //POP(R4);
  //POP(R3);
  //POP(R2);
  //POP(R1);

  POP(FP);
  RETURN;


