# GoodhaHash
Simple and fast 512-bit hashing algorithm.

## How to use
**Python-** Import GoodhaHash file into your script and call `GoodhaHash.hash` function by providing it with `input` paramether. Input can be of string, byte array, integer or float data type. The function is going to return string representation of hash value.

## How it works
Function `hash` first checks data type of input value and turns it into string of hex representation of the value.
There are 4 private function in the GoodhaHash for the purpose of mixing bytes:

+ **_spread** first creates empty string value. Then appends to it original value as many times is necessary until the string reach 256 characters in length.
+ **_shift** iterates through input string and takes every two characters and turns it to integer. Then it shifts bites left from 0 to 5 times. First byte is shifted 1 bit, next one 2 and so on until 5; then it resets counter to 0. In this way produced values are append to the new string value that is going to be returned.
+ **_cut** function have the purpose to turn input value into 128 characters hex representation. It iterates through input value and takes evety two characters and turns it into integer(**e** in the code). Than it mask that number with 0xff for the case when value exceeds one byte. Before it continues, another variable **count** is set to be 0 and one new list **row** of 64 bytes. If **count** % 7 is 0 then e is going to be xor-ed with element **count** in the row and is going to be stored at the same place. If **count** % 5 is 0, addition is going to be performed, and if **count** % 3 is 0, multiplication. In all other cases, value of **e** is going to be shifted n(% 7 index of byte presently iterated trough input value) bit to the left into **row** n(**count**) element. After this part is over, variable **count** is risen by 1 and if **count** reach 64 it is reset back to 0. In the final part of this function, all of elements from the **row** list are turned into string representation of the hex value and attached to the string value that is going to be returned from the function.
+ **_root** function iterates throug input value by the step of 8 places. In every step, takes 8 characters and turns them into integer value stored into variable **e**. Then creates variable **r** and stores into it squere root of e value. **f** variable holds integer part of variable **r**. **p** variable holds divisional part of the variable **r**. Variable **e** is then multiplied with **f** and xor-ed with **p**. 16 values produced by this loop are stored into list **l**. Value from this list are appended to the return value in index order 15, 13, 11, 9, 7, 5, 3, 1, 14, 12, 10, 8, 6, 0, 2, 4.

`hash` function calls supprot function in order:

+ if input length is more than 256, first is called `_spread` in other case, first `_cut` and then `_spread`
+ `_root`
+ `_shift`
+ `_cut`
+ `_spread`
+ `_shift`
+ `_cut`