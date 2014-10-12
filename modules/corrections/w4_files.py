# -*- coding: utf-8 -*-
from exercice import Exercice, Exercice_1arg, Exercice_multiline

import os

#################### 
# the function as it is specified does not fit in the 'exercice' framework
# so here create helpers to make all this compliant
def file_contents (filename):
    try:
        with open(filename) as input:
            return input.read()
    except:
        return ""

# this decorator does the trick to transform a student-written function
# into something that exercice/correction_table can deal with
def exercice_compliant (fun):
    def wrapped (in_name, out_name):
        # clean up output (in case the function does not create it
        try: 
            os.unlink(out_name)
        except:
            pass
        # run 
        fun(in_name,out_name)
        # return output's contents
        return file_contents (out_name)
    return wrapped

### might end up in exercice if there's enough interest
from IPython.display import HTML

# on lance la fonction dans un fichier temporaire et on le montre
def show_comptage (in_name, out_name, comptage, suffix):
    out_name += suffix
    comptage (in_name, out_name)
    try:
        input, output = file_contents (in_name), file_contents (out_name)
        os.unlink(out_name)
    except OSError:
        print "Votre fonction ne semble pas crÃ©er le fichier de sortie"
        return 
    html = ""
    html += "<table>"
    html += "<tr><th>EntrÃ©e</th></tr>"
    for line in input.split("\n"):
        html += "<tr><td>{}</td></tr>".format(line)
    html += "<tr><th>Sortie</th></tr>"
    for line in output.split("\n"):
        html += "<tr><td>{}</td></tr>".format(line)
    html += "</table>"
    return HTML(html)
    
####################
# comptage ()
@exercice_compliant
def comptage (in_filename, out_filename):
    with open(in_filename) as input:
        with open(out_filename,"w") as output:
            lineno = 0
            total_words = 0
            total_chars = 0
            for line in input:
                lineno += 1
                nb_words = len(line.split())
                total_words += nb_words
                nb_chars = len(line)
                total_chars += nb_chars
                output.write ("{}:{}:{}:{}".\
                              format(lineno,nb_words,nb_chars,line))
            output.write("{}:{}:{}\n".format(lineno,total_words, total_chars))

comptage_inputs = [
    ('data/romeo_and_juliet.txt', 'romeo_and_juliet.out'),
    ('data/lorem_ipsum.txt', 'lorem_ipsum.out'),
]

class ExerciceComptage (Exercice):

    def correction (self, student_comptage):
        # call the decorator on the student code
        return Exercice.correction (self, exercice_compliant(student_comptage))

    # on prend le premier jeu d'entrÃ©e
    def exemple (self):
        return show_comptage (*self.inputs[0], comptage=comptage, suffix=".ok")

    def debug (self, student_comptage):
        return show_comptage (*self.inputs[0], comptage=student_comptage, suffix="")


exo_comptage = ExerciceComptage (comptage, comptage_inputs)