/* minus.asm
 * R0 <- arg0 - sum(args[1..])
 *
 * Programmer: Amitai Degani, Tal Zelig, 2014
 */

 MINUS:
  PUSH(FP);
  MOV(FP,SP);
  MOV(R0, IMM(0)); // Result numerator
  MOV(R1, IMM(1)); // Result denumerator
  MOV(R5, FPARG(1)); // Argument number

  CMP(R5, IMM(0)); // No args
  JUMP_EQ(MINUS_EXIT);

  ADD(R5, IMM(2));
  CMP(R5, IMM(3)); // Only 1 argument
  JUMP_EQ(MINUS_LOOP);

  MOV(R2, FPARG(2)); // More than one arg. Add first twice.
  CMP(IND(R2), T_INTEGER);
  JUMP_NE(MINUS_FIRST_ARG_FRAC);
  MOV(R3, IMM(1));  // denum is 1
  MOV(R2, INDD(R2,1)); // num is the number
  JUMP(MINUS_ADD_FIRST_TWICE);

 MINUS_FIRST_ARG_FRAC:
  MOV(R3, INDD(R2,2));  // denum
  MOV(R3, INDD(R3,1));
  MOV(R2, INDD(R2,1));  // num
  MOV(R2, INDD(R2,1));

 MINUS_ADD_FIRST_TWICE:
  MUL(R1,R3);
  ADD(R0,R2);
  ADD(R0,R2);

 MINUS_LOOP:
  DECR(R5);
  CMP(R5,1);
  JUMP_EQ(MINUS_EXIT);
  MOV(R2, FPARG(R5));
  CMP(IND(R2), T_FRACTION);
  JUMP_EQ(MINUS_FRAC);
  CMP(IND(R2), T_INTEGER);
  JUMP_EQ(MINUS_INT);

 MINUS_INT:
  MOV(R2, INDD(R2,1)); // Number is int, only deal with numerator
  MUL(R2,R1);
  SUB(R0,R2);
  JUMP(MINUS_LOOP);

 MINUS_FRAC:
  MOV(R3, INDD(R2,2)); // Fraction denumerator
  MOV(R2, INDD(R2,1)); // Fraction numerator
  MOV(R2, INDD(R2,1));
  MOV(R3, INDD(R3,1));
  CMP(R1,R3);
  JUMP_EQ(MINUS_FRAC_SAME_DENUM);
  MUL(R2,R1);       // Mechane meshutaf
  MUL(R0,R3);
  MUL(R1,R3);
 MINUS_FRAC_SAME_DENUM:
  SUB(R0,R2);
  JUMP(MINUS_LOOP);

 MINUS_EXIT:
  PUSH(R1);
  PUSH(R0);
  CALL(MAKE_SOB_NUMBER);
  DROP(2);

  POP(FP);
  RETURN;