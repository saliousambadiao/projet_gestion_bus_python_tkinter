Bienvenue dans le projet de gestion du systeme de transport du Senegal, allant des utilisateurs, chauffeurs, receveurs aux bus. Nous detaillons ici toutes les etapes a suivre pour demarrer cette application deja fonctionnelle.

1. Ouvrez le projet dans un environnemnt de developpement comme vscode

2. Isolez les installations en creant un environnemnt virtuel avec la commande suivant
```bash 
$ python -m venv venv
```

3. Activez l'environnement avec la commande suivante
a. Pour windows
```bash
$ venv\Script\Activate
```

b. Pour Linux
```bash
$ source venv/activate
```

4. Installez maintenant les bibliotheques necessaires en executant la commande suivant
```bash
$ pip install -r requirements.txt
```

5. Maintenant que cela est fait ouvrez votre terminal et connectez vous a mysql pour creer une base de donnees avec les bonnes tables et les bons noms

a. Connexion a mysql, remplacez username par votre utilisateur mysql et mettez le mot de passe apres avoir appuyer sur entree
```bash
$ mysql -u username -p 
```

b. Creation de la base de donnees
```bash
$  CREATE DATABASE projetexamen;
```

c. Utilisation de la base de donnees
```bash 
$  use projetexamen;
```

d. Creation de la table utilisateurs
```bash 
$ CREATE TABLE utilisateurs (
    -> id INT AUTO_INCREMENT PRIMARY KEY,
    -> nom VARCHAR(255) NOT NULL,
    -> prenom VARCHAR(255) NOT NULL,
    -> telephone VARCHAR(20),
    -> email VARCHAR(255),
    -> login VARCHAR(50) NOT NULL UNIQUE,
    -> password VARCHAR(255) NOT NULL
    -> ); 
```

e. Creation de la table receveurs
```bash 
$  CREATE TABLE receveurs (
    -> id INT AUTO_INCREMENT PRIMARY KEY,
    -> nom VARCHAR(255) NOT NULL,
    -> prenom VARCHAR(255) NOT NULL,
    -> telephone VARCHAR(20),
    -> age INT
    -> );
```

f. Creation de la table chauffeurs
```bash 
$ CREATE TABLE chauffeurs (
    -> id INT AUTO_INCREMENT PRIMARY KEY,
    -> nom VARCHAR(255) NOT NULL,
    -> prenom VARCHAR(255) NOT NULL,
    -> telephone VARCHAR(20),
    -> age INT,
    -> type_permis ENUM('Permis A', 'Permis B') NOT NULL
    -> );
```

g. Creation de la table bus
```bash 
$ CREATE TABLE bus (
    -> id INT AUTO_INCREMENT PRIMARY KEY,
    -> couleur VARCHAR(50),
    -> marque VARCHAR(100),
    -> numero VARCHAR(20) UNIQUE
    -> );
```

h. Maintenant creez un utilisateur pour pouvoir vous connecter a l
application, il peut etre votre admin si vous voulez. Remplacez les informations par celles que vous voulez.
```bash 
$ INSERT INTO utilisateurs (nom, prenom, telephone, email, login, password)
    -> VALUES ('Admin', 'Admin', '1234567890', 'admin@gmail.com', 'admin', 'admin1234');
```

6. Maintenant allez dans le fichier db.py et renseignez les informations de votre base de donnees dans cette section :

```bash
$ connection = mysql.connector.connect(
            host="localhost",
            user="username",
            password="password",
            database="projetexamen"
        )
```
6. Vous etes maintenant bien parti pour voir le resultat. Exectutez la commande suivante 
```bash
$ python .\gestion_bus\main.py
```