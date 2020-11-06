package secret;

import javacard.framework.*;

public interface SecretInterface extends Shareable {
   public short setSecret(byte[] array, short off, short len);
   public short getSecret(byte[] array, short off, short len);
}
