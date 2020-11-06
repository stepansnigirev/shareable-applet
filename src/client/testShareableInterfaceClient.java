package client;

import javacard.framework.*;
import server.IShareableInterface;

public class testShareableInterfaceClient extends Applet
{
   final static byte[] serverAID = { 0x11, 0x22, 0x33, 0x44, 0x55, 0x00 };
   public static void install(byte[] bArray, short bOffset, byte bLength) 
   {
      new testShareableInterfaceClient().register(bArray, (short) (bOffset + 1), bArray[bOffset]);
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
         IShareableInterface sio = (IShareableInterface) JCSystem.getAppletShareableInterfaceObject(new AID(serverAID, (short) 0, (byte) (serverAID.length & 0xFF)), (byte) 0);
         short len = sio.getArray(buf, (short)0, (short)5);
         apdu.setOutgoingAndSend((short)0, len);
         break;
      default:
         ISOException.throwIt(ISO7816.SW_INS_NOT_SUPPORTED);
      }
   }

}