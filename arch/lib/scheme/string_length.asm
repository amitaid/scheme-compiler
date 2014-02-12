/* string_length.asm
 *
 *
 * Programmers: Amitai Degani, Tal Zelig, 2014
 */

 STRING_LENGTH:
  PUSH(FP);
  MOV(FP,SP);
  CMP(FPARG(1),IMM(1));
  JUMP_EQ(STRING_LENGTH_ARGS_CORRECT);

  // amount of args error comes here

 STRING_LENGTH_ARGS_CORRECT:
  MOV(R0, FPARG(2));
  CMP(INDD(R0,0), T_STRING);
  JUMP_EQ(STRING_LENGTH_TYPE_CORRECT);

  // type error comes here

 STRING_LENGTH_TYPE_CORRECT:
  PUSH(INDD(R0,1));
  CALL(MAKE_SOB_INTEGER);
  DROP(1);
  POP(FP);
  RETURN;