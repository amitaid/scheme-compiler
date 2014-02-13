/* list2vector.asm
 *
 * Programmer: Mayer Goldberg, 2010
 */

LIST_2_VECTOR:
    PUSH(FP);
    MOV(FP, SP);
    PUSH(R1);
    PUSH(R2);
    PUSH(R3);
    PUSH(R4);
    CMP(FPARG(1), IMM(1));
    JUMP_EQ(LIST_2_VECTOR_AMOUNT_OK);

    // ERROR - ARG AMOUNT NOT OK

LIST_2_VECTOR_AMOUNT_OK:
    MOV(R2,FPARG(2));
    CMP(IND(R2),T_VECTOR);
    JUMP_EQ(LIST_2_VECTOR_TYPE_OK);

    // ERROR TYPE WRONG

LIST_2_VECTOR_TYPE_OK:



LIST_2_VECTOR_LOOP_EXIT:
    POP(R4);
    POP(R3);
    POP(R2);
    POP(R1);
    POP(FP);
    RETURN;
