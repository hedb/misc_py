from math import floor

# https://projecteuler.net/problem=751
# https://docs.google.com/spreadsheets/d/1zghOv7uVNnVexK_hbJTECAkmFh0ohnAYhGHrHKxKwfs/edit#gid=0



class MyFloat:

    def __init__(self, int_value, decimal_shift):
        # I.e.          2.5 ~= (25,1), 0.25 ~= (25,2)
        self.int_value = int_value
        self.decimal_shift = decimal_shift

    def floor(self):
        v_str = str(self.int_value)
        significant_digits = len(v_str)-self.decimal_shift
        v = 0 if significant_digits==0 else int (v_str[0:significant_digits])
        return MyFloat(v,0)

    def toStr(self):
        return "({},{})".format(self.int_value,self.decimal_shift)

    def eq(self,o):
        return self.int_value == o.int_value and self.decimal_shift == o.decimal_shift

    def mult(self,o):
        return MyFloat(self.int_value*o.int_value,self.decimal_shift+o.decimal_shift)

    def minus(self,o):
        new_self_val = self.int_value if self.decimal_shift >= o.decimal_shift else self.int_value*pow(10,o.decimal_shift - self.decimal_shift)
        new_o_val = o.int_value if o.decimal_shift >= self.decimal_shift else o.int_value*pow(10,self.decimal_shift - o.decimal_shift)
        return MyFloat (new_self_val - new_o_val,max(self.decimal_shift,o.decimal_shift))

    def plus(self,o):
        new_self_val = self.int_value if self.decimal_shift >= o.decimal_shift else self.int_value*pow(10,o.decimal_shift - self.decimal_shift)
        new_o_val = o.int_value if o.decimal_shift >= self.decimal_shift else o.int_value*pow(10,self.decimal_shift - o.decimal_shift)
        return MyFloat (new_self_val + new_o_val,max(self.decimal_shift,o.decimal_shift))


# tests
v = MyFloat(25,1)
v1 = MyFloat(25,2)

# print(v.toStr(),v.floor().toStr())
# print(v1.toStr(),v1.floor().toStr())
assert (v.floor().eq( MyFloat(2,0)))
assert (v1.floor().eq( MyFloat(0,0)))


assert (v1.mult(v).eq( MyFloat(625,3)))

assert (v.minus(v1).eq( MyFloat(225,2)))
assert (v1.minus(v).eq( MyFloat(-225,2)))


assert (v.plus(v1).eq( MyFloat(275,2)))

# exit()


def calc_val(bn0):
    bn = bn0
    target = "2."
    for i in range(30):
        bn = floor(bn) * ( bn - floor(bn) + 1)
        an = floor(bn)
        target = target + str(an)

    return target



def generate_val(bn0):

    for i in range(30):
        target = calc_val(bn0)

        bn0_before = bn0
        bn0 = float(target[0:i+3])
        print('before, target, after')
        print(bn0_before)
        print(target)
        print(bn0)
        print()


def calc_val1(bn0):
    bn = bn0
    target = "2."
    for i in range(30):
        # bn = floor(bn) * ( bn - floor(bn) + 1)
        bn = bn.floor().mult(bn.minus ( bn.floor() ).plus( MyFloat(1,0) )   )

        an = bn.floor()
        target = target + str(an.int_value)
    return target

def generate_val1(bn0):

    for i in range(30):
        target = calc_val1(bn0)

        bn0 = MyFloat (  int ( "2" + target[2:i+3] )  , i+1 )

        print( "got:", target)
        print( "sending:", bn0.toStr())
        print()




# print (generate_val(2.2))
# print (calc_val(2.223561019))
# print (calc_val(2.223))


print (generate_val1( MyFloat(22,1)))