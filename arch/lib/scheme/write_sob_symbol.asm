/* scheme/write_sob_symbol.asm
 * Take a pointer to a Scheme symbol object, and
 * prints (to stdout) the character representation
 * of that object.
 *
 * Programmer: Mayer Goldberg, 2010
 */

 WRITE_SOB_SYMBOL:
  MOV(R0, STARG(0));
  MOV(R0, INDD(R0,1));
  MOV(R0, IND(R0));
  PUSH(R0);
  CALL(WRITE_SOB_STRING);
  DROP(1);

  RETURN;
