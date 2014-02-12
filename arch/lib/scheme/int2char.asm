/* int2char.asm
 * integer->char
 *
 * Programmers: Amitai Degani, Tal Zelig, 2014
 */

 INT_2_CHAR:
  PUSH(FP);
  MOV(FP,SP);
  CMP(FPARG(1),IMM(1));
  JUMP_EQ(INT_2_CHAR_AMOUNT_CORRECT);

  // ERROR - INCORRECT AMOUNT

 INT_2_CHAR_AMOUNT_CORRECT:
  MOV(R0,FPARG(2));
  CMP(IND(R0),T_INTEGER);
  JUMP_EQ(INT_2_CHAR_TYPE_CORRECT);
  //ERROR - input not an int

 INT_2_CHAR_TYPE_CORRECT:
  PUSH(INDD(R0,1));
  CALL(MAKE_SOB_CHAR);
  DROP(1);
  POP(FP);
  RETURN;