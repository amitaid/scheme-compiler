/* append.asm
 * concatenate lists
 *
 * Programmer: Amitai Degani, Tal Zelig, 2014
 */

 APPEND:
  PUSH(FP);
  MOV(FP,SP);

  MOV(R0, FPARG(2));   // R0 holds the pointer to the answer
  PUSH(R0);
  //MOV(R0,IND(R0));     // R0 now holds the first link
  MOV(R1, IMM(3));     // R1 holds the index of the current arg to iterate
  MOV(R2, FPARG(1));
  ADD(R2,IMM(2));

 APPEND_LOOP:
  CMP(R1,R2);
  JUMP_LE(APPEND_EXIT);

  /* inner loop for finding the last link*/
 FIND_LAST_LINK_LOOP:
  CMP(INDD(R0,2),IMM(2));               // checks that it is last link
  JUMP_EQ(FIND_LAST_LINK_LOOP_EXIT);   // if yes, jumps to the exit
  MOV(R0,INDD(R0,2));                  // else, jumps to the next link
  JUMP(FIND_LAST_LINK_LOOP);

 FIND_LAST_LINK_LOOP_EXIT:
  MOV(INDD(R0,2),FPARG(R1));
  INCR(R1);
  JUMP(APPEND_LOOP);

 APPEND_EXIT:
  POP(R0);

  POP(FP);
  RETURN;


