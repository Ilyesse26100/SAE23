import os
from Routine_Crud import delete_equipe , determine_winners,delete_joueur,delete_match,delete_pari,delete_performance,delete_supporteur,determine_losers,create_equipe,create_joueur,create_match,create_pari,create_performance,create_supporteur,read_equipes,read_joueurs,read_matches,read_paris,read_performances,read_supporteurs,update_equipe,update_joueur,update_match,update_pari,update_performance,update_supporteur

def menu_principal():
    running = True
    while running:
        print("\nBienvenue dans le système de gestion")
        print("1. Se connecter en tant qu'Admin")
        print("2. Se connecter en tant qu'Utilisateur")
        print("3. Quitter")

        choix = input("Entrez votre choix (1-3): ")
        if choix == '1':
            menuAdmin()
        elif choix == '2':
            menu_utilisateur()
        elif choix == '3':
            print("Merci d'avoir utilisait Real Madrid Bets. À bientôt !")
            running = False
        else:
            print("Choix non valide. Veuillez réessayer.")




def menu_utilisateur():
    while True:
        print("\nMenu Utilisateur")
        print("1. Voir les Matchs")
        print("2. Voir les Équipes")
        print("3. Voir les Performances")
        print("4. Voir les Joueurs")
        print("5. Voir les Supporteurs")
        print("6. Voir les Paris gagner")
        print("7. Voir les Paris perdus")
        print("8. Retour")

        choix = input("Entrez votre choix (1-7): ")
        if choix == '1': 
            if input("Voulez-vous continuer à voir un matche ? (oui/non): ").lower() == 'oui':
                read_matches()
                if input("Appuyez sur n'importe quelle touche pour revenir en arrière..."):
                    continue
        elif choix == '2': 
            if input("Voulez-vous continuer à voir une équipe ? (oui/non): ").lower() == 'oui':
                read_equipes()
                if input("Appuyez sur n'importe quelle touche pour revenir en arrière..."):
                    continue
        elif choix == '4': 
            if input("Voulez-vous continuer à voir des performances ? (oui/non): ").lower() == 'oui':
                read_performances()
                if input("Appuyez sur n'importe quelle touche pour revenir en arrière..."):
                    continue
        elif choix == '5': 
            if input("Voulez-vous continuer à voir des supporteurs ? (oui/non): ").lower() == 'oui':
                read_equipes()
                if input("Appuyez sur n'importe quelle touche pour revenir en arrière..."):
                    continue
        elif choix == '6': 
            if input("Voulez-vous continuer à voir les paris gagner ? (oui/non): ").lower() == 'oui':
                determine_winners()
                if input("Appuyez sur n'importe quelle touche pour revenir en arrière..."):
                    continue
        elif choix == '7': 
            if input("Voulez-vous continuer à voir les paris perdus ? (oui/non): ").lower() == 'oui':
                determine_losers()
                if input("Appuyez sur n'importe quelle touche pour revenir en arrière..."):
                    continue
        elif choix == '8':
            print("Retour au menu principal.")
            return
            
        else:
            print("Choix non valide. Veuillez réessayer.")



def menuAdmin():
    while True:
        print("\nMenu Admin")
        print("1. Gérer les Matches")
        print("2. Gérer les Équipes")
        print("3. Gérer les Performances")
        print("4. Gérer les Joueurs")
        print("5. Gérer les Supporteurs")
        print("6. Gérer les Paris")
        print("7. Quitter")

        choix = input("Entrez votre choix (1-7): ")
        if choix == '1':
            gerer_matches()
        elif choix == '2':
            gerer_equipes()
        elif choix == '3':
            gerer_performances()
        elif choix == '4':
            gerer_joueurs()
        elif choix == '5':
            gerer_supporteurs()
        elif choix == '6':
            gerer_paris()
        elif choix == '7':
            print("Fin du programme.")
            return
        else:
            print("Choix non valide. Veuillez réessayer.")

