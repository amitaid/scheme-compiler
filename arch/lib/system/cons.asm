/* cons.asm
 * R0 <- cons(arg1,args2) (?)
 *
 * Programmer: Amitai Degani the magnificent, Tal Zelig, 2014
 */

CONS:
 PUSH(IMM(2));
 CALL(MALLOC);
 DROP(1);
 MOV(INDD(R0, 0), FPARG(0));
 MOV(INDD(R0, 1), FPARG(1));
 RETURN;
