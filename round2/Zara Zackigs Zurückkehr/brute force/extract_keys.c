#include <stdio.h>
#include <stdbool.h> 


void print_int(const char* descripiton, int number) {
   printf(descripiton);
   printf(": ");
   printf("%d", number);
   printf("\n");
}

int main()
{
   int n = 20;
   int k = 4;
   int card_len = 32;
   char binary[20][32] = {
      {0b10111100,0b11000111,0b01000100,0b10101110},
      {0b10111100,0b11000111,0b10101010,0b00000011},
      {0b00111101,0b01011100,0b01101001,0b10011001},
      {0b11111110,0b00101101,0b00010000,0b00110111},
      {0b00010000,0b00110010,0b10001110,0b00010101},
      {0b11010111,0b11101011,0b11011011,0b11110000},
      {0b11011101,0b10010000,0b10010100,0b11000111},
      {0b11100011,0b10010001,0b10101001,0b01111101},
      {0b11100110,0b00110111,0b11000110,0b01010010},
      {0b10101100,0b11111101,0b10101000,0b11100000},
      {0b10000011,0b00101000,0b11010111,0b01101111},
      {0b10111000,0b01100111,0b00001010,0b10111110},
      {0b01101111,0b00100101,0b11010001,0b10100001},
      {0b10001110,0b11110001,0b10100100,0b00100011},
      {0b10000110,0b11100011,0b10010111,0b01100110},
      {0b01100101,0b11010110,0b00010011,0b11011111},
      {0b10110000,0b01101100,0b01011110,0b10010010},
      {0b00011111,0b10100011,0b00010001,0b11100000},
      {0b00111110,0b11110111,0b00010000,0b01011010},
      {0b00100100,0b01111111,0b11011011,0b00101111}
   };

   printf("started execution\n");

   bool found_duplicates = true;
   int needed_length = 0;

   while (found_duplicates)
   {
      needed_length++;

      bool found_something = false;

      for (int i=0; i<n; i++) {
         for (int j=0; j<n; j++) {
            if (i==j) continue;

            found_something = true;
            for (int o=0; o<needed_length; o++) {
               if (binary[i][o] != binary[j][o]){
                  found_something = false;
                  break;
               }
            }
            if (found_something) break;
         }
         if (found_something) break;
      }

      if (!(found_something)) {
         found_duplicates = false;
         break;
      }
   }
   print_int("needed length", needed_length);
}