// euler_386.cpp : This file contains the 'main' function. Program execution begins and ends there.
//


#include <chrono>
#include <iostream>
#include <ctime>
#include <array>
#include <map>
#include <algorithm>
#include <iostream>
#include <sstream>

#include <time.h>

using namespace std;


const unsigned int SIZE = pow(10,5);
const unsigned int PRIMES_ARR_LENGTH = floor(SIZE / 10);

// const unsigned int MAX_POWER = ceil(log2(SIZE)); // 27
const unsigned int MAX_DIFFERENT_PRIMES = 11;



unsigned int* primes = new unsigned int[1];
std::map<unsigned int, unsigned int> primes_rep;
//std::array<unsigned int, PRIMES_ARR_LENGTH> primes;
unsigned int primes_counter = 1;


std::map<string, unsigned int> primes_key_to_chain;


struct prime_signature { unsigned int primes[MAX_DIFFERENT_PRIMES]; unsigned char power[MAX_DIFFERENT_PRIMES]; };
prime_signature * sieve = new prime_signature[SIZE]();


unsigned int represent_as_primes_sieve(unsigned int n) {

	//if (n == 3163) {
	//	unsigned int stop = 1;
	//}

	if (sieve[n].primes[0] == 0) {
		// fell on prime

		unsigned int prev_n_power = 1;
		unsigned int n_power = 1;

		for (unsigned int power = 1;
			n < SIZE / n_power
			; power ++)
		{
			prev_n_power = n_power;
			n_power = pow(n, power);

			for (unsigned int i = n_power; i < SIZE; i += n_power) {
				for (unsigned int j = 0; j < (MAX_DIFFERENT_PRIMES + 1); j++) {
					if (j == MAX_DIFFERENT_PRIMES) {
						throw "more then expected unique primes caught";
					}

					if ((sieve[i].primes[j] == 0) || (sieve[i].primes[j] == n)) {
						sieve[i].primes[j] = n;
						sieve[i].power[j] = power;
						break;
					}
				}
			}
		}
	}

	// calc total from sieve
	unsigned int ret = 0;
	for (unsigned int j = 0; j < (MAX_DIFFERENT_PRIMES + 1); j++) {
		ret += sieve[n].power[j];
	}

	return ret;

}


unsigned int represent_as_primes(unsigned int n1) {
	unsigned int total = 0;
	unsigned int index = -1;
	unsigned int n = n1;


	for (unsigned int j=0; j < PRIMES_ARR_LENGTH ; j++) {
		unsigned int p = primes[j];
		index += 1;
		if (j >= primes_counter) break;

		while (n % p == 0) {
			total += 1;
			n = n / p;
		}

		if (primes_rep.find(n) != primes_rep.end()) {
			total += primes_rep[n];
			n = 1;
			break;
		}

	}
	if (n > 1) {
		primes[primes_counter] = n;
		primes_counter += 1;
		total = 1;
	}

	primes_rep[n1] = total;

	return total;
}

unsigned int run_calc_sum_represent_as_primes()
{
	clock_t ts = clock();
	primes[0] = 2;

	unsigned int s = 0;
	unsigned int print_threshold = 2;

	for (unsigned int i = 2; i < SIZE + 1; i++) {
		// cout << i << "\n";
		s += represent_as_primes_sieve(i);

		//if (i == 4096) {
		//	exit(1);
		//}

		//if (true) {
		 if (i % print_threshold == 0) {
			print_threshold *= 2;
			clock_t ts1 = clock();
			cout << i << "\t" << s << "\t" << ts1 - ts << "\n" ;
			ts = ts1;
		}
	}
	return s;
}



bool descending_order(unsigned int i, unsigned int j) { return (i > j); }


unsigned int count_options(unsigned char* position_limit, unsigned char len, unsigned int total) {

	if (len == 0 || total <= 0) {
		if (total == 0) {
			return 1;
		}
		else {
			return 0;
		}
	}
	unsigned int ret = 0;

	for (int i = position_limit[0]; i > -1; i = i - 1) {
		ret += count_options(position_limit + 1, len - 1, total - i);
	}

	return ret;
}



unsigned int calc_longets_chain(unsigned int n) {
	unsigned int ret = 0, total = 0;

	represent_as_primes_sieve(n);

	sort(sieve[n].power, sieve[n].power + MAX_DIFFERENT_PRIMES, descending_order);
	ostringstream primes_as_key;

	for (unsigned char& i: sieve[n].power) {
		primes_as_key << (int)i << '_';
	}

	string primes_as_key_str = primes_as_key.str();

	if (primes_key_to_chain.find(primes_as_key_str) != primes_key_to_chain.end()) {
		ret = primes_key_to_chain[primes_as_key_str];
	} else {
		unsigned char non_zeros = 0;
		for (unsigned char& i : sieve[n].power) {
			total += i;
			if (i != 0) non_zeros++;
		}
		total = floor(total / 2);

		ret = count_options(sieve[n].power, non_zeros, total);
		primes_key_to_chain[primes_as_key_str] = ret;
	}

	return ret;
}


unsigned int run_calc_antichain_sum() {

	clock_t ts = clock();

	unsigned int s = 0,current_anti_chain_length = 0;
	unsigned int print_threshold = 2;

	for (unsigned int i = 2; i < SIZE + 1; i++) {
		// cout << i << "\n";
		current_anti_chain_length = calc_longets_chain(i);
		s += current_anti_chain_length;

		//if (i == 4096) {
		//	exit(1);
		//}

		//if (true) {
		if ( (i % print_threshold == 0) || (i> SIZE-2)) {
			print_threshold *= 2;

			clock_t ts1 = clock();
//			cout << i << "\t" << current_anti_chain_length << "\tTotal Sum: " <<  s <<  "\tElapsed: " << ts1 - ts << "\n";
			cout << i << "\t" << s << "\t" << ts1 - ts << "\n";
			ts = ts1;
		}
	}

	return s;

}


unsigned int main()
{

	//run_calc_sum_represent_as_primes();

	unsigned int total_sum = run_calc_antichain_sum();

	cout << SIZE << "\t" << total_sum + 1 << "\n" ;

	for (auto x : primes_key_to_chain) {
		cout << x.first << "\t" << x.second << "\n";
	}


	delete[] sieve;
	delete[] primes;
}

