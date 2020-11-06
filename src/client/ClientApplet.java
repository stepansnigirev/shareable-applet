package client;

import javacard.framework.*;
import secret.SecretInterface;

public class ClientApplet extends Applet{

   final static byte[] secretAID = { 0x11, 0x22, 0x33, 0x44, 0x55, 0x00 };
   protected AID aid;

   public static void install(byte[] bArray, short bOffset, byte bLength) 
   {
      new ClientApplet().register(bArray, (short) (bOffset + 1), bArray[bOffset]);
   }

   ClientApplet(){
      aid = new AID(secretAID, (short) 0, (byte) (secretAID.length & 0xFF));
   }

   public void process(APDU apdu){
      if (selectingApplet())
      {
         return;
      }

      byte[] buf = apdu.getBuffer();
      apdu.setIncomingAndReceive();
      short len = Util.makeShort((byte)0, buf[ISO7816.OFFSET_LC]);
      SecretInterface sio = (SecretInterface)JCSystem.getAppletShareableInterfaceObject(aid, (byte)0);
      switch (buf[ISO7816.OFFSET_INS]){
         case (byte)0x00:
            len = sio.getSecret(buf, (short)0, (short)32);
            apdu.setOutgoingAndSend((short)0, len);
            break;
         case (byte)0x01:
            len = sio.setSecret(buf, (short)ISO7816.OFFSET_CDATA, len);
            apdu.setOutgoingAndSend((short)0, (short)0);
            break;
         default:
            ISOException.throwIt(ISO7816.SW_INS_NOT_SUPPORTED);
      }
   }

}