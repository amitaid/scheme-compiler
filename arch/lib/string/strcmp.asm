/* strcmp.asm
 * Takes two pointers to strings. Returns 1 if they are equal, 0 if not.
 * R0 = str1 == str2
 *
 * Programmer: Amitai Degani, Tal Zelig, 2013
 */

 STRCMP:
  PUSH(R1);
  PUSH(R2);
  PUSH(R3);

  MOV(R0, IMM(0));
  MOV(R1, STARG(0));
  MOV(R2, STARG(1));
  CMP(IND(R1), T_STRING);
  //ERROR

  CMP(IND(R2), T_STRING);
  //ERROR

  MOV(R3, INDD(R1,1));
  CMP(R3, INDD(R2,1));
  JUMP_NE(STRCMP_FAIL);  // Strings of different lengths
  INCR(R3);      // Displacement of last character

 STRCMP_LOOP:
  CMP(R3,IMM(1));
  JUMP_EQ(STRCMP_SUCCESS);
  CMP(INDD(R1,R3), INDD(R2,R3));
  JUMP_NE(STRCMP_FAIL);
  DECR(R3);
  JUMP(STRCMP_LOOP);


 STRCMP_SUCCESS:
  MOV(R0, IMM(1));
 STRCMP_FAIL:

  POP(R3);
  POP(R2);
  POP(R1);
  RETURN;
