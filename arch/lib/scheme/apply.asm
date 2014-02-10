/* apply.asm
 * Takes a function and a list of arguments and applies the function to the arguments.
 *
 * Programmer: Amitai Degani, Tal Zelig, 2014
 */

 APPLY:
  PUSH(FP);
  MOV(FP,SP);

  MOV(R1, IMM(0));  // Counter
  MOV(R2, FP);
  POP(R3);  // Old FP
  POP(R4);  // Return address
  POP(R5);  // Env
  DROP(1);  // Number of args
  POP(R6);  // Closure
  POP(R0);  // List of args

 APPLY_ARG_LOOP:
  CMP(INDD(R0,2), IMM(2));  // Compare to nil
  JUMP_EQ(APPLY_ARG_SWAP_PREP);
  PUSH(INDD(R0,1));
  MOV(R0, INDD(R0,2));
  INCR(R1);
  JUMP(APPLY_ARG_LOOP);

 APPLY_ARG_SWAP_PREP:
  PUSH(R1);
  ADD(R1,FP);

 APPLY_ARG_SWAP_LOOP:
  CMP(R1,R2);
  JUMP_LE(APPLY_PREP_EXIT);
  PUSH(R2);
  MOV(R2,R1);
  POP(R1);
  DECR(R1);
  INCR(R2);
  JUMP(APPLY_ARG_SWAP_LOOP);

 APPLY_PREP_EXIT:
  PUSH(INDD(R6,1));
  PUSH(R4);
  PUSH(R3);
  CALLA(INDD(R6,2));
  DROP(R1);

 APPLY_EXIT:
  POP(FP);
  RETURN;


