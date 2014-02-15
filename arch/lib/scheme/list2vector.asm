/* list2vector.asm
 *
 * Programmer: Mayer Goldberg, 2010
 */

LIST_2_VECTOR:
    PUSH(FP);
    MOV(FP, SP);

    //PUSH(R1);
    //PUSH(R2);
    //PUSH(R3);
    //PUSH(R4);

    CMP(FPARG(1), IMM(1));
    JUMP_EQ(LIST_2_VECTOR_AMOUNT_OK);

    // ERROR - ARG AMOUNT NOT OK

LIST_2_VECTOR_AMOUNT_OK:
    MOV(R2, FPARG(2));
    CMP(IND(R2),T_PAIR);
    JUMP_EQ(LIST_2_VECTOR_TYPE_OK);

    // ERROR TYPE WRONG

LIST_2_VECTOR_TYPE_OK:
    MOV(R1,IMM(0));
LIST_2_VECTOR_LOOP_FIRST:
    //HERE SUPPOSED TO COME A CHECK FOR THE TYPE CORRECTESS OF EACH LINK
    CMP(R2,IMM(2));
    JUMP_EQ(LIST_2_VECTOR_LOOP_FIRST_EXIT)
    PUSH(IMM(0));
    CALL(MAKE_SOB_INTEGER);
    DROP(1);
    PUSH(R0);
    INCR(R1);
    MOV(R2,INDD(R2,2));
    JUMP(LIST_2_VECTOR_LOOP_FIRST);

LIST_2_VECTOR_LOOP_FIRST_EXIT:
    PUSH(R1);
    CALL(MAKE_SOB_VECTOR);  // CREATES THE OPPOSITE VECTOR
    POP(R1);
    DROP(R1);

    MOV(R1, IMM(2));
    MOV(R2, FPARG(2));
LIST_2_VECTOR_LOOP_SECOND:
    CMP(R2, IMM(2));
    JUMP_EQ(LIST_2_VECTOR_LOOP_EXIT);
    MOV(INDD(R0,R1), INDD(R2,1));
    MOV(R2, INDD(R2,2));
    INCR(R1);
    JUMP(LIST_2_VECTOR_LOOP_SECOND);

LIST_2_VECTOR_LOOP_EXIT:
    //POP(R4);
    //POP(R3);
    //POP(R2);
    //POP(R1);
    POP(FP);
    RETURN;
