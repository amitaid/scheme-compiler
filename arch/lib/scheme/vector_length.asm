/* vector_length.asm
 *
 * Programmers: Amitai Degani, Tal Zelig, 2014
 */

 VECTOR_LENGTH:
  PUSH(FP);
  MOV(FP,SP);

  POP(FP);
  RETURN;