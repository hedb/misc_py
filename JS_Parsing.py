import esprima

# program = 'const answer = 42'
# program = "document.getElementById('demo').innerHTML = Date()"
program = """

var cars = ["BMW", "Volvo", "Saab", "Ford", "Fiat", "Audi"];
var text = "";
var i;
for (i = 0; i < cars.length; i++) {
    text += cars[i] + "<br>";
}
document.getElementById("demo").innerHTML = text;

"""

res = esprima.tokenize(program)
print(res)