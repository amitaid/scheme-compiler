/* vector_ref.asm
 * first arg is vector, second is index
 * Programmers: Amitai Degani, Tal Zelig, 2014
 */

 VECTOR_REF:
  PUSH(FP);
  MOV(FP,SP);

  PUSH(R1);

  CMP(FPARG(1),IMM(2));        // checks that we have 2 args in stack
  JUMP_EQ(VECTOR_REF_ARGS_CORRECT);

  // ERROR REGARDING AMOUNT OF ARGS COMES HERE

 VECTOR_REF_ARGS_CORRECT:
  MOV(R0, FPARG(2));           // R0 now holds the vector pointer
  CMP(INDD(R0,0), T_VECTOR);   // checks that the first is a vector
  JUMP_EQ(VECTOR_REF_TYPE_CORRECT);

  // ANOTHER ERROR REGARDING THE TYPE CORRECTNESS HERE

 VECTOR_REF_TYPE_CORRECT:
  CMP(FPARG(3), INDD(R0,1));      // checks if index is legal
  JUMP_LT(VECTOR_REF_INDEX_CORRECT);

  // third error of index out of bounds here

 VECTOR_REF_INDEX_CORRECT:
  MOV(R1,FPARG(3));        // move the integer arg to R1
  CMP(INDD(R1,0),T_INTEGER);
  JUMP_EQ(VECTOR_REF_INT_ARG_TYPE_CORRECT);

  // fourth error if the 2nd arg is not an integer

 VECTOR_REF_INT_ARG_TYPE_CORRECT:  // if we are here then the args are correct
  MOV(R1,INDD(R1,1));  // move the value of the integer to R1.
  ADD(R1,IMM(2));      // adds 2 because the first element is in the 3rd cell (1,2 are type and length)
  MOV(R0,INDD(R0,R1));

  POP(R1);

  POP(FP);
  RETURN;