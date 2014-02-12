/* scheme/make_sob_symbol.asm
 * Takes a pointer to a string object and returns a pointer
 * of a symbol object, whether in an existing bucket or a new bucket.
 *
 * Programmer: Mayer Goldberg, 2010
 */

 MAKE_SOB_SYMBOL:
  PUSH(FP);
  MOV(FP, SP);

  MOV(R1, IND(7));      // Symbol table link
  MOV(R2, FPARG(0));    // String to search for

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
  MOV(R1, INDD(R1,1));  // Next link
  JUMP(MAKE_SYMBOL_SEARCH_LOOP);

 MAKE_SYMBOL_FOUND:
  MOV(R0, R1);          // Move the correct link
  ADD(R0, IMM(2));      // Adjust to the symbol
  JUMP(MAKE_SOB_SYMBOL_EXIT);

 MAKE_SYMBOL_NOT_FOUND:
  PUSH(IMM(6));             // New bucket sextet
  CALL(MALLOC);
  DROP(1);
  MOV(IND(R0), R0);
  ADD(IND(R0), IMM(4));      // Pointer to the bucket
  MOV(INDD(R0,1), IMM(-1));  // Next link
  MOV(INDD(R0,2), T_SYMBOL); // Symbol type
  MOV(INDD(R0,3), IND(R0)); // Pointer to the bucket
  MOV(INDD(R0,4), R2);      // Symbol name, our string
  MOV(INDD(R0,5), IMM(-1)); // No value pointed to yet
  ADD(R0, IMM(2));      // Adjust to the symbol

 MAKE_SOB_SYMBOL_EXIT:
  POP(FP);
  RETURN;