def gerer_matches():
    while True:
        print("\nGestion des Matches")
        print("1. Ajouter un matche")
        print("2. Lire tous les matches")
        print("3. Mettre à jour un matche")
        print("4. Supprimer un matche")
        print("5. Retour")

        choix = input("Entrez votre choix (1-5): ")
        if choix == '1':
            print("""

                Voici l'affichage des equipe pour effectuer votre matche
                """                  
                  )
            read_equipes()
            if input("Voulez-vous continuer à ajouter un matche ? (oui/non): ").lower() == 'oui':
                create_match()
                if input("Appuyez sur n'importe quelle touche pour revenir en arrière..."):
                    continue
            else:
                continue
        elif choix == '2':
            read_matches()
            if input("Appuyez sur n'importe quelle touche pour revenir en arrière..."):
                continue
        elif choix == '3':
            print("""

                Voici l'affichage des matches pour pouvoir mettre à jour
                """
            )          
            read_matches()
            if input("Voulez-vous continuer à mettre à jour un match ? (oui/non): ").lower() == 'oui':
                update_match()
                if input("Appuyez sur n'importe quelle touche pour revenir en arrière..."):
                    continue
            else:
                continue
        elif choix == '4':
            print("""

                Voici l'affichage des matches pour pouvoir en supprimer
                """          
            )
            read_matches()
            if input("Voulez-vous continuer à mettre à jour un match ? (oui/non): ").lower() == 'oui':
                delete_match()
                if input("Appuyez sur n'importe quelle touche pour revenir en arrière..."):
                    continue
        elif choix == '5':
            print("Retour au menu principal.")
            break
        else:
            print("Choix non valide. Veuillez réessayer.")




def gerer_equipes():
    while True:
        print("\nGestion des Équipes")
        print("1. Ajouter une équipe")
        print("2. Lire toutes les équipes")
        print("3. Mettre à jour une équipe")
        print("4. Supprimer une équipe")
        print("5. Retour")

        choix = input("Entrez votre choix (1-5): ")
        if choix == '1':
            if input("Voulez-vous continuer à ajouter une équipe ? (oui/non): ").lower() == 'oui':
                create_equipe()
                if input("Appuyez sur n'importe quelle touche pour revenir en arrière..."):
                    continue
            else:
                continue
        elif choix == '2':
            read_equipes()
            if input("Appuyez sur n'importe quelle touche pour revenir en arrière..."):
                continue
        elif choix == '3':
            print("Voici l'affichage des équipes pour pouvoir mettre à jour:")
            read_equipes()
            if input("Voulez-vous continuer à mettre à jour une équipe ? (oui/non): ").lower() == 'oui':
                update_equipe()
                if input("Appuyez sur n'importe quelle touche pour revenir en arrière..."):
                    continue
            else:
                continue
        elif choix == '4':
            delete_equipe()
            if input("Appuyez sur n'importe quelle touche pour revenir en arrière..."):
                continue
        elif choix == '5':
            print("Retour au menu principal.")
            break
        else:
            print("Choix non valide. Veuillez réessayer.")




def gerer_performances():
    while True:
        print("\nGestion des Performances")
        print("1. Ajouter une performance")
        print("2. Lire toutes les performances")
        print("3. Mettre à jour une performance")
        print("4. Supprimer une performance")
        print("5. Retour")

        choix = input("Entrez votre choix (1-5): ")
        if choix == '1':
            if input("Voulez-vous continuer à ajouter une performance ? (oui/non): ").lower() == 'oui':
                create_performance()
                if input("Appuyez sur n'importe quelle touche pour revenir en arrière..."):
                    continue
            else:
                continue
        elif choix == '2':
            read_performances()
            if input("Appuyez sur n'importe quelle touche pour revenir en arrière..."):
                continue
        elif choix == '3':
            if input("Voulez-vous continuer à mettre à jour une performance ? (oui/non): ").lower() == 'oui':
                print("Voici l'affichage des performances pour pouvoir mettre à jour:")
                update_performance()
                if input("Appuyez sur n'importe quelle touche pour revenir en arrière..."):
                    continue
            else:
                continue
        elif choix == '4':
            print("Voici l'affichage des performances pour pouvoir en supprimer:")
            if input("Voulez-vous continuer à supprimer une performance ? (oui/non): ").lower() == 'oui':
                delete_performance()
                if input("Appuyez sur n'importe quelle touche pour revenir en arrière..."):
                    continue
        elif choix == '5':
            print("Retour au menu principal.")
            break
        else:
            print("Choix non valide. Veuillez réessayer.")



