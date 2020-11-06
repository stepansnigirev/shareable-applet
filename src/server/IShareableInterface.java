package server;

import javacard.framework.*;

public interface IShareableInterface extends Shareable {
   public short getArray(byte[] array, short off, short len);
}
