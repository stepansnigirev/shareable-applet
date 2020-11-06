package server;

import javacard.framework.*;

public class testShareableInterface extends Applet implements IShareableInterface
{
   private byte[] testArray;
   
   testShareableInterface() {
      testArray = new byte[5];
   }
   
   public Shareable getShareableInterfaceObject(AID clientAID, byte parameter) {
      return this;
   }
   
   public static void install(byte[] bArray, short bOffset, byte bLength) 
   {
      new testShareableInterface().register(bArray, (short) (bOffset + 1), bArray[bOffset]);
   }
   
   public short getArray(byte[] buf, short off, short len) {
      Util.arrayCopy(testArray, (short) 0, buf, off, len);
      return len;
   }

   public void process(APDU apdu)
   {
      if (selectingApplet())
      {
         return;
      }

      byte[] buf = apdu.getBuffer();
      switch (buf[ISO7816.OFFSET_INS])
      {
      case (byte)0x00:
         apdu.setIncomingAndReceive();
         Util.arrayCopy(buf, (short) ISO7816.OFFSET_CDATA, testArray, (short) 0, (short) 5);
         break;
      default:
         ISOException.throwIt(ISO7816.SW_INS_NOT_SUPPORTED);
      }
   }

}