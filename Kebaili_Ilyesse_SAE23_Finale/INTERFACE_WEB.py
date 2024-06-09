
import cherrypy, os, os.path
from mako.template import Template
from mako.lookup import TemplateLookup
from Crud_Web import get_equipes_data, get_joueurs_par_equipe,get_past_matches,get_equipes_sans_realmadrid,get_paris,get_upcoming_matches,get_victoires_defaites_nuls_par_equipe,get_combined_equipes_data,add_team,delete_team,get_all_equipes,update_team,team_exists,update_joueur,delete_joueur,add_joueur,get_all_joueurs,joueur_exists

mylookup = TemplateLookup(directories=['html'], input_encoding='utf-8', module_directory='html/mako_modules')

class Interface_Web_Real_Bets(object):
    @cherrypy.expose
    def index(self):
        mytemplate = mylookup.get_template("index.html")
        upcoming_matches = get_upcoming_matches()
        return mytemplate.render(upcoming_matches=upcoming_matches)

    @cherrypy.expose
    def show_equipe(self):
        equipes = get_equipes_data()
        mytemplate = mylookup.get_template("team.html")
        return mytemplate.render(equipes=equipes)

    @cherrypy.expose
    def match_history(self):
        past_matches = get_past_matches()
        output = ""
        if past_matches:
            for match in past_matches:
                output += f"""
                <div class="match">
                    <p><strong>Date:</strong> {match['date']}</p>
                    <p><strong>Équipe à domicile:</strong> {match['equipe_domicile']}</p>
                    <p><strong>Équipe à l'extérieur:</strong> {match['equipe_exterieur']}</p>
                    <p><strong>Résultat:</strong> {match['resultat']}</p>
                </div>
                """
        else:
            output = "<p class='rien'>Aucun match passé enregistré.</p>"
        return output

    @cherrypy.expose
    def show_joueurs(self, equipe_id, page_context):
        # Récupérer les joueurs de l'équipe sélectionnée
        joueurs = get_joueurs_par_equipe(equipe_id)
        
        # Récupérer les équipes en fonction du contexte
        if page_context == 'team':
            equipes = get_combined_equipes_data(get_equipes_data())
        elif page_context == 'OtherTeam':
            equipes = get_combined_equipes_data(get_equipes_sans_realmadrid())
        else:
            equipes = []

        # Rendre le template avec les données appropriées
        mytemplate = mylookup.get_template("team.html")
        return mytemplate.render(equipes=equipes, joueurs=joueurs, page_context=page_context)

    
    @cherrypy.expose
    def betting(self):
        paris_info = get_paris()
        mytemplate = mylookup.get_template("betting.html")
        return mytemplate.render(paris_info=paris_info)


    @cherrypy.expose
    def team(self, joueurs=None):
        # Utiliser la nouvelle fonction pour obtenir les données combinées du Real Madrid
        equipes = get_combined_equipes_data(get_equipes_data())
        mytemplate = mylookup.get_template("team.html")
        return mytemplate.render(equipes=equipes, joueurs=joueurs, page_context='team')

    @cherrypy.expose
    def OtherTeam(self, joueurs=None):
        # Utiliser la nouvelle fonction pour obtenir les données combinées des équipes sauf le Real Madrid
        equipes = get_combined_equipes_data(get_equipes_sans_realmadrid())
        mytemplate = mylookup.get_template("team.html")
        return mytemplate.render(equipes=equipes, joueurs=joueurs, page_context='OtherTeam')
    

    @cherrypy.expose
    def add_team(self, nom=None, stade=None, entraineur=None):
        if cherrypy.request.method == 'POST':
            success, message = add_team(nom, stade, entraineur)
            if not success:
                return f"<p style='color:red;'>{message}</p><a href='/add_team'>Réessayer</a>"
            raise cherrypy.HTTPRedirect("/OtherTeam")
        else:
            mytemplate = mylookup.get_template("Ajouter_equipe.html")
            return mytemplate.render()


    @cherrypy.expose
    def delete_team(self, equipe_id=None):
        if cherrypy.request.method == 'POST':
            if not equipe_id:
                return self.render_delete_team_page("ID de l'équipe est requis.")
            
            try:
                equipe_id = int(equipe_id)
                if equipe_id <= 0:
                    return self.render_delete_team_page("L'ID de l'équipe doit être un nombre positif.")
                
                success, message = delete_team(equipe_id)
                if not success:
                    return self.render_delete_team_page(message)
                raise cherrypy.HTTPRedirect("/team")
            except ValueError:
                return self.render_delete_team_page("L'ID de l'équipe doit être un nombre.")
        else:
            return self.render_delete_team_page()
        
    @cherrypy.expose
    def update_team(self, equipe_id=None, nom=None, stade=None, entraineur=None):
        if cherrypy.request.method == 'POST':
            if not equipe_id:
                return self.render_update_team_page("ID de l'équipe est requis.")
            
            try:
                equipe_id = int(equipe_id)
                if equipe_id <= 0:
                    return self.render_update_team_page("L'ID de l'équipe doit être un nombre positif.")
                
                success, message = update_team(equipe_id, nom, stade, entraineur)
                if not success:
                    return self.render_update_team_page(message)
                raise cherrypy.HTTPRedirect("/team")
            except ValueError:
                return self.render_update_team_page("L'ID de l'équipe doit être un nombre.")
        else:
            return self.render_update_team_page()
        


    @cherrypy.expose
    def joueurs(self):
        joueurs = get_all_joueurs()
        mytemplate = mylookup.get_template("joueurs.html")
        return mytemplate.render(joueurs=joueurs)    

    @cherrypy.expose
    def delete_joueur(self, joueur_id=None):
        if cherrypy.request.method == 'POST':
            try:
                joueur_id = int(joueur_id)
                success, message = delete_joueur(joueur_id)
                if not success:
                    return f"<p style='color:red;'>{message}</p><a href='/delete_joueur'>Réessayer</a>"
                raise cherrypy.HTTPRedirect("/joueurs")
            except ValueError:
                return f"<p style='color:red;'>L'ID du joueur doit être un nombre.</p><a href='/delete_joueur'>Réessayer</a>"
        else:
            mytemplate = mylookup.get_template("delete_joueur.html")
            return mytemplate.render()
        

    @cherrypy.expose
    def add_joueur(self, nom=None, prenom=None, poste=None, equipe_id=None):
        error_message = None
        if cherrypy.request.method == 'POST':
            try:
                equipe_id = int(equipe_id)
                success, message = add_joueur(nom, prenom, poste, equipe_id)
                if not success:
                    error_message = message
                else:
                    raise cherrypy.HTTPRedirect("/joueurs")
            except ValueError:
                error_message = "L'ID de l'équipe doit être un nombre."
        mytemplate = mylookup.get_template("add_joueur.html")
        return mytemplate.render(error_message=error_message)

    @cherrypy.expose
    def update_joueur(self, joueur_id=None, nom=None, prenom=None, poste=None, equipe_id=None):
        error_message = None
        if cherrypy.request.method == 'POST':
            try:
                joueur_id = int(joueur_id)
                if not joueur_exists(joueur_id):
                    error_message = "Le joueur avec cet ID n'existe pas."
                else:
                    if equipe_id:
                        equipe_id = int(equipe_id)
                    success, message = update_joueur(joueur_id, nom, prenom, poste, equipe_id)
                    if not success:
                        error_message = message
                    else:
                        raise cherrypy.HTTPRedirect("/joueurs")
            except ValueError:
                error_message = "L'ID du joueur et de l'équipe doivent être des nombres."
        mytemplate = mylookup.get_template("update_joueur.html")
        return mytemplate.render(error_message=error_message)

    def render_update_team_page(self, error_message=None):
        equipes = get_all_equipes()
        mytemplate = mylookup.get_template("modifier_une_equipe.html")
        return mytemplate.render(error_message=error_message, equipes=equipes)
    
    def render_delete_team_page(self, error_message=None):
        equipes = get_all_equipes()
        mytemplate = mylookup.get_template("Supprimer_equipe.html")
        return mytemplate.render(error_message=error_message, equipes=equipes)  
        
if __name__ == '__main__':
    rootPath = os.path.abspath(os.getcwd())
    conf = {
        '/': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'html',
            'tools.staticdir.root': rootPath
        },
        '/css': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './css'
        },
        '/images': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './images'
        }
    }
    cherrypy.quickstart(Interface_Web_Real_Bets(), '/', config=conf)