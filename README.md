# shareable-applet

```
>> /select 112233445500  // Server applet;
>> 00 A4 04 00 06 11 22 33 44 55 00 00
<< 90 00

>> /send 00000000051122334455  // Write shared array data: 1122334455;
>> 00 00 00 00 05 11 22 33 44 55
<< 90 00

>> /select 010203040500  // Client applet;
>> 00 A4 04 00 06 01 02 03 04 05 00 00
<< 90 00

>> /send 0000000005  // ReadArray from server applet by client applet;
>> 00 00 00 00 05
<< 11 22 33 44 55 90 00
```