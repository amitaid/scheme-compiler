/* apply.asm
 * Takes a function and a list of arguments and applies the function to the arguments.
 *
 * Programmer: Amitai Degani, Tal Zelig, 2014
 */

 APPLY:
  POP(R6);
  PUSH(R6);
  PUSH(FP);
  MOV(FP,SP);
  POP(R0);
  PUSH(R0);
  //PUSH(R1);
  //PUSH(R2);  // this will hold the number of args in the properlist
  //PUSH(R3);
  //PUSH(R4);
  //PUSH(R5);

  MOV(R2,IMM(0));
  CMP(FPARG(1),IMM(2));   // checks the number of args is more than 2 (proc, list, and args in between)
  JUMP_GE(APPLY_FIRST_ARG_CHECK);

  // NOT ENOUGH ARGS ERROR HERE

 APPLY_FIRST_ARG_CHECK:
  MOV(R1,FPARG(2));
  CMP(IND(R1),T_CLOSURE);  // checks that the first arg is a closure
  JUMP_EQ(APPLY_LAST_ARG_CHECK);

  // FIRST ARG NOT A PROC ERROR HERE

 APPLY_LAST_ARG_CHECK:
  MOV(R1,FPARG(1));
  INCR(R1);
  MOV(R1,FPARG(R1));  // R1 now holds the last arg, the next loop checks if it is a proper list

 APPLY_LAST_ARG_IS_PROPER_LIST_LOOP:
  CMP(IND(R1),T_NIL);                  //  checks if nil, if yes, jumps out, it is proper list
  JUMP_EQ(APPLY_ARGS_CORRECT);
  CMP(IND(R1),T_PAIR);                  // else, check if a pair, if yes, continues the loop
  JUMP_EQ(APPLY_CURR_LINK_CORRECT);

  // ERROR last arg not a proper list

 APPLY_CURR_LINK_CORRECT:
  INCR(R2);
  PUSH(INDD(R1,1));                    // push the arg to the stack
  MOV(R1,INDD(R1,2));                  // updates R1 to point the next link
  JUMP(APPLY_LAST_ARG_IS_PROPER_LIST_LOOP);


 APPLY_ARGS_CORRECT:
 /* at this point, all the data of the list is on the stack, but reversed,
  * R2 holds the length of the list */

  MOV(R1,SP);
  SUB(R1,R2); // now r1 points to the most bottom element of the list
  MOV(R3,SP);
  DECR(R3); // now arg 3 points to the top of the elements

 APPLY_REARRANGE_STACK_LOOP:
  CMP(R3,R1);
  JUMP_GE(APPLY_REARRANGE_STACK_LOOP_EXIT);
  MOV(R4,STACK(R3));
  MOV(STACK(R3),STACK(R1));
  MOV(STACK(R1),R4);
  INCR(R1);
  DECR(R3);
  JUMP(APPLY_REARRANGE_STACK_LOOP);

 APPLY_REARRANGE_STACK_LOOP_EXIT:
  MOV(R1,FPARG(1));

 APPLY_NON_LIST_ARGS_PUSH_LOOP:
  CMP(R1,IMM(3));
  JUMP_LT(APPLY_NON_LIST_ARGS_PUSH_LOOP_EXIT);
  PUSH(FPARG(R1));  // at the first time, fparg(r1) points to the before last element.
  DECR(R1);
  JUMP(APPLY_NON_LIST_ARGS_PUSH_LOOP);

 APPLY_NON_LIST_ARGS_PUSH_LOOP_EXIT:
  MOV(R1,FPARG(1));
  SUB(R1,IMM(2)); // because we dont count the list, and not the procedure
  ADD(R1,R2);     // now R1 holds the amount of args we pushed to the stack
  PUSH(R1);       // now the num and the args are on the top of the stack

  MOV(R4,R0);   // R4 holds the old fp now
  MOV(R5,R0);
  //ADD(R4,IMM(1));
  MOV(R0,FPARG(2));
  INCR(R1);    // R1 holds the amount needed to be copied down
  MOV(R3,SP);
  //SUB(R3,5);  // ADDING THE NUMBER OF BACKED UP REGISTERS
  SUB(R3,R1);  // R3 now points to the lowest arg to copy

 APPLY_COPY_DOWN_LOOP:
  CMP(R3,SP);
  JUMP_EQ(APPLY_COPY_DOWN_LOOP_EXIT);
  MOV(R2,STACK(R3));
  MOV(STACK(R4),R2);
  INCR(R3);
  INCR(R4);
  JUMP(APPLY_COPY_DOWN_LOOP);

 APPLY_COPY_DOWN_LOOP_EXIT:
  //INCR(R4);
  MOV(SP,R4);
  MOV(FP,R5);
  //DECR(R1);
  //PUSH(R1);  // now pushing the number of args
  PUSH(INDD(R0,1));  // push the environment
  PUSH(R6);
  JUMPA(INDD(R0,2));
  //DROP(1);    // drops the old env
  //POP(R1);    // R1 holds the amount of args on the stack
  //DROP(R1);   // drops the total amount of pushed args

  //POP(R5);
  //POP(R4);
  //POP(R3);
  //POP(R2);
  //POP(R1);
  //POP(FP);
  //RETURN;
