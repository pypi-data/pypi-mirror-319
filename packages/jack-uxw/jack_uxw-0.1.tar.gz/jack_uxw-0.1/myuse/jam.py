def is_prime(n):
    if n<=1:
        return False
    for i in range(2,int(n**0.5)+1):
        if n%i==0:
            return False
    return True
def r_prime(b,a=2):
    l=[]
    for i in range(a,b+1):
        c=0
        for j in range(2,int(i**0.5)+1):
            if i%j==0:
                c+=1
        if c==0:
            l.append(i)
    return l
def multiples(n,s=10):
    return [n*i for i in range(1,s+1)]
def is_fibonacci(n):
    a,b=0,1
    while b<n:
        a,b=b,a+b
    return n==b
def r_fibonacci(n):
    fib=[]
    a,b=0,1
    for i in range(n):
        fib.append(a)
        a,b=b,a+b
    return fib
def is_palindrome(a):
    if type(a)==str:
        k=a.lower()
        return k==k[::-1]
    elif type(a)==int:
        return str(a)==str(a)[::-1]
    else:
        return "Invalid parameter"
def r_palindrome(a,b=1):
    l=[]
    for i in range(b,a+1):
        if str(i)==str(i)[::-1]:
            l.append(i)
    return l
def is_armstrong(n):
    k=[int(str(n)[i]) for i in range(len(str(n)))]
    c=0
    for i in k:
        c+=i**len(str(n))
    return c==n
def is_happy(n):
    while True:
        c=0
        while n>0:
            s=n%10
            c+=s*s
            n//=10
        if len(str(c))==1:
            v=c
            break
        n=c
    return v==1
    
def flames(name1, name2):
    name1 = name1.replace(" ", "").lower()
    name2 = name2.replace(" ", "").lower()
    combined_name = list(name1) + list(name2)
    for char in name1:
        if char in name2:
            combined_name.remove(char)
            combined_name.remove(char)
            name2 = name2.replace(char, "", 1)
    remaining_count = len(combined_name)
    flames_list = ['F', 'L', 'A', 'M', 'E', 'S']
    index = 0
    while len(flames_list) > 1:
        index = (index + remaining_count - 1) % len(flames_list)
        flames_list.pop(index)
    return flames_list[0]
def H_design(text):
    length = len(text)
    border_length = length + 4  
    border = '*' * border_length
    print(border)
    print(f"* {text} *")
    print(border)
def list_int(n):
    return [int(str(n)[i]) for i in range(len(str(n)))]
def list_pow(a,b):
    return [i**b for i in a]
def list_div(a,b):
    return [i/b for i in a]
def list_fdiv(a,b):
    return [i//b for i in a]
def list_multi(a,b):
    return [i*b for i in a]
def int_to_roman(num):
    # Define a dictionary with the Roman numerals and their corresponding values
    val = [
        1000, 900, 500, 400,
        100, 90, 50, 40,
        10, 9, 5, 4,
        1
    ]
    syb = [
        "M", "CM", "D", "CD",
        "C", "XC", "L", "XL",
        "X", "IX", "V", "IV",
        "I"
    ]
    roman_num = ''
    i = 0
    while num > 0:
        for _ in range(num // val[i]):
            roman_num += syb[i]
            num -= val[i]
        i += 1
    return roman_num
def int_to_binary(num):
    # Check if the number is zero
    if num == 0:
        return "0"

    # Handle the sign of the number
    if num < 0:
        sign = "-"
        num = abs(num)
    else:
        sign = ""

    # Split the number into its integer and fractional parts
    integer_part = int(num)
    fractional_part = num - integer_part

    # Convert the integer part to binary
    integer_binary = ''
    if integer_part == 0:
        integer_binary = '0'
    else:
        while integer_part > 0:
            integer_binary = str(integer_part % 2) + integer_binary
            integer_part = integer_part // 2  # Fix: Add integer division here

    # Convert the fractional part to binary
    fractional_binary = ''
    while fractional_part > 0:
        fractional_part *= 2
        bit = int(fractional_part)
        fractional_binary += str(bit)
        fractional_part -= bit
        # Limit the length of fractional binary to avoid infinite loops
        if len(fractional_binary) > 52:  # Double precision floating-point limit
            break

    # Combine the integer and fractional parts
    if fractional_binary:
        binary_num = sign + integer_binary + '.' + fractional_binary
    else:
        binary_num = sign + integer_binary

    return binary_num
def is_leap(n):
    if n%4==0:
        if n%100==0:
            if n%400==0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False
def r_leap(a,b):
    k=[]
    for i in range(b,a+1):
        if i%4==0:
            if i%100==0:
                if i%400==0:
                    k.append(i)
            else:
                k.append(i)
    return k
def list_factors(n):
    l=[]
    for i in range(1,n+1):
        if n%i==0:
            l.append(i)
    return l
def extract_numbers(s):
    numbers = []
    current_number = ''
    is_decimal = False 
    for char in s:
        if char.isdigit():
            current_number += char 
        elif char == '.' and not is_decimal: 
            current_number += char  
            is_decimal = True
        else:
            if current_number: 
                numbers.append(float(current_number) if is_decimal else int(current_number))  # Convert to float or int
                current_number = ''  
                is_decimal = False  
    if current_number:
        numbers.append(float(current_number) if is_decimal else int(current_number))
    return numbers
def extract_substring(s, begin, end):
    begin_index = s.find(begin)
    end_index = s.find(end, begin_index + len(begin))
    if begin_index != -1 and end_index != -1:
        return s[begin_index + len(begin):end_index].strip()
    else:
        return ''  
def is_strongnumber(num):
    def factorial(n):
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
    sum_of_factorials = sum(factorial(int(digit)) for digit in str(num))
    return sum_of_factorials == num
def is_perfectnumber(num):
    if num <= 1:
        return False
    divisors_sum = sum(i for i in range(1, num) if num % i == 0)
    return divisors_sum == num











