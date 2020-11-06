package secret;

import javacard.framework.*;

public class SecretApplet extends Applet implements SecretInterface
{
   private byte[] secretArray;
   
   SecretApplet() {
      secretArray = new byte[32];
   }
   
   public Shareable getShareableInterfaceObject(AID clientAID, byte parameter) {
      return this;
   }
   
   public static void install(byte[] bArray, short bOffset, byte bLength) 
   {
      new SecretApplet().register(bArray, (short) (bOffset + 1), bArray[bOffset]);
   }
   
   public short getSecret(byte[] buf, short off, short len) {
      Util.arrayCopy(secretArray, (short)0, buf, off, len);
      return len;
   }

   public short setSecret(byte[] buf, short off, short len) {
      Util.arrayCopy(buf, off, secretArray, (short)0, len);
      return len;
   }

   // this applet doesn't accept any APDU commands
   public void process(APDU apdu)
   {
      if (selectingApplet())
      {
         return;
      }
      ISOException.throwIt(ISO7816.SW_INS_NOT_SUPPORTED);
   }

}