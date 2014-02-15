/* string.asm
 *
 * Programmers: Amitai Degani, Tal Zelig, 2014
 */


 STRING_CONSTRUCTOR:
  PUSH(FP);
  MOV(FP,SP);

  //PUSH(R1);
  //PUSH(R2);
  //PUSH(R3);

  MOV(R1,IMM(2));
  MOV(R2,FPARG(1));  // holds the number of args in the stack
  INCR(R2);

 STRING_CONSTRUCTOR_ARG_LOOP:
  CMP(R1,R2);
  JUMP_GT(STRING_CONSTRUCTOR_ARG_LOOP_EXIT);

  MOV(R3,FPARG(R1));
  CMP(IND(R3),T_CHAR);  // this checks that all the args are of type char

  JUMP_EQ(STRING_CONSTRUCTOR_CURRENT_ARG_CORRECT);

  // error that the current arg is not a char

 STRING_CONSTRUCTOR_CURRENT_ARG_CORRECT:
  PUSH(INDD(R3,1));
  INCR(R1);
  JUMP(STRING_CONSTRUCTOR_ARG_LOOP);

 STRING_CONSTRUCTOR_ARG_LOOP_EXIT:
  MOV(R1,FPARG(1));
  PUSH(R1);
  CALL(MAKE_SOB_STRING);
  ADD(R1,1);
  DROP(R1);

  POP(R3);
  POP(R2);
  POP(R1);

  POP(FP);
  RETURN;
