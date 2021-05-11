"""module permettant de créer à partir d'un texte un fichier audio """
import requests
import argparse


def get_all_voices():
  """Permet de récupérer la liste de toutes les voix"""
  r = requests.get("https://app.resemble.ai/api/v1/voices", headers={'Authorization': token})
  return r.json()

def create_new_clip(titre, texte, voix):
  """
  permet de créer un nouveau clip à partir d'un texte et d'un titre
  :param titre: le titre du clip
  :param texte: le texte que l'on souhaite convertir en audio
  :param voix: la voix qu'on souhaite utiliser
  :return: status code de l'API au format json
  """
  data = {
    "data": {
      "title": titre,
      "body": texte,
      "voice": voix
    },
    "callback_uri": "https://mycall.back/service"
  }
  r = requests.post(f"https://app.resemble.ai/api/v1/projects/{project}/clips",
                    headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {bearer}'},
                    data=data)
  print(r.json)
  return r.json

if __name__ == '__main__':
  # gestion des arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('-te', '--texte', action="store", help="texte à convertir en audio", required=True)
  parser.add_argument('-ti', '--titre', action="store", help="titre que l'on souhaite donner au clip", required=True)
  parser.add_argument('-to', '--token', action="store", help="token de l'API pour l'authentification", required=True)
  parser.add_argument('-p', '--project_name', action="store", help="nom du projet de l'API", required=True)
  parser.add_argument('-b', '--bearer', action="store", help="Bearer de l'API pour l'authentification", required=True)
  parser.add_argument('-v', '--voice_uuid', action="store", help="l'UUID de la voice qu'on souhaite utiliser", required=True)
  args = parser.parse_args()

  # création des variables d'authentification
  project = args.project_name
  bearer = args.bearer
  token = args.token

  # création du nouveau clip
  create_new_clip(args.titre, args.texte, args.voice_uuid)









