# GoodhaHash
Simple and fast 512-bit hashing algorithm.

## How to use
**Python-** Import GoodhaHash file into your script and call `GoodhaHash.hash` function by providing it with `input` paramether. Input can be of string, byte array, integer or float data type. The function is going to return string representation of hash value.

## How it works
Function `hash` have tree arguments. First is value to be processed, second is optional paramether `type` with posible values `hex`, `string`, `bytes` and `float`. Default type is `hex`. Second optional argument is `pack`. `pack` is boolean argument; True is defauld value. Usual digest of Goodha hash produces more that 350 hex characters. Packet version contains less that 128 hex characters.
There are 5 private function in the GoodhaHash for the purpose of mixing bytes:

+ **_spread** first creates empty string value. Then appends to it original value as many times is necessary until the string reach 256 characters in length.
+ **_shift** iterates through input string and takes every 8 characters and turns it to integer. Then it cyrcle shifts 3 bites left.
+ **_cut** function have the purpose to make final value shorter
+ **_mess** function mix values with one another using 
all bitvise operations.
+ **_pack** function is called to calculate shorter digest(128 hex characters or less). By default is called just beffore hash function returns value.

`hash` function calls supprot function in order:

+ if input length is more than 256, first is called `_spread` in other case, first `_cut` and then `_spread`
+ `_shift`
+ `_mess`
+ `_cut`
+ `_shift`