def gerer_joueurs():
    while True:
        print("\nGestion des Joueurs")
        print("1. Ajouter un joueur")
        print("2. Lire tous les joueurs")
        print("3. Mettre à jour un joueur")
        print("4. Supprimer un joueur")
        print("5. Retour")

        choix = input("Entrez votre choix (1-5): ")
        if choix == '1':
            if input("Voulez-vous continuer à ajouter une un joueur ? (oui/non): ").lower() == 'oui':
                create_joueur()
                if input("Appuyez sur n'importe quelle touche pour revenir en arrière..."):
                    continue
        elif choix == '2':
            if input("Voulez-vous continuer à voir les joueurs ? (oui/non): ").lower() == 'oui':
                read_joueurs()
                if input("Appuyez sur n'importe quelle touche pour revenir en arrière..."):
                    continue
        elif choix == '3':
            read_joueurs()
            if input("Voulez-vous continuer à mettre à jour un joueur ? (oui/non): ").lower() == 'oui':
                update_joueur()
                if input("Appuyez sur n'importe quelle touche pour revenir en arrière..."):
                    continue
        elif choix == '4':
            if input("Voulez-vous continuer à supprimer un joueur ? (oui/non): ").lower() == 'oui':
                delete_joueur()
                if input("Appuyez sur n'importe quelle touche pour revenir en arrière..."):
                    continue
        elif choix == '5':
            break
        else:
            print("Choix non valide. Veuillez réessayer.")


def gerer_supporteurs():
    while True:
        print("\nGestion des Supporteurs")
        print("1. Ajouter un supporteur")
        print("2. Lire tous les supporteurs")
        print("3. Mettre à jour un supporteur")
        print("4. Supprimer un supporteur")
        print("5. Retour")

        choix = input("Entrez votre choix (1-5): ")
        if choix == '1':
            if input("Voulez-vous continuer à ajouter une un supporteur ? (oui/non): ").lower() == 'oui':
                create_supporteur()
                if input("Appuyez sur n'importe quelle touche pour revenir en arrière..."):
                    continue
        elif choix == '2':
            if input("Voulez-vous continuer à lire un supporteur ? (oui/non): ").lower() == 'oui':
                read_supporteurs()
                if input("Appuyez sur n'importe quelle touche pour revenir en arrière..."):
                    continue
        elif choix == '3':
            read_supporteurs()
            if input("Voulez-vous continuer à mettre à jour le supporteur ? (oui/non): ").lower() == 'oui':
                update_supporteur()
                if input("Appuyez sur n'importe quelle touche pour revenir en arrière..."):
                    continue
        elif choix == '4':
            if input("Voulez-vous continuer à supprimer le supporteur ? (oui/non): ").lower() == 'oui':
                delete_supporteur()
                if input("Appuyez sur n'importe quelle touche pour revenir en arrière..."):
                    continue
        elif choix == '5':
            break
        else:
            print("Choix non valide. Veuillez réessayer.")

def gerer_paris():
    while True:
        print("\nGestion des Paris")
        print("1. Ajouter un pari")
        print("2. Lire tous les paris")
        print("3. Mettre à jour un pari")
        print("4. Supprimer un pari")
        print("5. Affiche qui à gagner")
        print("6. Affiche qui à perdu")
        print("7. Retour")

        choix = input("Entrez votre choix (1-5): ")
        if choix == '1':
            if input("Voulez-vous continuer à ajouter un paris ? (oui/non): ").lower() == 'oui':
                create_pari()
                if input("Appuyez sur n'importe quelle touche pour revenir en arrière..."):
                    continue
        elif choix == '2':
            if input("Voulez-vous continuer à ajouter un paris ? (oui/non): ").lower() == 'oui':
                read_paris()
                if input("Appuyez sur n'importe quelle touche pour revenir en arrière..."):
                    continue
        elif choix == '3':
            read_paris()
            if input("Voulez-vous continuer à ajouter un paris ? (oui/non): ").lower() == 'oui':
                update_pari()
                if input("Appuyez sur n'importe quelle touche pour revenir en arrière..."):
                    continue
        elif choix == '4':
            if input("Voulez-vous continuer à ajouter un paris ? (oui/non): ").lower() == 'oui':
                delete_pari()   
                if input("Appuyez sur n'importe quelle touche pour revenir en arrière..."):
                    continue
        elif choix == '5':
            if input("Voulez-vous continuer à voir les gagnants ? (oui/non): ").lower() == 'oui':
                determine_winners()  
                if input("Appuyez sur n'importe quelle touche pour revenir en arrière..."):
                    continue
        elif choix == '6':
            if input("Voulez-vous continuer à ajouter un paris ? (oui/non): ").lower() == 'oui':
                determine_losers() 
                if input("Appuyez sur n'importe quelle touche pour revenir en arrière..."):
                    continue
        elif choix == '7':
            break
        else:
            print("Choix non valide. Veuillez réessayer.")


# Les autres fonctions gerer_equipes, gerer_performances, gerer_joueurs, gerer_supporteurs, et gerer_paris suivraient une logique similaire.
# Chaque fonction aurait ses propres options spécifiques pour ajouter, lire, mettre à jour et supprimer des éléments.

if __name__ == "__main__":
    menu_principal()
