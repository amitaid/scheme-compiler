/* char2int.asm
 * char->integer
 *
 * Programmers: Amitai Degani, Tal Zelig, 2014
 */

 CHAR_2_INT:
  PUSH(FP);
  MOV(FP,SP);
  CMP(FPARG(1),IMM(1));
  JUMP_EQ(CHAR_2_INT_AMOUNT_CORRECT);

  // ERROR - INCORRECT AMOUNT

 CHAR_2_INT_AMOUNT_CORRECT:
  MOV(R0,FPARG(2));
  CMP(IND(R0),T_CHAR);
  JUMP_EQ(CHAR_2_INT_TYPE_CORRECT);

  //ERROR - input not a char

 CHAR_2_INT_TYPE_CORRECT:
  PUSH(INDD(R0,1));
  CALL(MAKE_SOB_INTEGER );
  DROP(1);
  POP(FP);
  RETURN;