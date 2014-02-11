/* divide.asm
 * R0 <- arg0 / product(args[1..])
 *
 * Programmer: Amitai Degani, Tal Zelig, 2014
 */

 DIVIDE:
  PUSH(FP);
  MOV(FP,SP);
  MOV(R0, IMM(1)); // Result numerator
  MOV(R1, IMM(1)); // Result denumerator
  MOV(R5, FPARG(1)); // Argument number

  CMP(R5, IMM(0)); // No args. Need to throw error.
  JUMP_EQ(DIVIDE_EXIT);

  ADD(R5, IMM(2));
  CMP(R5, IMM(3)); // Only 1 argument
  JUMP_EQ(DIVIDE_LOOP);

  MOV(R2, FPARG(2)); // More than one arg. Mult first twice.
  CMP(IND(R2), T_INTEGER);
  JUMP_NE(DIVIDE_FIRST_ARG_FRAC);
  MOV(R3, IMM(1));  // denum is 1
  MOV(R2, INDD(R2,1)); // num is the number
  JUMP(DIVIDE_MUL_FIRST_TWICE);
 DIVIDE_FIRST_ARG_FRAC:
  MOV(R3, INDD(R2,2));  // denum
  MOV(R3, INDD(R3,1));
  MOV(R2, INDD(R2,1));  // num
  MOV(R2, INDD(R2,1));

 DIVIDE_MUL_FIRST_TWICE:
  MUL(R1,R3);
  MUL(R1,R3);
  MUL(R0,R2);
  MUL(R0,R2);

 DIVIDE_LOOP:
  DECR(R5);
  CMP(R5,1);
  JUMP_EQ(DIVIDE_EXIT);
  MOV(R2, FPARG(R5));
  CMP(IND(R2), T_FRACTION);
  JUMP_EQ(DIVIDE_FRAC);
  CMP(IND(R2), T_INTEGER);
  JUMP_EQ(DIVIDE_INT);

 DIVIDE_INT:
  MOV(R2, INDD(R2,1)); // Number is int, only deal with numerator
  MUL(R0,R3);
  MUL(R1,R2);
  JUMP(DIVIDE_LOOP);

 DIVIDE_FRAC:
  MOV(R3, INDD(R2,2)); // Fraction denumerator
  MOV(R2, INDD(R2,1)); // Fraction numerator
  MOV(R2, INDD(R2,1));
  MOV(R3, INDD(R3,1));
  MUL(R1,R2);
  MUL(R0,R3);
  JUMP(DIVIDE_LOOP);

 DIVIDE_EXIT:
  PUSH(R1);
  PUSH(R0);
  CALL(MAKE_SOB_NUMBER);
  DROP(2);

  POP(FP);
  RETURN;