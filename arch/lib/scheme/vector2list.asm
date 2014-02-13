/* vector2list.asm
 *
 * Programmer: Mayer Goldberg, 2010
 */

VECTOR_2_LIST:
    PUSH(FP);
    MOV(FP, SP);

    PUSH(R1);
    PUSH(R2);
    PUSH(R3);
    PUSH(R4);

    CMP(FPARG(1), IMM(1));
    JUMP_EQ(VECTOR_2_LIST_AMOUNT_OK);

    // ERROR - ARG AMOUNT NOT OK

VECTOR_2_LIST_AMOUNT_OK:
    MOV(R2,FPARG(2));
    CMP(IND(R2),T_VECTOR);
    JUMP_EQ(VECTOR_2_LIST_TYPE_OK);

    // ERROR TYPE WRONG

VECTOR_2_LIST_TYPE_OK:
    MOV(R1,INDD(R2,1));  // R1 IS THE ITERATION VARIABLE
    ADD(R1,IMM(2));
    MOV(R0,IMM(2));  // R0 hold the answer
    //MOV(R3,IMM(2));  // r3 holds the ans

VECTOR_2_LIST_LOOP:
    CMP(R1,IMM(2));
    JUMP_LT(VECTOR_2_LIST_LOOP_EXIT);
    PUSH(R0);
    PUSH(INDD(R2,R1));
    CALL(MAKE_SOB_PAIR);
    DROP(2);
    DECR(R1);
    JUMP(VECTOR_2_LIST_LOOP);

VECTOR_2_LIST_LOOP_EXIT:

    POP(R4);
    POP(R3);
    POP(R2);
    POP(R1);

    POP(FP);
    RETURN;
