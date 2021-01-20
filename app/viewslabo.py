# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 10:36:56 2020

@author: Marek Oomu
"""
from app import app
from flask import render_template
from flask import request 
from flask import jsonify
from flask_mysqldb import MySQL
from hashlib import sha512

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'Mydb'

mysql = MySQL(app)

getUtilisateur = []

@app.route("/", methods=['GET','POST']) #on définit autant que l'on veut ici le / correspond au dernier / de l'url http://localhost:5000/
def index():
    if request.method == "POST":
        
        details = request.form
        nomdecompte = details['identifiant']
        motdepasse = details['motdepasse']
        motdepasse = motdepasse.encode()
        motdepassehash = sha512(motdepasse).hexdigest()
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Utilisateur WHERE identifiant=%s and motdepasse=%s ", (nomdecompte ,motdepassehash))
        isOk = cur.fetchone()
        #print(isOk)
        cur.close()
        if isOk == None :
            return render_template('pagedeconnexion.html')
        else :
            global getUtilisateur
            getUtilisateur = isOk
            return render_template('pagedegarde.html')
        
    return render_template('pagedeconnexion.html')    

@app.route("/connexion") #idem http://localhost:5000/connexion
def params(): #partie 5
    return render_template('pagedegarde.html')
@app.route('/formulaire', methods=['GET', 'POST'])
def form():
    #print("ON EST LA")
    #print(getUtilisateur)
    getUtilisateurList = list(getUtilisateur)
    idUtilisateur=str(getUtilisateurList[0])      
    if request.method == "POST":
        
        details = request.form
        nom = details['nom']
        prenom = details['prenom']
        email = details['email']
        age = details['age']
        addresse = details['addresse']
        #print('ici addresse')
        #print(nom)
        antecedent = details['antecedent']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE Utilisateur SET nom = %s, prenom= %s, email= %s, age= %s, addresse= %s, antecedent= %s WHERE id=%s", (nom, prenom, email, age, addresse, antecedent, idUtilisateur))
        mysql.connection.commit()
        cur.close()
    
    cur = mysql.connection.cursor()
 
    #print("liste ici")
    #print(getUtilisateurList)
    #print(getUtilisateurList[1])
    cur.execute("SELECT * FROM Utilisateur WHERE id=%s", (idUtilisateur))
    curUtilisateur=cur.fetchone()
    #print(getUtilisateur)
    #print(getUtilisateur[0])
    cur.close()
    #print('cur ici')
    #print(curUtilisateur)
    #print(curUtilisateur[1])
    return render_template('informationpersonnelleform.html', utilisateur = curUtilisateur)

@app.route('/perso', methods=['GET', 'POST'])
def perso():
    return render_template('informationpersonnelleform.html')
@app.route('/resultats')
def resultat():
    return render_template('testpdf.html')

if __name__ == "__main__":
    app.run()
