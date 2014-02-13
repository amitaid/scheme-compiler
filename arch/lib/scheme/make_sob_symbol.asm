/* scheme/make_sob_symbol.asm
 * Takes a pointer to a string object and returns a pointer
 * of a symbol object, whether in an existing bucket or a new bucket.
 *
 * Programmer: Amitai Degani, Tal Zelig, 2014
 */

 MAKE_SOB_SYMBOL:
  PUSH(FP);
  MOV(FP, SP);

  PUSH(R1);
  PUSH(R2);
  PUSH(R3);
  PUSH(R4);

  MOV(R2, FPARG(2));    // String to search for
  MOV(R1, IND(7));      // Symbol table location

 MAKE_SYMBOL_SEARCH_LOOP:
  CMP(R1, IMM(-1));     // Last link in the chain
  JUMP_EQ(MAKE_SYMBOL_NOT_FOUND);

  MOV(R3, INDD(R1,3));  // Move the symbol's link to R3

  PUSH(IND(R3));        // Push the string pointed to
  PUSH(R2);             // Push our string
  CALL(STRCMP);         // Compare
  DROP(2);

  CMP(R0, IMM(1));
  JUMP_EQ(MAKE_SYMBOL_FOUND);
  MOV(R4, R1);
  MOV(R1, INDD(R1,1));  // Next link
  JUMP(MAKE_SYMBOL_SEARCH_LOOP);

 MAKE_SYMBOL_FOUND:
  MOV(R0, R1);          // Move the correct link
  JUMP(MAKE_SOB_SYMBOL_EXIT);

 MAKE_SYMBOL_NOT_FOUND:
  PUSH(R4);
  PUSH(R2);
  PUSH(IMM(6));             // New bucket sextet
  CALL(MALLOC);
  DROP(1);
  POP(R2);
  POP(R4);
  MOV(IND(R0), R0);
  ADD(IND(R0), IMM(4));      // Pointer to the bucket
  MOV(INDD(R0,1), IMM(-1));  // Next link
  MOV(INDD(R0,2), T_SYMBOL); // Symbol type
  MOV(INDD(R0,3), IND(R0)); // Pointer to the bucket
  MOV(INDD(R0,4), R2);      // Symbol name, our string
  MOV(INDD(R0,5), IMM(-1)); // No value pointed to yet

  CMP(IND(7), IMM(-1));
  JUMP_EQ(FIRST_LINK);
  MOV(INDD(R4,1), R0);      // Update the previous link
  JUMP(MAKE_SOB_SYMBOL_EXIT);

 FIRST_LINK:
  MOV(IND(7), R0);

 MAKE_SOB_SYMBOL_EXIT:
  ADD(R0, IMM(2));      // Adjust to the symbol

  POP(R4);
  POP(R3);
  POP(R2);
  POP(R1);

  POP(FP);
  RETURN;

