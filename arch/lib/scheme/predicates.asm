/* predicates.asm

 * NULL? : IS_NULL, NUMBER? : IS_NUMBER

 *  SOB_False = ADDR(3)    SOB_True = ADDR(5)

 * Programmer: Amitai Degani, Tal Zelig, 2014
 */

//              AUXILARY FUNCTION - add info


 UPDATE_BOOL_POINTER:
  CMP(R0,IMM(0));
  JUMP(PUT_TRUE);
 PUT_TRUE:
  MOV(R0(IMM(3));  // puts the pointer to sob_false in R0
  JUMP(UPDATE_EXIT);
 PUT_TRUE:
  MOV(R0(IMM(5));  // puts the pointer to sob_true in R0
 UPDATE_EXIT:
  RETURN;


 /*   null?   */

 IS_NULL:
  PUSH(FP);
  MOV(FP,SP);
  CMP(FPARG(1),IMM(1));     // checks that there is only one arg
  JUMP_EQ(IS_NULL_ARGS_CORRECT);

  //ERROR COMES HERE

 IS_NULL_ARGS_CORRECT:
  PUSH(FPARG(2));
  CALL(IS_SOB_NIL);
  DROP(1);
  MUL(R0, IMM(2));
  ADD(R0, IMM(3));
  POP(FP);
  RETURN;

 /*   number?   */

 IS_NUMBER:
  PUSH(FP);
  MOV(FP,SP);
  CMP(FPARG(1),IMM(1));     // checks that there is only one arg
  JUMP_EQ(IS_NUMBER_ARGS_CORRECT);

  //ERROR COMES HERE

 IS_NUMBER_ARGS_CORRECT:

  PUSH(FPARG(2));   //first checks whether it is an integer
  CALL(IS_SOB_INTEGER);
  DROP(1);
  CMP(R0,IMM(1));   // if positive, jumps to exit
  JUMP_EQ(IS_NUMBER_EXIT);

  PUSH(FPARG(2));   // else, checks if it is a fraction
  CALL(IS_SOB_FRACTION);
  DROP(1);          // no jump cuz just returns the value

 IS_NUMBER_EXIT:
  MUL(R0, IMM(2));
  ADD(R0, IMM(3));
  POP(FP);
  RETURN;

 /*   pair?   */

 IS_PAIR:
  PUSH(FP);
  MOV(FP,SP);
  CMP(FPARG(1),IMM(1));     // checks that there is only one arg
  JUMP_EQ(IS_PAIR_ARGS_CORRECT);

  //ERROR COMES HERE

 IS_PAIR_ARGS_CORRECT:
  PUSH(FPARG(2));
  CALL(IS_SOB_PAIR);
  DROP(1);
  MUL(R0, IMM(2));
  ADD(R0, IMM(3));
  POP(FP);
  RETURN;



   /*   procedure?   */

 IS_PROCEDURE:
  PUSH(FP);
  MOV(FP,SP);
  CMP(FPARG(1),IMM(1));     // checks that there is only one arg
  JUMP_EQ(IS_PROCEDURE_ARGS_CORRECT);

  //ERROR COMES HERE

 IS_PROCEDURE_ARGS_CORRECT:
  PUSH(FPARG(2));
  CALL(IS_SOB_CLOSURE);
  DROP(1);
  MUL(R0, IMM(2));
  ADD(R0, IMM(3));
  POP(FP);
  RETURN;


   /*   boolean?   */

 IS_BOOLEAN:
  PUSH(FP);
  MOV(FP,SP);
  CMP(FPARG(1),IMM(1));     // checks that there is only one arg
  JUMP_EQ(IS_BOOLEAN_ARGS_CORRECT);

  //ERROR COMES HERE

 IS_BOOLEAN_ARGS_CORRECT:
  PUSH(FPARG(2));
  CALL(IS_SOB_BOOL);
  DROP(1);
  MUL(R0, IMM(2));
  ADD(R0, IMM(3));
  POP(FP);
  RETURN;

     /*   char?   */

 IS_CHAR:
  PUSH(FP);
  MOV(FP,SP);
  CMP(FPARG(1),IMM(1));     // checks that there is only one arg
  JUMP_EQ(IS_CHAR_ARGS_CORRECT);

  //ERROR COMES HERE

 IS_CHAR_ARGS_CORRECT:
  PUSH(FPARG(2));
  CALL(IS_SOB_CHAR);
  DROP(1);
  MUL(R0, IMM(2));
  ADD(R0, IMM(3));
  POP(FP);
  RETURN;

       /*   integer?   */

 IS_INTEGER:
  PUSH(FP);
  MOV(FP,SP);
  CMP(FPARG(1),IMM(1));     // checks that there is only one arg
  JUMP_EQ(IS_INTEGER_ARGS_CORRECT);

  //ERROR COMES HERE

 IS_INTEGER_ARGS_CORRECT:
  PUSH(FPARG(2));
  CALL(IS_SOB_INTEGER);
  DROP(1);
  MUL(R0, IMM(2));
  ADD(R0, IMM(3));
  POP(FP);
  RETURN;

       /*   string?   */

 IS_STRING:
  PUSH(FP);
  MOV(FP,SP);
  CMP(FPARG(1),IMM(1));     // checks that there is only one arg
  JUMP_EQ(IS_STRING_ARGS_CORRECT);

  //ERROR COMES HERE

 IS_STRING_ARGS_CORRECT:
  PUSH(FPARG(2));
  CALL(IS_SOB_STRING);
  DROP(1);
  MUL(R0, IMM(2));
  ADD(R0, IMM(3));
  POP(FP);
  RETURN;

         /*   string?   */

 IS_STRING:
  PUSH(FP);
  MOV(FP,SP);
  CMP(FPARG(1),IMM(1));     // checks that there is only one arg
  JUMP_EQ(IS_STRING_ARGS_CORRECT);

  //ERROR COMES HERE

 IS_STRING_ARGS_CORRECT:
  PUSH(FPARG(2));
  CALL(IS_SOB_STRING);
  DROP(1);
  MUL(R0, IMM(2));
  ADD(R0, IMM(3));
  POP(FP);
  RETURN;

  // end of the trivial ones
           /*   zero?   */

 IS_ZERO:
  PUSH(FP);
  MOV(FP,SP);
  CMP(FPARG(1),IMM(1));     // checks that there is only one arg
  JUMP_EQ(IS_ZERO_ARGS_CORRECT);

  //ERROR COMES HERE

 IS_ZERO_ARGS_CORRECT:
  PUSH(FPARG(2));
  CALL(IS_SOB_INTEGER);
  DROP(1);

  CMP(R0,IMM(0));  // if not number, jumps to exit;
  JUMP_EQ(IS_ZERO_EXIT);

  CMP(INDD(R0,1),IMM(0));  // checks if the number holds zero
  JUMP_EQ(IS_ZERO_PUT_TRUE); // jumps to label if true

  MOV(R0,IMM(0));     // puts zero in R0
  JUMP(IS_ZERO_EXIT); // and jumps to exit

 IS_ZERO_PUT_TRUE:    // here we come if number is zero
  MOV(R0,IMM(1));    // puts one is R0, and doesnt jump

 IS_ZERO_EXIT:
  MUL(R0, IMM(2));
  ADD(R0, IMM(3));
  POP(FP);
  RETURN;
