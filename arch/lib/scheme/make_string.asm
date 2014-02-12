/* make_string.asm
 * first arg is STRING, second is index
 * Programmers: Amitai Degani, Tal Zelig, 2014
 */

 MAKE_STRING:
  PUSH(FP);
  MOV(FP,SP);
  PUSH(R1);
  PUSH(R2);
  PUSH(R3);
  MOV(R1,IMM(2));
  CMP(FPARG(1),IMM(2));        // checks that we have less then 3 args in stack
  JUMP_LE(MAKE_STRING_ARGS_COUNT_LESS_THAN_3);

  // error - more than 2 args

 MAKE_STRING_ARGS_COUNT_LESS_THAN_3:
  CMP(FPARG(1),IMM(0));        // checks that is not zero
  JUMP_EQ(MAKE_STRING_FIRST_ARG_CHECK);

  // error - zero args

 MAKE_STRING_FIRST_ARG_CHECK:
  MOV(R1,FPARG(2));
  CMP(IND(R1),T_INTEGER);        // checks that is not zero
  JUMP_EQ(MAKE_STRING_ARGS_CORRECT);

  // error - zero args


 MAKE_STRING_ARGS_CORRECT:
  CMP(FPARG(1),IMM(2));        // checks if we have second arg, if no, we jump to the actual creation
  JUMP_NE(MAKE_STRING_CREATION);
  MOV(R1,FPARG(3));           // if yes then it is put in R1

  CMP(IND(R1),T_CHAR);
  JUMP_EQ(MAKE_STRING_CREATION_W_ARG);

  // ERROR - 2ND ARG NOT A CHAR

 MAKE_STRING_CREATION_W_ARG:
  MOV(R1,INDD(R1,1));

 MAKE_STRING_CREATION:
  MOV(R2,IMM(0));
  MOV(R3,FPARG(2));            // puts in R3 the length of the STRING to be created
  MOV(R3,INDD(R3,1));

 MAKE_STRING_ARGS_PUSH_LOOP:
  CMP(R2,R3);
  JUMP_GE(MAKE_STRING_ARGS_PUSH_LOOP_EXIT);
  PUSH(R1);
  INCR(R2);
  JUMP(MAKE_STRING_ARGS_PUSH_LOOP);

 MAKE_STRING_ARGS_PUSH_LOOP_EXIT:
  MOV(R2,FPARG(2));
  PUSH(R3);
  CALL(MAKE_SOB_STRING);
  INCR(R3);
  DROP(R3);

  POP(R3);
  POP(R2);
  POP(R1);
  POP(FP);
  RETURN;