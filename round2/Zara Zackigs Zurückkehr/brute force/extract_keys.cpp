#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <bitset>

#include <stdio.h>
#include <stdbool.h> 
using namespace std;

void print(string description,vector <unsigned int> const &a) {
   cout << "The " << description << " elements are : ";

   for(int i=0; i < a.size(); i++)
   {
      cout << a.at(i) << ' ';
   }

   cout << "\n";
}

void print_binary(unsigned char output) {
   char text[16];
   itoa(output, text, 2);
   printf("%s\n", text);
}

struct increment_data
{
   vector<unsigned int> indices;
   int new_value;
};
typedef struct increment_data Increment;



Increment increment(vector<unsigned int> indices, vector<unsigned int> maximums, int i) {
   indices[i]++;
   if (indices[i] > maximums[i] && i>0)
   {
      Increment r = increment(indices, maximums, i-1);
      indices = r.indices;
      indices[i] = r.new_value + 1;
   }

   Increment s;
   s.indices = indices;
   s.new_value = indices[i];
   
   return s;
}

int main()
{
   int n;
   int k;
   int card_len;

   // einlesen des Files
   ifstream data_file ("examples/stapel2.txt");
   string data_str;
   if (data_file.is_open()) 
   {
      getline(data_file, data_str);
      cout << data_str << "\n";

      int whitespace_1 = data_str.find(" ");
      int whitespace_2 = data_str.find(" ", whitespace_1+1);

      cout << whitespace_2 << "\n";
      
      n = stoi(data_str.substr(0, whitespace_1));
      k = stoi(data_str.substr(whitespace_1+1, whitespace_2-3));
      card_len = stoi(data_str.substr(whitespace_2+1, data_str.size()-1));
      cout << "values are: " << n << ";" << k << ";" << card_len << "\n";
   }

   // erstellen des vektors der alle unsigned chars beinhaltet
   vector<vector<unsigned char>> cards(n);

   //cout << "start creating list\n";
   for (int i=0; i<n; i++) 
   {
      getline(data_file, data_str);
      //cout << data_str << "\n";

      for (int j=0; j<card_len; j+=8) {
         const string sub = data_str.substr(j,8);
         unsigned char byte = static_cast<char>(bitset<8>(sub).to_ulong());
         //cout << sub << byte << "\n";
         //print_binary(byte);
         cards[i].push_back(byte);
      }
      //cout << "\n";
   }
   //cout << "finished creating list\n";

   /*
   // die noetige laenge bekommen
   bool found_duplicates = true;
   int needed_length = 1;

   while (found_duplicates)
   {
      needed_length++;

      bool found_something = false;

      for (int i=0; i<n; i++) {
         for (int j=0; j<n; j++) {
            if (i==j) continue;

            found_something = true;
            for (int o=0; o<needed_length; o++) {
               if (cards[i][o] != cards[j][o]){
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
   cout << "needet length: " << needed_length << "\n";
   vector<vector<unsigned char>> neccesarry_cards(n);
   for (int i=0; i<n; i++) 
   {
      vector<unsigned char>::const_iterator first = cards[i].begin() + 0;
      vector<unsigned char>::const_iterator last = cards[i].begin() + needed_length;
      vector<unsigned char> subvector (first, last);
      print_binary(subvector[0]);
      neccesarry_cards[i] = subvector;
   }*/
   int needed_length = card_len;
   vector<vector<unsigned char>> neccesarry_cards = cards;


   // hauptberechnung
   vector<unsigned int> indices(k);
   vector<unsigned int> maximums(k);
   for (int i=0; i<k; i++) {
      int j = n-k+i;
      maximums[i] = j;
      indices[i] = i;
   }
   print("maximal value", maximums);

   unsigned int tries = 0;
   bool found_keys = false;
   while (indices[0]<=maximums[0] && !found_keys)
   {
      print("indice",indices);

      // xor'e die Kombination
      vector<unsigned char> xored = neccesarry_cards[indices[0]];

      for (int i=1; i<k; i++) {
         vector<unsigned char> current_card = neccesarry_cards[indices[i]];
         for (int j=0; j<current_card.size(); j++) {
            xored[j] = xored[j] ^ current_card[j];
         }
      }

      // schaue ob das xor'te in der liste ist
      for (int i=0; i<n; i++) {
         if (xored == neccesarry_cards[i]) {
            found_keys = true;

            cout << "xored: ";
            print_binary(xored[0]);
            break;
         }
      }

      if (found_keys) {
         break;
      }

      // bekomme die naechste moegliche Kombination
      Increment s = increment(indices, maximums, k-1);
      indices = s.indices;

      tries++;
   }
   
   cout << "tries: " << tries << "\n";
   print("sollution", indices);

   return 0;
}